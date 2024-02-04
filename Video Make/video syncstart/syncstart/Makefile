.PHONY: man test up check dist

test:
	pytest

man:
	pip install --user -e .
	stpl README.rst.stpl README.rst
	pandoc README.rst -s -t man -o syncstart.1

check:
	restview --long-description --strict

dist: man
	sudo python setup.py bdist_wheel

up:
	twine upload dist/`ls dist -rt | tail -1`


