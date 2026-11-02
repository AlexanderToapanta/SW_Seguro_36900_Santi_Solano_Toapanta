"""Pruebas de productos en una BD temporal; no modifica los datos del taller."""
import os
from pathlib import Path
import sys
import unittest
from uuid import uuid4
import psycopg
from psycopg import sql
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / '.env')
name = 'products_test_' + uuid4().hex
with psycopg.connect(host=os.environ['DB_HOST'], port=os.environ['DB_PORT'],
    user=os.environ['DB_USER'], password=os.environ['DB_PASSWORD'],
    dbname=os.environ['DB_NAME'], autocommit=True) as admin:
    admin.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(name)))
    try:
        os.environ['DB_NAME'] = name
        os.environ['ENABLE_SEED'] = 'true'
        suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    finally:
        from app.db.session import engine
        engine.dispose()
        admin.execute(sql.SQL('DROP DATABASE {} WITH (FORCE)').format(sql.Identifier(name)))
sys.exit(0 if result.wasSuccessful() else 1)
