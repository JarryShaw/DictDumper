coverage:
	pipenv run coverage run tests/test.py
	pipenv run coverage html
	open htmlcov/index.html
	read
	rm -rf htmlcov
	rm .coverage
