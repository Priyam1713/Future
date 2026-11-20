import {
  useEffect,
  useRef,
  useState,
  type CSSProperties,
  type KeyboardEvent,
} from "react";
import {
  ArrowLeft,
  ArrowUpRight,
  AudioWaveform,
  CircuitBoard,
  Grid3X3,
} from "lucide-react";
import { api } from "../types";
import type { Oracle } from "../hooks/useOracle";
import type { Study } from "../futures/contracts";
import { Circuit } from "../futures/Instruments";
import { ArtifactSurface } from "../components/ArtifactSurface";
import { Sources } from "../futures/Sources";
import { channels, games, mission, programs, settle, type Game } from "./games";
import "./arcade.css";

const icons = [Grid3X3, CircuitBoard, AudioWaveform];
const secureDraw = () =>
  crypto.getRandomValues(new Uint32Array(1))[0] / 2 ** 32;

function Loom({
  cells,
  initial,
  toggle,
  locked,
}: {
  cells: number[];
  initial: number[];
  toggle: (index: number) => void;
  locked: boolean;
}) {
  const [cursor, setCursor] = useState(24);
  function move(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    const next: Record<string, number> = {
      ArrowLeft: index % 7 ? index - 1 : index,
      ArrowRight: index % 7 < 6 ? index + 1 : index,
      ArrowUp: index >= 7 ? index - 7 : index,
      ArrowDown: index < 42 ? index + 7 : index,
      Home: 0,
      End: 48,
    };
    if (!(event.key in next)) return;
    event.preventDefault();
    const target = event.currentTarget.parentElement?.children[
      next[event.key]
    ] as HTMLButtonElement | undefined;
    target?.focus();
  }
  return (
    <div
      className="arcade-loom"
      role="group"
      aria-label={locked ? "Final cell pattern" : "Starting cell pattern"}
    >
      {cells.map((bit, index) =>
        locked ? (
          <span key={index} data-alive={Boolean(bit)} aria-hidden="true" />
        ) : (
          <button
            key={index}
            type="button"
            tabIndex={index === cursor ? 0 : -1}
            data-alive={Boolean(bit)}
            data-changed={bit !== initial[index]}
            aria-label={`Cell ${Math.floor(index / 7) + 1},${(index % 7) + 1}`}
            aria-pressed={Boolean(bit)}
            onFocus={() => setCursor(index)}
            onKeyDown={(event) => move(event, index)}
            onClick={() => toggle(index)}
          />
        ),
      )}
    </div>
  );
}

function Switchboard({
  picked,
  choose,
  targets,
  study,
}: {
  picked: number | null;
  choose: (option: number) => void;
  targets: readonly string[];
  study?: Study;
}) {
  return (
    <div className="arcade-switchboard">
      <div
        className="arcade-ports"
        aria-label={`Target outputs ${targets.join(" and ")}`}
      >
        {channels.map((bit) => (
          <span key={bit} data-target={targets.includes(bit)}>
            {bit}
          </span>
        ))}
      </div>
      {study ? (
        <Circuit data={study.view.instrument} />
      ) : (
        <div
          className="arcade-cartridges"
          role="group"
          aria-label="Wire cartridges"
        >
          {programs.map(([name, route], index) => (
            <button
              type="button"
              key={name}
              className="tactile"
              aria-pressed={picked === index}
              onClick={() => choose(index)}
            >
              <CircuitBoard size={24} aria-hidden="true" />
              <strong>{name}</strong>
              <small>{route}</small>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

function Receiver({
  forecast,
  change,
  detected,
}: {
  forecast: number;
  change?: (value: number) => void;
  detected?: boolean;
}) {
  return (
    <div className="arcade-receiver" data-detected={detected}>
      <div
        className="arcade-dial"
        style={{ "--forecast": forecast } as CSSProperties}
      >
        <svg viewBox="0 0 180 180" aria-hidden="true">
          <circle cx="90" cy="90" r="77" className="dial-scale" />
          <circle cx="90" cy="90" r="59" className="dial-glass" />
          <path d="M90 90 90 22" className="forecast-needle" />
        </svg>
        <strong>{forecast}%</strong>
      </div>
      {detected !== undefined ? (
        <p className="arcade-reception">
          {detected ? "Pulse logged" : "Receiver quiet"}
        </p>
      ) : (
        change && (
          <label className="arcade-tuner">
            <span>Your probability of a signal</span>
            <input
              type="range"
              min={0}
              max={100}
              step={1}
              value={forecast}
              aria-valuetext={forecast + "%"}
              onChange={(event) => change(event.target.valueAsNumber)}
            />
          </label>
        )
      )}
    </div>
  );
}

function GameRoom({ game, oracle }: { game: Game; oracle: Oracle }) {
  const [round, setRound] = useState(0);
  const [started, setStarted] = useState(false);
  const task = mission(round);
  const [cells, setCells] = useState(() => task.cells);
  const [picked, setPicked] = useState<number | null>(null);
  const [forecast, setForecast] = useState(20);
  const [generation, setGeneration] = useState(0);
  const [proof, setProof] = useState<{ study: Study; sample: number }>();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const flight = useRef<AbortController | null>(null);
  const resultHeading = useRef<HTMLHeadingElement>(null);
  const gameStage = useRef<HTMLHeadingElement>(null);
  const instrument = useRef<HTMLDivElement>(null);
  const study = proof?.study;
  const result =
    proof && settle(game.id, round, forecast, proof.study, proof.sample);
  const edits = cells.filter((bit, i) => bit !== task.cells[i]).length;
  const frames = study?.view.instrument.frames;
  useEffect(() => () => flight.current?.abort(), []);
  useEffect(() => {
    if (result) resultHeading.current?.focus();
    else if (started)
      instrument.current
        ?.querySelector<HTMLElement>("button[tabindex='0'], button, input")
        ?.focus();
  }, [Boolean(result), started, round]);

  function toggle(index: number) {
    if (!started || busy || (edits >= 3 && cells[index] === task.cells[index]))
      return;
    setCells(cells.map((bit, i) => (index === i ? 1 - bit : bit)));
    oracle.sound.cue("select");
  }
  async function submit() {
    if (flight.current || study) return;
    const request =
      game.id === "play-loom"
        ? { option: 4, cells }
        : game.id === "play-switch"
          ? { option: picked }
          : { option: task.clue.option };
    if (request.option === null) return;
    const controller = new AbortController();
    flight.current = controller;
    setBusy(true);
    setError("");
    try {
      const response = await api<Study>(
        "/api/future-study",
        { oracle: game.oracle, ...request },
        controller.signal,
      );
      if (controller.signal.aborted) return;
      setGeneration(
        response.view.instrument.frames?.length
          ? response.view.instrument.frames.length - 1
          : 0,
      );
      setProof({
        study: response,
        sample: game.id === "play-signal" ? secureDraw() : 0,
      });
      oracle.sound.cue("reveal");
    } catch (failure) {
      if (!controller.signal.aborted) setError((failure as Error).message);
    } finally {
      flight.current = null;
      if (!controller.signal.aborted) setBusy(false);
    }
  }
  function replay() {
    setRound(round + 1);
    setCells(mission(round + 1).cells);
    setForecast(20);
    setPicked(null);
    setProof(undefined);
    setGeneration(0);
    setError("");
  }
  return (
    <div className={`arcade-layout ${game.id}`}>
      <div className="arcade-instrument-wrap" ref={instrument}>
        <ArtifactSurface
          still={oracle.reduced || oracle.paused}
          className="arcade-instrument"
        >
          {started && !result && (
            <p className="arcade-instrument-brief">
              {game.id === "play-loom"
                ? `Target ${task.goal} cells · ${3 - edits} edits left`
                : game.id === "play-switch"
                  ? "Keep both marked outputs fed"
                  : task.clue.copy}
            </p>
          )}
          {!started && (
            <div className="arcade-instrument-preview" aria-hidden="true">
              {game.id === "play-loom" ? (
                <Loom cells={cells} initial={cells} toggle={() => {}} locked />
              ) : game.id === "play-switch" ? (
                <CircuitBoard size={132} strokeWidth={0.65} />
              ) : (
                <Receiver forecast={20} />
              )}
            </div>
          )}
          {started && game.id === "play-loom" && (
            <>
              <Loom
                cells={frames?.[generation] ?? cells}
                initial={task.cells}
                toggle={toggle}
                locked={Boolean(frames)}
              />
              {frames && (
                <label className="arcade-tuner">
                  <span>
                    Generation <b>{generation} of 4</b>
                  </span>
                  <input
                    type="range"
                    min={0}
                    max={4}
                    value={generation}
                    onChange={(event) =>
                      setGeneration(event.target.valueAsNumber)
                    }
                  />
                </label>
              )}
            </>
          )}
          {started && game.id === "play-switch" && (
            <Switchboard
              picked={picked}
              choose={(option) => {
                if (!busy) {
                  setPicked(option);
                  oracle.sound.cue("select");
                }
              }}
              targets={task.targets}
              study={study}
            />
          )}
          {started && game.id === "play-signal" && (
            <Receiver
              forecast={forecast}
              change={(value) => {
                if (!busy) setForecast(value);
              }}
              detected={result ? result.title === "Signal received" : undefined}
            />
          )}
        </ArtifactSurface>
      </div>
      <div className="arcade-console" aria-busy={busy}>
        {result ? (
          <div className="artifact-arrival">
            <p className="eyebrow">Round {round + 1} · Virtual points</p>
            <h2 ref={resultHeading} tabIndex={-1}>
              {result.title}
            </h2>
            <p className="arcade-score">
              {result.points}
              <small> / 100</small>
            </p>
            <p>{result.detail}</p>
            <button className="primary tactile" onClick={replay}>
              Play next round
            </button>
            <Sources sources={study!.sources} />
          </div>
        ) : (
          <>
            <p className="eyebrow">
              {started ? `Round ${round + 1}` : game.tag}
            </p>
            <h2 ref={gameStage} tabIndex={-1}>
              {!started
                ? "Your objective"
                : game.id === "play-loom"
                  ? `Keep ${task.goal} cells alive`
                  : game.id === "play-switch"
                    ? `Feed ports ${task.targets.join(" and ")}`
                    : "Will the signal arrive?"}
            </h2>
            {!started ? (
              <>
                <p>{game.instruction}</p>
                <button
                  className="primary tactile"
                  onClick={() => setStarted(true)}
                >
                  Begin round
                </button>
              </>
            ) : (
              <>
                <p>
                  {game.id === "play-loom"
                    ? "Select cells to toggle them. Use arrow keys to move around the board."
                    : game.id === "play-switch"
                      ? "Select a cartridge to set the gates on both wires."
                      : task.clue.copy}
                </p>
                {game.id === "play-loom" && (
                  <p role="status">
                    <strong>{3 - edits}</strong> changes available
                  </p>
                )}
                {game.id === "play-signal" && (
                  <p>
                    Starting chance <strong>20%</strong> · Evidence ratio{" "}
                    <strong>{task.clue.ratio}</strong>
                  </p>
                )}
                <button
                  className="primary tactile"
                  disabled={
                    busy || (game.id === "play-switch" && picked === null)
                  }
                  onClick={() => void submit()}
                >
                  {busy
                    ? "Resolving…"
                    : game.id === "play-loom"
                      ? "Advance four generations"
                      : game.id === "play-switch"
                        ? "Send the pulse"
                        : "Seal my forecast"}
                </button>
              </>
            )}
          </>
        )}
        {error && <p role="alert">{error}</p>}
      </div>
    </div>
  );
}

export default function PlayScreen({ oracle }: { oracle: Oracle }) {
  const game = games.find(({ id }) => id === oracle.screen);
  const header = useRef<HTMLHeadingElement>(null);
  useEffect(() => {
    if (document.activeElement === document.body) {
      const from = oracle.playReturn.current;
      const link = !game && from ? document.getElementById(from) : null;
      (link ?? header.current)?.focus({ preventScroll: true });
    }
  }, [game]);
  return (
    <article className="arcade" data-game={game?.id}>
      <header className="arcade-hero">
        <picture aria-hidden="true">
          <source
            media="(max-width: 700px)"
            srcSet="/art/future-tomorrow-720.webp"
          />
          <img
            src="/art/future-tomorrow-1440.webp"
            alt=""
            width="1440"
            height="960"
          />
        </picture>
        <div>
          {game && (
            <button
              className="text-button arcade-return"
              onClick={() => oracle.navigate("play")}
            >
              <ArrowLeft size={16} aria-hidden="true" /> Play hall
            </button>
          )}
          <p className="eyebrow">{game ? game.tag : "FATE · Arcade"}</p>
          <h1 tabIndex={-1} ref={header}>
            {game?.name ?? "The Play Hall"}
          </h1>
          {!game && <p>Three instruments. A few choices. See what follows.</p>}
        </div>
      </header>
      {game ? (
        <GameRoom key={game.id} game={game} oracle={oracle} />
      ) : (
        <nav className="arcade-doors" aria-label="Arcade games">
          {games.map((entry, i) => {
            const Icon = icons[i];
            return (
              <a
                id={entry.id}
                key={entry.id}
                href={`#${entry.id}`}
                onClick={(event) => {
                  if (
                    event.ctrlKey ||
                    event.metaKey ||
                    event.shiftKey ||
                    event.altKey
                  )
                    return;
                  event.preventDefault();
                  oracle.playReturn.current = entry.id;
                  oracle.sound.cue("select");
                  oracle.navigate(entry.id);
                }}
              >
                <Icon strokeWidth={1.2} size={50} aria-hidden="true" />
                <span>
                  <small>{entry.tag}</small>
                  <strong>{entry.name}</strong>
                </span>
                <ArrowUpRight size={20} aria-hidden="true" />
              </a>
            );
          })}
        </nav>
      )}
      <p className="arcade-scope">
        Simulated outcomes and virtual points · played in this visit
      </p>
    </article>
  );
}
