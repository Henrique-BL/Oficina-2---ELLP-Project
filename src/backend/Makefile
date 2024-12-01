run:
	uvicorn app:app --reload
	
create-migration:
	set "PYTHONPATH=%PYTHONPATH%;$(subst /,\,$(CURDIR))" && alembic revision --autogenerate -m "$(d)"

run-migrations:
	set "PYTHONPATH=%PYTHONPATH%;$(subst /,\,$(CURDIR))" && alembic upgrade head

test:
	set "PYTHONPATH=%PYTHONPATH%;$(subst /,\,$(CURDIR))" && pytest tests/ -v

create-db:
	set PGPASSWORD=root && "C:\Program Files\PostgreSQL\{version}\bin\psql" -U root -h localhost -c "CREATE DATABASE ellp_db;"

drop-db:
	set PGPASSWORD=root && psql -U root -h localhost -c "DROP DATABASE IF EXISTS ellp_db;"

recreate-db: drop-db create-db run-migrations