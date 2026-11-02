import { MiddlewareConsumer, Module, NestModule } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { APP_GUARD } from '@nestjs/core';
import { ThrottlerGuard, ThrottlerModule } from '@nestjs/throttler';
import { TypeOrmModule } from '@nestjs/typeorm';
import { envSchema } from './config/env.schema.js';
import { RolesModule } from './roles/roles.module.js';
import { UserRolesModule } from './user-roles/user-roles.module.js';
import { UsersModule } from './users/users.module.js';
import { RequestIdMiddleware } from './common/middleware/request-id/request-id.middleware.js';
import { AuthModule } from './auth/auth.module.js';
import { JwtAuthGuard } from './auth/guards/jwt-auth/jwt-auth.guard.js';
import { RolesGuard } from './auth/guards/roles/roles.guard.js';
import { AppController } from './app.controller.js';
import { databaseOptions } from './database/database-options.js';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      cache: true,
      validationSchema: envSchema,
    }),

    TypeOrmModule.forRootAsync({
      inject: [ConfigService],

      useFactory: (config: ConfigService) => ({
        ...databaseOptions(
          envSchema.parse({
            ...process.env,
            ...Object.fromEntries(
              [
                'DB_HOST',
                'DB_PORT',
                'DB_USERNAME',
                'DB_PASSWORD',
                'DB_DATABASE',
                'DB_SSL',
              ].map((key) => [key, config.get(key)]),
            ),
          }),
        ),
        retryAttempts: 5,
        retryDelay: 2000,
      }),
    }),

    ThrottlerModule.forRootAsync({
      inject: [ConfigService],
      useFactory: (config: ConfigService) => [
        {
          ttl: Number(config.getOrThrow('RATE_LIMIT_TTL_MS')),
          limit: Number(config.getOrThrow('RATE_LIMIT_MAX')),
          blockDuration: Number(config.getOrThrow('RATE_LIMIT_BLOCK_MS')),
        },
      ],
    }),
    UsersModule,
    RolesModule,
    UserRolesModule,
    AuthModule,
  ],
  controllers: [AppController],
  providers: [
    /*
     * 1. Rate Limiting
     */
    {
      provide: APP_GUARD,

      useClass: ThrottlerGuard,
    },

    /*
     * 2. Autenticación JWT
     */
    {
      provide: APP_GUARD,

      useClass: JwtAuthGuard,
    },

    /*
     * 3. Autorización por roles
     */
    {
      provide: APP_GUARD,

      useClass: RolesGuard,
    },
  ],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer.apply(RequestIdMiddleware).forRoutes('*');
  }
}
