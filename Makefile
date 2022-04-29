test:
	pytest -v --tb=line --language=en -m need_review --alluredir=reports -n 3

# Borrowed from
#   https://github.com/jfrazelle/dockerfiles/blob/master/kiwi-builder/Makefile

.PHONY: all build run shell clean

repo_name = myrepo

all: run

build:
	docker build --rm --force-rm -t $(repo_name) .

run: build
	docker run --rm $(repo_name)

shell: build
	docker run -it --rm $(repo_name) bash

clean:
	docker rmi $(repo_name)
