all: run

setup:
	@docker build -t vache .

run:
	@flask --app app --debug run

.PHONY: all run setup