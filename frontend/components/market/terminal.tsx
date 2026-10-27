"use client";

import { ChartLineUp, Database, Globe, Pulse } from "@phosphor-icons/react";
import { useEffect, useState } from "react";

import { InstrumentSearch } from "@/components/market/instrument-search";
import { Panel } from "@/components/ui/panel";
import { StatusBadge } from "@/components/ui/status-badge";
import { useMarketConnection } from "@/hooks/use-market-connection";
import { getPublicDataStatus } from "@/services/api";
import type {
  Instrument,
  PublicDataStatusResponse,
  PublicSourceStatus,
} from "@/types/market";

const unavailableMetrics = [
  ["Open", "—"],
  ["High", "—"],
  ["Low", "—"],
  ["Prev. close", "—"],
  ["Volume", "—"],
  ["VWAP", "—"],
  ["Best bid", "—"],
  ["Best ask", "—"],
] as const;

const marketState = [
  ["Spread", "Unavailable"],
  ["Order imbalance", "Requires depth"],
  ["Trade imbalance", "Unavailable"],
  ["Realized volatility", "Unavailable"],
  ["Liquidity", "Unavailable"],
  ["Current regime", "Insufficient data"],
] as const;

export function Terminal() {
  const [instrument, setInstrument] = useState<Instrument | null>(null);
  const [publicData, setPublicData] = useState<PublicDataStatusResponse | null>(
    null,
  );
  const connection = useMarketConnection();
  const connectionTone =
    connection.state === "connected"
      ? "success"
      : connection.state === "connecting"
        ? "warning"
        : "danger";

  useEffect(() => {
    const controller = new AbortController();
    void getPublicDataStatus(controller.signal)
      .then(setPublicData)
      .catch(() => setPublicData(null));
    return () => controller.abort();
  }, []);

  const priceSource = publicData?.market_price_source;
  const officialSources = publicData?.sources ?? [];

  const sourceTone = (source: PublicSourceStatus) =>
    source.status === "available"
      ? "success"
      : source.status === "needs_operator_configuration"
        ? "warning"
        : "neutral";

  return (
    <div className="terminal">
      <header className="topbar">
        <InstrumentSearch onSelect={setInstrument} />
        <div className="topbar__status" aria-live="polite" aria-atomic="true">
          <StatusBadge label="Market closed" tone="neutral" />
          <StatusBadge
            label={`Gateway ${connection.state}`}
            tone={connectionTone}
          />
          <StatusBadge label="Provider not configured" tone="warning" />
        </div>
      </header>

      <main id="main-content" className="workspace" tabIndex={-1}>
        <div className="workspace__heading">
          <div>
            <div className="workspace__identity">
              <h1>{instrument?.symbol ?? "Select an instrument"}</h1>
              {instrument ? (
                <StatusBadge label={instrument.asset_class.toUpperCase()} />
              ) : null}
            </div>
            <p>
              {instrument?.name ??
                "Use search to initialize a symbol workspace."}
            </p>
          </div>
          <div className="workspace__mode">
            <Globe size={16} aria-hidden="true" />
            <span>Public access · no account required</span>
          </div>
        </div>

        <section className="availability-banner" aria-label="Data availability">
          <Database size={18} aria-hidden="true" />
          <div>
            <strong>No publicly redistributable market-price feed</strong>
            <p>
              Free provider tiers reviewed so far do not grant anonymous public
              price redistribution. Official fundamentals and macro sources are
              separate and do not supply equity prices. Public access requires
              no sign-in.
            </p>
          </div>
          <span>NO LIVE FEED</span>
        </section>

        <dl className="data-provenance" aria-label="Market data provenance">
          <div>
            <dt>Data source</dt>
            <dd>{priceSource?.source ?? "None"}</dd>
          </div>
          <div>
            <dt>Status</dt>
            <dd>UNAVAILABLE</dd>
          </div>
          <div>
            <dt>Last update</dt>
            <dd>Not available</dd>
          </div>
          <div>
            <dt>Delay</dt>
            <dd>{priceSource?.display_delay ?? "Not applicable"}</dd>
          </div>
          <div>
            <dt>Resolution</dt>
            <dd>{priceSource?.resolution ?? "No market-price series"}</dd>
          </div>
        </dl>

        <div className="metric-strip" aria-label="Market summary">
          <div className="metric-strip__primary">
            <p>Last price</p>
            <strong>—</strong>
            <span>Awaiting provider</span>
          </div>
          {unavailableMetrics.map(([label, value]) => (
            <div className="metric" key={label}>
              <p>{label}</p>
              <strong>{value}</strong>
            </div>
          ))}
        </div>

        <div className="workspace-grid">
          <Panel
            title="Price & volume"
            eyebrow="Live market"
            className="panel--chart"
            action={<StatusBadge label="Feed unavailable" tone="warning" />}
          >
            <div className="chart-empty">
              <div className="chart-empty__grid" aria-hidden="true" />
              <ChartLineUp size={28} aria-hidden="true" />
              <strong>No licensed data stream</strong>
              <p>
                The chart will initialize after an instrument and provider
                subscription are active.
              </p>
            </div>
          </Panel>

          <Panel title="Market state" eyebrow="Streaming features">
            <dl className="state-list">
              {marketState.map(([term, value]) => (
                <div key={term}>
                  <dt>{term}</dt>
                  <dd>{value}</dd>
                </div>
              ))}
            </dl>
          </Panel>

          <Panel title="AI forecast" eyebrow="Model inference">
            <div className="empty-state empty-state--compact">
              <Pulse size={24} aria-hidden="true" />
              <strong>Forecast unavailable</strong>
              <p>
                No model is deployed and no point-in-time feature stream is
                available.
              </p>
            </div>
            <div
              className="forecast-horizons"
              aria-label="Planned forecast horizons"
            >
              {["1 min", "5 min", "30 min", "1 hour", "1 day"].map(
                (horizon) => (
                  <span key={horizon}>{horizon}</span>
                ),
              )}
            </div>
          </Panel>

          <Panel title="Official public sources" eyebrow="Fundamental & macro">
            <dl className="readiness-list">
              {officialSources.length > 0 ? (
                officialSources.map((source) => (
                  <div key={source.source}>
                    <dt>
                      {source.source}
                      <small>{source.resolution}</small>
                    </dt>
                    <dd>
                      <StatusBadge
                        label={source.status.replaceAll("_", " ")}
                        tone={sourceTone(source)}
                      />
                    </dd>
                  </div>
                ))
              ) : (
                <div>
                  <dt>Source registry</dt>
                  <dd>Status unavailable</dd>
                </div>
              )}
            </dl>
          </Panel>

          <Panel title="System readiness" eyebrow="Operational status">
            <dl className="readiness-list">
              <div>
                <dt>API gateway</dt>
                <dd>
                  <StatusBadge label={connection.state} tone={connectionTone} />
                </dd>
              </div>
              <div>
                <dt>Market provider</dt>
                <dd>
                  <StatusBadge label="Not configured" tone="warning" />
                </dd>
              </div>
              <div>
                <dt>Model serving</dt>
                <dd>
                  <StatusBadge label="No production model" tone="neutral" />
                </dd>
              </div>
              <div>
                <dt>Data latency</dt>
                <dd>Not measurable</dd>
              </div>
            </dl>
          </Panel>
        </div>
      </main>
    </div>
  );
}
