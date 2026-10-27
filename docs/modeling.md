# Modeling methodology

QStream will compare majority, random, persistence, momentum, mean-reversion,
logistic-regression, and boosted-tree baselines before complex models. Candidate
families include tabular trees, temporal sequence models, depth-specific models when
licensed data exists, context models, NLP event models, graph experiments, and gated
ensembles.

Splits are chronological, rolling, expanding, or walk-forward. Overlapping targets
require purging and embargo. All preprocessing, calibration, selection, and threshold
tuning occur inside training/validation boundaries. Point-in-time constituent and
corporate-action data are mandatory. Ablations compare price; price+volume;
microstructure; market context; and news only when each source is valid at forecast
time.

Promotion requires out-of-sample evidence, calibration, regime stability, latency and
resource measurements, and paper results after costs. Training completion alone never
promotes a model.

The prediction horizon must be no shorter than the input price resolution. The planned
public comparison set is 1-minute, 5-minute, 30-minute, 1-hour and daily only if lawful
data at those resolutions becomes available. Five-second and 30-second targets are not
valid with minute bars. No price model is trained or served while real price history is
unavailable.
