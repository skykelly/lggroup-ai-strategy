import { cp, mkdir, rm } from "node:fs/promises";
import { resolve } from "node:path";

const source = resolve("assets/images");
const target = resolve("web/public/assets/images");
const heroSource = resolve("assets/hero_images");
const heroTarget = resolve("web/public/assets/hero_images");

await rm(target, { recursive: true, force: true });
await rm(heroTarget, { recursive: true, force: true });
await mkdir(target, { recursive: true });
await mkdir(heroTarget, { recursive: true });
await cp(source, target, { recursive: true });
await cp(heroSource, heroTarget, { recursive: true });

console.log(`Copied web images to ${target} and ${heroTarget}`);
