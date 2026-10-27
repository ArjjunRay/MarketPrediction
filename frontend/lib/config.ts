export const runtimeConfig = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:38000",
  wsUrl: process.env.NEXT_PUBLIC_WS_URL ?? "ws://localhost:38000",
} as const;
