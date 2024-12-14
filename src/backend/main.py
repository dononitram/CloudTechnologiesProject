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
        model.train()
        models["model"] = model
        return JSONResponse(content={"status": "ok", "message": "Model training successful."}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)


@app.get("/predict")
async def predict(input: str):
    try:
        output = models["model"].predict(input.replace(",", "."))
        output = output.tolist()[0]
        prediction = ",".join([str(x) for x in output])
        
        return JSONResponse(content={"status": "ok", "prediction": prediction}, status_code=200)
    except Exception as e:
        e.with_traceback()
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)