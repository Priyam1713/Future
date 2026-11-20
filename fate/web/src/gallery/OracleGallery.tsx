import { useId, useLayoutEffect, useRef, useState } from "react";
import { ArrowLeft, ArrowRight, ArrowUpRight, Search } from "lucide-react";
import type { Oracle } from "../hooks/useOracle";
import { rooms, worlds, type GalleryRoom, type GalleryWorld } from "./worlds";

const tokens: Partial<Record<GalleryWorld["id"], string>> = {
  sky: "/art/fate_orrery.svg",
  ritual: "/art/deck/fate-back-v1/card-back-360.webp",
  earth: "/art/folio-compass-720.webp",
};

function RoomLink({ room, oracle }: { room: GalleryRoom; oracle: Oracle }) {
  const { method, name, screen, description, historical } = room;
  const descriptionId = useId();
  return (
    <li data-technique-id={method.id} className="gallery-room-entry">
      <a
        href={`#${screen}`}
        aria-label={`Enter ${name}`}
        aria-describedby={descriptionId}
        onClick={(event) => {
          if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey)
            return;
          event.preventDefault();
          if (method.id === 16) oracle.begin();
          else {
            oracle.sound.cue("select");
            oracle.navigate(screen);
          }
        }}
      >
        <span>
          <strong>{name}</strong>
          <span className="room-link-description" id={descriptionId}>
            {description}
          </span>
        </span>
        <ArrowUpRight size={19} aria-hidden="true" />
      </a>
      {(historical || oracle.explored.includes(method.id)) && (
        <small className="room-link-context">
          {historical && "Historical reference"}
          {historical && oracle.explored.includes(method.id) && " · "}
          {oracle.explored.includes(method.id) && "Explored this visit"}
        </small>
      )}
    </li>
  );
}

function WorldArt({
  world,
  eager = false,
  expanded = false,
}: {
  world: GalleryWorld;
  eager?: boolean;
  expanded?: boolean;
}) {
  return (
    <picture aria-hidden="true">
      <source
        media="(max-width: 700px)"
        srcSet={`/art/${world.art}-720.webp`}
      />
      <img
        src={`/art/${world.art}-720.webp`}
        srcSet={`/art/${world.art}-720.webp 720w, /art/${world.art}-1440.webp 1440w`}
        sizes={
          expanded
            ? "(max-width: 700px) 96vw, 1160px"
            : "(max-width: 1240px) 50vw, 580px"
        }
        alt=""
        loading={eager ? "eager" : "lazy"}
        decoding="async"
        width="1440"
        height="960"
        style={{ objectPosition: world.focus }}
      />
    </picture>
  );
}

export function OracleGallery({
  oracle,
  embedded = false,
}: {
  oracle: Oracle;
  embedded?: boolean;
}) {
  const [query, setQuery] = useState("");
  const [world, setWorld] = useState<GalleryWorld | null>(null);
  const [all, setAll] = useState(false);
  const entrance = useRef<HTMLButtonElement | null>(null);
  const destination = useRef<HTMLHeadingElement>(null);
  const focusDestination = useRef(false);
  const headingId = useId();
  const text = query.trim().toLocaleLowerCase();
  const matches = rooms.filter(({ method, name, description }) =>
    `${method.name} ${name} ${method.variations} ${description}`
      .toLocaleLowerCase()
      .includes(text),
  );
  const worldRooms =
    world &&
    rooms.filter(({ method }) =>
      (world.rooms as readonly number[]).includes(method.id),
    );
  const listed = text || all ? matches : worldRooms;
  const featured =
    world && worldRooms?.find(({ method }) => method.id === world.featured);
  const title = text ? "Search results" : all ? "All rooms" : world?.title;

  useLayoutEffect(() => {
    if (focusDestination.current) {
      destination.current?.focus();
      focusDestination.current = false;
    }
  }, [world, all]);

  function open(next: GalleryWorld | null, from: HTMLButtonElement) {
    entrance.current = from;
    focusDestination.current = true;
    oracle.sound.cue("select");
    setQuery("");
    setWorld(next);
    setAll(next === null);
  }

  function returnToDoors() {
    const trigger = entrance.current;
    setQuery("");
    setWorld(null);
    setAll(false);
    requestAnimationFrame(() => {
      const id = trigger?.dataset.door;
      const target = id && document.getElementById(id);
      if (target) target.focus();
    });
  }

  return (
    <section className="living-gallery" aria-labelledby={headingId}>
      {embedded ? (
        <h2 id={headingId}>Six worlds to explore</h2>
      ) : (
        <h2 id={headingId} className="gallery-sr-only">
          Discover the Gallery
        </h2>
      )}
      <div className="gallery-toolbar">
        <label className="gallery-search">
          <span>Find a tradition</span>
          <span className="gallery-search-field">
            <Search size={18} aria-hidden="true" />
            <input
              type="search"
              value={query}
              placeholder="Try dreams, runes or astrology"
              onChange={(event) => setQuery(event.target.value)}
            />
          </span>
        </label>
        <p className="gallery-visit" aria-live="polite">
          {text
            ? `${matches.length} matching techniques`
            : `${oracle.explored.length} of 54 rooms explored this visit`}
        </p>
      </div>
      {listed ? (
        <section className="world-interior" aria-label={title}>
          <div
            className={
              world && !text
                ? `interior-heading interior-${world.id}`
                : "interior-heading"
            }
          >
            {world && !text && <WorldArt world={world} eager expanded />}
            {!text && (
              <button
                className="text-button world-return"
                onClick={returnToDoors}
              >
                <ArrowLeft size={15} aria-hidden="true" /> All worlds
              </button>
            )}
            <h3 tabIndex={-1} ref={destination}>
              {title}
            </h3>
            {world && !text && <p>{world.description}</p>}
          </div>
          {world && !text && featured && (
            <div className={`world-feature world-feature-${world.id}`}>
              <div className="world-token" aria-hidden="true">
                {tokens[world.id] ? (
                  <img src={tokens[world.id]} alt="" width="104" height="104" />
                ) : (
                  <span />
                )}
              </div>
              <div>
                <p className="eyebrow">Start here</p>
                <ul>
                  <RoomLink room={featured} oracle={oracle} />
                </ul>
              </div>
            </div>
          )}
          <nav
            aria-label={
              text ? "Matching rooms" : all ? "All rooms" : `${title} rooms`
            }
          >
            <ul className="gallery-room-list">
              {listed
                .filter((room) => text || room !== featured)
                .map((room) => (
                  <RoomLink key={room.method.id} room={room} oracle={oracle} />
                ))}
            </ul>
          </nav>
          {listed.length === 0 && (
            <p className="gallery-empty">
              No tradition matches that search. Try another name.
            </p>
          )}
        </section>
      ) : (
        <>
          <div className="world-entrances">
            {worlds.map((item, index) => (
              <button
                type="button"
                className={`world-door door-${item.id}`}
                key={item.id}
                id={`${headingId}-${item.id}`}
                data-door={`${headingId}-${item.id}`}
                aria-label={item.title}
                onClick={(event) => open(item, event.currentTarget)}
              >
                <WorldArt world={item} eager={!embedded && index < 3} />
                <span className="world-door-copy">
                  <strong>{item.title}</strong>
                  <span>{item.description}</span>
                </span>
                <span className="world-door-arrow">
                  <ArrowUpRight size={21} aria-hidden="true" />
                </span>
              </button>
            ))}
          </div>
          <button
            className="text-button all-rooms"
            id={`${headingId}-all`}
            data-door={`${headingId}-all`}
            onClick={(event) => open(null, event.currentTarget)}
          >
            View all 54 rooms <ArrowRight size={17} aria-hidden="true" />
          </button>
        </>
      )}
    </section>
  );
}
