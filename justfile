install:
    python -m venv .venv 
    ./.venv/Scripts/pip install -r requirements.txt

uninstall:
    rm -rf ./.venv

clean:
    rm src/*.sqlite3

run:
    cd src && ../.venv/Scripts/uvicorn app:app --host 0.0.0.0 --port 8000 --reload

