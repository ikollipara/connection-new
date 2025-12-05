/**
 * Project:     conneCTION
 * Name:        postcss.config.js
 * Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
 * Date:        2025-12-04
 * Description: PostCSS Configuration
 */

module.exports = {
  plugins: [
    require("cssnano")({
      preset: ["default", { svgo: false }],
    }),
  ],
};
