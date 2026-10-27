"use client";

import { MagnifyingGlass, SpinnerGap } from "@phosphor-icons/react";
import { useEffect, useId, useRef, useState } from "react";

import { searchInstruments } from "@/services/api";
import type { Instrument } from "@/types/market";

interface InstrumentSearchProps {
  onSelect: (instrument: Instrument) => void;
}

export function InstrumentSearch({ onSelect }: InstrumentSearchProps) {
  const labelId = useId();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Instrument[]>([]);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const controller = new AbortController();
    const timer = setTimeout(async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await searchInstruments(query, controller.signal);
        setResults(response.results);
        setOpen(true);
      } catch (reason) {
        if (controller.signal.aborted) return;
        setError(reason instanceof Error ? reason.message : "Search failed.");
        setResults([]);
        setOpen(true);
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }, 180);
    return () => {
      controller.abort();
      clearTimeout(timer);
    };
  }, [query]);

  useEffect(() => {
    const close = (event: PointerEvent) => {
      if (!containerRef.current?.contains(event.target as Node)) setOpen(false);
    };
    document.addEventListener("pointerdown", close);
    return () => document.removeEventListener("pointerdown", close);
  }, []);

  return (
    <div className="instrument-search" ref={containerRef}>
      <label id={labelId} className="sr-only" htmlFor="instrument-search-input">
        Search stocks, ETFs, sectors, or industries
      </label>
      <MagnifyingGlass
        size={18}
        aria-hidden="true"
        className="instrument-search__icon"
      />
      <input
        id="instrument-search-input"
        role="combobox"
        aria-labelledby={labelId}
        aria-expanded={open}
        aria-controls="instrument-search-results"
        aria-autocomplete="list"
        autoComplete="off"
        placeholder="Search stocks, ETFs, sectors..."
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        onFocus={() => setOpen(true)}
      />
      {loading ? (
        <SpinnerGap
          className="instrument-search__spinner"
          size={18}
          aria-label="Searching"
        />
      ) : (
        <kbd>⌘K</kbd>
      )}
      {open ? (
        <div
          className="search-results"
          id="instrument-search-results"
          role="listbox"
        >
          {error ? (
            <p className="search-results__message" role="alert">
              {error}
            </p>
          ) : null}
          {!error && results.length === 0 && !loading ? (
            <p className="search-results__message">
              No matching instruments in the development catalog.
            </p>
          ) : null}
          {results.map((instrument) => (
            <button
              type="button"
              role="option"
              aria-selected="false"
              key={instrument.id}
              onClick={() => {
                onSelect(instrument);
                setQuery(instrument.symbol);
                setOpen(false);
              }}
            >
              <span className="search-results__symbol">
                {instrument.symbol}
              </span>
              <span className="search-results__name">{instrument.name}</span>
              <span className="search-results__type">
                {instrument.asset_class}
              </span>
            </button>
          ))}
        </div>
      ) : null}
    </div>
  );
}
