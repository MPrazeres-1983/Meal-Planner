import psycopg2

# USA A TUA STRING DO NEON
DATABASE_URL = "postgresql://neondb_owner:npg_z7KpcdZlW6Mr@ep-red-frost-abg4eerj-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require"

def popular():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # 1. Dados dos Utilizadores (Copiados do teu ficheiro)
    users = [
        (1, 'Mário', 'mario@email.com', 'scrypt:32768:8:1$LsxJ5wRU0X8tVjSj$81a734d9905e0771167380434e6af2be03443324025c63cc2f99cd7a1c1bd6d4f357209e864d17a6d967f8a6b5d132c3bc417910b21e0df7e4130c2380c00c18', 3, '2025-04-05 21:59:54.722675', True),
        (3, 'Matilde', 'matilde@email.com', 'scrypt:32768:8:1$iYJOXMgqzLXNmiPK$5c1ff5b15e0707d8d1148676e37648cf6636ad9a855fce19ea7c6a301b9f416d6f1631ac34549ca5f8beb92eab3e51caf813c2b39b1b07c0e9e33a47bf6a8dee', 1, '2025-04-07 11:21:05.931927', True),
        (4, 'Admin', 'admin@mealplanner.com', 'scrypt:32768:8:1$ix9rhxSmLo19A7hh$c8f66656e43665d6f29f15ae2244b99f5a54e14e333698ef3ddf6be81bce24e52ade3ab7b7df5476bcf36deeb6ad8abed8d76ec9f1945aec22b56cb671561ea2', 3, '2025-04-07 13:03:18.849320', True)
    ]

    # 2. Categorias (Crucial para as receitas não darem erro de FK)
    categories = [(1, 'Diversos', None), (2, 'Pequeno-almoço', None), (3, 'Saladas', None), (4, 'Vegetarianas', None), (5, 'Carne', None), (6, 'Lanches', None), (7, 'Prato principal', None), (8, 'Sopas', None), (9, 'Peixe', None), (10, 'Bebidas', None)]

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