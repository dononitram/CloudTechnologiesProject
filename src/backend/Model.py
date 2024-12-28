import numpy as np

from sklearn.linear_model import LinearRegression

class Model:
    
    def __init__(self, modeldata):
        """
        Initializes the Model class with the provided model data.
        Args:
            modeldata (ModelData): An instance of ModelData containing the cells attribute.
        Attributes:
            model (LinearRegression): An instance of the LinearRegression model.
            X (list): A list to store feature data.
            Y (list): A list to store target data.
            cells (list): A list of cells from the provided model data.
        Methods:
            set_XY: Sets the feature (X) and target (Y) data.
        """

        self.model = LinearRegression()
        self.X, self.Y = [], []
        self.cells = modeldata.cells
        self.set_XY()
    
    def set_XY(self):
        """
        Processes the cell values and organizes them into two separate lists, X and Y, 
        based on the row number of each cell. Cells in even-numbered rows are added to 
        the X list, while cells in odd-numbered rows are added to the Y list. The values 
        are converted from strings to floats, with commas replaced by periods.
        The method performs the following steps:
        1. Iterates through the cells and appends their values to a temporary row list.
        2. When a change in row number is detected, the row list is appended to either 
           the X or Y list based on the row number's parity (even or odd).
        3. Converts the X and Y lists to numpy arrays.
        Prints the X and Y lists before converting them to numpy arrays.
        Attributes:
            cells (list): A list of cell objects, each containing a value and a row attribute.
            X (list): A list to store rows of cell values from even-numbered rows.
            Y (list): A list to store rows of cell values from odd-numbered rows.
        """

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
        
        print("X: ", self.X)
        print("Y: ", self.Y)
        
        self.X = np.array(self.X)
        self.Y = np.array(self.Y)
    
    def train(self):
        """
        Trains the model using the provided input (X) and output (Y) data.
        Raises:
            ValueError: If X or Y is empty.
            ValueError: If the lengths of X and Y do not match.
        Returns:
            The trained model.
        """

        if len(self.X) == 0 or len(self.Y) == 0:
            raise ValueError("X or Y is empty. Ensure data is properly populated.")
        
        if len(self.X) != len(self.Y):
            raise ValueError("Input and output matrix sizes do not match.")

        # Fit the model
        self.model.fit(self.X, self.Y)
        return self.model

    def predict(self, input: np.ndarray):
        """
        Predict the output based on the given input.
        Args:
            input (np.ndarray): A numpy array containing the input data.
        Returns:
            list: The prediction result as a list.
        """

        parsed_input = [x.replace(",",".") for x in input.split("%")] # Split by delimiter and replace commas with periods just in case
        parsed_input = [float(i) for i in parsed_input] # Convert to floats
        parsed_input = np.array(parsed_input).reshape(1, -1) # Reshape to 2D array

        prediction = self.model.predict(parsed_input) # Make prediction
        prediction = prediction.tolist()[0] # Convert to list

        return prediction