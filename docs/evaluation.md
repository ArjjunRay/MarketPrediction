# Evaluation

Classification reports accuracy, balanced accuracy, precision, recall, F1, Brier
score, calibration curves, and expected calibration error. Regression reports MAE,
RMSE, and rank correlation where meaningful. Results are sliced by horizon, symbol,
sector, regime, confidence, volatility, liquidity, model version, and time.

Each immutable forecast is resolved only after its horizon matures. Realized outcome
records reference, but never overwrite, the original prediction. Evaluation stores
model, feature and dataset versions, inference latency, probabilities, point forecast,
uncertainty, and regime.

Backtest and paper metrics include spread, fees, slippage, latency, turnover, drawdown,
Sharpe/Sortino, and execution assumptions. Statistical uncertainty and sample size
must accompany comparisons. Live degradation and calibration drift are monitored
separately from training metrics.
