import { cn } from "@/lib/cn";

type Tone = "neutral" | "success" | "warning" | "danger";

const toneClass: Record<Tone, string> = {
  neutral: "status-badge--neutral",
  success: "status-badge--success",
  warning: "status-badge--warning",
  danger: "status-badge--danger",
};

interface StatusBadgeProps {
  label: string;
  tone?: Tone;
}

export function StatusBadge({ label, tone = "neutral" }: StatusBadgeProps) {
  return (
    <span className={cn("status-badge", toneClass[tone])}>
      <span className="status-badge__marker" aria-hidden="true" />
      {label}
    </span>
  );
}
