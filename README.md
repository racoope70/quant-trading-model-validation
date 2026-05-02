# Market ML Signals — Backtested Research Pipeline

This repository contains a walk-forward PPO-based trading research system used for model validation, backtesting, and paper trading.  
It represents the structured middle stage between exploratory research and a production-ready implementation.

The system runs per-ticker walk-forward training and evaluation, saves artifacts per fold, and exports trading signals for downstream execution frameworks such as QuantConnect (LEAN).

It provides a reproducible workflow for validating models and generating trading signals prior to production deployment.

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
- **Signal serving** — JSON schema for downstream consumers; QuantConnect example for consuming signals and executing trades in backtesting or paper trading.
- **Reporting** — summary metrics, backtest metrics and risk analysis (Sharpe, PSR, Win Rate), and run logs.

---

## Repo layout

The `trained_models/` directory contains saved PPO artifacts per ticker and walk-forward window.

```text
quantitative-trading-system/
├── README.md
├── requirements.txt
├── ppo_research_pipeline/
│   ├── GE/
│   │   ├── ge_signal_backtest.ipynb
│   │   ├── GE_PPO_QuantConnect_Prep.ipynb
│   │   ├── ExternalSignals_LongOnly_Backtest_*.pdf
│   │   ├── GE_logs_*.txt
│   │   └── *_orders_*.csv
│   │
│   ├── UNH/
│   │   ├── unh_signal_backtest.ipynb
│   │   ├── UNH_PPO_QuantConnect_Prep.ipynb
│   │   ├── ExternalSignals_LongOnly_Backtest_*.pdf
│   │   ├── UNH_logs_*.txt
│   │   └── *_orders_*.csv
│   │
│   ├── trained_models/
│   │   ├── ppo_*_model.zip
│   │   ├── *_vecnorm.pkl
│   │   ├── *_features.json
│   │   ├── *_model_info.json
│   │   └── *_probability_config.json
│   │
│   └── ppo_multi_stock_training_pipeline.ipynb
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

### Reference implementation
- **PPO** — walk-forward training, reward shaping, and signal generation for downstream execution

### Planned / scaffolded

- **Reinforcement Learning:** A2C, SAC, TD3, DDPG, Deep SARSA  
- **Tree / Boosting:** XGBoost, LightGBM  
- **Clustering:** KMeans (regime and feature bucketing)

---

## Platforms

- **QuantConnect:** example consumer for polling signals and executing trades in backtesting or paper trading environments.

- **Alpaca (paper/live):** adapters for integration and paper trading evaluation.
