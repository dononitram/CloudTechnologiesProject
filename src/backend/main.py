import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4  # For generating unique hashes
from model.model import Model
from schemas.model_data import ModelData

app = FastAPI()

# A dictionary to store trained models with their hashes
models = {}

@app.get("/healthcheck")
async def healthcheck():
    """
    An asynchronous function that performs a health check.
    Returns:
        JSONResponse: A JSON response indicating the status of the service.
    """
    return JSONResponse(content={"status": "ok"}, status_code=200)

@app.post("/train")
async def receive_params(modeldata: ModelData):
    """
    Receive model parameters, train the model, and generate a hash to identify it.
    Args:
        modeldata (ModelData): The data required to train the model.
    Returns:
        JSONResponse: Contains the status of the operation and the generated model hash.
    """
    try:
        # Create and train the model
        model = Model(modeldata)
        model.train()

        # Generate a unique hash for the model
        model_hash = str(uuid4())
        models[model_hash] = model

        # Return the model hash
        return JSONResponse(
            content={"status": "ok", "message": "Model training successful.", "model_hash": model_hash},
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.get("/predict")
async def predict(input: str, model_hash: str):
    """
    Make a prediction using the specified model.
    Args:
        input (str): The input string to be used for prediction.
        model_hash (str): The unique identifier for the model.
    Returns:
        JSONResponse: Contains the prediction result or an error message.
    """
    try:
        # Retrieve the model by hash
        if model_hash not in models:
            raise HTTPException(status_code=404, detail="Model not found. Train a model first.")

        model = models[model_hash]
        output = model.predict(input)
        prediction = ",".join([str(x) for x in output])

        return JSONResponse(content={"status": "ok", "prediction": prediction}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
