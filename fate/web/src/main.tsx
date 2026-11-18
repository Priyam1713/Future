import { ArrowUpRight, Info, Volume2, VolumeX } from "lucide-react";
import { createRoot } from "react-dom/client";
import { useOracle } from "./hooks/useOracle";
import ExploreScreen from "./screens/ExploreScreen";
import RitualScreen from "./screens/RitualScreen";
import ReadingScreen from "./screens/ReadingScreen";
import { SettingsDialog } from "./components/SettingsDialog";
import "./style.css";
import "./cinematic.css";
function App() {
  const oracle = useOracle();
  const { screen, reduced, paused, dialog, sound, navigate, skipToContent } =
    oracle;
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
          <img src="/art/fate_sigil.svg" alt="" width="34" height="34" />
          <span>FATE</span>
        </a>
        <span className="masthead-caption">THE FUTURE IS YOURS TO EXPLORE</span>
        <div className="header-actions">
          <button
            className="icon-button"
            aria-label={sound.on ? "Mute sound" : "Enable sound"}
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
      <main id="main" tabIndex={-1}>
        {screen === "explore" ? (
          <ExploreScreen oracle={oracle} />
        ) : screen === "ritual" ? (
          <RitualScreen oracle={oracle} />
        ) : (
          <ReadingScreen oracle={oracle} />
        )}
      </main>
      <footer>
        <img src="/art/fate_sigil.svg" alt="" width="22" height="22" />
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
