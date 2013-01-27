HERE = $(shell pwd)
BIN = $(HERE)/bin
PYTHON = $(BIN)/python

PIP_DOWNLOAD_CACHE ?= $(HERE)/.pip_cache
INSTALL = $(BIN)/pip install
INSTALL += --download-cache $(PIP_DOWNLOAD_CACHE) -U --use-mirrors

BUILD_DIRS = bin build include lib lib64 man share .Python .pip_cache

.PHONY: all build clean test

all: build

$(PYTHON):
	virtualenv --distribute .

build: $(PYTHON)
	$(INSTALL) -r requirements.txt
	$(PYTHON) setup.py develop

clean:
	rm -rf $(BUILD_DIRS)

test:
	$(BIN)/nosetests -d --with-coverage

html:
	cd docs && \
	make html
