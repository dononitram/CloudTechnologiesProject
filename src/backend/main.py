import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from Model import Model
from ModelData import ModelData

app = FastAPI()

# A dictionary to store the trained model
models = {}

@app.get("/healthcheck")
async def healthcheck():
    """
    An asynchronous function that performs a health check.
    This function returns a JSON response indicating the status of the service.

    Returns:
        JSONResponse: A JSON response with a status message and HTTP status code 200.
    """
    
    return JSONResponse(content={"status": "ok"}, status_code=200)

@app.post("/train")
async def receive_params(modeldata: ModelData):
    """
    Receive model parameters, train the model, and store it.

    Args:
        modeldata (ModelData): The data required to train the model.
    Returns:
        JSONResponse: A JSON response indicating the status of the operation.
            - If successful, returns a status of "ok" and a message "Model training successful."
            - If an error occurs, returns a status of "error" and the error message.
    """

    try:
        model = Model(modeldata)
        model.train()
        models["model"] = model
        return JSONResponse(content={"status": "ok", "message": "Model training successful."}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)


@app.get("/predict")
async def predict(input: str = None):
    if not input:
        return JSONResponse(
            content={"status": "error", "message": "'input' parameter is missing or empty"},
            status_code=422,
        )

    try:
        print(f"Received input: {input}")  # Debugging
        if "model" not in models:
            return JSONResponse(
                content={"status": "error", "message": "Model is not trained. Please train the model first."},
                status_code=500,
            )
        output = models["model"].predict(input)
        prediction = ",".join([str(x) for x in output])
        return JSONResponse(content={"status": "ok", "prediction": prediction}, status_code=200)
    except Exception as e:
        print(f"Error during prediction: {e}")  # Debugging
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)