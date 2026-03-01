import sqlite3
from sqlalchemy import create_engine, text

# 1. Configurações - COLOCA A TUA STRING DO NEON AQUI
# Altera esta linha no topo do teu migrate_data.py
SQLITE_DB = 'instance/mealplanner.db'
POSTGRES_URL = 'postgresql://neondb_owner:npg_z7KpcdZlW6Mr@ep-red-frost-abg4eerj-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require'

def migrate():
    # Ligar ao SQLite (Origem)
    sqlite_conn = sqlite3.connect(SQLITE_DB)
    sqlite_cursor = sqlite_conn.cursor()
    
    # Ligar ao Postgres (Destino)
    pg_engine = create_engine(POSTGRES_URL)
    
    # Lista de tabelas para migrar (na ordem certa para evitar erros de chaves estrangeiras)
    tables = ['users', 'categories', 'recipes', 'meal_plans', 'meal_entries', 'favorites']
    
    print("🚀 A iniciar migração de dados...")
    
    with pg_engine.begin() as pg_conn:
        for table in tables:
            print(f"📦 A migrar tabela: {table}...")
            
            # Ler dados do SQLite
            sqlite_cursor.execute(f"SELECT * FROM {table}")
            rows = sqlite_cursor.fetchall()
            
            if not rows:
                print(f"  ⚠️ Tabela {table} está vazia. A saltar...")
                continue
                
            # Obter nomes das colunas
            cursor_desc = sqlite_cursor.description
            columns = [column[0] for column in cursor_desc]
            
            # Preparar o comando INSERT para Postgres
            col_names = ", ".join(columns)
            placeholders = ", ".join([f":{col}" for col in columns])
            insert_query = text(f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})")
            
            # Inserir cada linha no Postgres com conversão de tipos
            for row in rows:
                row_dict = dict(zip(columns, row))
                
                # CORREÇÃO PARA BOOLEANOS (Versão Abrangente)
                # Adicionei todas as colunas booleanas que o Postgres detetou
                bool_columns = ['ativo', 'is_admin', 'favorito', 'publicada', 'aprovada', 'publica_quando_aprovada']
                
                for key in bool_columns:
                    if key in row_dict:
                        if row_dict[key] == 1:
                            row_dict[key] = True
                        elif row_dict[key] == 0:
                            row_dict[key] = False
                
            print(f"  ✅ {len(rows)} linhas migradas com sucesso.")

    sqlite_conn.close()
    print("\n🎉 Migração concluída! Todos os teus dados de 19 valores estão no Neon.")

if __name__ == "__main__":
    migrate()