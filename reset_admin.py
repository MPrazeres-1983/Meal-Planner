import psycopg2
import os
from werkzeug.security import generate_password_hash

# 1. Configura a tua ligação ao Neon
DATABASE_URL = "postgresql://neondb_owner:npg_z7KpcdZlW6Mr@ep-red-frost-abg4eerj-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require"

# 2. Define a tua NOVA password aqui
NOVA_PASSWORD = "Mudar123!" 

def reset():
    hash_novo = generate_password_hash(NOVA_PASSWORD)
    
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Vamos atualizar o utilizador Mário (ID 1) ou Admin (ID 4)
    cur.execute("""
        UPDATE users 
        SET password_hash = %s 
        WHERE id = 4 OR email = 'mario@email.com'
    """, (hash_novo,))
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Sucesso! Agora já podes fazer login com a password: {NOVA_PASSWORD}")

if __name__ == "__main__":
    reset()