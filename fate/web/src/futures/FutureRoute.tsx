import { useEffect, useState, type ComponentProps } from "react";
import type FutureScreen from "./FutureScreen";

type FutureModule = { default: typeof FutureScreen };
let ready: FutureModule | undefined;
let pending: Promise<FutureModule> | undefined;

function loadRoom() {
  return (pending ??= import("./FutureScreen")
    .then((module) => (ready = module))
    .catch((error) => {
      pending = undefined;
      throw error;
    }));
}

export function warmFutureRoom() {
  void loadRoom().catch(() => {});
}

export function FutureRoute(props: ComponentProps<typeof FutureScreen>) {
  const [route, setRoute] = useState<FutureModule | undefined>(() => ready);
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    if (route) return;
    let current = true;
    void loadRoom().then(
      (module) => {
        if (current) setRoute(module);
      },
      () => {
        if (current) setFailed(true);
      },
    );
    return () => {
      current = false;
    };
  }, [route]);
  if (route) return <route.default {...props} />;
  return failed ? (
    <p className="scope-note" role="alert">
      The room could not load. Refresh this page to try again.
    </p>
  ) : (
    <p className="scope-note" role="status">
      Opening the instrument…
    </p>
  );
}
