"use client";

import {
  Brain,
  ChartLine,
  ClockCounterClockwise,
  Gauge,
  Heartbeat,
  Newspaper,
  SlidersHorizontal,
  Swap,
  TrendUp,
  UsersThree,
  Wallet,
  Waveform,
} from "@phosphor-icons/react";

const groups = [
  {
    label: "Workspace",
    items: [
      ["Overview", Gauge],
      ["Market", ChartLine],
      ["Microstructure", Waveform],
      ["Forecasts", TrendUp],
    ],
  },
  {
    label: "Research",
    items: [
      ["AI / Models", Brain],
      ["Relationships", Swap],
      ["News", Newspaper],
      ["Historical", ClockCounterClockwise],
    ],
  },
  {
    label: "Operations",
    items: [
      ["Paper Trading", Wallet],
      ["Model Health", Heartbeat],
      ["Watchlist", UsersThree],
      ["Settings", SlidersHorizontal],
    ],
  },
] as const;

export function Sidebar() {
  return (
    <aside className="sidebar" aria-label="Primary navigation">
      <div className="brand">
        <span className="brand__mark" aria-hidden="true">
          Q
        </span>
        <div>
          <p className="brand__name">QStream</p>
          <p className="brand__tagline">Quant research terminal</p>
        </div>
      </div>
      <nav className="sidebar__nav">
        {groups.map((group) => (
          <div className="nav-group" key={group.label}>
            <p className="nav-group__label">{group.label}</p>
            {group.items.map(([label, Icon], index) => (
              <button
                type="button"
                className="nav-item"
                data-active={group.label === "Workspace" && index === 0}
                aria-current={
                  group.label === "Workspace" && index === 0
                    ? "page"
                    : undefined
                }
                key={label}
              >
                <Icon size={17} weight="regular" aria-hidden="true" />
                <span>{label}</span>
                {label === "Microstructure" ? (
                  <span className="nav-item__lock">L2</span>
                ) : null}
              </button>
            ))}
          </div>
        ))}
      </nav>
      <div className="sidebar__footer">
        <p>PUBLIC MODE</p>
        <span>No account required</span>
      </div>
    </aside>
  );
}
