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
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${backendUrl.replace(/\/$/, "")}/:path*` }];
  },
};

export default nextConfig;
