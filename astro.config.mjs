import { defineConfig } from "astro/config";

export default defineConfig({
  site: process.env.SITE_URL || "https://lg-ai-strategy-journal.pages.dev",
  srcDir: "./web/src",
  publicDir: "./web/public",
  output: "static",
  build: {
    assets: "_assets"
  },
  markdown: {
    shikiConfig: {
      theme: "github-light"
    }
  }
});
