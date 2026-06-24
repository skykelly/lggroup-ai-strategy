import { defineMiddleware } from "astro:middleware";
import { SESSION_COOKIE, verifySession } from "./lib/auth";

// Paths that don't require authentication
const PUBLIC_PATHS = new Set(["/login"]);

export const onRequest = defineMiddleware(async (ctx, next) => {
  const { pathname } = ctx.url;

  // Allow public pages and static assets (anything with a file extension)
  if (PUBLIC_PATHS.has(pathname) || /\.\w+$/.test(pathname)) {
    return next();
  }

  const session = ctx.cookies.get(SESSION_COOKIE);
  if (session?.value && await verifySession(session.value)) {
    return next();
  }

  return ctx.redirect(`/login?next=${encodeURIComponent(pathname)}`);
});
