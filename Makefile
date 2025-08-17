# Centralize pycache to avoid clutter in src directories
export PYTHONPYCACHEPREFIX := .cache/pycache

# Colors
YELLOW := \033[1;33m
GREEN  := \033[1;32m
CYAN   := \033[1;36m
GRAY   := \033[0;37m
RESET  := \033[0m

.DEFAULT_GOAL := help
.PHONY: install start clean example help

install: ## Install/update necessary Python packages
	@echo "Installing dependencies..."
	poetry install

start: install ## Start the Discord bot
	@echo "Starting the Discord LLM Chatbot..."
	poetry run start

clean: ## Remove virtualenv, centralized pycache, and any scattered __pycache__ dirs
	@echo "Cleaning up..."
	rm -rf .venv
	rm -rf $(PYTHONPYCACHEPREFIX)
	find . -type d -name '__pycache__' -exec rm -rf {} +

help: ## Show this help message
	@echo ""
	@echo "$(GREEN)Available commands:$(RESET)"
	@awk '\
		BEGIN {FS=":.*##"; target="";} \
		/^[a-zA-Z0-9_.-]+:.*##/ { \
			target=$$1; gsub(/^ +| +$$/, "", target); \
			summary=$$2; gsub(/^ +| +$$/, "", summary); \
			printf "  $(CYAN)%-12s$(RESET) %s\n", target, summary; \
			next; \
		} \
		/^## @arg / { \
			sub(/^## @arg[ ]*/, "", $$0); \
			gsub(/\[[^]]+\]/, "$(YELLOW)&$(GRAY)"); \
			printf "      $(GRAY)%s$(RESET)\n", $$0; \
			next; \
		} \
		/^[^#]/ { target=""; } \
	' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Usage$(RESET): make <target> [key=value ...]"
	@echo ""
	

# 	example: ## Example command with args [requiredArg] [optionalArg=defaultVal]
#		@echo "Required arg: $(arg)"
# 		@echo "Optional arg: $(opt)"
# 	## @arg [arg]          Required example arg (use: make example arg=value)
# 	## @arg [opt=42]       Optional example arg with default (use: make example arg=foo opt=99)