# ML House Price Prediction
This project is about building a ML model to predict prices of houses in Warsaw.

The aim is to build a model with maximized performance, using PyTorch. Hyperparameters are to be defined during the research.

### Dataset
The dataset can be found in `datasets/warsaw_houses.csv` file. This is a dataset created by scrapping a website with house rental offers. There are just 4 columns:

- district (categorical)
- rooms (number)
- square_meters (number)
- price (to be predicted)

# API

There is a FastAPI app with a source code in `api.py` file. 
To run it create a virtual environment and install dependencies from requirements.txt file.

Then run the app with:
```
uvicorn api:app --reload
```

You should see API docs in your browser under `http://127.0.0.1:8000/docs`.

