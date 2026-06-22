import { neon, type NeonQueryFunction } from "@neondatabase/serverless";

let sqlClient: NeonQueryFunction<false, false> | undefined;

export function getDatabase(): NeonQueryFunction<false, false> {
  const connectionString = import.meta.env.DATABASE_URL;

  if (!connectionString) {
    throw new Error("DATABASE_URL is not configured.");
  }

  sqlClient ??= neon(connectionString);
  return sqlClient;
}
