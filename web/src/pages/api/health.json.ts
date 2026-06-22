import type { APIRoute } from "astro";
import { getDatabase } from "../../lib/db";

export const prerender = false;

export const GET: APIRoute = async () => {
  try {
    const sql = getDatabase();
    const [database] = await sql`
      SELECT
        current_database() AS database,
        now() AS checked_at
    `;

    return Response.json({
      ok: true,
      service: "lg-ai-strategy-journal",
      database
    });
  } catch (error) {
    return Response.json(
      {
        ok: false,
        service: "lg-ai-strategy-journal",
        error: error instanceof Error ? error.message : "Database check failed."
      },
      { status: 503 }
    );
  }
};
