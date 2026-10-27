# Paper trading

QStream permits simulated trading only. The public product will use browser-local or a
global model simulation without login. Existing generic order, fill, position, trade and
account tables are retained as harmless extensibility, not a private-account roadmap.
Every surface must say `SIMULATED / PAPER TRADING`.

Execution accounts for observable spread plus explicit fees, slippage, and latency.
No live-broker order route exists. Adding one is a separate high-impact decision that
requires explicit approval, credentials, controls, and legal/compliance review.
