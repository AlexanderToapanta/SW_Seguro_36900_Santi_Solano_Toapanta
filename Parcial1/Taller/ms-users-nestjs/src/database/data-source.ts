import 'reflect-metadata';
import 'dotenv/config';
import { DataSource } from 'typeorm';
import { envSchema } from '../config/env.schema.js';
import { databaseOptions } from './database-options.js';

export default new DataSource(databaseOptions(envSchema.parse(process.env)));
