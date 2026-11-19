import { ArrowRight, ArrowUpRight, Pause, Play } from "lucide-react";
import CardArt from "../CardArt";
import type { Oracle } from "../hooks/useOracle";
import { lazy, Suspense } from "react";
import type { Card } from "../types";
import { OrbPoster } from "../orb/OrbPoster";
import { ROOMS } from "../chambers/contracts";
import { OracleGallery } from "../gallery/OracleGallery";
const Orb = lazy(() => import("../Orb"));
const previewCard: Card = {
  id: "major-17",
  name: "The Star",
  number: 17,
  suit: null,
  rank: "trump",
  rank_number: null,
  arcana: "major",
};
const moonCard: Card = {
  ...previewCard,
  id: "major-18",
  name: "The Moon",
  number: 18,
};
export default function ExploreScreen({ oracle }: { oracle: Oracle }) {
  const { heading, begin, reduced, paused, setPaused } = oracle;
  return (
    <div className="explore page-enter">
      <div className="hero">
        <div className="hero-copy">
          <p className="eyebrow">
            <span className="tiny-star">✧</span> THE ORACLE GALLERY
          </p>
          <h1 ref={heading} tabIndex={-1}>
            Some answers
            <br />
            begin with <em>wonder.</em>
          </h1>
          <p className="hero-description">
            Ancient symbols. Quiet patterns.
            <br />
            Fourteen open rooms in a universe of discovery.
          </p>
          <nav className="room-index" aria-label="Open oracle rooms">
            <button onClick={begin}>
              <span>01</span> Tarot
            </button>
            <span aria-hidden="true">/</span>
            <button onClick={() => oracle.navigate("numerology")}>
              <span>02</span> Numerology
            </button>
            <span aria-hidden="true">/</span>
            <button onClick={() => oracle.navigate("western")}>
              <span>03</span> Astrology
            </button>
          </nav>
          <div className="new-room-links" aria-label="Four new chambers">
            {Object.values(ROOMS).map((room) => (
              <button
                key={room.slug}
                className="text-button"
                onClick={() => oracle.navigate(room.slug)}
              >
                {room.name} <span aria-hidden="true">↗</span>
              </button>
            ))}
          </div>
          <button
            className="collection-shortcut text-button"
            onClick={() => oracle.navigate("gallery")}
          >
            Browse all 54 techniques <span aria-hidden="true">↗</span>
          </button>
          <a
            className="primary desktop-cta"
            href="#ritual"
            onClick={(e) => {
              e.preventDefault();
              begin();
            }}
          >
            Enter the oracle <ArrowRight size={17} />
          </a>
          <p className="hero-footnote desktop-cta">
            No account. Just your curiosity.
          </p>
        </div>
        <div className="hero-art">
          <span className="orb-coordinate coordinate-left">EST. IN WONDER</span>
          <div className="orb-wrap">
            <Suspense
              fallback={
                <div className="orb">
                  <OrbPoster />
                </div>
              }
            >
              <Orb reduced={reduced} paused={paused} />
            </Suspense>
          </div>
          <div className="orb-caption">
            <span /> TOUCH THE MYSTERY <span />
          </div>
          <button
            className="motion-control"
            aria-pressed={paused}
            onClick={() => setPaused((p) => !p)}
          >
            {paused ? <Play size={12} /> : <Pause size={12} />}{" "}
            {paused ? "Resume atmosphere" : "Pause atmosphere"}
          </button>
        </div>
      </div>
      <div className="mobile-cta">
        <button className="primary" onClick={begin}>
          Begin a reading <ArrowRight size={17} />
        </button>
        <a href="#open-rooms">Choose your room ↓</a>
      </div>
      <section
        id="open-rooms"
        className="oracle-section"
        aria-labelledby="oracle-title"
      >
        <div className="section-label">
          <span>01 / YOUR FIRST CHAPTER</span>
          <span>AN ANCIENT ART, REIMAGINED</span>
        </div>
        <a
          href="#ritual"
          onClick={(e) => {
            e.preventDefault();
            begin();
          }}
          className="oracle-tile"
        >
          <div className="tile-art" aria-hidden="true">
            <div className="mini-card back-preview">
              <CardArt card={moonCard} />
            </div>
            <div className="mini-card front-preview">
              <CardArt card={previewCard} />
            </div>
            <span className="tile-glow" />
          </div>
          <div className="tile-copy">
            <p className="eyebrow">THE ART OF REFLECTION</p>
            <h2 id="oracle-title">The Tarot</h2>
            <p>
              Let the cards open
              <br className="mobile-break" /> a new perspective.
            </p>
            <span className="tile-meta">
              {oracle.explored.includes(16)
                ? "EXPLORED THIS VISIT"
                : "ARCHIVE EDITION"}{" "}
              <span>·</span> 78 ILLUSTRATED CARDS
            </span>
          </div>
          <span className="tile-arrow">
            <ArrowUpRight size={22} />
          </span>
        </a>
      </section>
      <OracleGallery oracle={oracle} />
      <div className="explore-invitation">
        <span className="gold-star">✦</span>
        <p>
          You don’t need to know the question.
          <br />
          Sometimes, curiosity is enough.
        </p>
      </div>
    </div>
  );
}
