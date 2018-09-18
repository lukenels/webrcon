
dev:
	pipenv run app-dev

prod:
	pipenv run app-prod

socket:
	pipenv run app-sock

PHONY: dev prod socket