import uvicorn

from app.presentation.startup import get_app

app = get_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8800)
