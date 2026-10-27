# UI implementation rules

The local UI skills require a dense but legible professional terminal: semantic design
tokens, a restrained Swiss/minimal hierarchy, dark-first surfaces, IBM Plex typography,
consistent spacing, keyboard-visible focus, and limited functional motion. Color is
never the sole status signal; icons and text reinforce health and direction. The shell
must reflow rather than horizontally overflow at narrow widths.

The UI is capability-driven. Missing provider data renders an explicit unavailable
state with a reason, never fabricated values. Top-of-book is labeled as such and depth
components remain disabled without L2/L3 entitlement. Simulation, delayed data, stale
feeds, disconnected WebSockets, and partial service failures are visually explicit.

Charts must prioritize readable axes, units, timestamps, accessible contrast, bounded
updates, and last-updated state. Animation is restrained and respects reduced-motion
preferences. Native semantic controls and Phosphor icons are preferred over decorative
glyphs. See `docs/design-system.md` for the token mapping.
