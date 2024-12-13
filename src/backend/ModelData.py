from CellData import CellData

from pydantic import BaseModel
from typing import List

class ModelData(BaseModel):
    cells: List[CellData]