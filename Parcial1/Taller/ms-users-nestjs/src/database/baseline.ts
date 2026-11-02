import dataSource from './data-source.js';

// Adopta únicamente una BD del laboratorio que coincide con el esquema inicial.
// No borra registros ni ejecuta CREATE TABLE sobre tablas existentes.
await dataSource.initialize();
try {
  const history = (await dataSource.query(
    `SELECT to_regclass('public.migrations') AS name`,
  )) as { name: string | null }[];
  if (history[0]?.name) {
    throw new Error('La base ya tiene historial. Usa npm run migration:run.');
  }
  const pending = dataSource.migrations;
  if (pending.length !== 1 || !pending[0]?.name?.startsWith('InitialSchema')) {
    throw new Error(
      'La adopción requiere únicamente la migración InitialSchema.',
    );
  }
  const changes = await dataSource.driver.createSchemaBuilder().log();
  if (changes.upQueries.length > 0) {
    throw new Error(
      'El esquema no coincide con las entidades. No se ha registrado la migración.',
    );
  }
  await dataSource.runMigrations({ fake: true, transaction: 'all' });
  console.log(
    'Esquema existente verificado y migración inicial registrada. Datos conservados.',
  );
} finally {
  await dataSource.destroy();
}
