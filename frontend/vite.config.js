import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Standard Vite + React config. Dev server runs on port 5173 by default,
// which matches FRONTEND_ORIGIN in the backend's .env.
export default defineConfig({
  plugins: [react()],
});
