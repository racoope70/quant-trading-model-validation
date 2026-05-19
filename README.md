# Market ML Signals — Backtested Research Pipeline

This repository contains walk-forward machine learning trading research pipelines used for model validation, backtesting, and paper trading.
It represents the structured middle stage between exploratory research and a production-ready implementation.

The system runs per-ticker walk-forward training and evaluation, saves artifacts per fold, and exports trading signals for downstream execution frameworks such as QuantConnect (LEAN).

It provides a reproducible workflow for validating models and generating trading signals prior to production deployment.

---

## Status

Two model candidates have completed the validation stage: a standalone PPO signal model and a PPO + Random Forest Gate hybrid. The PPO model has already been promoted into the deployment repository; the PPO + RF hybrid is the next candidate for deployment conversion.

This repository represents the validated research layer.  
A separate repository will contain the fully production-ready implementation with modular code, CLI workflows, and local execution support.

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

The dry run loads PPO artifacts, fetches Alpaca bars, predicts target weights, compares target versus actual paper-account positions, and logs diagnostics.  It does **not** submit orders.

---

## Repository Context

This repository represents the **validated research stage** of the system:

- Exploratory research and model experimentation are developed separately
- This repo contains structured walk-forward training, backtesting, and signal validation
- A final production repository will implement a fully modular, deployment-ready system

---

## What’s inside

- **Feature pipeline** — robust OHLCV normalization, wavelet denoising, technical + regime features, optional FinBERT sentiment.
- **Model validation framework** — structured comparison of PPO-only and hybrid PPO + supervised-gate approaches under consistent walk-forward assumptions.
- **Walk-forward training (PPO reference)** — rolling windows, confidence-based reward shaping, whipsaw penalty, regime filter.
- **Artifacts for deployment** — saved models, `VecNormalize`/scalers, feature lists, probability config.
- **Signal serving** — JSON schema for downstream consumers; QuantConnect example for consuming signals and executing trades in backtesting or paper trading.
- **Reporting** — summary metrics, backtest metrics and risk analysis (Sharpe, PSR, Win Rate), and run logs.
- **Paper-trading dry run** — local VS Code-compatible Alpaca dry-run module for no-order artifact/prediction validation.
- **Validated model candidates** — PPO-only and PPO + Random Forest Gate have both completed validation; PPO has been migrated to the deployment repository, and PPO + RF is next in the deployment queue.

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

Run the notebooks in sequence (training → backtesting → execution prep):

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

### Validated models

- **PPO** — validated walk-forward reinforcement learning model for position sizing, reward shaping, and downstream signal generation. This model has been promoted into the deployment repository.

- **PPO + Random Forest Gate** — validated hybrid model where PPO handles position sizing and the Random Forest gate filters low-quality trade environments before exposure is allowed. This model is the next candidate for deployment conversion.

### Next hybrid candidate

- **PPO + XGBoost Gate** — planned challenger model using the same data, feature set, walk-forward structure, and validation assumptions as PPO + RF. The goal is to compare XGBoost against Random Forest as the supervised trade-participation gate while keeping the PPO policy layer consistent.

---

## Platforms

- **QuantConnect:** example consumer for polling signals and executing trades in backtesting or paper trading environments.

- **Alpaca (paper/live):** adapters for integration and paper trading evaluation.
