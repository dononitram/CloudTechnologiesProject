from schemas.cell_data import CellData

from pydantic import BaseModel
from typing import List

class ModelData(BaseModel):
    cells: List[CellData]