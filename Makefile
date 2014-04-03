test:
	coverage run --source dropboxfs -m py.test \
    && echo \
    && coverage report

verify:
	pyflakes -x W dropboxfs.py
	pep8 --exclude=migrations --ignore=E501,E225 dropboxfs.py

install:
	python setup.py install

dev_install:
	pip install coverage pytest six fs dropbox

publish:
	python setup.py register
	python setup.py sdist upload
