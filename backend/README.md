### backend

1. `python -m venv .venv`
2. `source .venv/Scripts/activate`
3. `pip install -r requirements.txt`
4. `pre-commit install`, this will run a pre-commit hook when u commit
5. `cd src`
6. `flask run`
7. Access flask api at `localhost:5000`

- poetry guide: https://python-poetry.org/docs/basic-usage/
- flask guide: https://flask.palletsprojects.com/en/2.3.x/quickstart/#a-minimal-application
- for all environment variables, please create in a `.env` file, the `docker-compose.yml` uses it
