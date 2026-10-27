"use client";

import { useEffect, useState } from "react";

import { runtimeConfig } from "@/lib/config";

export type ConnectionState = "connecting" | "connected" | "disconnected";

interface MarketConnection {
  state: ConnectionState;
  dataStatus: "unavailable" | "available";
  message: string;
}

const initialState: MarketConnection = {
  state: "connecting",
  dataStatus: "unavailable",
  message: "Connecting to the QStream gateway",
};

export function useMarketConnection(): MarketConnection {
  const [connection, setConnection] = useState<MarketConnection>(initialState);

  useEffect(() => {
    let socket: WebSocket | undefined;
    let retry: ReturnType<typeof setTimeout> | undefined;
    let stopped = false;

    const connect = () => {
      if (stopped) return;
      setConnection((current) => ({ ...current, state: "connecting" }));
      socket = new WebSocket(`${runtimeConfig.wsUrl}/ws/market`);

      socket.onmessage = (event) => {
        const payload = JSON.parse(String(event.data)) as {
          data_status?: "unavailable" | "available";
          message?: string;
        };
        setConnection({
          state: "connected",
          dataStatus: payload.data_status ?? "unavailable",
          message: payload.message ?? "Gateway connected",
        });
      };
      socket.onopen = () => {
        setConnection((current) => ({ ...current, state: "connected" }));
      };
      socket.onerror = () => socket?.close();
      socket.onclose = () => {
        if (stopped) return;
        setConnection({
          state: "disconnected",
          dataStatus: "unavailable",
          message: "Gateway disconnected; retrying",
        });
        retry = setTimeout(connect, 3000);
      };
    };

    connect();
    return () => {
      stopped = true;
      if (retry) clearTimeout(retry);
      socket?.close();
    };
  }, []);

  return connection;
}
