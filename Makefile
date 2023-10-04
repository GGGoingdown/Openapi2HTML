image_name = "openapi2html:0.1"

build:
	docker build -t $(image_name) .

run:
	docker run -it -v "${PWD}/example:/app/example" -v "${PWD}/docs:/app/docs" --rm $(image_name) python src/main.py --source ./example/openapi.json --auto-latest

test:
	poetry run python src/main.test.py

ci_test:
	drone exec --pipeline test

.PHONY: build
