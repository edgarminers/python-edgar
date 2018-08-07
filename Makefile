clean:
	python3 setup.py clean --all

dist:
	python3 setup.py sdist bdist_wheel

release_test: clean dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	open https://test.pypi.org/project/python-edgar

release: clean dist
	twine upload dist/*
	open https://pypi.org/project/python-edgar
