# PPO Walk-Forward Trading System — Backtested Research Pipeline

This repository contains a walk-forward PPO-based trading research pipeline that generates external trading signals for downstream execution systems such as QuantConnect (LEAN).  
The model runs per-ticker walk-forward training/evaluation, saves artifacts per fold, and exports a clean signal feed for backtesting, paper trading, and downstream execution testing.

**Status:** This repository represents a structured research, backtesting, and paper-trading validation layer. It is not the final production-ready VS Code implementation.

## Core Capabilities

1) **Execution & Slippage Simulation**
   - Constant and impact-style slippage profiles; fee model hooks.
   - Designed for integration with QuantConnect (LEAN); tested in paper-trading and backtesting environments.

2) **Noise Filtering**
   - **Wavelet denoising** on price/feature series to reduce microstructure noise.

3) **Market Regime Detection**
   - Volatility & trend state machine; regime used for feature gating and reward shaping.

4) **Signal Export & Execution Interface (Research-Level)**
   - JSON signal emitter (RAW Gist alias) with `valid_until_utc` freshness guard.
   - Confidence-weighted targets (mapped to 10–50% caps) with cash buffer normalization.

5) **Risk Controls (Research-Level)**
   - Per-name caps, portfolio gross cap (~95% exposure), optional trade-cooldowns.

6) **Feature Additions**
   - **FinBERT** sentiment scores (headline/text ingestion optional).
   - **Mock option Greeks** (synthetic IV surface heuristics) for skew/convexity proxies.
   - Technical suite + wavelet-filtered variants.

7) **PPO Walk-Forward Enhancements**
   - Confidence-based rewards, **whipsaw penalty**, regime filtering.
   - Expanding/rolling windows; per-fold early-stopping and checkpointing.

8) **Evaluation & Logging**
   - Extended metrics (return, Sharpe, Sortino, PSR, drawdown, turnover, hit-rate).
   - QC end-of-run `RUN_SUMMARY` log (orders, fills, closed trades, win-rate).

---

## Pipeline Overview (Research Workflow)

- **Data → Features**: raw OHLCV (+ sentiment, Greeks proxies) → wavelet denoise → scale/clip.
- **Split**: walk-forward folds (expanding or rolling).
- **Train**: PPO per fold with reward shaping (confidence & whipsaw).
- **Validate**: per fold; keep best checkpoint.
- **Emit**: merge fold predictions → `live_signals.json` (per symbol).
- **Execute (Simulated)**: Signals can be consumed by external frameworks (e.g., QuantConnect) for backtesting or paper trading.

---

## Key metrics we track

- Net Return, CAGR, Max Drawdown, **Sharpe**, **PSR (Sharpe>0)**, Sortino, Information Ratio, Turnover, Trades/Day.
- Per-trade and daily PnL distributions; regime-aware attribution (optional).

---

## Saved artifacts (consistent naming)

All artifacts are grouped by **ticker** and **fold** under `artifacts/`.  
Use these patterns so everything lines up with the report and orders CSV:

Example artifact layout:

```text
ppo_research_pipeline/
  trained_models/
  GE/
  UNH/
  ppo_multi_stock_training_pipeline.ipynb
```

## Installation & Usage

### Prerequisites
- Python 3.9+
- pip or conda
- Git
- Google Colab (primary environment used for training and experimentation)

### Setup
```bash
git clone https://github.com/racoope70/quantitative-trading-system.git
cd quantitative-trading-system

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### Usage (Research Workflow)

Run the following notebooks:

- Training pipeline:
  - `ppo_research_pipeline/ppo_multi_stock_training_pipeline.ipynb`

- Backtesting:
  - `ppo_research_pipeline/UNH/`
  - `ppo_research_pipeline/GE/`

> Recommended: Open notebooks in Google Colab for compatibility.

### Limitations / Next Step

This project is notebook-centered and intended for research validation.  
A separate production-ready repository will refactor the workflow into modular Python files with CLI commands, local path handling, and no Google Colab dependencies.
