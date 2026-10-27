import { expect, test } from "@playwright/test";

test("search selects a symbol without inventing market data", async ({
  page,
}, testInfo) => {
  const consoleErrors: string[] = [];
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });

  await page.goto("/");
  await expect(
    page.getByText("No publicly redistributable market-price feed"),
  ).toBeVisible();
  await expect(
    page.getByText("Public access requires no sign-in."),
  ).toBeVisible();
  const providerBadge = page.getByText("Provider not configured");
  if (testInfo.project.name === "mobile-chromium") {
    await expect(providerBadge).toBeHidden();
  } else {
    await expect(providerBadge).toBeVisible();
  }

  const search = page.getByRole("combobox", {
    name: "Search stocks, ETFs, sectors, or industries",
  });
  await search.fill("NVDA");
  await page.getByRole("option").filter({ hasText: "NVDA" }).click();

  await expect(
    page.getByRole("heading", { level: 1, name: "NVDA" }),
  ).toBeVisible();
  await expect(
    page.getByText("NVIDIA Corporation", { exact: true }),
  ).toBeVisible();
  await expect(page.getByText("Forecast unavailable")).toBeVisible();
  await expect(page.getByText("No licensed data stream")).toBeVisible();
  await expect(page.getByText("5 sec", { exact: true })).toHaveCount(0);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
  expect(consoleErrors).toEqual([]);
});
