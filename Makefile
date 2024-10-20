run:
	docker compose up --build --remove-orphans

.DEFAULT_GOAL := run
