# Makefile

# Define the default target
.PHONY: run

# Load environment variables from .env file
include .env
export $(shell sed 's/=.*//' .env)

# Target to run the Flask app
run:
	@echo "Starting Flask app..."
	flask run

# Target to install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Target to setup the environment (e.g., creating virtual environment)
setup:
	@echo "Setting up the environment..."
	python -m venv my_env
	. my_env/bin/activate
	make install

# Target to clean up (e.g., remove __pycache__ directories)
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -r {} +
