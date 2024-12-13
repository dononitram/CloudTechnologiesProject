from pydantic import BaseModel

class CellData(BaseModel):
    row: int
    col: int
    value: str