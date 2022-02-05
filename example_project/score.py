import numpy as np
from sklearn.linear_model import LinearRegression
from dotenv import load_dotenv

load_dotenv()

def init():
    global model
    X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
    y = np.dot(X, np.array([1, 2])) + 3
    model = LinearRegression().fit(X,y)    
    
def run(data):
    return {"result": model.predict(np.array(data.get("data"))).tolist()}

