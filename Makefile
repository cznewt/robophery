CWD=$(shell pwd)

help:
	@echo "Available actions:"
	@echo "  build         Build robophery docker container"
	@echo "  publish       Publish robophery docker container"
	@echo "  doc           Build project documentation"

all: build

build:
	docker build -t cznewt/robophery:latest -f ./Dockerfile .

publish:
	docker push cznewt/robophery:latest

doc:
	cd doc && make html && cd ..; done
