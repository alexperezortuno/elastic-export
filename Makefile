run: compile clean

.PHONY: compile
compile:
	pyinstaller -F --clean --noconfirm -n pylastic_report main.py

.PHONY: clean
clean:
	rm -r build/ && rm -r *.spec

.PHONY: clean-all
clean-all:
	rm -r dist/ && rm -r build/ && rm -r *.spec