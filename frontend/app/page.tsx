import { Sidebar } from "@/components/layout/sidebar";
import { Terminal } from "@/components/market/terminal";

export default function Home() {
  return (
    <div className="app-shell">
      <Sidebar />
      <Terminal />
    </div>
  );
}
