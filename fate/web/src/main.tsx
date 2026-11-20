import { ArrowUpRight, Info, Volume2, VolumeX } from "lucide-react";
import { createRoot } from "react-dom/client";
import { useOracle } from "./hooks/useOracle";
import ExploreScreen from "./screens/ExploreScreen";
import RitualScreen from "./screens/RitualScreen";
import ReadingScreen from "./screens/ReadingScreen";
import { SettingsDialog } from "./components/SettingsDialog";
import "./style.css";
import "./cinematic.css";
import "./gallery.css";
import "./codex.css";
import "./astrology.css";
import "./turning.css";
import "./chambers.css";
import "./ritual.css";
import "./signs.css";
import "./manuscript.css";
import "./futures.css";
import "./living.css";
import "./platform.css";
import { isGame } from "./arcade/games";
import { FutureRoute } from "./futures/FutureRoute";
import { futureId } from "./futures/contracts";
import { roomId } from "./manuscript/contracts";
import { signId } from "./signs/contracts";
import { ritualId } from "./ritual/contracts";
import { chamberId } from "./chambers/contracts";
import { lazy, Suspense } from "react";
const WesternScreen = lazy(() => import("./screens/WesternScreen"));
const NumerologyScreen = lazy(() => import("./screens/NumerologyScreen"));
const CodexScreen = lazy(() => import("./screens/CodexScreen"));
const GalleryScreen = lazy(() => import("./screens/GalleryScreen"));
const ChamberScreen = lazy(() => import("./chambers/ChamberScreen"));
const RitualWing = lazy(() => import("./ritual/RitualWingScreen"));
const SignsScreen = lazy(() => import("./signs/SignsScreen"));
const Manuscript = lazy(() => import("./manuscript/ManuscriptScreen"));
const PlayScreen = lazy(() => import("./arcade/PlayScreen"));
function App() {
  const oracle = useOracle();
  const { screen, reduced, paused, dialog, sound, navigate, skipToContent } =
    oracle;
  const chamber = chamberId(screen);
  const wing = ritualId(screen);
  const sign = signId(screen);
  const folio = roomId(screen);
  const future = futureId(screen);
  const playing = screen === "play" || isGame(screen);
  return (
    <div className={`app ${reduced || paused ? "still" : ""}`}>
      <a
        className="skip"
        href="#main"
        onClick={(event) => {
          event.preventDefault();
          skipToContent();
        }}
      >
        Skip to content
      </a>
      <header className="masthead">
        <a
          href="#explore"
          className="wordmark"
          onClick={(e) => {
            e.preventDefault();
            navigate("explore");
          }}
          aria-label="FATE home"
        >
          <img src="/art/fate-seal.svg" alt="" width="34" height="34" />
          <span>FATE</span>
        </a>
        <span className="masthead-caption">THE FUTURE IS YOURS TO EXPLORE</span>
        <div className="header-actions">
          <button
            className="icon-button"
            aria-label={sound.on ? "Mute sound" : "Enable sound"}
            data-sound-toggle
            aria-pressed={sound.on}
            onClick={() => void sound.toggle()}
          >
            {sound.on ? <Volume2 size={18} /> : <VolumeX size={18} />}
          </button>
          <button
            className="icon-button"
            aria-label="About FATE and settings"
            onClick={() => dialog.current?.showModal()}
          >
            <Info size={18} />
          </button>
        </div>
      </header>
      <nav className="fate-navigation" aria-label="FATE navigation">
        {(
          [
            { screen: "explore", href: "#explore", label: "Explore" },
            { screen: "gallery", href: "#gallery", label: "54 techniques" },
            { screen: "play", href: "#play", label: "Play" },
            { screen: "codex", href: "#my-fate", label: "My Fate" },
          ] as const
        ).map((item) => (
          <a
            key={item.screen}
            href={item.href}
            aria-current={
              screen === item.screen || (item.screen === "play" && playing)
                ? "page"
                : undefined
            }
            onClick={(e) => {
              if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
              e.preventDefault();
              navigate(item.screen);
            }}
          >
            <span>{item.label}</span>
            {item.screen === "codex" && oracle.codex.chapters.length > 0 && (
              <small
                aria-label={`${oracle.codex.chapters.length} saved chapters`}
              >
                {oracle.codex.chapters.length}
              </small>
            )}
          </a>
        ))}
      </nav>
      <main id="main" tabIndex={-1}>
        {playing ? (
          <Suspense
            fallback={
              <p className="scope-note" role="status">
                Opening the Play Hall…
              </p>
            }
          >
            <PlayScreen oracle={oracle} />
          </Suspense>
        ) : future ? (
          <FutureRoute key={future} id={future} oracle={oracle} />
        ) : folio ? (
          <Suspense
            fallback={
              <p className="scope-note" role="status">
                Opening the instrument…
              </p>
            }
          >
            <Manuscript key={folio} id={folio} oracle={oracle} />
          </Suspense>
        ) : sign ? (
          <Suspense
            fallback={
              <p className="scope-note" role="status">
                Opening the observatory…
              </p>
            }
          >
            <SignsScreen key={sign} id={sign} oracle={oracle} />
          </Suspense>
        ) : wing ? (
          <Suspense
            fallback={
              <p className="scope-note" role="status">
                Opening the ritual…
              </p>
            }
          >
            <RitualWing id={wing} key={wing} oracle={oracle} />
          </Suspense>
        ) : chamber ? (
          <Suspense
            fallback={
              <p className="scope-note" role="status">
                Opening the chamber…
              </p>
            }
          >
            <ChamberScreen key={chamber} id={chamber} oracle={oracle} />
          </Suspense>
        ) : screen === "explore" ? (
          <ExploreScreen oracle={oracle} />
        ) : screen === "codex" ? (
          <Suspense
            fallback={
              <p className="scope-note" role="status">
                Opening your Codex…
              </p>
            }
          >
            <CodexScreen oracle={oracle} />
          </Suspense>
        ) : screen === "gallery" ? (
          <Suspense
            fallback={
              <p className="scope-note" role="status">
                Opening the collection…
              </p>
            }
          >
            <GalleryScreen oracle={oracle} />
          </Suspense>
        ) : screen === "western" ? (
          <Suspense
            fallback={
              <p className="scope-note" role="status">
                Opening the Astral Observatory...
              </p>
            }
          >
            <WesternScreen oracle={oracle} />
          </Suspense>
        ) : screen === "numerology" ? (
          <Suspense
            fallback={
              <p className="scope-note" role="status">
                Opening the observatory…
              </p>
            }
          >
            <NumerologyScreen oracle={oracle} />
          </Suspense>
        ) : screen === "ritual" ? (
          <RitualScreen oracle={oracle} />
        ) : (
          <ReadingScreen oracle={oracle} />
        )}
      </main>
      <footer>
        <img src="/art/fate-seal.svg" alt="" width="22" height="22" />
        <p>A little mystery. A new perspective.</p>
        <span>SYMBOLIC REFLECTION · NOT A CERTAIN FORECAST</span>
        <button
          className="text-button"
          onClick={() => dialog.current?.showModal()}
        >
          About this experience <ArrowUpRight size={12} />
        </button>
      </footer>
      <SettingsDialog oracle={oracle} />
    </div>
  );
}
createRoot(document.getElementById("root")!).render(<App />);
