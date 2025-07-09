install:
	python -m pip install -r requirements.txt

run:
	streamlit run auth.py

build:
	docker compose build

up:
	docker volume create postgres-data-voice-poc || true; \
	docker compose up -d

down:
	docker compose down --rmi all

stop:
	docker compose stop