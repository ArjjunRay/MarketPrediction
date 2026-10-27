# Zero-cost public data policy

QStream is an anonymous public display. Market data must cost $0 and its terms must
explicitly permit the operator to display or redistribute it to unrelated public users.
A free developer key is not the same as public-display permission. No browser user is
ever asked for a provider account or key.

## Decision

No reviewed free US-equity price feed is enabled. The common free APIs below either
prohibit redistribution, restrict free access to personal/non-commercial use, or require
a separate display agreement. QStream therefore reports its market-price source as
`None / UNAVAILABLE`; it does not relabel government fundamentals or macro series as
market prices.

The first enabled external adapters are:

- SEC EDGAR submissions and company facts (operator must supply a descriptive
  `QSTREAM_SEC_USER_AGENT`; this is contact identification, not an API key)
- BLS public API v2 under its unregistered limits
- U.S. Treasury daily par yield curve XML
- BEA NIPA macro data when the operator supplies a free BEA API key
- the existing deterministic simulated/replay boundary for local development only

## Free equity-provider review

| Source / free access | Latency and coverage | Transport and limits | History | Public display finding | Decision |
|---|---|---|---|---|---|
| Alpaca Basic | IEX real-time equities; bars, trades and quotes; not consolidated SIP | REST and WebSocket; 30 subscribed symbols and 200 historical API requests/minute | Recent SIP access is constrained on Basic | Alpaca states that API data cannot be redistributed | Reject for public display |
| Twelve Data Basic | REST/WebSocket availability and credits are plan-dependent; equities include price/bar and some quote fields | API key; credit-based limits | Plan-dependent | Terms say Free Tier cannot be used commercially and redistribution requires a separate add-on/agreement | Reject |
| Alpha Vantage free | Primarily historical/end-of-day access; real-time and 15-minute delayed US data are premium-entitlement products | API key; 25 requests/day | Daily and technical series | Terms classify public/shared use beyond personal individual research as commercial | Reject |
| FINRA API | Regulatory datasets, not a general live equity-price feed | Dataset-specific REST access and limits | Dataset-specific | General terms restrict distribution unless the dataset-specific terms allow it | Do not use as a public price feed |
| SEC MIDAS downloads | Aggregated market-structure metrics, not live prices or a quote stream | File downloads | Historical aggregate statistics | Public SEC research data | Eligible for later research, not live display |

Official references:

- [Alpaca market-data plans](https://docs.alpaca.markets/us/docs/about-market-data-api)
  and [Alpaca redistribution statement](https://alpaca.markets/support/redistribute-alpaca-api)
- [Twelve Data terms](https://twelvedata.com/terms)
- [Alpha Vantage terms](https://www.alphavantage.co/terms_of_service/),
  [real-time policy](https://www.alphavantage.co/realtime_data_policy/), and
  [support/limits](https://www.alphavantage.co/support/)
- [FINRA API terms](https://developer.finra.org/finra-api-terms-service)
- [SEC market-structure downloads](https://www.sec.gov/data-research/market-structure-data)

## Official public sources

| Source | Cost/key | Limits and cadence | Data used | Display/licensing basis |
|---|---|---|---|---|
| SEC EDGAR | Free; no key; descriptive operator User-Agent required | Fair-access policy; stay at or below 10 requests/second; submissions update throughout the day and XBRL facts are typically updated in under a minute | 10-K/10-Q/8-K events, submissions and company facts | SEC records are public; attribution is retained |
| BLS | Free; no key for unregistered v2 use | 25 queries/day, 25 series/query, 10 years/query without registration | Official labor/economic series | BLS-authored material is public domain; source labels retained |
| U.S. Treasury | Free; no key | Official daily publication | Daily par yield curve rates | Official government feed; source labels retained |
| BEA | Free; operator registration key required | Dataset-specific official release schedules | NIPA/GDP and industry macro series | Published BEA statistics are generally public domain; attribution retained |
| FRED | Free developer key | API-specific limits and series-specific cadence | Not enabled | Current API-key guidance expects application users to use their own keys, and underlying series can carry third-party copyright. This conflicts with the operator-only-key requirement. |

References:

- [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces),
  [SEC fair access](https://www.sec.gov/os/accessing-edgar-data), and
  [SEC copyright/public-record statement](https://www.sec.gov/about/privacy-information)
- [BLS API FAQ](https://www.bls.gov/developers/api_FAQs.htm) and
  [BLS copyright statement](https://www.bls.gov/opub/copyright-information.htm)
- [Treasury daily rate XML feed](https://home.treasury.gov/treasury-daily-interest-rate-xml-feed)
- [BEA API registration and datasets](https://apps.bea.gov/api/signup/) and
  [BEA public-domain statement](https://www.bea.gov/help/faq/145)
- [FRED API key guidance](https://fred.stlouisfed.org/docs/api/fred/v2/api_key.html)
  and [FRED API terms](https://fred.stlouisfed.org/docs/api/terms_of_use.html)

## Capability rules

- L2, L3/MBO, cancellations, replenishment and consolidated order flow remain disabled.
- Top-of-book features are enabled only if a future source supplies bid, ask and valid
  sizes with explicit public-display rights. Top-of-book is never called a full book.
- News remains disabled. Filing events from SEC are event inputs, not “news.”
- A future price adapter must document exact source, status, delay, resolution,
  polling/streaming method, limits, key ownership and public-display permission.
- Provider payloads terminate at adapter boundaries; normalized contracts remain vendor-neutral.
