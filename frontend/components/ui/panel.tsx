import type { HTMLAttributes, ReactNode } from "react";

import { cn } from "@/lib/cn";

interface PanelProps extends HTMLAttributes<HTMLElement> {
  title: string;
  eyebrow?: string;
  action?: ReactNode;
}

export function Panel({
  title,
  eyebrow,
  action,
  className,
  children,
  ...props
}: PanelProps) {
  return (
    <section className={cn("panel", className)} {...props}>
      <header className="panel__header">
        <div>
          {eyebrow ? <p className="eyebrow">{eyebrow}</p> : null}
          <h2 className="panel__title">{title}</h2>
        </div>
        {action}
      </header>
      <div className="panel__content">{children}</div>
    </section>
  );
}
