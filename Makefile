install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

format:
	black *.py

lint:
	pylint --disable=R,C --ignore-patterns=test_.*?py *.py

test:
	python -m pytest --cov=main test_main.py

generate:
	# Assuming the script generates a report or markdown file
	python main.py

generate_and_push: generate
	# Add, commit, and push the generated file
	git add *.md
	git commit -m "Auto-generated markdown file"
	git push origin main

all: install format lint test