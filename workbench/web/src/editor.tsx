import { useState } from "react";
import { Button } from "./components/ui/button";
export function human(s: string) {
  return s
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}
const protectedKey = (k: string) =>
  /sha256$/.test(k) ||
  [
    "schema_version",
    "profile",
    "profile_id",
    "catalog",
    "code_sha256",
  ].includes(k);
export function Tree({
  value,
  label = "Details",
  depth = 0,
}: {
  value: any;
  label?: string;
  depth?: number;
}) {
  const [opened, setOpened] = useState(depth < 1);
  if (value === null || typeof value !== "object")
    return (
      <div className="value-row">
        <span>{human(label)}</span>
        <b>{value === null ? "Not supplied" : String(value)}</b>
      </div>
    );
  return (
    <details
      open={opened}
      onToggle={(e) => setOpened(e.currentTarget.open)}
      className="tree"
    >
      <summary>
        {human(label)}{" "}
        <small>
          {Array.isArray(value)
            ? `${value.length} items`
            : `${Object.keys(value).length} fields`}
        </small>
      </summary>
      <div>
        {opened &&
          Object.entries(value).map(([k, v]) => (
            <Tree key={k} value={v} label={k} depth={depth + 1} />
          ))}
      </div>
    </details>
  );
}
// A verified example is a starting document, never advertised as a complete schema.
export function Editor({
  value,
  onChange,
  label = "Input",
  depth = 0,
  path = "input",
  readonly = false,
}: {
  value: any;
  onChange: (v: any) => void;
  label?: string;
  depth?: number;
  path?: string;
  readonly?: boolean;
}) {
  const [kind, setKind] = useState("text");
  const locked = readonly || protectedKey(label);
  if (value !== null && typeof value === "object") {
    const arr = Array.isArray(value);
    return (
      <details className="editor-group" open={depth < 2}>
        <summary>
          {human(label)}{" "}
          <small>
            {arr ? `${value.length} items` : "Fields"}
            {locked ? " · pinned contract" : ""}
          </small>
        </summary>
        <div className="fields">
          {Object.entries(value).map(([k, v]) => (
            <div key={k} className="field-wrap">
              <Editor
                value={v}
                label={arr ? `${label} ${Number(k) + 1}` : k}
                depth={depth + 1}
                path={`${path}.${k}`}
                readonly={locked}
                onChange={(next) => {
                  const out = arr ? [...value] : { ...value };
                  out[k] = next;
                  onChange(out);
                }}
              />
              {arr && !locked && (
                <Button
                  variant="ghost"
                  type="button"
                  aria-label={`Remove ${label} ${Number(k) + 1}`}
                  onClick={() =>
                    onChange(
                      value.filter((_: any, i: number) => i !== Number(k)),
                    )
                  }
                >
                  Remove
                </Button>
              )}
            </div>
          ))}
          {arr && !locked && (
            <Button
              type="button"
              variant="outline"
              onClick={() =>
                onChange([
                  ...value,
                  value.length ? structuredClone(value[value.length - 1]) : "",
                ])
              }
            >
              Add {human(label)} item
            </Button>
          )}
        </div>
      </details>
    );
  }
  return (
    <label className="field">
      <span>
        {human(label)} {locked && <small>pinned</small>}
      </span>
      {typeof value === "boolean" ? (
        <input
          aria-label={path}
          type="checkbox"
          checked={value}
          disabled={locked}
          onChange={(e) => onChange(e.target.checked)}
        />
      ) : (
        <>
          <input
            aria-label={path}
            readOnly={locked}
            type={typeof value === "number" ? "number" : "text"}
            step="any"
            value={value === null ? "" : String(value)}
            placeholder={value === null ? "Unspecified (null)" : undefined}
            onChange={(e) =>
              onChange(
                typeof value === "number"
                  ? Number(e.target.value)
                  : e.target.value,
              )
            }
          />
          {value === null && !locked && (
            <select
              aria-label={`${path} null type`}
              value={kind}
              onChange={(e) => {
                setKind(e.target.value);
                if (e.target.value === "boolean") onChange(false);
                if (e.target.value === "number") onChange(0);
                if (e.target.value === "object") onChange({});
                if (e.target.value === "array") onChange([]);
              }}
            >
              <option value="text">Enter text, or leave null</option>
              <option value="number">Use number</option>
              <option value="boolean">Use boolean</option>
              <option value="object">Use object</option>
              <option value="array">Use array</option>
            </select>
          )}
        </>
      )}
    </label>
  );
}
function literal(v: string | undefined) {
  if (!v) return "";
  try {
    return JSON.parse(v.replaceAll("'", '"'));
  } catch {
    return "";
  }
}
export function cliValues(op: any, args: string[]) {
  const out: Record<string, string> = {};
  let pos = 0;
  for (const f of op.cli_arguments || []) {
    const name = f.names[0];
    if (name === "--kernel" || name === "--format") continue;
    if (!name.startsWith("--")) out[name] = args[pos++] || "";
    else {
      const i = args.indexOf(name);
      out[name] =
        i < 0
          ? ""
          : f.options.action === "'store_true'"
            ? "true"
            : args[i + 1] || "";
    }
  }
  return out;
}
export function cliArguments(op: any, vals: Record<string, string>) {
  const args: string[] = [];
  for (const f of op.cli_arguments || []) {
    const n = f.names[0];
    if (n === "--kernel" || n === "--format") continue;
    const v = vals[n] || "";
    if (!n.startsWith("--")) args.push(v);
    else if (v) {
      args.push(n);
      if (f.options.action !== "'store_true'") args.push(v);
    }
  }
  return args;
}
export function CLIEditor({
  op,
  args,
  onChange,
}: {
  op: any;
  args: string[];
  onChange: (a: string[]) => void;
}) {
  const vals = cliValues(op, args);
  return (
    <div className="fields">
      {op.cli_arguments
        .filter((f: any) => !["--kernel", "--format"].includes(f.names[0]))
        .map((f: any) => {
          const n = f.names[0],
            choices = literal(f.options.choices),
            flag = f.options.action === "'store_true'";
          return (
            <label className="field" key={n}>
              <span>
                {human(n.replace(/^--/, ""))}{" "}
                {!n.startsWith("--") && <small>required</small>}
              </span>
              {flag ? (
                <input
                  type="checkbox"
                  aria-label={n}
                  checked={!!vals[n]}
                  onChange={(e) =>
                    onChange(
                      cliArguments(op, {
                        ...vals,
                        [n]: e.target.checked ? "true" : "",
                      }),
                    )
                  }
                />
              ) : Array.isArray(choices) ? (
                <select
                  aria-label={n}
                  value={vals[n]}
                  onChange={(e) =>
                    onChange(cliArguments(op, { ...vals, [n]: e.target.value }))
                  }
                >
                  <option value="">
                    {f.options.default
                      ? `Default: ${f.options.default}`
                      : "Select…"}
                  </option>
                  {choices.map((v: any) => (
                    <option key={v}>{v}</option>
                  ))}
                </select>
              ) : (
                <input
                  aria-label={n}
                  type={
                    ["float", "int"].includes(f.options.type)
                      ? "number"
                      : "text"
                  }
                  step={f.options.type === "int" ? 1 : "any"}
                  value={vals[n]}
                  placeholder={String(literal(f.options.default) || "")}
                  onChange={(e) =>
                    onChange(cliArguments(op, { ...vals, [n]: e.target.value }))
                  }
                />
              )}
              <small>
                {f.options.help?.replace(/^'|'$/g, "") ||
                  (!n.startsWith("--")
                    ? "Native positional input"
                    : "Optional native setting")}
              </small>
            </label>
          );
        })}
    </div>
  );
}
