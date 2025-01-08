import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from model.model import Model
from schemas.model_data import ModelData
from uuid import uuid4  # For generating unique hashes

app = FastAPI()

# Hashtable to store models with their hashes
model_table = {}

@app.post("/train")
async def train_model(modeldata: ModelData):
    """
    Train a model and generate a hash to identify it.
    """
    try:
        # Create and train a model
        model = Model(modeldata)
        model.train()

        # Generate a unique hash for the model
        model_hash = str(uuid4())
        model_table[model_hash] = model

        # Return the hash to the client
        return JSONResponse(
            content={"status": "ok", "model_hash": model_hash},
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500,
        )

@app.get("/predict")
async def predict(input: str, model_hash: str):
    """
    Use a hash to retrieve a model and make a prediction.
    """
    try:
        # Retrieve the model by hash
        if model_hash not in model_table:
            raise HTTPException(status_code=404, detail="Model not found. Train a model first.")

        model = model_table[model_hash]
        output = model.predict(input)
        prediction = ",".join([str(x) for x in output])

        return JSONResponse(
            content={"status": "ok", "prediction": prediction},
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500,
        )
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)