.PHONY: help docs-check

help: ## Show available make targets
	@awk 'BEGIN {FS = ":.*?## "}; /^[a-zA-Z0-9_-]+:.*?##/ { printf "  make %-12s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

docs-check: ## Validate Shared Goals repository map and README cross-links
	python3 scripts/check_repository_map.py
