import json
import numpy as np
import pickle

# Load the model and data columns once when the module is imported
with open("columns.json", "r") as f:
    data_columns = json.load(f)['data_columns']
    locations = data_columns[3:]  # first 3 columns are sqft, bath, bhk

with open('banglore_home_prices_model.pickle', 'rb') as f:
    model = pickle.load(f)

def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    price_in_lakhs = model.predict([x])[0]
    price_in_dollars = round(price_in_lakhs * 100000 / 83.0)
    return f'{price_in_dollars:,} Dollars'

def get_price_vs_sqft_data(location):
    try:
        loc_index = data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    sqft_range = np.arange(600, 5000, 100)
    prices = []

    for sqft in sqft_range:
        x = np.zeros(len(data_columns))
        x[0] = sqft
        x[1] = max(1, round(sqft / 500))  # Ensure no division by zero
        x[2] = max(1, round(sqft / 500))
        if loc_index >= 0:
            x[loc_index] = 1
        price_in_lakhs = model.predict([x])[0]
        prices.append(price_in_lakhs * 100000 / 83.0)

    return prices

def get_location_names():
    return locations

def get_data_columns():
    return data_columns

if __name__ == '__main__':
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
