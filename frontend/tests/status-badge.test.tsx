import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { StatusBadge } from "../components/ui/status-badge";

describe("StatusBadge", () => {
  it("always communicates status with text", () => {
    render(<StatusBadge label="Provider not configured" tone="warning" />);
    expect(screen.getByText("Provider not configured")).toBeInTheDocument();
  });
});
