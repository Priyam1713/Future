import { useId } from "react";
import type { Card } from "./types";

// Original FATE celestial edition: vector illustrations, not historical deck reproductions.
const roman = [
  "0",
  "I",
  "II",
  "III",
  "IV",
  "V",
  "VI",
  "VII",
  "VIII",
  "IX",
  "X",
  "XI",
  "XII",
  "XIII",
  "XIV",
  "XV",
  "XVI",
  "XVII",
  "XVIII",
  "XIX",
  "XX",
  "XXI",
];
function Star({ x, y, r = 7 }: { x: number; y: number; r?: number }) {
  return (
    <path
      d={`M${x} ${y - r}Q${x + 1} ${y - 1} ${x + r} ${y}Q${x + 1} ${y + 1} ${x} ${y + r}Q${x - 1} ${y + 1} ${x - r} ${y}Q${x - 1} ${y - 1} ${x} ${y - r}Z`}
    />
  );
}
function Emblem({ kind }: { kind: number }) {
  const rays = Array.from({ length: 12 }, (_, i) => {
    const a = (i * Math.PI) / 6;
    return (
      <path
        key={i}
        d={`M${100 + Math.cos(a) * 35} ${117 + Math.sin(a) * 35}L${100 + Math.cos(a) * 46} ${117 + Math.sin(a) * 46}`}
      />
    );
  });
  switch (kind) {
    case 0:
      return (
        <>
          <circle cx="100" cy="110" r="33" />
          <path d="M80 135L100 92 120 135M87 122H113M93 88L100 76 107 88" />
          <Star x={100} y={67} />
        </>
      );
    case 1:
      return (
        <>
          <path d="M70 112C70 84 100 84 100 112S130 140 130 112 100 84 100 112 70 140 70 112ZM100 70V80M100 145V160" />
          <Star x={100} y={66} />
        </>
      );
    case 2:
    case 18:
      return (
        <>
          <circle cx="100" cy="113" r="34" />
          <path
            d="M112 81C77 92 77 138 112 145C59 153 57 75 112 81Z"
            fill="currentColor"
            stroke="none"
          />
          <Star x={125} y={107} r={9} />
          <Star x={78} y={65} r={4} />
        </>
      );
    case 3:
      return (
        <>
          <path d="M69 130L65 96 85 110 100 84 115 110 135 96 131 130ZM70 140H130M77 148H123" />
          <circle cx="100" cy="115" r="6" />
        </>
      );
    case 4:
      return (
        <>
          <path d="M73 145V84H127V145M68 145H132M85 145V112H115V145M73 91H127M88 84V74H112V84" />
          <Star x={100} y={64} />
        </>
      );
    case 5:
      return (
        <>
          <path d="M100 75V151M78 92H122M83 110H117M89 130H111" />
          <circle cx="100" cy="68" r="7" />
          <path d="M66 153L76 143 86 153M114 153L124 143 134 153" />
        </>
      );
    case 6:
      return (
        <>
          <circle cx="85" cy="113" r="26" />
          <circle cx="115" cy="113" r="26" />
          <Star x={100} y={70} r={10} />
          <path d="M100 142V157" />
        </>
      );
    case 7:
      return (
        <>
          <path d="M69 132L76 93H124L131 132ZM100 93V68M84 78H116" />
          <circle cx="78" cy="141" r="9" />
          <circle cx="122" cy="141" r="9" />
          <Star x={100} y={64} />
        </>
      );
    case 8:
      return (
        <>
          <path d="M71 102C71 79 100 79 100 102S129 125 129 102 100 79 100 102 71 125 71 102ZM80 137Q100 162 120 137M88 134L100 123 112 134" />
        </>
      );
    case 9:
      return (
        <>
          <path d="M85 95H115V137H85ZM100 83V95M92 83H108M85 137L78 149H122L115 137M100 105V125" />
          <Star x={100} y={115} r={10} />
          <path d="M66 105L74 109M126 109L134 105" />
        </>
      );
    case 10:
    case 21:
      return (
        <>
          <circle cx="100" cy="117" r="35" />
          <circle cx="100" cy="117" r="26" />
          {rays}
          <Star x={100} y={117} r={19} />
        </>
      );
    case 11:
      return (
        <>
          <path d="M100 78V148M80 151H120M68 99H132M76 99L61 124H91ZM124 99L109 124H139Z" />
          <Star x={100} y={73} />
        </>
      );
    case 12:
      return (
        <>
          <path d="M68 81H132M100 81V112L83 132M100 112L118 130 107 140M83 132V146" />
          <circle cx="83" cy="154" r="7" />
          <circle cx="83" cy="154" r="15" opacity=".5" />
        </>
      );
    case 13:
      return (
        <>
          <path d="M100 153V112M100 133Q72 136 75 120Q96 118 100 133M100 143Q128 146 125 130Q104 129 100 143" />
          <path d="M100 80C74 81 75 112 100 112S126 81 100 80Z" />
          <Star x={100} y={96} r={11} />
        </>
      );
    case 14:
      return (
        <>
          <path d="M73 85H97L94 109H77ZM108 126H132L129 150H112ZM85 109C85 130 120 104 120 126" />
          <Star x={120} y={90} />
        </>
      );
    case 15:
      return (
        <>
          <path d="M72 91Q62 121 83 137L100 149 117 137Q138 121 128 91L112 109H88ZM87 117L93 122M113 117L107 122M94 134H106" />
          <circle cx="100" cy="80" r="11" />
        </>
      );
    case 16:
      return (
        <>
          <path d="M80 151L84 100H116L120 151ZM79 100H121L117 88H83ZM97 151V133H104V151M100 62L89 80H104L96 97" />
          <path d="M64 112L70 122M134 112L128 122" />
        </>
      );
    case 17:
      return (
        <>
          <Star x={100} y={110} r={38} />
          <Star x={65} y={78} r={6} />
          <Star x={136} y={91} r={6} />
          <Star x={131} y={148} r={5} />
          <path d="M66 148Q100 136 134 154" />
        </>
      );
    case 19:
      return (
        <>
          <circle cx="100" cy="117" r="25" />
          {rays}
          <circle cx="100" cy="117" r="16" opacity=".6" />
        </>
      );
    default:
      return (
        <>
          <path d="M76 138L100 91 124 138ZM100 91V74M68 148H132" />
          <Star x={100} y={68} r={10} />
          <circle cx="100" cy="123" r="8" />
        </>
      );
  }
}
function Suit({
  suit,
  x,
  y,
  scale = 1,
}: {
  suit: string;
  x: number;
  y: number;
  scale?: number;
}) {
  return (
    <g transform={`translate(${x} ${y}) scale(${scale})`}>
      {suit === "cups" ? (
        <>
          <path d="M-10-8H10Q10 7 0 7Q-10 7-10-8ZM0 7V15M-7 15H7M-10-6Q-21-6-12 3M10-6Q21-6 12 3" />
        </>
      ) : suit === "swords" ? (
        <>
          <path d="M0-19L4-10 2 8H-2L-4-10ZM-9 8H9M0 8V18M-3 18H3" />
        </>
      ) : suit === "wands" ? (
        <>
          <path d="M-2 18L2-18M0-5Q-12-15-8-17Q3-17 0-5M0 7Q12-3 9-6Q-1-4 0 7" />
        </>
      ) : (
        <>
          <circle r="14" />
          <path d="M0-11L6 9-10-3H10L-6 9Z" />
        </>
      )}
    </g>
  );
}
export default function CardArt({
  card,
  back = false,
}: {
  card?: Card;
  back?: boolean;
}) {
  const uid = useId().replace(/:/g, "");
  const num = card?.number ?? 0;
  const suit = card?.suit ?? "major";
  const count = Math.min(card?.rank_number ?? 1, 10);
  const color = back
    ? "#ae83c9"
    : suit === "cups"
      ? "#81bab8"
      : suit === "wands"
        ? "#cc9169"
        : suit === "swords"
          ? "#a5adce"
          : suit === "pentacles"
            ? "#bcaf78"
            : "#ccae77";
  return (
    <svg
      className="card-illustration"
      viewBox="0 0 200 320"
      role="img"
      aria-label={
        back
          ? "Celestial card back"
          : `${card?.name} · original FATE celestial illustration`
      }
    >
      <defs>
        <linearGradient id={`${uid}sky`} x2=".7" y2="1">
          <stop stopColor={back ? "#2d2345" : "#292c45"} />
          <stop offset="1" stopColor="#0b1420" />
        </linearGradient>
        <radialGradient id={`${uid}halo`}>
          <stop stopColor={color} stopOpacity=".24" />
          <stop offset="1" stopColor={color} stopOpacity="0" />
        </radialGradient>
        <linearGradient id={`${uid}gold`} x2=".8" y2="1">
          <stop stopColor="#f1db9b" />
          <stop offset=".5" stopColor="#92734d" />
          <stop offset="1" stopColor="#d9bb7c" />
        </linearGradient>
      </defs>
      <rect
        x="1"
        y="1"
        width="198"
        height="318"
        rx="10"
        fill={`url(#${uid}sky)`}
      />
      <rect
        x="8"
        y="8"
        width="184"
        height="304"
        rx="5"
        fill="none"
        stroke={`url(#${uid}gold)`}
        strokeWidth=".8"
      />
      <g fill="none" stroke={color} strokeWidth=".6" opacity=".65">
        <path d="M14 55V20H49M151 20H186V55M14 265V300H49M151 300H186V265" />
        <path d="M20 244V103A80 80 0 0 1 180 103V244" />
        <path d="M27 244V105A73 73 0 0 1 173 105V244" />
      </g>
      <ellipse cx="100" cy="122" rx="92" ry="112" fill={`url(#${uid}halo)`} />
      <g fill="#e3cb96" opacity=".65">
        {Array.from({ length: 32 }, (_, i) => (
          <circle
            key={i}
            cx={28 + ((i * 43.7) % 144)}
            cy={32 + ((i * 31.3) % 180)}
            r={i % 5 === 0 ? 1 : 0.5}
          />
        ))}
      </g>
      {back ? (
        <g stroke={`url(#${uid}gold)`} fill="none" strokeWidth=".8">
          <circle cx="100" cy="160" r="58" />
          <circle cx="100" cy="160" r="65" strokeDasharray="1 6" />
          <ellipse
            cx="100"
            cy="160"
            rx="45"
            ry="84"
            transform="rotate(35 100 160)"
          />
          <ellipse
            cx="100"
            cy="160"
            rx="45"
            ry="84"
            transform="rotate(-35 100 160)"
          />
          <path
            d="M100 112C62 140 62 181 108 199C82 172 83 143 100 112Z"
            fill={`url(#${uid}gold)`}
          />
          <g fill="#e3cb96" stroke="none">
            <Star x={114} y={151} r={17} />
            <Star x={100} y={57} />
            <Star x={100} y={263} />
          </g>
        </g>
      ) : (
        <>
          <g
            fill="none"
            stroke={color}
            color={color}
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            {suit === "major" ? (
              <Emblem kind={num} />
            ) : (
              <>
                {card!.rank_number! > 10 ? (
                  <>
                    <path d="M77 80L82 65 94 76 100 60 106 76 118 65 123 80ZM81 87H119" />
                    <Suit suit={suit} x={100} y={124} scale={2} />
                  </>
                ) : (
                  Array.from({ length: count }, (_, i) => {
                    const angle = (i / count) * Math.PI * 2 - Math.PI / 2;
                    return (
                      <Suit
                        key={i}
                        suit={suit}
                        x={
                          count === 1
                            ? 100
                            : 100 + Math.cos(angle) * (count < 4 ? 32 : 44)
                        }
                        y={
                          count === 1
                            ? 118
                            : 120 + Math.sin(angle) * (count < 4 ? 32 : 44)
                        }
                        scale={count > 6 ? 0.64 : count > 3 ? 0.8 : 1.2}
                      />
                    );
                  })
                )}
              </>
            )}
          </g>
          <g stroke={color} strokeWidth=".6" fill="none" opacity=".7">
            <path
              d={`M20 231L52 ${180 + (num % 4) * 5}L84 217L119 183L180 239`}
            />
            <path d="M20 240L65 208L103 238L137 209L180 246" />
            <path d="M20 252Q56 238 100 252T180 252M27 260Q60 247 100 260T173 260M39 267Q70 257 100 267T161 267" />
            <path d="M100 180L95 202 100 230 105 202Z" opacity=".6" />
          </g>
          <text
            x="100"
            y="37"
            textAnchor="middle"
            fill="#e2c995"
            fontSize="10"
            fontFamily="Georgia,serif"
            letterSpacing="3"
          >
            {suit === "major" ? roman[num] : card?.rank.toUpperCase()}
          </text>
          <text
            x="100"
            y="289"
            textAnchor="middle"
            fill="#e2c995"
            fontSize="9"
            fontFamily="Georgia,serif"
            letterSpacing="1.2"
          >
            {card?.name.toUpperCase()}
          </text>
        </>
      )}
      <g fill="#d5b67a">
        <Star x={20} y={20} r={3} />
        <Star x={180} y={20} r={3} />
        <Star x={20} y={300} r={3} />
        <Star x={180} y={300} r={3} />
      </g>
    </svg>
  );
}
