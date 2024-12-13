import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.exceptions import NotFittedError

class Model:
    
    def __init__(self, modeldata):
        self.model = LinearRegression()
        self.X, self.Y = [], []
        self.cells = modeldata.cells
        self.set_XY()
    
    def set_XY(self):
        i = 0
        row = []
        while i < len(self.cells) - 1:
            row.append(float(self.cells[i].value.replace(",", ".")))
            
            if self.cells[i].row != self.cells[i+1].row:
                if self.cells[i].row % 2 == 0:
                    self.X.append(row)
                    row = []
                else:
                    self.Y.append(row)
                    row = []
                    
            i = i + 1
        
        row.append(float(self.cells[i].value.replace(",", ".")))
        self.Y.append(row)
        
        print(self.X)
        print(self.Y)
        
        self.X = np.array(self.X)
        self.Y = np.array(self.Y)
    
    def train(self):

        if len(self.X) == 0 or len(self.Y) == 0:
            raise ValueError("X or Y is empty. Ensure data is properly populated.")
        
        if len(self.X) != len(self.Y):
            raise ValueError("Input and output matrix sizes do not match.")

        # Fit the model
        self.model.fit(self.X, self.Y)
        return self.model

    def predict(self, input: np.ndarray):

        try:
            parsed_input = np.array([float(i) for i in [x.replace(",",".") for x in input.split(",")]]).reshape(1, -1)
            return self.model.predict(parsed_input)
        except NotFittedError:
            raise ValueError("Model is not trained yet. Call the `train` method first.")