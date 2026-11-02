import assert from 'node:assert/strict';
import { spawn, spawnSync } from 'node:child_process';
import { once } from 'node:events';
import { randomUUID } from 'node:crypto';
import { setTimeout as delay } from 'node:timers/promises';
import { test } from 'node:test';
import pg from 'pg';

// Cada ejecución crea y elimina su propia BD; no modifica los usuarios locales.
test('API completa con PostgreSQL y JWT reales', { timeout: 120_000 }, async (t) => {
  const database = `users_test_${randomUUID().replaceAll('-', '')}`;
  const port = 13_000 + Math.floor(Math.random() * 10_000);
  const env = { ...process.env, NODE_ENV: 'test', DB_DATABASE: database, PORT: String(port) };
  const admin = new pg.Client({
    host: process.env.DB_HOST, port: Number(process.env.DB_PORT),
    user: process.env.DB_USERNAME, password: process.env.DB_PASSWORD,
    database: process.env.DB_DATABASE,
    ssl: process.env.DB_SSL === 'true' ? { rejectUnauthorized: true } : false,
  });
  let server;
  let output = '';
  let created = false;
  const base = `http://127.0.0.1:${port}/api/v1`;
  async function call(method, path, token, body, status = 200) {
    const response = await fetch(`${base}${path}`, {
      method,
      headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...(body ? { 'Content-Type': 'application/json' } : {}) },
      ...(body ? { body: JSON.stringify(body) } : {}),
    });
    const text = await response.text();
    assert.equal(response.status, status, `${method} ${path}: ${text}`);
    assert.ok(response.headers.get('x-request-id'));
    return text ? JSON.parse(text) : undefined;
  }
  async function login(identifier, password = 'ClaveSegura2026!') {
    return call('POST', '/auth/login', undefined, { identifier, password });
  }
  try {
    await admin.connect();
    await admin.query(`CREATE DATABASE "${database}"`);
    created = true;
    function migrate(command) {
      const result = spawnSync(process.execPath,
        ['node_modules/typeorm/cli.js', '-d', 'dist/database/data-source.js', command],
        { env, encoding: 'utf8', timeout: 30_000 });
      assert.equal(result.status, 0, `${command}: ${result.stdout} ${result.stderr}`);
      return result.stdout;
    }
    await t.test('migración inicial: crea, revierte y vuelve a aplicar sin sincronización', async () => {
      migrate('migration:run');
      assert.match(migrate('migration:run'), /No migrations are pending/);
      migrate('migration:revert');
      migrate('migration:run');
      const verify = spawnSync(process.execPath, ['--input-type=module', '-e',
        "import ds from './dist/database/data-source.js'; await ds.initialize(); try { const log=await ds.driver.createSchemaBuilder().log(); if(log.upQueries.length) throw new Error('Esquema diferente a las entidades'); } finally { await ds.destroy(); }"],
        { env, encoding: 'utf8', timeout: 30_000 });
      assert.equal(verify.status, 0, verify.stdout + verify.stderr);
    });
    const seed = spawnSync(process.execPath, ['dist/database/seed.js'], { env, encoding: 'utf8', timeout: 30_000 });
    assert.equal(seed.status, 0, `Siembra de prueba: ${seed.stdout} ${seed.stderr}`);
    server = spawn(process.execPath, ['dist/main.js'], { env, stdio: ['ignore', 'pipe', 'pipe'] });
    server.stdout.on('data', (chunk) => { output += chunk; });
    server.stderr.on('data', (chunk) => { output += chunk; });
    let ready = false;
    for (let i = 0; i < 100; i++) {
      if (server.exitCode !== null) throw new Error(output);
      try { ready = (await fetch(`${base}/health`)).ok; } catch {}
      if (ready) break;
      await delay(100);
    }
    assert.ok(ready, `El servidor no arrancó: ${output}`);
    let adminToken, operatorToken, clientToken, roles, userId, roleId, temporaryToken;
    await t.test('health público', async () => {
      assert.equal((await call('GET', '/health')).status, 'ok');
    });
    await t.test('rechaza peticiones sin token o con token alterado', async () => {
      await call('GET', '/users', undefined, undefined, 401);
      await call('GET', '/users', 'token-invalido', undefined, 401);
    });
    await t.test('login por usuario y correo; devuelve roles sin incluirlos en el JWT', async () => {
      const a = await login('jperez');
      const o = await login('amendoza@example.com');
      const c = await login('mgomez');
      adminToken = a.accessToken; operatorToken = o.accessToken; clientToken = c.accessToken;
      assert.deepEqual(a.user.roles, ['ADMIN']);
      const payload = JSON.parse(Buffer.from(adminToken.split('.')[1], 'base64url'));
      assert.equal(payload.roles, undefined);
      assert.equal(payload.typ, 'access');
    });
    await t.test('me devuelve la identidad autenticada', async () => {
      assert.equal((await call('GET', '/auth/me', adminToken)).username, 'jperez');
    });
    await t.test('CLIENTE no administra; OPERADOR solo consulta', async () => {
      await call('GET', '/users', clientToken, undefined, 403);
      await call('GET', '/users', operatorToken);
      await call('POST', '/users', operatorToken, {}, 403);
      await call('DELETE', `/roles/${randomUUID()}`, operatorToken, undefined, 403);
    });
    await t.test('paginación y consultas ocultan contraseñas', async () => {
      const result = await call('GET', '/users?page=1&limit=2', adminToken);
      assert.equal(result.data.length, 2);
      assert.equal(result.meta.total, 5);
      assert.ok(!JSON.stringify(result).includes('password'));
      roles = (await call('GET', '/roles', adminToken)).data;
    });
    await t.test('valida parámetros, paginación y campos inesperados', async () => {
      await call('GET', '/users/no-es-uuid', adminToken, undefined, 400);
      await call('GET', '/users/cedula/abc', adminToken, undefined, 400);
      await call('GET', '/users?limit=101', adminToken, undefined, 400);
      await call('POST', '/roles', adminToken, { rol: 'PRUEBA', esAdministrador: true }, 400);
    });
    await t.test('CRUD de roles y conflicto de duplicados', async () => {
      const role = await call('POST', '/roles', adminToken, { rol: 'supervisor' }, 201);
      roleId = role.id;
      assert.equal(role.rol, 'SUPERVISOR');
      await call('POST', '/roles', adminToken, { rol: 'SUPERVISOR' }, 409);
      await call('GET', `/roles/${roleId}`, operatorToken);
      assert.equal((await call('PATCH', `/roles/${roleId}`, adminToken, { rol: 'SUPERVISOR_GENERAL' })).rol, 'SUPERVISOR_GENERAL');
    });
    await t.test('crea usuario, detecta duplicados y permite buscar y actualizar', async () => {
      const dto = { cedula: '1712345678', nombres: 'Usuario', apellidos: 'Prueba',
        fechaNacimiento: '1993-04-18', username: 'prueba_api', email: 'prueba@example.com',
        telefono: '0987654321', password: 'ClaveSegura2026!' };
      const user = await call('POST', '/users', adminToken, dto, 201);
      userId = user.id;
      assert.equal(user.passwordHash, undefined);
      await call('POST', '/users', adminToken, dto, 409);
      assert.equal((await call('GET', `/users/${userId}`, adminToken)).username, 'prueba_api');
      assert.equal((await call('GET', `/users/cedula/${dto.cedula}`, adminToken)).id, userId);
      assert.equal((await call('PATCH', `/users/${userId}`, adminToken, { nombres: 'Actualizado' })).nombres, 'Actualizado');
      temporaryToken = (await login('prueba_api')).accessToken;
    });
    await t.test('asigna y retira roles con efecto sobre el mismo token', async () => {
      const operator = roles.find((r) => r.rol === 'OPERADOR');
      await call('GET', '/users', temporaryToken, undefined, 403);
      await call('POST', '/user-roles', adminToken, { userId, roleId: operator.id }, 201);
      await call('GET', '/users', temporaryToken);
      assert.ok((await call('GET', `/user-roles/user/${userId}`, adminToken)).some((r) => r.roleId === operator.id));
      await call('DELETE', `/user-roles/${userId}/${operator.id}`, adminToken, undefined, 204);
      await call('GET', '/users', temporaryToken, undefined, 403);
    });
    await t.test('rol desactivado y usuario desactivado pierden acceso', async () => {
      const operator = roles.find((r) => r.rol === 'OPERADOR');
      await call('POST', '/user-roles', adminToken, { userId, roleId: operator.id }, 201);
      await call('PATCH', `/roles/${operator.id}`, adminToken, { estado: false });
      await call('GET', '/users', temporaryToken, undefined, 403);
      await call('PATCH', `/roles/${operator.id}`, adminToken, { estado: true });
      await call('PATCH', `/users/${userId}`, adminToken, { estado: false });
      await call('GET', '/auth/me', temporaryToken, undefined, 401);
      await call('PATCH', `/users/${userId}`, adminToken, { estado: true });
    });
    await t.test('cambiar contraseña invalida tokens anteriores y acepta la nueva clave', async () => {
      await call('PATCH', `/users/${userId}`, adminToken, { password: 'NuevaClaveSegura2026!' });
      await call('GET', '/auth/me', temporaryToken, undefined, 401);
      temporaryToken = (await login('prueba_api', 'NuevaClaveSegura2026!')).accessToken;
    });
    await t.test('logout invalida el token utilizado', async () => {
      await call('POST', '/auth/logout', temporaryToken, undefined, 204);
      await call('GET', '/auth/me', temporaryToken, undefined, 401);
    });
    await t.test('eliminación lógica de usuarios y roles', async () => {
      await call('DELETE', `/users/${userId}`, adminToken, undefined, 204);
      await call('GET', `/users/${userId}`, adminToken, undefined, 404);
      await call('DELETE', `/roles/${roleId}`, adminToken, undefined, 204);
      await call('GET', `/roles/${roleId}`, adminToken, undefined, 404);
    });
    await t.test('el login aplica el límite de solicitudes', async () => {
      await call('POST', '/auth/login', undefined, { identifier: 'jperez', password: 'incorrecta' }, 429);
    });
  } finally {
    if (server && server.exitCode === null) {
      const exited = once(server, 'exit');
      server.kill('SIGTERM');
      await exited;
    }
    if (created) await admin.query(`DROP DATABASE "${database}" WITH (FORCE)`);
    await admin.end();
  }
});
