import type { ReactNode } from "react";

export function ResultLeaf({
  status,
  title,
  children,
  evidence,
}: {
  status: string;
  title: string;
  children: ReactNode;
  evidence?: ReactNode;
}) {
  return (
    <div className="result-leaf">
      <div className="result-leaf-main">
        <p className="eyebrow">{status}</p>
        <h2>{title}</h2>
        {children}
      </div>
      {evidence}
    </div>
  );
}
