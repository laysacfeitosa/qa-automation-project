# QA Automation — API & Web

[![API Tests](https://github.com/SEU_USUARIO/SEU_REPO/actions/workflows/api-tests.yml/badge.svg)](https://github.com/SEU_USUARIO/SEU_REPO/actions/workflows/api-tests.yml)
[![Web Tests](https://github.com/SEU_USUARIO/SEU_REPO/actions/workflows/web-tests.yml/badge.svg)](https://github.com/SEU_USUARIO/SEU_REPO/actions/workflows/web-tests.yml)

Projeto de automação de testes cobrindo dois cenários:

1. **API** — Swagger Petstore (`https://petstore.swagger.io/v2`) cobrindo Pet, Store e User.
2. **Web** — SauceDemo (`https://www.saucedemo.com/`) com fluxo E2E de login, carrinho e checkout.

## Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12 |
| Test runner | pytest |
| HTTP client | requests |
| Browser automation | Selenium 4 |
| Validação de contrato | jsonschema |
| Geração de dados | Faker |
| Reporting | pytest-html |
| CI/CD | GitHub Actions |
| Design Pattern (Web) | Page Object Model |

## Estrutura

```
qa-automation-project/
├── api-tests/
│   ├── tests/              # Testes pytest (test_pet, test_store, test_user)
│   ├── utils/              # ApiClient, config, data builders
│   ├── data/               # JSON Schemas para validação de contrato
│   ├── reports/            # Relatórios HTML
│   ├── pytest.ini
│   └── requirements.txt
├── web-tests/
│   ├── tests/              # Testes pytest (test_login, test_cart, test_e2e_checkout)
│   ├── pages/              # Page Objects (BasePage, LoginPage, InventoryPage, ...)
│   ├── utils/              # DriverFactory, config
│   ├── reports/            # Relatórios HTML + screenshots de falhas
│   ├── pytest.ini
│   └── requirements.txt
├── .github/workflows/
│   ├── api-tests.yml       # Pipeline de CI da API
│   └── web-tests.yml       # Pipeline de CI da Web
└── README.md
```

## Pré-requisitos

- Python 3.12+
- Chrome instalado (para os testes Web)
- Git

## Como executar

> ⚠️ **Importante:** rode os testes **de dentro de cada pasta** (`api-tests/` ou `web-tests/`). Cada projeto tem seu próprio `pytest.ini` e dependências. Rodar `pytest` direto na raiz vai falhar porque o pytest tenta coletar os dois projetos de uma vez.

### Atalho com Makefile

```bash
make install       # instala tudo
make test-api      # roda só API
make test-web      # roda só Web
make test          # roda os dois
```

### Testes de API

```bash
cd api-tests
python -m venv .venv
source .venv/bin/activate            # Linux/Mac
# .venv\Scripts\activate             # Windows
pip install -r requirements.txt
pytest                               # roda tudo
pytest -m smoke                      # só smoke
pytest -m pet                        # só Pet
pytest tests/test_user.py -v         # arquivo específico
```

Relatório gerado em `api-tests/reports/report.html`.

### Testes Web

```bash
cd web-tests
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest                               # headless por padrão
HEADLESS=false pytest                # com janela visível
pytest -m e2e                        # só fluxo ponta a ponta
pytest tests/test_login.py -v
```

Relatório em `web-tests/reports/report.html`. Screenshots de falhas em `web-tests/reports/screenshots/`.

## Cobertura de testes

### API — 26 testes

**Pet (9)** — CRUD completo, busca por status, validação de schema, retornos 404 para recursos inexistentes.
**Store (7)** — Inventário, criação/leitura/deleção de pedidos com validação de contrato.
**User (10)** — CRUD, criação em lote, login/logout, atualização de dados.

### Web — 13 testes

**Login (4)** — credenciais válidas, usuário bloqueado, senha inválida, campos vazios.
**Carrinho (4)** — adição simples, múltipla, remoção, persistência ao navegar.
**Checkout (3)** — validação de campos obrigatórios.
**E2E (2)** — fluxo completo com 1 produto e com múltiplos produtos.

## Design Patterns

- **Page Object Model** nos testes Web: cada página tem sua classe (`LoginPage`, `InventoryPage`, `CartPage`, `CheckoutPage`) herdando de `BasePage`. Locators e ações ficam isolados das asserções.
- **Factory** para o WebDriver (`DriverFactory`) — centraliza configuração e facilita troca de browser.
- **Data Builder** com Faker — payloads gerados dinamicamente evitam colisão entre execuções e isolamento entre testes.
- **Fixtures pytest** com cleanup automático (`yield` + delete) — cada teste deixa o ambiente limpo.

## CI/CD

Dois workflows independentes em `.github/workflows/`:

- **api-tests.yml** — roda em push, PR para `main`, manual e semanalmente (segunda 06:00 UTC).
- **web-tests.yml** — mesmo schedule, com Chrome instalado via `browser-actions/setup-chrome`.

Ambos:
- Fazem cache de pip para acelerar builds
- Publicam relatório HTML como artifact (retenção de 30 dias)
- O workflow Web também faz upload de screenshots quando há falha

## Variáveis de ambiente

| Variável | Padrão | Onde |
|---|---|---|
| `PETSTORE_BASE_URL` | `https://petstore.swagger.io/v2` | API |
| `SAUCEDEMO_URL` | `https://www.saucedemo.com/` | Web |
| `HEADLESS` | `true` | Web |

## Markers do pytest

```bash
pytest -m smoke         # Smoke tests (rápidos, críticos)
pytest -m e2e           # Fluxo ponta a ponta
pytest -m pet           # Endpoint Pet
pytest -m store         # Endpoint Store
pytest -m user          # Endpoint User
pytest -m login         # Login Web
pytest -m cart          # Carrinho Web
pytest -m checkout      # Checkout Web
```
