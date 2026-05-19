"""No-order Alpaca PPO paper-trading dry run.

Command:
    python -m src.paper_trading.paper_trade_dry_run

This validates the deployable path only: load artifacts, fetch Alpaca bars,
predict target weights, compare target vs actual positions, and write logs.
It deliberately does not submit orders.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
import logging
import os
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from .artifact_loader import load_artifact_bundle, predict_target_weight
from .artifact_manifest import load_manifest_entries, repo_root, resolve_path

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    load_dotenv = None

try:
    from alpaca.data.historical import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest
    from alpaca.data.timeframe import TimeFrame
    from alpaca.trading.client import TradingClient
except Exception as exc:  # pragma: no cover
    StockHistoricalDataClient = None
    StockBarsRequest = None
    TimeFrame = None
    TradingClient = None
    ALPACA_IMPORT_ERROR = exc
else:
    ALPACA_IMPORT_ERROR = None

LOGGER = logging.getLogger("paper_trade_dry_run")


def env_value(*names: str) -> str | None:
    for name in names:
        if os.getenv(name):
            return os.getenv(name)
    return None


def configure_logging(results_dir: Path) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(results_dir / "paper_trade_dry_run.log", encoding="utf-8"),
        ],
        force=True,
    )


def load_environment(root: Path, env_file: str | None) -> None:
    if load_dotenv is None:
        return
    if env_file:
        load_dotenv(resolve_path(env_file, root), override=False)
    elif (root / ".env").exists():
        load_dotenv(root / ".env", override=False)


def init_alpaca_clients() -> tuple[Any, Any]:
    if ALPACA_IMPORT_ERROR is not None:
        raise RuntimeError("alpaca-py is required. Run `pip install -r requirements.txt`.") from ALPACA_IMPORT_ERROR
    key_id = env_value("APCA_API_KEY_ID", "ALPACA_API_KEY_ID")
    secret_key = env_value("APCA_API_SECRET_KEY", "ALPACA_API_SECRET_KEY")
    if not key_id or not secret_key:
        raise RuntimeError("Missing Alpaca credentials in environment variables.")
    return TradingClient(key_id, secret_key, paper=True), StockHistoricalDataClient(key_id, secret_key)


def timeframe(value: str) -> Any:
    value = value.lower().replace("_", "").replace("-", "")
    if value in {"1h", "hour", "hourly"}:
        return TimeFrame.Hour
    if value in {"1d", "day", "daily"}:
        return TimeFrame.Day
    if value in {"1min", "minute"}:
        return TimeFrame.Minute
    raise ValueError(f"Unsupported timeframe: {value}")


def bars_to_frame(bars: Any, symbol: str) -> pd.DataFrame:
    df = bars.df
    if df is None or df.empty:
        return pd.DataFrame()
    if isinstance(df.index, pd.MultiIndex):
        df = df.xs(symbol, level="symbol")
    df = df.reset_index().rename(
        columns={"timestamp": "Datetime", "open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"}
    )
    required = ["Datetime", "Open", "High", "Low", "Close", "Volume"]
    df = df[required].copy()
    df["Datetime"] = pd.to_datetime(df["Datetime"], utc=True)
    df["Symbol"] = symbol.upper()
    return df.sort_values("Datetime").reset_index(drop=True)


def fetch_bars(data_client: Any, symbol: str, tf: Any, lookback_bars: int, feed: str) -> pd.DataFrame:
    start = datetime.now(timezone.utc) - timedelta(hours=max(48, lookback_bars * 4))
    request = StockBarsRequest(symbol_or_symbols=[symbol], timeframe=tf, start=start, feed=feed)
    frame = bars_to_frame(data_client.get_stock_bars(request), symbol)
    return frame.tail(lookback_bars).reset_index(drop=True)


def add_common_features(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy().sort_values("Datetime").reset_index(drop=True)
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["SMA_20"] = df["Close"].rolling(20).mean()
    df["STD_20"] = df["Close"].rolling(20).std()
    df["Upper_Band"] = df["SMA_20"] + 2 * df["STD_20"]
    df["Lower_Band"] = df["SMA_20"] - 2 * df["STD_20"]
    df["Lowest_Low"] = df["Low"].rolling(14).min()
    df["Highest_High"] = df["High"].rolling(14).max()
    rng = (df["Highest_High"] - df["Lowest_Low"]).replace(0, np.nan)
    df["Stoch"] = ((df["Close"] - df["Lowest_Low"]) / rng) * 100
    df["ROC"] = df["Close"].pct_change(10)
    df["OBV"] = (np.sign(df["Close"].diff()).fillna(0) * df["Volume"].fillna(0)).cumsum()
    tp = (df["High"] + df["Low"] + df["Close"]) / 3
    sma_tp = tp.rolling(20).mean()
    md = (tp - sma_tp).abs().rolling(20).mean()
    df["CCI"] = (tp - sma_tp) / (0.015 * md.replace(0, np.nan))
    df["EMA_10"] = df["Close"].ewm(span=10, adjust=False).mean()
    df["EMA_50"] = df["Close"].ewm(span=50, adjust=False).mean()
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD_Line"] = ema12 - ema26
    df["MACD_Signal"] = df["MACD_Line"].ewm(span=9, adjust=False).mean()
    delta = df["Close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    df["RSI"] = 100 - (100 / (1 + gain / loss.replace(0, np.nan)))
    tr = pd.concat([(df["High"] - df["Low"]), (df["High"] - df["Close"].shift()).abs(), (df["Low"] - df["Close"].shift()).abs()], axis=1).max(axis=1)
    df["ATR"] = tr.rolling(14).mean()
    df["Volatility"] = df["Close"].pct_change().rolling(20).std()
    df["Denoised_Close"] = df["Close"]
    df["Vol20"] = df["Close"].pct_change().rolling(20).std()
    df["Ret20"] = df["Close"].pct_change(20)
    df["Regime4"] = ((df["Vol20"] > df["Vol20"].median()).astype(int) * 2) + (df["Ret20"].abs() > df["Ret20"].abs().median()).astype(int)
    df["SentimentScore"] = 0.0
    df["Delta"] = df["Close"].pct_change(1).fillna(0)
    df["Gamma"] = df["Delta"].diff().fillna(0)
    return df.replace([np.inf, -np.inf], np.nan).ffill().bfill().fillna(0)


def current_positions(trading_client: Any, equity: float) -> dict[str, dict[str, float]]:
    out = {}
    for pos in trading_client.get_all_positions():
        mv = float(pos.market_value or 0.0)
        out[str(pos.symbol).upper()] = {"qty": float(pos.qty or 0.0), "market_value": mv, "actual_weight": mv / equity if equity else 0.0}
    return out


def run_dry_run(manifest_path: str, env_file: str | None = None) -> Path:
    root = repo_root()
    manifest, entries = load_manifest_entries(manifest_path)
    results_dir = resolve_path(manifest.get("results_dir", "reports/paper_trading/dry_run"), root)
    configure_logging(results_dir)
    load_environment(root, env_file or manifest.get("env_file"))
    if manifest.get("allow_orders", False):
        raise RuntimeError("This module is no-order only. Set allow_orders=false.")
    if not entries:
        raise RuntimeError("No loadable artifacts resolved from manifest.")

    trading_client, data_client = init_alpaca_clients()
    equity = float(trading_client.get_account().equity)
    positions = current_positions(trading_client, equity)
    tf = timeframe(manifest.get("bar_timeframe", "1H"))
    rows = []

    for entry in entries:
        symbol = entry.symbol
        try:
            bundle = load_artifact_bundle(entry)
            raw = fetch_bars(data_client, symbol, tf, int(manifest.get("lookback_bars", 240)), manifest.get("data_feed", "iex"))
            if raw.empty:
                raise RuntimeError("No Alpaca bars returned")
            pred = predict_target_weight(bundle, add_common_features(raw), float(manifest.get("weight_cap", 0.40)), bool(manifest.get("deterministic", True)), manifest.get("feature_fill_policy", "zero_fill_with_warning"))
            latest = raw.iloc[-1]
            pos = positions.get(symbol, {"qty": 0.0, "market_value": 0.0, "actual_weight": 0.0})
            rows.append({
                "datetime_utc": datetime.now(timezone.utc).isoformat(),
                "symbol": symbol,
                "latest_bar_time": pd.Timestamp(latest["Datetime"]).isoformat(),
                "latest_close": float(latest["Close"]),
                "equity": equity,
                "raw_action": pred["raw_action"],
                "target_weight": pred["target_weight"],
                "actual_weight": pos["actual_weight"],
                "target_minus_actual": pred["target_weight"] - pos["actual_weight"],
                "position_qty": pos["qty"],
                "position_market_value": pos["market_value"],
                "feature_count": pred["feature_count"],
                "missing_features_filled": "|".join(pred["missing_features_filled"]),
                "order_submitted": False,
                "note": "dry_run_no_orders",
            })
            LOGGER.info("[%s] target=%.4f actual=%.4f", symbol, pred["target_weight"], pos["actual_weight"])
        except Exception as exc:
            LOGGER.exception("[%s] Dry-run failure", symbol)
            rows.append({"datetime_utc": datetime.now(timezone.utc).isoformat(), "symbol": symbol, "error": str(exc), "order_submitted": False, "note": "dry_run_error"})

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out = results_dir / f"paper_trade_dry_run_decisions_{stamp}.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    (results_dir / f"resolved_artifacts_{stamp}.json").write_text(json.dumps([e.as_dict() for e in entries], indent=2), encoding="utf-8")
    LOGGER.info("Wrote %s", out)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Run PPO Alpaca paper-trading dry run without orders.")
    parser.add_argument("--manifest", default="config/paper_trading_six_ticker_manifest.json")
    parser.add_argument("--env-file", default=None)
    args = parser.parse_args()
    run_dry_run(args.manifest, args.env_file)


if __name__ == "__main__":
    main()
