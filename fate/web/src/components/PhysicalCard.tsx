import type { ReactNode } from "react";
import { useArtifactLight } from "./ArtifactSurface";

export function PhysicalCard({
  children,
  still,
}: {
  children: ReactNode;
  still: boolean;
}) {
  const light = useArtifactLight(still);
  return (
    <div className="physical-card" {...light}>
      {children}
    </div>
  );
}
