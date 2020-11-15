SOURCE_DIR?=evernote2

# .PHONY: docs

init:
	pip install -e .
	pip install -r requirements-dev.txt

test:
	# quick test of local code and show test coverage
	pytest --cov-config .coveragerc --verbose --cov-report \
		term-missing:skip-covered --cov-report xml \
		--capture=no -p no:cacheprovider \
		--cov-fail-under 1 \
		--cov=$(SOURCE_DIR) tests

flake8:
	flake8 $(SOURCE_DIR)

# test:
#	# This runs all of the tests, on both Python 2 and Python 3.
#	detox

ci:
	pytest tests --junitxml=report.xml

publish:
	# remove old versions first
	rm -fr build dist .egg $(SOURCE_DIR).egg-info
	pip install 'twine>=3.2.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg $(SOURCE_DIR).egg-info
