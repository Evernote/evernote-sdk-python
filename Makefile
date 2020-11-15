SOURCE_DIR?=evernote

.PHONY: docs
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


# ================== below commands are not verified ==================

# test:
#	# This runs all of the tests, on both Python 2 and Python 3.
#	detox
ci:
	pytest tests --junitxml=report.xml

test-readme:
	python setup.py check --restructuredtext --strict && ([ $$? -eq 0 ] && echo "README.rst and HISTORY.rst ok") || echo "Invalid markup in README.rst or HISTORY.rst!"

publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg $(SOURCE_DIR).egg-info

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"
