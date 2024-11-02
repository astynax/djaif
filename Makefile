MANAGE := uv run python manage.py

run:
	$(MANAGE) runserver

repl:
	$(MANAGE) shell_plus
