import { ImageResponse } from "next/og";

// Ícono para iOS (pantalla de inicio): PNG con el mismo birrete que src/app/icon.svg.
export const size = { width: 180, height: 180 };
export const contentType = "image/png";

export default function AppleIcon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "#2f5bd3",
        }}
      >
        <svg viewBox="0 0 32 32" width="150" height="150">
          <path d="M16 8 5 13l11 5 11-5-11-5Z" fill="#fff" />
          <path
            d="M9.5 15.2v4.6c0 1.6 2.9 3.2 6.5 3.2s6.5-1.6 6.5-3.2v-4.6L16 18.1l-6.5-2.9Z"
            fill="#fff"
            fillOpacity="0.85"
          />
          <path d="M26 13.5v5.5" stroke="#fff" strokeWidth="1.6" strokeLinecap="round" />
          <circle cx="26" cy="20" r="1.4" fill="#f5a524" />
        </svg>
      </div>
    ),
    size,
  );
}
