export const SESSION_COOKIE = "lg_session";
export const SESSION_MAX_AGE = 60 * 60 * 24 * 30; // 30 days

async function hmacSign(secret: string, data: string): Promise<string> {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const buf = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(data));
  return btoa(String.fromCharCode(...new Uint8Array(buf)));
}

export async function createSession(username: string): Promise<string> {
  const secret = import.meta.env.AUTH_SECRET ?? "";
  const sig = await hmacSign(secret, username);
  return `${btoa(username)}.${sig}`;
}

export async function verifySession(token: string): Promise<boolean> {
  try {
    const dot = token.indexOf(".");
    if (dot < 0) return false;
    const username = atob(token.slice(0, dot));
    const expected = await createSession(username);
    if (token.length !== expected.length) return false;
    // Constant-time comparison to prevent timing attacks
    let diff = 0;
    for (let i = 0; i < token.length; i++) {
      diff |= token.charCodeAt(i) ^ expected.charCodeAt(i);
    }
    return diff === 0;
  } catch {
    return false;
  }
}
