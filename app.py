from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import util  # Assuming util is a module you've created
from pydantic import BaseModel
app = FastAPI()

class Item(BaseModel):
    location: str 
    total_sqft: int
    bhk: int
    bath: int
    
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get('/get_location_names')
async def get_location_names():
    locations = util.get_location_names()
    return JSONResponse(content={"locations": locations})


@app.post('/predict_home_price')
async def predict_home_price(item: Item):
    return {"estimated_price": util.get_estimated_price(item.location, item.total_sqft, item.bhk, item.bath)}

@app.post('/price_vs_sqft')
async def price_vs_sqft(location: str):
    data = util.get_price_vs_sqft_data(location)  # You'll need to implement this function
    return data

if __name__ == "__main__":
    print("Starting Python FastAPI Server For Home Price Prediction...")
    uvicorn.run(app, host="0.0.0.0", port=8000)