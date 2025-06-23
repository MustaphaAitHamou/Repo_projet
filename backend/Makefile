# backend/Makefile

.PHONY: up-db up-backend test

up-db:
	docker-compose up -d mysql     # lance MySQL en arrière-plan
	@sleep 10                      # attends 10s le temps que MySQL soit prêt

up-backend: up-db
	docker-compose up -d backend   # lance ton API Flask

test: up-backend
	pytest --maxfail=1 --disable-warnings --cov=app
