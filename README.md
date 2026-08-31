# Quantitative Trading Model Validation Research

![Status](https://img.shields.io/badge/status-legacy%20validation-lightgrey)
![Python](https://img.shields.io/badge/Python-research-blue?logo=python&logoColor=white)
![Google Colab](https://img.shields.io/badge/Google%20Colab-original%20environment-F9AB00?logo=googlecolab&logoColor=white)
![Models](https://img.shields.io/badge/models-PPO%20%2B%20Random%20Forest-blueviolet)
![Validation](https://img.shields.io/badge/validation-walk--forward-informational)

> **Status: Historical structured model-validation research**
>
> This repository preserves historical PPO and PPO + Random Forest model-validation research, including chronological / walk-forward evaluation, backtesting, model artifacts, signal validation, QuantConnect integration, and Alpaca Paper reliability testing. It is not the current canonical research platform, and its historical models are not current trading-ready candidates.

## Overview

This repository contains structured historical machine-learning trading research used for model validation, backtesting, signal evaluation, artifact preservation, and paper-trading reliability work. It followed earlier exploratory ML/RL research, preceded later modular PPO implementation and execution research, and ultimately informed the current quantitative trading research platform.

The historical workflow runs per-ticker walk-forward training and evaluation, saves artifacts per fold, and exports trading signals for downstream execution frameworks such as QuantConnect (LEAN).

It preserves a structured validation workflow and its associated research evidence for auditing baseline models and supporting later model-development decisions.

---

## Role in the Research Progression

1. **Exploration — [`exploratory-daytrading`](https://github.com/racoope70/exploratory-daytrading)**  
   Historical exploratory ML/RL research, feature engineering, model experimentation, mixed results, and early evaluation/execution work.

2. **Structured model validation — this repository**  
   Historical PPO and PPO + Random Forest research with chronological / walk-forward evaluation, backtesting, signal validation, preserved model artifacts, QuantConnect work, and Alpaca Paper reliability evidence.

3. **Modular PPO implementation / execution research — [`ppo-trading-pipeline`](https://github.com/racoope70/ppo-trading-pipeline)**  
   Later historical modular PPO research and engineering covering execution realism, holdout work, broker integration, and subsequent stricter model-quality review.

4. **Current canonical research platform — [`quantitative-trading-research-platform`](https://github.com/racoope70/quantitative-trading-research-platform)**  
   Current research platform with stricter reproducibility, leakage control, provenance, testing, and model-evaluation methodology.

This progression documents an evolution in research methodology and engineering discipline. It does not imply that each stage automatically validated the previous stage or that any historical repository established production readiness.

---

## Research Scope / What Was Evaluated

- **Feature pipeline** - robust OHLCV normalization, wavelet denoising, technical + regime features, optional FinBERT sentiment.
- **Model validation framework** - structured comparison of PPO-only and hybrid PPO + supervised-gate approaches under consistent chronological / walk-forward assumptions.
- **Walk-forward training (PPO reference)** - rolling windows, confidence-based reward shaping, whipsaw penalty, regime filter.
- **PPO + Random Forest research** - chronological validation, no-lookahead checks, Random Forest participation gating, threshold evaluation, and baseline comparison work.
- **Legacy artifacts** - saved models, `VecNormalize`/scalers, feature lists, probability config, gate artifacts, model-info files, and selector outputs preserved for audit and historical reproducibility work.
- **Signal serving evidence** - JSON schema for downstream consumers; QuantConnect examples for consuming signals and executing trades in backtesting or paper-trading environments.
- **Reporting** - summary metrics, backtest metrics and risk analysis (including Sharpe, PSR, Win Rate), selector outputs, and run logs.
- **Paper-trading reliability evidence** - Alpaca Paper broker-side reliability validation with preserved reports and run summaries.
- **Paper-trading dry run** - local VS Code-compatible Alpaca Paper dry-run module for no-order artifact and prediction validation.

---

## Research Outcome / Legacy Status

Two model candidates emerged from the original research pipeline: a standalone PPO signal model and a PPO + Random Forest Gate hybrid. Under today's stricter trading-readiness standard, these models are legacy baselines. They were research-promising and infrastructure-worthy, but they do not satisfy the criteria for controlled paper submission, live trading, or hybrid deployment.

The PPO model is preserved for audit and infrastructure-validation purposes, and the PPO + Random Forest hybrid remains a research baseline. Neither model is promoted for deployment conversion under the current standard. Favorable, weak, and unfavorable historical evidence remains part of the research record rather than being rewritten to fit the later disposition.

See [`LEGACY_STATUS.md`](LEGACY_STATUS.md) for the detailed historical model disposition, mixed PPO evidence, Alpaca reliability interpretation, and modern validation gaps.

Any future trading-ready candidate should be retrained and evaluated under a modern validation standard before promotion.

---

## Paper-Trading Reliability Validation

The first Alpaca Paper reliability phase is documented under:

```text
validation/paper_trading/phase_1_reliability/
```

The Phase 1 Alpaca Paper reliability evaluation passed its operational checks.**

The preserved evidence confirms that PPO artifacts loaded correctly, Alpaca Paper credentials connected, model predictions executed, paper orders were submitted and filled, no duplicate-order or stale-bar failures were observed, strict flatten completed successfully, and run summaries/logs were produced.

**This is an operational reliability pass, not a profitability or trading-edge claim.**

---

## Local Paper-Trading Dry Run

Broker-facing dry-run logic is implemented separately from the preserved reliability evidence:

```text
src/paper_trading/
config/paper_trading_six_ticker_manifest.json
```

The local command is intentionally no-order:

```bash
python -m src.paper_trading.paper_trade_dry_run
```

The dry run loads historical PPO artifacts, uses Alpaca Paper account and market-data state, predicts target weights, compares target versus actual paper-account positions, and logs diagnostics. It deliberately does **not** submit orders.

This dry run is infrastructure and inference validation only; it is not controlled paper-submit approval.

---

## Research Workflow / Usage

The original research workflow was developed primarily in Google Colab and should be interpreted in that historical environment context.

- **Historical training workflow source**
  - `ppo_research_pipeline/ppo_multi_stock_training_pipeline.py`
  - This file is an automatically generated Google Colab export of the original notebook workflow and retains notebook-style shell directives. It should be treated as a historical Colab-centered research artifact rather than as a clean ordinary local Python training command.

- **Per-ticker backtesting notebooks**
  - `ppo_research_pipeline/GE/ge_signal_backtest.ipynb`
  - `ppo_research_pipeline/UNH/unh_signal_backtest.ipynb`

- **QuantConnect integration preparation**
  - `*_PPO_QuantConnect_Prep.ipynb`

Google Colab is the original environment for much of the historical training and experimentation. Local execution may require environment or path adjustments.

---

## Models and Platforms

### Models

- **PPO** - legacy walk-forward reinforcement-learning model for position sizing and reward shaping. It served as a research-promising, infrastructure-worthy baseline and is preserved for audit and future comparison. Under today's standards it is not paper-submit-ready, live-trading-ready, or hybrid-deployment-ready.

- **PPO + Random Forest Gate** - legacy hybrid where PPO handles position sizing and a Random Forest gate filters low-quality trade environments. This model is retained as a research baseline for comparison against future PPO v2 hybrids; it is not a candidate for deployment conversion under the current standard.

- **PPO + XGBoost Gate** - future/planned challenger concept only after the baseline audit and PPO v2 design are complete. It should not be treated as implemented, qualified, or deployment-ready unless later research establishes that status under the stricter validation standard.

### Platforms

- **QuantConnect / LEAN:** example consumer for polling signals and executing trades in backtesting or paper-trading environments.

- **Alpaca Paper:** broker-side paper-trading reliability evidence plus local no-order artifact, prediction, account-state, and position-comparison testing.

---

## Repository Layout

The repository preserves historical research pipelines, model artifacts, broker-reliability evidence, and local no-order paper-trading support.

```text
quant-trading-model-validation/
├── README.md
├── LEGACY_STATUS.md
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
├── ppo_research_pipeline/
│   ├── GE/
│   ├── UNH/
│   └── trained_models/
└── ppo_rf_research_pipeline/
    ├── Model Selector/
    ├── PPO RF Models Master/
    └── PPO RF Models QC Top/
```

---

## Limitations / Successor Research

This repository is a historical structured validation layer, not the current forward-development platform. Its notebooks, generated Colab exports, saved artifacts, and environment assumptions preserve the research stage in which the work was performed and may require adjustment in a modern local environment.

The historical PPO and PPO + Random Forest systems remain useful as research baselines and infrastructure evidence, but they do not meet the current standard for controlled paper submission, live trading, or deployment conversion. Successful walk-forward experiments, favorable Sharpe values, gate behavior, model-selector outputs, broker connectivity, paper fills, or working execution code should not be interpreted by themselves as proof of a profitable trading edge.

Current forward research continues in [`quantitative-trading-research-platform`](https://github.com/racoope70/quantitative-trading-research-platform), where stricter reproducibility, leakage control, provenance, testing, model evaluation, and trading-readiness boundaries are applied.
