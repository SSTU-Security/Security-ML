from fastapi import Request, FastAPI
import uvicorn
from cloudweb.camera import Camera

app = FastAPI()


@app.post("/giveSocket")
async def giveSocket():
    return {"ip": "127.0.0.1", "port": 8082}


@app.post("/update")
async def update(request: Request):
    data = await request.json()
    d.setServer(data['ip'], data['port'])
    return {"error": "ok"}


@app.post("/setCamera")
async def setCamera(request: Request):
    try:
        data = await request.json()
        d.setCamera(data['ip'], data['port'])
    except Exception as e:
        return {"error": str(e)}
    return {"error": "ok"}


if __name__ == '__main__':
    d = Camera()
    d.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
