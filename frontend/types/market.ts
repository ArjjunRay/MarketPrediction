export type AssetClass = "equity" | "etf" | "sector";

export interface Instrument {
  id: string;
  symbol: string;
  name: string;
  exchange: string | null;
  sector: string | null;
  industry: string | null;
  currency: string;
  asset_class: AssetClass;
}

export interface InstrumentSearchResponse {
  query: string;
  results: Instrument[];
  source: "development_reference_catalog";
}

export type Capability = "trades" | "bars" | "nbbo" | "l2" | "l3_mbo" | "news";

export interface ProviderCapabilities {
  provider: string;
  configured: boolean;
  simulated: boolean;
  capabilities: Capability[];
  public_display: Capability[];
  notes: string[];
}

export type PublicDataAvailability =
  "available" | "needs_operator_configuration" | "not_available";

export interface PublicSourceStatus {
  source: string;
  role: string;
  status: PublicDataAvailability;
  api_key_required: boolean;
  operator_configuration: string | null;
  access_method: string;
  update_cadence: string;
  display_delay: string;
  resolution: string;
  capabilities: string[];
  redistribution_note: string;
  official_documentation: string;
}

export interface PublicDataStatusResponse {
  market_price_source: PublicSourceStatus;
  sources: PublicSourceStatus[];
}
