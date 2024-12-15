from CellData import CellData
import hashlib
from pydantic import BaseModel
from typing import List

class ModelData(BaseModel):
    cells: List[CellData]
    def generate_model_hash(self) -> str:
        """
        Generates a unique haseh based on the data from the cells
        """
        # row to generate the hash itself
        concatenated_data = "".join(
            f"{cell.row}-{cell.col}-{cell.value}" for cell in self.cells
        )
      
        hash_object = hashlib.sha256(concatenated_data.encode())
        return hash_object.hexdigest()