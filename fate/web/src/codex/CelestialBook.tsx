import { useEffect, useRef, useState } from "react";
import type { Oracle } from "../hooks/useOracle";
import type { Chapter } from "./records";
import { chapterTitle } from "./reference";
import { ChapterContent, ChapterIllustration } from "./ChapterContent";
import { initialQuality } from "../orb/policy";
export function CelestialBook({
  oracle,
  onCompare,
}: {
  oracle: Oracle;
  onCompare: (id: string) => void;
}) {
  const { codex } = oracle;
  const [open, setOpen] = useState(!!codex.selectedId),
    [visible, setVisible] = useState(false),
    [hidden, setHidden] = useState(document.hidden);
  const [quality] = useState(initialQuality);
  const [wide, setWide] = useState(
    () => matchMedia("(min-width:701px)").matches,
  );
  const [coverGone, setCoverGone] = useState(false);
  const [oldScroll, setOldScroll] = useState(0);
  const [old, setOld] = useState<Chapter | null>(null),
    [direction, setDirection] = useState(1);
  const host = useRef<HTMLDivElement>(null),
    cover = useRef<HTMLButtonElement>(null),
    timer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);
  const index = Math.max(
    0,
    codex.chapters.findIndex((c) => c.id === codex.selectedId),
  );
  const current = codex.chapters[index];
  const moving = !oracle.reduced && !oracle.paused && visible && !hidden;
  useEffect(() => {
    if (!open) {
      setCoverGone(false);
      return;
    }
    if (oracle.reduced || oracle.paused) {
      setCoverGone(true);
      return;
    }
    const id = setTimeout(() => setCoverGone(true), 880);
    return () => clearTimeout(id);
  }, [open, oracle.reduced, oracle.paused]);
  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) =>
      setVisible(entry.isIntersecting),
    );
    if (host.current) observer.observe(host.current);
    const visibility = () => setHidden(document.hidden);
    document.addEventListener("visibilitychange", visibility);
    const width = matchMedia("(min-width:701px)");
    const resize = () => setWide(width.matches);
    width.addEventListener("change", resize);
    return () => {
      observer.disconnect();
      document.removeEventListener("visibilitychange", visibility);
      width.removeEventListener("change", resize);
      clearTimeout(timer.current);
    };
  }, []);
  useEffect(() => {
    if (open)
      host.current
        ?.querySelector<HTMLElement>(".codex-current h2")
        ?.focus({ preventScroll: true });
  }, [open, current?.id]);
  useEffect(() => {
    if (open)
      host.current?.scrollIntoView({ block: "start", behavior: "instant" });
  }, [open]);
  useEffect(() => {
    if (old && !codex.chapters.some((c) => c.id === old.id)) setOld(null);
  }, [codex.chapters, old]);
  function select(next: number) {
    if (next < 0 || next >= codex.chapters.length || next === index) return;
    clearTimeout(timer.current);
    setDirection(next > index ? 1 : -1);
    setOld(moving ? current : null);
    setOldScroll(host.current?.querySelector(".codex-current")?.scrollTop ?? 0);
    codex.setSelectedId(codex.chapters[next].id);
    oracle.sound.cue("select");
    timer.current = setTimeout(() => setOld(null), 720);
  }
  function close() {
    setCoverGone(false);
    setOpen(false);
    setOld(null);
    requestAnimationFrame(() => cover.current?.focus());
  }
  const swipe = useRef<{ x: number; y: number } | null>(null);
  return (
    <div
      ref={host}
      className={`celestial-book ${open ? "book-open" : "book-closed"} ${moving ? "book-moving" : "book-still"} ${quality === "low" ? "book-economy" : ""}`}
      data-renderer="layered-codex"
      data-render-state={moving ? "running" : "paused"}
    >
      <div className="book-binding" aria-hidden="true" />
      <button
        ref={cover}
        className="codex-cover"
        style={coverGone ? { display: "none" } : undefined}
        aria-label="Open your Codex"
        aria-hidden={open || undefined}
        tabIndex={open ? -1 : 0}
        onClick={() => {
          setOpen(true);
          if (current) codex.setSelectedId(current.id);
          oracle.sound.cue("select");
        }}
      >
        <img
          src="/art/codex-cover-400.webp"
          srcSet="/art/codex-cover-400.webp 400w, /art/codex-cover-v1.webp 768w"
          sizes="(max-width:700px) 280px, 340px"
          alt=""
          width="768"
          height="1152"
        />
        <span className="cover-engraving">
          <small>THE LIVING CODEX</small>
          <strong>My Fate</strong>
          <i>A place for your perspectives.</i>
        </span>
        <span className="cover-collection">
          {codex.chapters.length
            ? `${codex.chapters.length} ${codex.chapters.length === 1 ? "CHAPTER" : "CHAPTERS"} KEPT HERE`
            : "YOUR STORY IS STILL UNWRITTEN"}
          <b>Open your Codex ↗</b>
        </span>
        <span className="codex-beam" />
        <span className="cover-spine" />
      </button>
      {open && (
        <div
          className="codex-spread"
          tabIndex={0}
          aria-label="Codex pages. Use left and right arrows to change chapter."
          onKeyDown={(e) => {
            if (e.target !== e.currentTarget) return;
            if (e.key === "ArrowRight") {
              e.preventDefault();
              select(index + 1);
            }
            if (e.key === "ArrowLeft") {
              e.preventDefault();
              select(index - 1);
            }
          }}
          onTouchStart={(e) => {
            if (e.touches.length !== 1) {
              swipe.current = null;
              return;
            }
            swipe.current = {
              x: e.touches[0].clientX,
              y: e.touches[0].clientY,
            };
          }}
          onTouchCancel={() => {
            swipe.current = null;
          }}
          onTouchEnd={(e) => {
            if (!swipe.current) return;
            const dx = e.changedTouches[0].clientX - swipe.current.x,
              dy = e.changedTouches[0].clientY - swipe.current.y;
            swipe.current = null;
            if (Math.abs(dx) > 65 && Math.abs(dy) < 45)
              select(index + (dx < 0 ? 1 : -1));
          }}
        >
          <aside className="codex-verso">
            <details className="codex-contents" open={wide}>
              <summary>
                Contents <span>{codex.chapters.length} chapters</span>
              </summary>
              <ol>
                {codex.chapters.map((c, i) => (
                  <li key={c.id}>
                    <button
                      aria-current={c.id === current?.id ? "page" : undefined}
                      onClick={() => select(i)}
                    >
                      <span>{String(i + 1).padStart(2, "0")}</span>
                      <div>
                        {chapterTitle(c)}
                        <small>
                          {c.snapshot.oracle === 16 ? "TAROT" : "NUMEROLOGY"}
                        </small>
                      </div>
                    </button>
                  </li>
                ))}
              </ol>
              {!current && (
                <p>
                  Each chapter begins with a completed reading you choose to
                  save.
                </p>
              )}
            </details>
            {current && (
              <div className="folio-desktop-art">
                <ChapterIllustration chapter={current} />
                <p className="folio-plate">
                  AN OBSERVATION KEPT · A PERSPECTIVE TO REVISIT
                </p>
              </div>
            )}
          </aside>
          <div className="codex-recto">
            <div
              className="codex-current"
              key={current?.id ?? "empty"}
              role="region"
              aria-label="Chapter content"
              tabIndex={0}
            >
              {current ? (
                <ChapterContent chapter={current} index={index} />
              ) : (
                <div className="empty-folio">
                  <p className="eyebrow">THE FIRST LEAF</p>
                  <h2 tabIndex={-1}>
                    A chapter begins
                    <br />
                    with <em>curiosity.</em>
                  </h2>
                  <p>
                    Complete a reading, then choose Save to this device. Its
                    symbols will become a chapter here.
                  </p>
                  <button className="folio-button" onClick={oracle.begin}>
                    Enter Tarot →
                  </button>
                  <button
                    className="folio-button"
                    onClick={() => oracle.navigate("numerology")}
                  >
                    Enter Numerology →
                  </button>
                </div>
              )}
            </div>
            {old && (
              <div
                className={`folio-turn ${direction < 0 ? "turn-back" : ""}`}
                inert
                aria-hidden="true"
                key={current?.id}
              >
                <div style={{ transform: `translateY(-${oldScroll}px)` }}>
                  <ChapterContent
                    chapter={old}
                    index={Math.max(
                      0,
                      codex.chapters.findIndex((c) => c.id === old.id),
                    )}
                  />
                </div>
              </div>
            )}
            <nav className="folio-navigation" aria-label="Chapter navigation">
              <button
                onClick={() => select(index - 1)}
                disabled={!current || index === 0}
                aria-label="Previous chapter"
              >
                ←
              </button>
              <span>
                {current
                  ? `Chapter ${index + 1} of ${codex.chapters.length}`
                  : "A blank beginning"}
              </span>
              <button
                onClick={() => select(index + 1)}
                disabled={!current || index === codex.chapters.length - 1}
                aria-label="Next chapter"
              >
                →
              </button>
            </nav>
            {current && (
              <button
                className="folio-compare"
                onClick={() => onCompare(current.id)}
              >
                Compare this perspective ↗
              </button>
            )}
          </div>
        </div>
      )}
      {open && (
        <button className="close-codex text-button" onClick={close}>
          Close the Codex
        </button>
      )}
    </div>
  );
}
