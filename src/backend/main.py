from Model import Model
from ModelData import ModelData

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import traceback
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
        print(f"Received model data: {modeldata}")
        model = Model(modeldata)
        
        # generate hash
        model_hash = model.generate_model_hash()
        
        print(f"Training model with hash: {model_hash}")
        model.train()
        
        # save the model in the dict using hash
        models[model_hash] = model
        print("Model training successful.")
        
        return JSONResponse(
            content={"status": "ok", "model_hash": model_hash, "message": "Model training successful."},
            status_code=200
        )
    except ValueError as e:
        print(f"ValueError: {e}")
        return JSONResponse(content={"status": "error", "message": f"ValueError: {str(e)}"}, status_code=400)
    except Exception as e:
        print("An error occurred during model training:")
        print(traceback.format_exc())
        return JSONResponse(content={"status": "error", "message": f"An unexpected error occurred: {str(e)}"}, status_code=500)


@app.get("/predict")
async def predict(input: str, model_hash: str):
    try:
        # check if the model with the following hash exists
        if model_hash not in models:
            return JSONResponse(content={"status": "error", "message": "Model not found."}, status_code=404)
        
        # getting model with the following hash
        model = models[model_hash]
        output = model.predict(input.replace(",", "."))
        output = output.tolist()[0]
        
        prediction = ",".join([str(x) for x in output])
        return JSONResponse(content={"status": "ok", "prediction": prediction}, status_code=200)
    except Exception as e:
        print("An error occurred during prediction:")
        print(traceback.format_exc())
        return JSONResponse(content={"status": "error", "message": f"An unexpected error occurred: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)