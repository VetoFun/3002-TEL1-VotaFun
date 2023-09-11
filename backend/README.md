### backend

1. `pre-commit install`, this will run a pre-commit hook
2. `python -m venv .venv`
3. `source .venv/Scripts/activate`
4. `pip install -r requirements.txt`
5. `cd src`
6. `flask run`
7. Access flask api at `localhost:5000`

- poetry guide: https://python-poetry.org/docs/basic-usage/
- flask guide: https://flask.palletsprojects.com/en/2.3.x/quickstart/#a-minimal-application
- for all environment variables, please create in a `.env` file, the `docker-compose.yml` uses it
