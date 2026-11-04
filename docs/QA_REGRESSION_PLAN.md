# Plano de regressão pós-merge — Meal Planner

**Ambiente automático:** Flask test client + SQLite em memória, sem acesso à base de dados real.
**Ambiente publicado:** Render; executar só GETs públicos sem autorização adicional.
**Critério de saída:** CI verde, deployment `live`, GET da página inicial HTTP 200, sem fugas de informação/autorizações indevidas.

| ID | Tipo/fluxo | Passos resumidos | Resultado esperado | Execução |
|---|---|---|---|---|
| MP-REG-001 | Público | Abrir `/` sem sessão | Página inicial HTTP 200 | Smoke Render |
| MP-REG-002 | Autenticação | Abrir `/auth/login` | Formulário HTTP 200 | Staging |
| MP-REG-003 | Autenticação | Registar utilizador válido em BD de teste | Utilizador nível 1, sem privilégios | Automático |
| MP-REG-004 | Autenticação | Login válido e acesso a `/home` | Sessão válida | Automático |
| MP-REG-005 | Autenticação | Login com password incorreta | Recusado, sem sessão | Automático |
| MP-REG-006 | Autenticação | Logout e voltar a `/home` | Acesso negado | Automático |
| MP-REG-007 | Sessões | Bloquear conta após autenticação; repetir pedido | Sessão invalidada, redireção para login | Automático |
| MP-REG-008 | Sessões | Apagar conta mantendo cookie antigo | Sessão invalidada, redireção para login | Automático |
| MP-REG-009 | Administração | Despromover admin com sessão antiga; consultar utilizadores | Acesso administrativo negado | Automático |
| MP-REG-010 | Administração | Utilizador comum tenta consultar/editar outro utilizador | Acesso negado | Automático |
| MP-REG-011 | Administração | Aprovar/recusar receita via GET | HTTP 405 | Automático |
| MP-REG-012 | Administração | Aprovar/recusar receita via POST com token CSRF | Operação autorizada apenas ao admin | Staging |
| MP-REG-013 | Planos | Criar plano com receitas/datas válidas | Persistência correta apenas para dono | Staging |
| MP-REG-014 | Planos | Editar plano de outro utilizador | Operação bloqueada | Automático |
| MP-REG-015 | Planos | Apagar plano de outro utilizador | Operação bloqueada, dados preservados | Automático |
| MP-REG-016 | CSRF | Apagar plano via POST sem token CSRF | HTTP 400, plano preservado | Automático |
| MP-REG-017 | Receitas | Submeter receita e aprovar/rejeitar como admin | Workflow e permissões corretos | Staging |
| MP-REG-018 | Exportação | Gerar PDF de plano do próprio utilizador | PDF íntegro ou erro controlado | Staging |
| MP-REG-019 | Segredos | Verificar configuração Render e rotação Neon | Credential antiga revogada, nova funcional | Externo — pendente |
| MP-REG-020 | Deploy | Merge na `main` e observar Render | Build + arranque + HTTP 200 | Pós-merge |

**Atenção:** não executar testes destrutivos na base de dados de produção. Os casos marcados Staging não são considerados executados. Guardar evidências por ID antes de fechar o ciclo.
