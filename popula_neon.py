import os
import psycopg2

from app.utils.seed_credentials import seed_password_hash

def popular():
    # As passwords têm de ser definidas antes de abrir a ligação.
    users = [
        (1, 'Mário', 'mario@email.com', seed_password_hash(1), 3, '2025-04-05 21:59:54.722675', True),
        (3, 'Matilde', 'matilde@email.com', seed_password_hash(3), 1, '2025-04-07 11:21:05.931927', True),
        (4, 'Admin', 'admin@mealplanner.com', seed_password_hash(4), 3, '2025-04-07 13:03:18.849320', True)
    ]

    # 2. Categorias (Crucial para as receitas não darem erro de FK)
    categories = [(1, 'Diversos', None), (2, 'Pequeno-almoço', None), (3, 'Saladas', None), (4, 'Vegetarianas', None), (5, 'Carne', None), (6, 'Lanches', None), (7, 'Prato principal', None), (8, 'Sopas', None), (9, 'Peixe', None), (10, 'Bebidas', None)]

    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = conn.cursor()

    # 3. Inserir Utilizadores
    for u in users:
        cur.execute("INSERT INTO users (id, nome, email, password_hash, nivel, criado_em, ativo) VALUES (%s,%s,%s,%s,%s,%s,%s)", u)
    
    # 4. Inserir Categorias
    for c in categories:
        cur.execute("INSERT INTO categories (id, nome, descricao) VALUES (%s,%s,%s)", c)

    conn.commit()
    print("✅ Utilizadores e Categorias inseridos! Agora corre o teu script anterior de migração para as receitas.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    popular()
