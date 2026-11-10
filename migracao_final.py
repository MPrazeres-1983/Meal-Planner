import os
import sqlite3
from sqlalchemy import create_engine, text

# CONFIGURAÇÃO
SQLITE_PATH = 'instance/mealplanner.db'

def migrar():
    sqlite_conn = sqlite3.connect(SQLITE_PATH)
    pg_engine = create_engine(os.environ["DATABASE_URL"])
    
    # ORDEM CRÍTICA: users e categories PRIMEIRO
    tables = ['users', 'categories', 'recipes', 'meal_plans', 'meal_entries']
    bool_cols = ['ativo', 'publicada', 'aprovada', 'publica_quando_aprovada']

    with pg_engine.begin() as pg_conn:
        for table in tables:
            cursor = sqlite_conn.execute(f"SELECT * FROM {table}")
            cols = [d[0] for d in cursor.description]
            rows = cursor.fetchall()
            
            print(f"📦 Migrando {table} ({len(rows)} linhas)...")
            
            for row in rows:
                data = dict(zip(cols, row))
                # Ajuste de booleanos para o Postgres
                for col in bool_cols:
                    if col in data:
                        data[col] = bool(data[col])
                
                query = text(f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join([':'+c for c in cols])})")
                pg_conn.execute(query, data)
            
    print("✅ Mário, agora as 24 receitas ESTÃO lá!")

if __name__ == "__main__":
    migrar()
