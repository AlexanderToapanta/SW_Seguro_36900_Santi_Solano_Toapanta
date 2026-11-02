import { fileURLToPath } from 'node:url';
import { envSchema } from '../config/env.schema.js';
import { User } from '../users/entities/user.entity.js';
import { Role } from '../roles/entities/role.entity.js';
import { UserRole } from '../user-roles/entities/user-role.entity.js';

export function databaseOptions(env: ReturnType<typeof envSchema.parse>) {
  return {
    type: 'postgres' as const,
    host: env.DB_HOST,
    port: env.DB_PORT,
    username: env.DB_USERNAME,
    password: env.DB_PASSWORD,
    database: env.DB_DATABASE,
    entities: [User, Role, UserRole],
    migrations: [fileURLToPath(new URL('./migrations/*.js', import.meta.url))],
    synchronize: false,
    migrationsRun: false,
    logging: ['error' as const],
    ssl: env.DB_SSL === 'true' ? { rejectUnauthorized: true } : false,
    extra: { max: 10, connectionTimeoutMillis: 5000, idleTimeoutMillis: 30000 },
  };
}
