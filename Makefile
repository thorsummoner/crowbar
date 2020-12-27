%.html: %.md; python3 -m markdown < $^ > $@
readme.html:

.PHONY: dist

PYTHON_BIN?=python3
sdist:
	$(PYTHON_BIN) setup.py sdist

