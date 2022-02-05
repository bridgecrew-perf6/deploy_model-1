import requests
import numpy as np

host = "http://localhost:5000"

data={"data": np.array([[1, 1], [1, 2], [2, 2], [2, 3]]).tolist()}

print(requests.post(host, json=data).json())