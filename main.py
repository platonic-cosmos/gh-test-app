from fastapi import FastAPI
import uvicorn
from google.cloud import spanner
from fastapi.responses import HTMLResponse
import json
import google.cloud.logging
import logging

app = FastAPI()
instance_id="appdb"
database_id="ghtest"
database_id=database_id.lower()
client = google.cloud.logging.Client()
client.setup_logging()

@app.get("/hc/")
def healthcheck():
    logging.info("Called /hc endpoint.")
    return {"message": "Health - OK"}

@app.get("/tasks/")
def get_db_data():
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)
    logging.info("Called /tasks endpoint.")
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT id, title, status FROM tasks"
        )
    logging.info("SELECT id, title, status FROM tasks")
    return results.to_dict_list();

@app.get("/")
async def root():
    logging.info("Called / endpoint.")
    return {"message": "Hello from gh-test API"}

@app.get("/logwarning")
def log_warning():
    logging.warning("Test log warning message.")
    return {"message": "Test log warning message."}

@app.get("/logerror")
def log_error():
    logging.error("Test log error message.")
    return {"message": "Test log error message."}

@app.get("/logdebug")
def log_debug():
    logging.debug("Test log debug message.")
    return {"message": "Test log debug message."}

if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=8080, log_level="info")
    server = uvicorn.Server(config)
    logging.info("Application initialized.")
    server.run()
