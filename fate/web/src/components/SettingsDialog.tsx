import { Compass, X } from "lucide-react";
import type { Oracle } from "../hooks/useOracle";
export function SettingsDialog({ oracle }: { oracle: Oracle }) {
  const { dialog, paused, setPaused, reduced, sound } = oracle;
  return (
    <dialog
      ref={dialog}
      className="settings-dialog"
      onClick={(e) => {
        if (e.target === dialog.current) dialog.current?.close();
      }}
    >
      <button
        className="icon-button close-dialog"
        aria-label="Close settings"
        onClick={() => dialog.current?.close()}
      >
        <X size={20} />
      </button>
      <img src="/art/fate_sigil.svg" alt="" width="44" height="44" />
      <p className="eyebrow">FATE · THE LIVING ORACLE</p>
      <h2>A space for wonder.</h2>
      <p>
        Tarot is a symbolic tradition, not an empirically validated forecast.
        FATE uses the existing Future engine’s Waite 1922 text profile, with
        historical Pamela Colman Smith illustrations and an original FATE card
        back.
      </p>
      <p>
        Numerology uses the existing Future Decoz component-reduction profile.
        Its direct interpretations cover Expression and Personal Year; other
        numbers are calculated context. The Gallery distinguishes open consumer
        rooms from upcoming experiences and historical references.
      </p>
      <p>
        No account or automatic personal-data storage. Your question, name or
        dates are processed by this server for your reading. Gemini is optional
        and requires explicit consent. Numerology commentary sends only
        source-grounded themes to Google, without your name or dates.
        Explored-room markers last only until you reload this page. Save to this device explicitly keeps a minimal Codex chapter in this browser, excluding original inputs and Gemini commentary. Local chapters are unencrypted, can be cleared by browser policies, and have no automatic backup or sync. Manage and export them in My Fate.
      </p>
      <div className="settings-row">
        <span>Atmosphere</span>
        <button className="secondary" onClick={() => setPaused((p) => !p)}>
          {paused ? "Resume motion" : "Pause motion"}
        </button>
      </div>
      <p className="settings-note">
        {reduced
          ? "Your device’s reduced-motion preference is active."
          : "Your device’s reduced-motion preference is respected."}
      </p>
      <div className="settings-row">
        <span>Sound</span>
        <button className="secondary" onClick={() => void sound.toggle()}>
          {sound.on ? "Turn off" : "Turn on"}
        </button>
      </div>
      <label className="volume-label">
        Ambient volume{" "}
        <input
          type="range"
          min="0"
          max="0.4"
          step="0.01"
          value={sound.music}
          onChange={(e) => sound.setMusic(Number(e.target.value))}
        />
      </label>
      <label className="volume-label">
        Card & selection volume{" "}
        <input
          type="range"
          min="0"
          max="0.6"
          step="0.01"
          value={sound.effects}
          onChange={(e) => sound.setEffects(Number(e.target.value))}
        />
      </label>
      <div className="about-colophon">
        <Compass size={16} /> CHAPTER 01 · BUILT FOR CURIOSITY
      </div>
    </dialog>
  );
}
