import type { APIRoute } from "astro";
import { SESSION_COOKIE } from "../../lib/auth";

export const POST: APIRoute = (ctx) => {
  ctx.cookies.delete(SESSION_COOKIE, { path: "/" });
  return ctx.redirect("/login");
};
