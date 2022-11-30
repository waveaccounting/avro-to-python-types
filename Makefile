.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build 
build: ## Build docker image
	docker build -f Dockerfile -t avro-to-python-types .

.PHONY: test 
test: build ## Build docker image
	docker run -t --rm \
		-v /$(PWD):/app \
		avro-to-python-types 
	
.PHONY: update_poetry
update_poetry: build ## Update poetry from inside the continer
	docker run -ti --rm \
		-v /$(PWD):/app \
		--entrypoint=bash \
		avro-to-python-types 

.PHONY: test_debug 
test_debug: build ## Build docker image
	docker run -t --rm \
		-v /$(PWD):/app \
		-p 9009:9009 \
		--entrypoint poetry \
		avro-to-python-types \
		run python -m debugpy --listen :9009 --wait-for-client  -m pytest tests
	
