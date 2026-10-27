# QStream design system

The terminal uses a dense, restrained Swiss-inspired information design. It avoids decorative gradients and excessive glow. Dark mode is the default, with compact surfaces and clear hierarchy.

## Tokens

Tokens follow primitive, semantic, and component layers. Components consume semantic/component variables instead of raw colors.

## Accessibility

- Visible keyboard focus and a skip link
- Search has an explicit label and status messaging
- Status is communicated by text and shape, not color alone
- Live regions are polite and atomic
- Motion respects `prefers-reduced-motion`
- Data visualization will include tabular/narrative alternatives

## Typography

IBM Plex Sans is the primary interface family. Numeric data uses tabular figures. The application must remain usable when the web font is unavailable.

## Density

Desktop layouts prioritize information density with an 8px rhythm. Mobile collapses the sidebar and secondary panels without horizontal page scrolling.

