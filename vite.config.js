/**
 * Project:     conneCTION
 * Name:        vite.config.js
 * Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
 * Date:        2025-11-12
 * Description: Vite Configuration
 */

import {defineConfig} from "vite";
import * as path from "node:path";

export default defineConfig({
  plugins: [],
  base: "/static/",
  build: {
    outDir: path.resolve("./static/dist"),
    manifest: "manifest.json",
    rollupOptions: {
      input: path.resolve("./static/src/app.js"),
    }
  }
});
