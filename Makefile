test: dependencies test-dependencies
	pytest -v

test-integrated: test-dependencies
	pytest -v --integrated

install:
	python setup.py install

wheel:
	python setup.py bdist_wheel

dependencies:
	pip install -r requirements.txt -q

test-dependencies:
	pip install -q pytest pytest-asyncio

docker:
	docker build -t sitemon .

compose:
	docker-compose up -d

.PHONY: test test-integrated dependencies test-dependencies