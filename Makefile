run: compile

.PHONY: compile
compile:
	./build.sh

.PHONY: venv
venv:
	source bin/activate

.PHONY: clean
clean:
	rm -r build/ && rm -r *.spec

.PHONY: clean-all
clean-all:
	rm -r dist/ && rm -r build/ && rm -r *.spec