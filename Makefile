DOCKER_RUNNER=docker-compose run web
DOCKER_RUNNER_CI=docker-compose -f docker-compose-ci.yml run web
DOCKER_EXEC=docker-compose exec web

build: stop
	docker-compose build
	$(DOCKER_RUNNER) migrate

build-ci:
	docker-compose -f docker-compose-ci.yml build
	$(DOCKER_RUNNER_CI) migrate

start:
	docker-compose up -d

stop:
	docker-compose down

restart: stop start

logs:
	docker-compose logs -f --tail=15

lint:
	$(DOCKER_RUNNER) lint_local

test:
	$(DOCKER_RUNNER) test

test-ci:
	$(DOCKER_RUNNER_CI) test

shell:
	$(DOCKER_EXEC) bash

generate-migrations:
	@read -p "Describe your migration (e.g. 'Create domain table'):" description; \
		clean_migration_name=$$(echo $$description | sed -e 's/ /_/g' | tr '[:upper:]' '[:lower:]'); \
		$(DOCKER_RUNNER) generate_migrations $$clean_migration_name

migrate:
	$(DOCKER_RUNNER) migrate

rollback-migration:
	$(DOCKER_RUNNER) rollback_last_migration
	