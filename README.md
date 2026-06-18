# Market ML Signals - Backtested Research Pipeline

This repository contains walk-forward machine learning trading research pipelines used for model validation, backtesting, and paper trading.
It represents the structured middle stage between exploratory research and a production-ready implementation.

The system runs per-ticker walk-forward training and evaluation, saves artifacts per fold, and exports trading signals for downstream execution frameworks such as QuantConnect (LEAN).

It provides a reproducible workflow for preserving research evidence, auditing baseline models, and supporting future model-development decisions.

---

## Status

Two model candidates emerged from the original research pipeline: a standalone PPO signal model and a PPO + Random Forest Gate hybrid. Under today's stricter trading-readiness standard, these models are legacy baselines. They were research-promising and infrastructure-worthy, but they do not satisfy the criteria for controlled paper submission, live trading, or hybrid deployment. The PPO model is preserved for audit and infrastructure validation purposes, and the PPO + RF hybrid remains a research baseline. Neither model is promoted for deployment conversion under the current standard.

This repository represents a legacy research validation layer. A separate deployment repository implements the governed no-submit infrastructure and audit pipeline; it does not contain trading-ready logic. Any future production implementation should follow a new PPO v2 retraining and modern audit process.

---

## Paper-Trading Reliability Validation

The first Alpaca paper-trading reliability phase is documented under:

```text
validation/paper_trading/phase_1_reliability/
```

**Phase 1 Reliability: PASSED**

The validation evidence confirms that PPO artifacts loaded correctly, Alpaca paper credentials connected, model predictions executed, paper orders were submitted/filled, no duplicate-order or stale-bar failures were observed, strict flatten completed successfully, and run summaries/logs were produced.

This is an operational reliability pass, not a profitability claim.

---

## Local Paper-Trading Dry Run

Broker-facing logic is implemented separately from validation evidence:

```text
src/paper_trading/
config/paper_trading_six_ticker_manifest.json
```

The first local command is intentionally no-order:

```bash
python -m src.paper_trading.paper_trade_dry_run
```

The dry run loads legacy PPO artifacts, fetches Alpaca bars, predicts target weights, compares target versus actual paper-account positions, and logs diagnostics. It does **not** submit orders.

---

## Repository Context

This repository represents the legacy research validation stage of the system:

- Exploratory research and model experimentation are developed separately
- This repo contains structured walk-forward training, backtesting, and signal validation evidence for baseline models
- The current deployment repo is responsible for governed no-submit infrastructure and audit behavior
- Future trading-readiness work requires PPO v2 retraining under stricter validation standards

---

## What is inside

- **Feature pipeline** - robust OHLCV normalization, wavelet denoising, technical + regime features, optional FinBERT sentiment.
- **Model validation framework** - structured comparison of PPO-only and hybrid PPO + supervised-gate approaches under consistent walk-forward assumptions.
- **Walk-forward training (PPO reference)** - rolling windows, confidence-based reward shaping, whipsaw penalty, regime filter.
- **Legacy artifacts** - saved models, `VecNormalize`/scalers, feature lists, probability config, and model-info files preserved for audit and reproducibility.
- **Signal serving evidence** - JSON schema for downstream consumers; QuantConnect example for consuming signals and executing trades in backtesting or paper trading.
- **Reporting** - summary metrics, backtest metrics and risk analysis (Sharpe, PSR, Win Rate), and run logs.
- **Paper-trading dry run** - local VS Code-compatible Alpaca dry-run module for no-order artifact/prediction validation.
- **Legacy baseline models** - PPO-only and PPO + Random Forest Gate are preserved as research baselines. They are research-promising and infrastructure-worthy but do not meet current trading-readiness standards. Neither model is promoted for controlled paper submission or live deployment.

---

## Repo layout

The `trained_models/` directory contains saved PPO artifacts per ticker and walk-forward window.

```text
quant-trading-model-validation/
├── README.md
├── requirements.txt
├── config/
│   └── paper_trading_six_ticker_manifest.json
├── src/
│   └── paper_trading/
│       ├── __init__.py
│       ├── artifact_manifest.py
│       ├── artifact_loader.py
│       └── paper_trade_dry_run.py
├── validation/
│   └── paper_trading/
│       └── phase_1_reliability/
│           ├── README.md
│           ├── true_alpaca_evaluation_report.txt
│           ├── run_summary_sample.csv
│           ├── symbol_order_fill_summary.csv
│           └── artifact_symbol_summary.csv
└── ppo_research_pipeline/
    ├── GE/
    ├── UNH/
    └── trained_models/
```

---

## Usage (Research Workflow)

Run the notebooks in sequence (training -> backtesting -> execution prep):

- **Training pipeline**
  - `ppo_research_pipeline/ppo_multi_stock_training_pipeline.ipynb`

- **Per-ticker backtesting**
  - `ppo_research_pipeline/GE/ge_signal_backtest.ipynb`
  - `ppo_research_pipeline/UNH/unh_signal_backtest.ipynb`

- **QuantConnect integration prep**
  - `*_PPO_QuantConnect_Prep.ipynb`

> Recommended: Run notebooks in Google Colab for compatibility with the original environment.

This project was developed and tested in Google Colab.  
Local execution may require minor path adjustments.

---

## Models

### Legacy baseline models

- **PPO** - legacy walk-forward reinforcement learning model for position sizing and reward shaping. It served as a research-promising, infrastructure-worthy baseline and is preserved for audit and future comparison. Under today's standards it is not paper-submit-ready, live-trading-ready, or hybrid-deployment-ready.

- **PPO + Random Forest Gate** - legacy hybrid where PPO handles position sizing and a Random Forest gate filters low-quality trade environments. This model is retained as a research baseline for comparison against future PPO v2 hybrids; it is not a candidate for deployment conversion under the current standard.

### Future candidate

- **PPO + XGBoost Gate** - planned challenger model only after the baseline audit and PPO v2 design are complete. XGBoost should not be treated as deployment-ready until it passes the same stricter validation standard.

---

## Platforms

- **QuantConnect:** example consumer for polling signals and executing trades in backtesting or paper trading environments.

- **Alpaca (paper/live):** adapters for integration and paper trading evaluation.
