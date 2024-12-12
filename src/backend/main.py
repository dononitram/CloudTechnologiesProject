from fastapi import FastAPI
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from typing import List

class CellData(BaseModel):
    row: int
    col: int
    value: str

class Item(BaseModel):
    cells: List[CellData]

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck():
    """
    Healthcheck endpoint to verify server status.
    Returns a simple JSON response indicating the server is running.
    """
    return JSONResponse(content={"status": "ok"}, status_code=200)

@app.post("/receive_params")
async def receive_params(item: Item):
    # Print the received parameters
    for cell in item.cells:
        print(f"Received cell at row {cell.row}, col {cell.col}, with value {cell.value}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)