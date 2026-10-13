import type { NextConfig } from "next";

// Obligatoria y sin valor por defecto: sin backend no hay aplicación (igual que en el backend).
const backendUrl = process.env.BACKEND_URL;
if (!backendUrl) {
  throw new Error("Falta BACKEND_URL (ver frontend/.env.example)");
}

const nextConfig: NextConfig = {
  cacheComponents: true,
  partialPrefetching: true,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
  // El navegador solo habla con este origen: /api/* se reenvía al backend. Así la cookie de
  // sesión es de primera parte y el backend ve el Origin del frontend (control CSRF).
  // Cabeceras de seguridad para todas las respuestas del frontend.
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains" },
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "X-Frame-Options", value: "DENY" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
          // El micrófono se permite solo al propio sitio (simulación oral); el resto, a nadie.
          { key: "Permissions-Policy", value: "camera=(), microphone=(self), geolocation=()" },
        ],
      },
    ];
  },
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${backendUrl.replace(/\/$/, "")}/:path*` }];
  },
};

export default nextConfig;
