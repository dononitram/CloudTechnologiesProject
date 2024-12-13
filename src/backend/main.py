from Model import Model
from ModelData import ModelData

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

models = {}

@app.get("/healthcheck")
async def healthcheck():
    """
    Healthcheck endpoint to verify server status.
    Returns a simple JSON response indicating the server is running.
    """
    return JSONResponse(content={"status": "ok"}, status_code=200)

@app.post("/train")
async def receive_params(modeldata: ModelData):
    try:
        model = Model(modeldata)
        print(model.get_XY())
        model.train()
        
        return JSONResponse(content={"status": "ok", "message": "Model training successful.", "model": "model"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)


@app.get("/predict")
async def predict(inputs: str, model: str):
    try:
        predictions = models[model].predict(inputs)
        return JSONResponse(content={"status": "ok", "predictions": predictions.tolist()}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)