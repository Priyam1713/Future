import { useId, type CSSProperties } from "react";
import { ROOMS, type ArchiveId } from "./contracts";

const hand =
  "M102 288 C101 259 92 242 79 226 L40 182 C28 167 39 153 55 159 L84 179 L79 119 L73 79 C69 59 89 55 95 74 L108 124 L106 53 C105 33 126 29 131 49 L139 115 L145 43 C147 22 168 24 170 45 L174 115 L187 62 C192 45 212 49 209 68 L201 145 C201 171 219 179 209 214 C202 239 182 254 184 287 Z";
const head =
  "M77 258 C128 251 111 211 101 199 C69 194 66 178 72 165 L67 151 L54 147 C47 142 57 132 66 115 C65 72 94 39 139 37 C198 34 217 77 212 123 C209 151 190 179 184 202 C176 230 203 249 225 258";
const foot =
  "M92 267 C66 254 66 227 76 197 C82 175 105 153 100 126 C96 107 87 88 91 67 C93 48 110 38 122 49 C126 22 147 22 153 42 C159 26 177 30 179 45 C191 30 206 39 204 57 C221 50 230 68 222 86 C216 124 196 162 173 193 C157 214 174 235 154 259 C141 275 111 275 92 267Z";
const swatches: Record<string, string> = {
  black: "#403744",
  brick_to_scarlet: "#d74f40",
  dragon_blood: "#782b3a",
  brown: "#b16d4e",
  brown_grey: "#857069",
  pale_grey: "#bfc6ce",
  grey_green: "#87988a",
  brown_green_scarlet: "#82834d",
  rose_family: "#dc83a1",
  crimson_brown_grey: "#9b6576",
  orange: "#e39647",
  yellow_family: "#d9c18b",
  yellow_ochre: "#b69249",
  gamboge: "#e7b84d",
  primrose: "#e6e2a3",
  violet: "#a189ce",
  pale_rose: "#eea8b1",
  green: "#85c9a4",
  carmine: "#cf5870",
  deep_grey: "#8790a6",
  blue: "#8da9e9",
  "figure-8": "#eeb2d0",
  "figure-9": "#ed9fae",
  "figure-12": "#a38dcc",
  "figure-18": "#d3ca8d",
};

export function ArchiveInstrument({
  id,
  group,
  groups,
  onGroup,
  entry,
  side,
}: {
  id: ArchiveId;
  group: string;
  groups: string[];
  onGroup: (group: string) => void;
  entry: string;
  side: "left" | "right" | "";
}) {
  const unique = useId();
  const plate = `url(#${unique}-plate)`;
  const shade = swatches[entry] ?? "#c291b4";
  return (
    <div
      className={`archive-instrument archive-${ROOMS[id][0]}`}
      style={{ "--pigment": shade } as CSSProperties}
    >
      <svg
        viewBox="0 0 280 305"
        role="img"
        aria-label={
          id === 8
            ? "Illustrated hand with three teaching lines"
            : "Decorative archival illustration"
        }
      >
        <defs>
          <linearGradient id={`${unique}-plate`} x2="75%" y2="95%">
            <stop stopColor="#e4ba89" stopOpacity=".28" />
            <stop offset="1" stopColor="#3f202e" stopOpacity=".4" />
          </linearGradient>
        </defs>
        {id === 8 && (
          <g className={side === "left" ? "hand-left" : ""}>
            <path d={hand} fill={plate} className="archive-engraving" />
            <path
              d="M95 155Q142 130 193 143"
              className={group === "Heart line" ? "active-ink" : ""}
            />
            <path
              d="M96 177Q142 160 191 194"
              className={group === "Head line" ? "active-ink" : ""}
            />
            <path
              d="M102 171Q129 183 124 218Q119 237 113 246"
              className={group === "Life line" ? "active-ink" : ""}
            />
            <path
              d="M81 120 l17 2 m17 -9 l19 -1 m12 -4 l20 0 m16 14 l16 2 m-97 125 q34 15 75 2"
              opacity=".43"
            />
          </g>
        )}
        {[9, 10, 11].includes(id) && (
          <g>
            <path d={head} fill={plate} className="archive-engraving" />
            <path
              d="M70 120Q88 112 104 123 M88 123h8 M73 167q15-2 23 2 M145 122q29-18 30 11q-3 18-18 18 M103 199q22 8 42-13"
              opacity=".76"
            />
            {id === 9 && (
              <path
                d="M51 96H231 M51 124H231 M51 163H231 M51 198H231"
                strokeDasharray="1.5 5"
                opacity=".5"
              />
            )}
            {id === 10 && (
              <>
                <circle cx="140" cy="146" r="112" strokeDasharray="1 2.4" />
                <text x="203" y="235" className="archive-number">
                  {entry.split("/")[1] || "X"}
                </text>
              </>
            )}
            {id === 11 && (
              <g>
                {[82, 119, 157, 196].map((x, i) => (
                  <path
                    key={x}
                    d={`M${x} ${62 + i * 42}h18m-18 0l-13 -11`}
                    strokeDasharray="2 5"
                    opacity=".65"
                  />
                ))}
              </g>
            )}
          </g>
        )}
        {id === 12 && (
          <g>
            <path d={foot} fill={plate} className="archive-engraving" />
            <path
              d="M102 107q36 24 95 9 M99 132q33 25 90 10 M96 155q38 26 82 8 M105 232q20 10 42 0"
              strokeDasharray="2 3"
            />
          </g>
        )}
        {id === 13 && (
          <g transform="rotate(-8 140 152)">
            <rect x="38" y="51" width="204" height="205" rx="4" fill={plate} />
            {[96, 133, 170, 207].map((y) => (
              <path
                key={y}
                d={`M54 ${y} H222`}
                strokeDasharray="1 4"
                opacity=".48"
              />
            ))}
            <path
              d={
                group === "Baseline direction"
                  ? "M67 167 Q92 125 104 142 T139 125 T176 112 T212 82"
                  : "M64 172 Q78 138 90 166 T120 155 Q137 125 144 160 T175 155 Q197 112 203 149 T220 145"
              }
              className="active-ink"
            />
          </g>
        )}
        {id === 14 && (
          <g>
            <circle cx="140" cy="152" r="109" strokeDasharray="1 3" />
            <circle cx="140" cy="152" r="96" opacity=".47" />
            <path
              className="lantern-pigment"
              d="M139 59C166 96 214 108 205 156C198 200 128 242 91 188C51 127 115 104 139 59Z"
            />
            <path
              d="M140 89C158 118 186 126 174 167C158 191 124 201 104 167C92 142 127 128 140 89Z"
              opacity=".57"
            />
          </g>
        )}
        {id === 15 && (
          <g>
            {[78, 202].map((x, i) => (
              <g
                key={x}
                opacity={group.startsWith(i === 0 ? "Right" : "Left") ? 1 : 0.5}
              >
                <circle cx={x} cy="150" r="58" fill={plate} />
                <circle cx={x} cy="150" r="50" strokeDasharray="1 3" />
                <circle cx={x} cy="150" r="36" />
                <circle cx={x} cy="150" r="18" fill="#170e16" />
                <text className="archive-number" x={x} y="244">
                  {i === 0 ? "R" : "L"}
                </text>
              </g>
            ))}
          </g>
        )}
      </svg>
      {id === 8 && (
        <div className="hand-markers">
          {groups.map((name) => (
            <button
              key={name}
              aria-pressed={group === name}
              className={name.split(" ")[0].toLowerCase()}
              onClick={() => onGroup(name)}
            >
              {name}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
