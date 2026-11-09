import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

export default defineConfig({
  plugins: [
    react(),
    {
      name: "standalone-documents",
      configureServer(server) {
        server.middlewares.use(async (request, response, next) => {
          const filename = (request.url ?? "").split("?")[0].slice(1);
          if (!["ccl-introduction.html", "department.html"].includes(filename))
            return next();
          try {
            const html = await readFile(
              resolve(".generated/documents", filename),
            );
            response.setHeader("Content-Type", "text/html; charset=utf-8");
            response.end(html);
          } catch {
            next();
          }
        });
      },
    },
  ],
  base: "./",
  server: { headers: { "Referrer-Policy": "strict-origin-when-cross-origin" } },
  preview: {
    headers: { "Referrer-Policy": "strict-origin-when-cross-origin" },
  },
  build: {
    manifest: true,
    rollupOptions: { input: "src/main.tsx" },
  },
});
