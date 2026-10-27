import { runtimeConfig } from "@/lib/config";
import type {
  InstrumentSearchResponse,
  ProviderCapabilities,
  PublicDataStatusResponse,
} from "@/types/market";

export async function searchInstruments(
  query: string,
  signal?: AbortSignal,
): Promise<InstrumentSearchResponse> {
  const url = new URL("/api/v1/instruments/search", runtimeConfig.apiUrl);
  url.searchParams.set("q", query);
  url.searchParams.set("limit", "8");
  const response = await fetch(url, { signal, cache: "no-store" });
  if (!response.ok) {
    throw new Error("Instrument search is currently unavailable.");
  }
  return response.json() as Promise<InstrumentSearchResponse>;
}

export async function getCapabilities(
  signal?: AbortSignal,
): Promise<ProviderCapabilities> {
  const response = await fetch(`${runtimeConfig.apiUrl}/api/v1/capabilities`, {
    signal,
    cache: "no-store",
  });
  if (!response.ok) {
    throw new Error("Provider capability status is unavailable.");
  }
  return response.json() as Promise<ProviderCapabilities>;
}

export async function getPublicDataStatus(
  signal?: AbortSignal,
): Promise<PublicDataStatusResponse> {
  const response = await fetch(
    `${runtimeConfig.apiUrl}/api/v1/public-data/status`,
    { signal, cache: "no-store" },
  );
  if (!response.ok) {
    throw new Error("Public data source status is unavailable.");
  }
  return response.json() as Promise<PublicDataStatusResponse>;
}
