import { defineConfig } from "astro/config";
import vercel from "@astrojs/vercel";

const deploymentHost =
  process.env.SITE_URL ||
  (process.env.VERCEL_PROJECT_PRODUCTION_URL
    ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`
    : process.env.VERCEL_URL
      ? `https://${process.env.VERCEL_URL}`
      : "http://localhost:4321");

export default defineConfig({
  site: deploymentHost,
  srcDir: "./web/src",
  publicDir: "./web/public",
  output: "server",
  adapter: vercel(),
  build: {
    assets: "_assets"
  },
  markdown: {
    shikiConfig: {
      theme: "github-light"
    }
  }
});
