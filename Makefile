.PHONY: help lint format check migrations migrate run shell clean

PYTHON = poetry run python
DJANGO_APPS = barter_app barter_project

BLUE = \033[36m
GREEN = \033[32m
YELLOW = \033[33m
RED = \033[31m
NC = \033[0m

help:
	@echo "$(BLUE)Доступные команды:$(NC)"
	@echo "  $(YELLOW)make lint$(NC)       - запуск проверки кода (black + ruff + mypy)"
	@echo "  $(YELLOW)make format$(NC)     - автоматическое форматирование кода (black + ruff --fix)"
	@echo "  $(YELLOW)make check$(NC)      - проверка без изменения кода"
	@echo "  $(YELLOW)make migrations$(NC) - создание миграций"
	@echo "  $(YELLOW)make migrate$(NC)    - применение миграций"
	@echo "  $(YELLOW)make run$(NC)        - запуск сервера для разработки"
	@echo "  $(YELLOW)make shell$(NC)      - запуск Django shell"
	@echo "  $(YELLOW)make clean$(NC)      - удаление временных файлов"

lint: format check

format:
	@echo "$(BLUE)🚀 Форматирование кода с помощью ruff...$(NC)"
	$(PYTHON) -m ruff format $(DJANGO_APPS)
	$(PYTHON) -m ruff check --fix $(DJANGO_APPS)
	@echo "$(GREEN)✅ Форматирование завершено!$(NC)"

check:
	@echo "$(BLUE)🔍 Проверка кода...$(NC)"
	$(PYTHON) -m ruff check $(DJANGO_APPS)
	@echo "$(GREEN)✅ Проверка кода успешно пройдена!$(NC)"

migrations:
	@echo "$(BLUE)🔄 Создание миграций...$(NC)"
	$(PYTHON) manage.py makemigrations

migrate:
	@echo "$(BLUE)🔄 Применение миграций...$(NC)"
	$(PYTHON) manage.py migrate

run:
	@echo "$(BLUE)🚀 Запуск сервера разработки...$(NC)"
	$(PYTHON) manage.py runserver

shell:
	@echo "$(BLUE)🐚 Запуск Django shell...$(NC)"
	$(PYTHON) manage.py shell

clean:
	@echo "$(BLUE)🧹 Удаление временных файлов...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".DS_Store" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@echo "$(GREEN)✅ Временные файлы удалены!$(NC)"
