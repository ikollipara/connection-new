/**
 * Project:     conneCTION
 * Name:        vite.config.js
 * Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
 * Date:        2025-11-12
 * Description: Vite Configuration
 */

import { defineConfig } from "vite";
import * as path from "node:path";
import compression, { defineAlgorithm } from "vite-plugin-compression2";

export default defineConfig({
  plugins: [
    compression({
      algorithms: [
        "gzip",
        defineAlgorithm("brotliCompress", {
          params: {
            [require("zlib").constants.BROTLI_PARAM_QUALITY]: 11,
          },
        }),
      ],
    }),
  ],
  base: "/static/",
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./static/src"),
    },
  },
  build: {
    outDir: path.resolve("./static/dist"),
    manifest: "manifest.json",
    rollupOptions: {
      input: path.resolve("./static/src/app.js"),
    },
  },
});
