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
async def predict(input: str):
    """
    Asynchronously predicts the output based on the given input string.

    Args:
        input (str): The input string to be used for prediction.
    Returns:
        JSONResponse: A JSON response containing the prediction result with a status code of 200 if successful,
                      or an error message with a status code of 500 if an exception occurs.
    Raises:
        Exception: If an error occurs during the prediction process.
    """
    
    try:
        output = models["model"].predict(input)
        prediction = ",".join([str(x) for x in output])
        
        return JSONResponse(content={"status": "ok", "prediction": prediction}, status_code=200)
    except Exception as e:
        e.with_traceback()
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)