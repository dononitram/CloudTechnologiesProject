from fastapi import FastAPI
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from typing import List

import numpy as np

class CellData(BaseModel):
    row: int
    col: int
    value: str

class Item(BaseModel):
    cells: List[CellData]

def checkArray(arr):
    # Check if all subarrays have the same length
    subarray_lengths = [len(subarray) for subarray in arr]
    if len(set(subarray_lengths)) == 1:
        return True
    else:
        return False

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
        
    X = []
    Y = []
        
    i = 0
    row = []
    while i < len(item.cells) - 1:
        row.append(float(item.cells[i].value))
        if item.cells[i].row != item.cells[i+1].row:
            if item.cells[i].row % 2 == 0:
                X.append(row)
                row = []
            else:
                Y.append(row)
                row = []
        i = i + 1
    
    print(np.array(X))
    print(np.array(Y))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)