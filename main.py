from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from managers.userManger import Users
from serverssocket.wsocket import router as ws_socket

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

list = []
user = Users()

@app.get("/health", status_code=200)
def health():
    return {"Status": "Good"}

app.include_router(ws_socket, tags=["ws"])
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
