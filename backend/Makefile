.SILENT:

## help: print this help message
.PHONY: help
help:
	@echo 'Usage:'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'

## fmt: run isort and black
.PHONY: fmt
fmt:
	poetry run isort src/ tests/
	poetry run black src/ tests/

## test: run tests
.PHONY: test
test:
	poetry run python -m pytest
