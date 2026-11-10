
import psycopg2
import os
from dotenv import load_dotenv
from app.utils.seed_credentials import seed_password_hash



def main():
    load_dotenv()
    # Inserir dados na tabela users
    users_data = [
        (1, 'Mário', 'mario@email.com', seed_password_hash(1), 3, '2025-04-05 21:59:54.722675', True),
        (3, 'Matilde', 'matilde@email.com', seed_password_hash(3), 1, '2025-04-07 11:21:05.931927', True),
        (4, 'Admin', 'admin@mealplanner.com', seed_password_hash(4), 3, '2025-04-07 13:03:18.849320', True),
        (5, 'Diana', 'diana@mail.pt', seed_password_hash(5), 2, '2025-04-07 17:33:16.211005', True),
    ]
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = conn.cursor()
    for row in users_data:
        try:
            cur.execute("""
                INSERT INTO users (id, nome, email, password_hash, nivel, criado_em, ativo) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, row)
        except Exception as e:
            raise RuntimeError("Erro ao inserir utilizadores") from e

    # Inserir dados na tabela categories
    categories_data = [
        (1, 'Diversos', None),
        (2, 'Pequeno-almoço', None),
        (3, 'Saladas', None),
        (4, 'Vegetarianas', None),
        (5, 'Carne', None),
        (6, 'Lanches', None),
        (7, 'Prato principal', None),
        (8, 'Sopas', None),
        (9, 'Peixe', None),
        (10, 'Bebidas', None),
    ]
    for row in categories_data:
        try:
            cur.execute("""
                INSERT INTO categories (id, nome, descricao) VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, row)
        except Exception as e:
            print(f"Erro ao inserir em categories: {e} - dados: {row}")

    # Inserir dados na tabela recipes
    recipes_data = [
        (1, 'Panquecas com Fruta', 'Panquecas integrais com fruta fresca.', '- 1 banana\r\n- 1 ovo\r\n- 3 colheres de sopa de aveia\r\n- Canela a gosto', '1. Esmaga a banana.\r\n2. Junta o ovo e a aveia.\r\n3. Cozinha numa frigideira antiaderente.\r\n4. Polvilha com canela.', 15, 1, 'pequeno almoço, saudável, rápido', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 2, True, False),
        (2, 'Salada de Quinoa com Frango', 'Salada fresca e nutritiva com quinoa e frango grelhado.', '- 1 chávena de quinoa\n- 1 peito de frango grelhado\n- Pepino, tomate, cenoura\n- Azeite e limão', '1. Coze a quinoa.\n2. Grelha o frango e corta em tiras.\n3. Junta os legumes e tempera.', 25, 2, 'almoço, leve, proteína', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 3, True, False),
        (3, 'Sopa de Legumes', 'Sopa reconfortante com legumes frescos.', '- 2 batatas\n- 2 cenouras\n- 1 courgette\n- 1 cebola\n- Espinafres\n- Sal e azeite', '1. Corta os legumes e coze com água e sal.\n2. Tritura tudo.\n3. Junta espinafres e deixa ferver mais 5 minutos.', 30, 1, 'jantar, leve, saudável', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 8, True, False),
        (4, 'Iogurte com Granola e Fruta', 'Rápido e nutritivo.', '- 1 iogurte natural\n- 2 colheres de sopa de granola\n- Fruta a gosto', '1. Coloca o iogurte numa taça.\n2. Adiciona granola e fruta fatiada.\n3. Mistura e serve.', 5, 1, 'pequeno almoço, rápido, leve', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 2, True, False),
        (5, 'Bacalhau à Brás', 'Clássico prato português com bacalhau desfiado.', '- 400g de bacalhau desfiado\n- 200g de batata palha\n- 4 ovos\n- 1 cebola\n- Salsa', '1. Refoga a cebola em azeite.\n2. Junta o bacalhau e deixa cozinhar.\n3. Adiciona a batata palha.\n4. Envolve com ovos batidos e salsa.', 35, 3, 'almoço, tradicional, intenso', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 9, True, False),
        (6, 'Tortilha de Batata', 'Tortilha espanhola simples e saborosa.', '- 4 batatas\n- 1 cebola\n- 5 ovos\n- Azeite\n- Sal', '1. Frita as batatas e cebola.\n2. Bate os ovos e mistura.\n3. Cozinha em lume médio até dourar dos dois lados.', 25, 2, 'jantar, clássico, reconfortante', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 4, True, False),
        (7, 'Papas de Aveia', 'Aveia cremosa com banana e canela.', '- 1 chávena de aveia\n- 2 chávenas de leite\n- 1 banana\n- Canela a gosto', '1. Cozinha aveia com leite.\n2. Junta banana esmagada e canela.\n3. Serve quente.', 10, 1, 'pequeno almoço, saudável, quente', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 2, True, False),
        (8, 'Arroz de Pato', 'Pato desfiado com arroz e chouriço no forno.', '- 1 pato\n- 2 chávenas de arroz\n- Chouriço\n- Louro e cravinho', '1. Coze o pato com especiarias.\n2. Desfia e reserva.\n3. Cozinha o arroz no caldo.\n4. Leva ao forno com chouriço às rodelas.', 60, 3, 'almoço, tradicional, forno', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 5, True, False),
        (9, 'Douradinhos com Puré', 'Jantar rápido com peixe e puré.', '- Douradinhos de peixe\n- 500g de batata\n- Leite e manteiga\n- Sal', '1. Leva os douradinhos ao forno.\n2. Coze batatas e reduz a puré com leite e manteiga.\n3. Serve com legumes.', 30, 1, 'jantar, simples, rápido', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 9, True, False),
        (10, 'Ovos Mexidos com Espinafres', 'Fonte rápida de proteína.', '- 3 ovos\n- Espinafres frescos\n- Azeite\n- Sal', '1. Refoga os espinafres.\n2. Junta os ovos batidos.\n3. Mexe até ficarem cremosos.', 8, 1, 'pequeno almoço, verde, rápido', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 4, True, False),
        (11, 'Frango à Brás', 'Versão de frango do clássico à Brás.', '- 300g de frango cozido\n- 200g de batata palha\n- 4 ovos\n- 1 cebola', '1. Refoga cebola e junta frango desfiado.\n2. Mistura batata palha e ovos batidos.\n3. Serve com salsa.', 30, 2, 'almoço, criativa, tradicional', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 5, True, False),
        (12, 'Lasanha de Legumes', 'Lasanha vegetariana no forno.', '- Placas de lasanha\n- Beringela, courgette, tomate\n- Queijo ralado\n- Molho de tomate', '1. Grelha os legumes.\n2. Monta a lasanha em camadas.\n3. Cobre com queijo e leva ao forno.', 45, 2, 'jantar, forno, leve', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 4, True, False),
        (13, 'Tapioca Recheada com Queijo', 'Simples e sem glúten.', '- 2 colheres de sopa de goma de tapioca\n- Queijo e fiambre', '1. Cozinha a goma na frigideira.\n2. Recheia e dobra.\n3. Serve quente.', 10, 1, 'pequeno almoço, rápido, leve', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 6, True, False),
        (14, 'Hambúrguer de Grão', 'Alternativa vegetariana ao hambúrguer.', '- 1 lata de grão\n- 1 cebola\n- Alho e salsa\n- Farinha de aveia', '1. Tritura os ingredientes.\n2. Molda hambúrgueres.\n3. Cozinha em frigideira antiaderente.', 25, 2, 'almoço, proteico, saudável', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 4, True, False),
        (15, 'Arroz de Marisco', 'Delicioso e aromático.', '- Miolo de camarão e amêijoa\n- Arroz carolino\n- Cebola e alho\n- Coentros', '1. Refoga os temperos.\n2. Junta o marisco e o arroz.\n3. Adiciona caldo e deixa cozinhar.\n4. Finaliza com coentros.', 40, 3, 'jantar, marisco, intenso', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 9, True, False),
        (16, 'Smoothie Bowl', 'Tigela fresca e nutritiva.', '- 1 banana\n- Frutos vermelhos\n- Iogurte natural\n- Toppings: granola, sementes', '1. Tritura banana e frutos vermelhos com iogurte.\n2. Verte numa taça.\n3. Decora com toppings.', 5, 1, 'pequeno almoço, fresco, verão', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 2, True, False),
        (17, 'Esparguete à Bolonhesa', 'Massa clássica com carne.', '- 250g carne picada\n- 1 cebola\n- Molho de tomate\n- Esparguete', '1. Refoga carne com cebola.\n2. Junta o molho.\n3. Coze o esparguete e junta tudo.', 30, 2, 'almoço, massa, clássico', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 5, True, False),
        (18, 'Salada Russa com Atum', 'Prato frio e fácil.', '- 2 batatas\n- 1 cenoura\n- Ervilhas\n- 1 lata de atum\n- Maionese', '1. Coze os legumes.\n2. Junta o atum.\n3. Envolve tudo com maionese e serve fresco.', 20, 1, 'jantar, frio, simples', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 3, True, False),
        (19, 'Croissant com Queijo e Fiambre', 'Pequeno-almoço no forno.', '- 1 croissant\n- Queijo e fiambre', '1. Recheia o croissant.\n2. Leva ao forno até o queijo derreter.\n3. Serve quente.', 10, 1, 'pequeno almoço, forno, rápido', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 6, True, False),
        (20, 'Empadão de Carne', 'Camadas de carne e puré gratinadas.', '- 500g carne picada\n- Batatas\n- Leite, manteiga\n- Cebola e alho', '1. Refoga a carne.\n2. Faz o puré.\n3. Monta camadas e leva ao forno.', 40, 2, 'almoço, forno, tradicional', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 5, True, False),
        (21, 'Pizza Caseira', 'Base artesanal e recheio a gosto.', '- Massa de pizza\n- Molho de tomate\n- Queijo\n- Legumes ou fiambre', '1. Estende a massa.\n2. Recheia com os ingredientes.\n3. Leva ao forno até dourar.', 30, 2, 'jantar, pizza, forno', '2025-04-05 23:28:52.961463', True, 'meal_planner', 1, 7, True, False),
        (22, 'Sangria de Frutos Vermelhos e Espumante', 'Uma bebida sofisticada, refrescante e frutada, ideal para dias quentes ou para brindar em boa companhia.', '- 250g de frutos vermelhos (morango, framboesa, amora)\r\n- 1 maçã verde cortada em cubos\r\n- 1 laranja em rodelas\r\n- 1 garrafa de espumante bem fresco\r\n- 250 ml de água com gás\r\n- 4 colheres de sopa de açúcar mascavado (opcional)\r\n- Folhas de hortelã a gosto\r\n- Gelo a gosto\r\n', '1. Lava bem os frutos e corta a maçã e a laranja.\r\n2. Numa jarra grande, junta todos os frutos e o açúcar.\r\n3. Mexe suavemente para ajudar o açúcar a dissolver.\r\n4. Junta a água com gás e o espumante.\r\n5. Acrescenta gelo e folhas de hortelã a gosto.\r\n6. Mexe mais uma vez e serve bem fresco!\r\n', 10, 1, 'bebida, festa, verão, rápida, refrescante', '2025-04-06 10:21:43.640994', True, 'utilizador', 1, 10, True, False),
        (23, 'Salada De Quinoa Mediterrânea', 'Uma salada fresca e nutritiva, perfeita para o almoço ou como acompanhamento.', '- 200g de quinoa\r\n- 1 pepino médio, cortado em cubos\r\n- 200g de tomates cereja, cortados ao meio\r\n- 100g de queijo feta, esfarelado\r\n- 50g de azeitonas pretas, sem caroço\r\n- 1 cebola roxa pequena, picada finamente\r\n- 2 colheres de sopa de azeite de oliva extra virgem\r\n- Suco de 1 limão\r\n- 2 colheres de sopa de hortelã fresca picada\r\n- 2 colheres de sopa de salsa fresca picada\r\n- Sal e pimenta a gosto', '1. Lave bem a quinoa em água corrente usando uma peneira fina.\r\n2. Cozinhe a quinoa em 400ml de água com uma pitada de sal por cerca de 15 minutos ou até que toda a água seja absorvida.\r\n3. Deixe a quinoa esfriar completamente.\r\n4. Em uma tigela grande, misture a quinoa, o pepino, os tomates, o queijo feta, as azeitonas e a cebola.\r\n5. Em um recipiente pequeno, misture o azeite, o suco de limão, sal e pimenta para fazer o molho.\r\n6. Regue a salada com o molho e misture bem.\r\n7. Adicione a hortelã e a salsa picadas, misture novamente.\r\n8. Sirva imediatamente ou refrigere por até 2 horas antes de servir.', 30, 1, 'saudável, vegetariano, almoço, rápido', '2025-04-07 17:37:57.841626', True, 'utilizador', 5, 3, True, True),
        (24, 'Sopa De Abóbora E Gengibre', 'Uma sopa cremosa e reconfortante, perfeita para os dias mais frios. O gengibre adiciona um toque picante que complementa a doçura natural da abóbora.', '- 1 abóbora média (cerca de 1kg), descascada e cortada em cubos\r\n- 2 cenouras médias, cortadas em rodelas\r\n- 1 cebola média, picada\r\n- 2 dentes de alho, picados\r\n- 1 pedaço de gengibre fresco (3cm), ralado\r\n- 1 litro de caldo de legumes\r\n- 200ml de leite de coco\r\n- 2 colheres de sopa de azeite de oliva\r\n- 1 colher de chá de cominho em pó\r\n- 1/2 colher de chá de canela em pó\r\n- Sal e pimenta a gosto\r\n- Sementes de abóbora torradas para decorar (opcional)\r\n- Coentros frescos picados para decorar (opcional)', '1. Aqueça o azeite numa panela grande em fogo médio.\r\n2. Adicione a cebola e refogue até ficar translúcida, cerca de 3-4 minutos.\r\n3. Adicione o alho e o gengibre, e refogue por mais 1 minuto até liberar o aroma.\r\n4. Adicione a abóbora e as cenouras, e refogue por 5 minutos, mexendo ocasionalmente.\r\n5. Adicione o cominho e a canela, e mexa para envolver os vegetais com as especiarias.\r\n6. Despeje o caldo de legumes, aumente o fogo e deixe ferver.\r\n7. Reduza o fogo, tampe parcialmente a panela e deixe cozinhar por 20-25 minutos, ou até que os vegetais estejam bem macios.\r\n8. Retire do fogo e deixe esfriar ligeiramente.\r\n9. Transfira a sopa para um liquidificador (ou use um mixer de imersão) e triture até obter um creme liso.\r\n10. Volte a sopa para a panela, adicione o leite de coco e aqueça em fogo baixo.\r\n11. Tempere com sal e pimenta a gosto.\r\n12. Sirva quente, decorada com sementes de abóbora torradas e coentros frescos, se desejar.', 45, 1, 'inverno, vegetariano, sem glúten, saudável', '2025-04-07 17:52:49.323460', True, 'utilizador', 5, 8, True, True),
    ]
    for row in recipes_data:
        try:
            cur.execute("""
                INSERT INTO recipes (id, titulo, descricao, ingredientes, instrucoes, tempo_preparacao, dificuldade, tags, data_submetida, publicada, fonte, utilizador_id, categoria_id, aprovada, publica_quando_aprovada) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, row)
        except Exception as e:
            print(f"Erro ao inserir em recipes: {e} - dados: {row}")

    # Inserir dados na tabela meal_plans
    meal_plans_data = [
        (5, '2025-04-17', '2025-04-06 17:28:31.075839', 1),
    ]
    for row in meal_plans_data:
        try:
            cur.execute("""
                INSERT INTO meal_plans (id, data_inicio, criado_em, utilizador_id) VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, row)
        except Exception as e:
            print(f"Erro ao inserir em meal_plans: {e} - dados: {row}")

    # Inserir dados na tabela meal_entries
    meal_entries_data = [
        (1, '2025-04-17', 'pequeno_almoço', 5, 3),
        (2, '2025-04-19', 'pequeno_almoço', 5, 18),
        (3, '2025-04-19', 'almoço', 5, 13),
        (4, '2025-04-19', 'jantar', 5, 14),
    ]
    for row in meal_entries_data:
        try:
            cur.execute("""
                INSERT INTO meal_entries (id, data_refeicao, refeicao_tipo, plano_id, receita_id) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, row)
        except Exception as e:
            print(f"Erro ao inserir em meal_entries: {e} - dados: {row}")

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Todas as tabelas foram migradas com sucesso (conflitos ignorados).")


if __name__ == "__main__":
    main()
