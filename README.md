# ripio faucet challenge


the api is located on `/api/airdrops/` or (http://localhost:8080/api/airdrops/ if running locally)

the django admin is located on `/admin/` or (http://localhost:8080/admin/ if running locally)

.env file should look like:
```
DJANGO_SECRET_KEY=
ETH_SECRET_KEY= wallet private key
ETH_RPC_URL= http rpc url
DATABASE_URL= optional postgres url, or using default sqlite
CELERY_BROKER_URL= redis url for celery tasks
```

for running locally:

 - `poetry install`
 - `poetry run ./manage.py migrate`
 - `poetry run ./manage.py createsuperuser`
 - `poetry run ./manage.py runserver 8080`

this project needs configuration on the "Wallet" object before the api can be used. use http://localhost:8080/admin/faucet/wallet/ for configure it

for running celery locally:
- `poetry run python -m celery -A config worker`

this repository is using ruff for formatting/precommit:

https://github.com/astral-sh/ruff
