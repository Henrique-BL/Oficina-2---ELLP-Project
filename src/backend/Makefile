run:
	uvicorn app:app --reload
	
create-migration:
	set "PYTHONPATH=%PYTHONPATH%;$(subst /,\,$(CURDIR))" && alembic revision --autogenerate -m "$(d)"

run-migrations:
	set "PYTHONPATH=%PYTHONPATH%;$(subst /,\,$(CURDIR))" && alembic upgrade head

test:
	set "PYTHONPATH=%PYTHONPATH%;$(subst /,\,$(CURDIR))" && pytest tests/ -v