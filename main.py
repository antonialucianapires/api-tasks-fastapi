from fastapi import FastAPI
from task_router import router

app = FastAPI(
    title="Tasks API",
    version="0.0.1",
    description="API to manage tasks")

app.include_router(router, tags=["tasks"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
