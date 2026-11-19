import { useState } from "react";
import type { Oracle } from "../hooks/useOracle";
import inventory from "./inventory.json";
import { isChamberId, ROOMS } from "../chambers/contracts";
import { isRitualId, RITUAL_ROOMS } from "../ritual/contracts";
import { EXPERIENCES } from "../experiences/contracts";
import { NumberDial } from "../numerology/NumberDial";

const collections = [
  {
    title: "Written in the heavens",
    subtitle: "The language of cycles, charts and numbers.",
    tone: "celestial",
  },
  {
    title: "The human manuscript",
    subtitle: "Traditions that read the traces of being human.",
    tone: "human",
  },
  {
    title: "Beyond the visible",
    subtitle: "Cards, symbols and the interior world.",
    tone: "symbols",
  },
  {
    title: "Whispers of the earth",
    subtitle: "Water, fire, stone and the art of noticing.",
    tone: "earth",
  },
  {
    title: "At the edge of knowing",
    subtitle: "Intuition, dreams and the limits of perception.",
    tone: "dream",
  },
  {
    title: "Possible tomorrows",
    subtitle: "Models, scenarios and scientific imagination.",
    tone: "future",
  },
];
export function OracleGallery({
  oracle,
  libraryOnly = false,
}: {
  oracle: Oracle;
  libraryOnly?: boolean;
}) {
  const [query, setQuery] = useState("");
  const matches = inventory.methods.filter((m) =>
    `${m.name} ${m.variations}`
      .toLowerCase()
      .includes(query.toLowerCase().trim()),
  );
  return (
    <>
      {!libraryOnly && (
        <section className="number-door" aria-labelledby="number-door-title">
          <div className="number-door-art">
            <NumberDial
              reduced={oracle.reduced}
              paused={oracle.paused}
              decorative
            />
          </div>
          <div className="number-door-copy">
            <p className="eyebrow">02 / THE SECOND DOOR · OPEN NOW</p>
            <h2 id="number-door-title">
              There is a rhythm
              <br />
              in <em>your name.</em>
            </h2>
            <p>
              A name. A date. A constellation of numbers.
              <br />
              Enter the observatory and meet your patterns.
            </p>
            <button
              className="primary"
              onClick={() => {
                oracle.sound.cue("select");
                oracle.navigate("numerology");
              }}
            >
              Explore Numerology <span aria-hidden="true">↗</span>
            </button>
            <span className="door-note">
              {EXPERIENCES[4].room} ·{" "}
              {oracle.explored.includes(4)
                ? "Explored this visit"
                : "A new room awaits"}
            </span>
          </div>
        </section>
      )}
      {!libraryOnly && (
        <section
          className="western-gateway"
          aria-labelledby="western-gateway-title"
        >
          <picture>
            <source
              media="(max-width:700px)"
              srcSet="/art/western-observatory-portrait-450.webp 450w, /art/western-observatory-portrait-750.webp 750w"
              sizes="100vw"
            />
            <img
              src="/art/western-observatory-960.webp"
              width="1672"
              height="941"
              loading="lazy"
              alt="Original brass armillary within FATE's Western Observatory"
            />
          </picture>
          <div>
            <p className="eyebrow">03 / THE THIRD DOOR · OPEN NOW</p>
            <h2 id="western-gateway-title">
              A moment,
              <br />
              <em>written in light.</em>
            </h2>
            <p>
              Your actual sky becomes an instrument to explore. Enter with a
              known birth time and place.
            </p>
            <button
              className="primary"
              onClick={() => oracle.navigate("western")}
            >
              Explore Western Astrology ↗
            </button>
            <span className="door-note">
              {oracle.explored.includes(1)
                ? "Explored this visit"
                : "The Astral Observatory"}
            </span>
          </div>
        </section>
      )}
      <section className="gallery-library" aria-labelledby="gallery-title">
        {!libraryOnly && (
          <div className="gallery-intro">
            <img
              src="/art/gallery-hall-768.webp"
              srcSet="/art/gallery-hall-768.webp 768w, /art/gallery-hall-v1.webp 1536w"
              sizes="(max-width: 700px) 100vw, 1100px"
              width="1536"
              height="1024"
              loading="lazy"
              alt="An original FATE observatory: six shadowed alcoves beneath a celestial oculus"
            />
            <div>
              <p className="eyebrow">THE COLLECTION · 54 RETAINED TECHNIQUES</p>
              <h2 id="gallery-title">
                A universe,
                <br />
                <em>still unfolding.</em>
              </h2>
              <p>
                Three rooms are open. Beyond them, a library of traditions and
                possible futures waits to be discovered.
              </p>
            </div>
          </div>
        )}
        <details className="ritual-wing-discovery">
          <summary>
            The Ritual Wing <span>Seven hands-on rooms</span>
          </summary>
          <nav aria-label="The Ritual Wing rooms">
            {Object.values(RITUAL_ROOMS).map((room) => (
              <button
                key={room.slug}
                className="text-button ritual-wing-link"
                onClick={() => oracle.navigate(room.slug)}
              >
                {room.name} <span aria-hidden="true">↗</span>
              </button>
            ))}
          </nav>
        </details>
        <div className="gallery-tools">
          <label>
            Find a tradition
            <input
              type="search"
              value={query}
              placeholder="Try dreams, runes or astrology"
              onChange={(e) => setQuery(e.target.value)}
            />
          </label>
          <p aria-live="polite">
            {query
              ? `${matches.length} matching techniques`
              : `${oracle.explored.length} of ${inventory.methods.filter((method) => method.status === "available").length} rooms explored this visit`}
          </p>
        </div>
        <div className="gallery-legend">
          <span>✦ Open now</span>
          <span>◌ Upcoming experience</span>
          <span>◇ Historical reference</span>
        </div>
        {collections.map((collection, i) => {
          const methods = matches.filter((m) => m.phase === i + 1);
          if (!methods.length) return null;
          return (
            <details
              className={`collection collection-${collection.tone}`}
              key={collection.title}
              open={query.trim() ? true : undefined}
            >
              <summary>
                <span className="collection-index">0{i + 1}</span>
                <div>
                  <h3>{collection.title}</h3>
                  <p>{collection.subtitle}</p>
                </div>
                <span className="collection-count">
                  {methods.length} <span aria-hidden="true">＋</span>
                </span>
              </summary>
              <div className="collection-body">
                <p className="collection-context">
                  Original inventory phase {i + 1}. Consumer availability is
                  separate from engine readiness. Upcoming rooms have no launch
                  date.
                </p>
                {methods.map((m) => (
                  <details
                    className="inventory-entry"
                    key={m.id}
                    data-technique-id={m.id}
                  >
                    <summary>
                      <span className="inventory-id">
                        {String(m.id).padStart(2, "0")}
                      </span>
                      <span className="inventory-name">{m.name}</span>
                      <span className={`availability ${m.status}`}>
                        {m.status === "available"
                          ? oracle.explored.includes(m.id)
                            ? "Explored this visit"
                            : "Open now"
                          : m.status === "historical"
                            ? "Historical reference"
                            : "Upcoming experience"}
                      </span>
                    </summary>
                    <div className="inventory-depth">
                      <p>
                        {m.status === "historical"
                          ? "A historical reference, never a personal assessment. "
                          : ""}
                        {m.mechanism}.
                      </p>
                      <p>{m.variations}</p>
                      <p>
                        {m.evidence}. {m.limits}.
                      </p>
                      <p>
                        Inventory reference:{" "}
                        {m.source.url ? (
                          <a
                            href={m.source.url}
                            target="_blank"
                            rel="noreferrer"
                          >
                            {m.source.title}
                          </a>
                        ) : (
                          m.source.title
                        )}{" "}
                        — {m.source.author}. Inventory references describe the
                        wider tradition; each open room names its own supported
                        profile.
                      </p>
                      {m.status === "available" && (
                        <button
                          className="secondary"
                          onClick={() =>
                            m.id === 16
                              ? oracle.begin()
                              : oracle.navigate(
                                  isRitualId(m.id)
                                    ? RITUAL_ROOMS[m.id].slug
                                    : isChamberId(m.id)
                                      ? ROOMS[m.id].slug
                                      : m.id === 1
                                        ? "western"
                                        : "numerology",
                                )
                          }
                        >
                          Enter {m.name}
                        </button>
                      )}
                    </div>
                  </details>
                ))}
              </div>
            </details>
          );
        })}
        {!matches.length && (
          <p className="scope-note">
            No tradition matches that search. Try another name.
          </p>
        )}
        <p className="scope-note">
          The original Future inventory, in six collections. Six excluded
          techniques remain excluded. Symbolic traditions, historical references
          and scientific models have different evidence standards.
        </p>
      </section>
    </>
  );
}
