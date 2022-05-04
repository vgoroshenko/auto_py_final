test:
	pytest -v --tb=line --language=en -m need_review --alluredir=reports -n 3

pull:
	docker pull selenoid/chrome:latest
	docker pull selenoid/firefox:latest
	docker pull browsers/edge
	docker pull browsers/safari:15.0

clean:
	docker rmi -f selenoid/chrome:latest
	docker rmi -f selenoid/firefox:latest
	docker rmi -f browsers/edge
	docker rmi -f browsers/safari:15.0

# Borrowed from
#   https://github.com/jfrazelle/dockerfiles/blob/master/kiwi-builder/Makefile

#.PHONY: all build run shell clean
#
#repo_name = myrepo
#
#all: run
#
#build:
#	docker build --rm --force-rm -t $(repo_name) .
#
#run: build
#	docker run --rm $(repo_name)
#
#shell: build
#	docker run -it --rm $(repo_name) bash
#
#clean:
#	docker rmi $(repo_name)
