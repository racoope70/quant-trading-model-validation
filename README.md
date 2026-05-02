# Market ML Signals — Backtested Research Pipeline

This repository contains a walk-forward PPO-based trading research system used for model validation, backtesting, and paper trading.  
It represents the structured middle stage between exploratory research and a production-ready implementation.

The system runs per-ticker walk-forward training and evaluation, saves artifacts per fold, and exports trading signals for downstream execution frameworks such as QuantConnect (LEAN).

It provides a reproducible, structured workflow for validating models and generating signals prior to full production deployment.

---

## Status

PPO is the primary fully implemented and validated model, with results confirmed through walk-forward backtesting and paper trading.

This repository represents the validated research layer.  
A separate repository will contain the fully production-ready implementation with modular code, CLI workflows, and local execution support.

---
## Repository Context

This repository represents the **validated research stage** of the system:

- Exploratory research and model experimentation are developed separately
- This repo contains structured walk-forward training, backtesting, and signal validation
- A final production repository will implement a fully modular, deployment-ready system

---

## What’s inside

- **Feature pipeline** — robust OHLCV normalization, wavelet denoising, technical + regime features, optional FinBERT sentiment.
- **Model zoo** — interchangeable learners behind a standard inference adapter.
- **Walk-forward training (PPO reference)** — rolling windows, confidence-based reward shaping, whipsaw penalty, regime filter.
- **Artifacts for deployment** — saved models, `VecNormalize`/scalers, feature lists, probability config.
- **Signal serving** — JSON schema for downstream consumers; QuantConnect strategy polls and trades.
- **Reporting** — summary metrics, daily risk plots (Sharpe, PSR, Win Rate), and run logs.

---

## Repo layout

```text
quant-trading-model-zoo/
├── README.md
├── src/
│   ├── features/                # feature engineering, regimes, denoise
│   ├── models/                  # model wrappers (PPO, XGB, LGBM, etc.)
│   ├── adapters/                # one-line predict() adapters
│   └── serving/                 # JSON signal writer, web handler
├── training/
│   ├── walkforward_ppo.py       # reference walkforward trainer
│   └── configs/                 # hyperparams per symbol/bucket
├── artifacts/
│   ├── models/                  # *.zip / *.pkl / feature lists
│   └── signals/                 # latest live_signals.json
├── platforms/
│   └── quantconnect/
│       └── main.py              # ExternalSignalConsumer (polls JSON)
├── notebooks/                   # exploratory notebooks (optional)
├── scripts/                     # CLI helpers (train, serve, export)
├── reports/                     # backtest summaries/plots
└── .env.example                 # example secrets (no real keys)

```
---

## Models

### Reference implementation
- **PPO** — walk-forward training, reward shaping, and signal generation for downstream execution

### Planned / scaffolded
- **Reinforcement Learning:** A2C, SAC, TD3, DDPG, Deep SARSA
- **Tree / Boosting:** XGBoost, LightGBM
- **Clustering:** KMeans (regime and feature bucketing)


## Platforms

- **QuantConnect:** example for polling signals and executing trades in backtesting environments.

- **Alpaca (paper/live):** adapters for integration and paper trading evaluation.
