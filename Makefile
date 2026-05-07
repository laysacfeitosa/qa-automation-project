.PHONY: install install-api install-web test test-api test-web test-smoke clean help

help:
	@echo "Comandos disponíveis:"
	@echo "  make install       - Instala todas as dependências (API + Web)"
	@echo "  make install-api   - Instala só dependências da API"
	@echo "  make install-web   - Instala só dependências do Web"
	@echo "  make test          - Roda todos os testes (API + Web)"
	@echo "  make test-api      - Roda só testes da API"
	@echo "  make test-web      - Roda só testes Web"
	@echo "  make test-smoke    - Roda só testes smoke"
	@echo "  make clean         - Limpa caches e relatórios"

install: install-api install-web

install-api:
	pip install -r api-tests/requirements.txt

install-web:
	pip install -r web-tests/requirements.txt

test-api:
	cd api-tests && pytest

test-web:
	cd web-tests && pytest

test: test-api test-web

test-smoke:
	cd api-tests && pytest -m smoke
	cd web-tests && pytest -m smoke

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	rm -f api-tests/reports/*.html web-tests/reports/*.html
	rm -rf web-tests/reports/screenshots/*
