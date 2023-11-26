import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import flask
import pandas as pd

from flask import Flask
from torchinfo import summary
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

model = nn.Sequential(
    nn.Linear(174, 2048),
    nn.ReLU(),
    nn.Linear(2048, 1024),
    nn.ReLU(),
    nn.Linear(1024, 2048),
    nn.ReLU(),
    nn.Linear(2048, 512),
    nn.ReLU(),
    nn.Linear(512, 1)
)
places_df = None
scaler = None

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/test", methods=["GET"])
def test():
    data = {"success": False}
    return flask.jsonify(data)

@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary
    data = {"success": False}

    if flask.request.method == "POST":
        
        place = places_df[places_df.GeoId==2572600]
        actual = place.iloc[0].All_Revenue
        place_scaled = scaler.transform(place.drop(columns=['Place_Name', 'GeoId', 'All_Revenue']))
        print("scaled values")
        print(place_scaled)
        prediction = model(torch.tensor(place_scaled, dtype=torch.float32)).item()
        
        data["model"] = f'{type(model)}'
        data["name"] = place.iloc[0].Place_Name
        data["actual"] = f'{int(actual):,}'
        data["prediction"] = f'{prediction:,}'
        diff = int(abs(prediction-actual))
        percent_diff = int((diff/actual)*100)
        data["difference"] = f'{percent_diff:,}'

        data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data)

def load_model():
    global model
    model.load_state_dict(torch.load("../places_model.pt"))
    model.eval()

def load_places():
    global places_df
    places_df = pd.read_csv('https://raw.githubusercontent.com/markstiles/us-data-analysis/main/places_data.csv')
    places_df.drop(places_df.columns[[0]], axis=1, inplace=True)
    places_df = places_df.fillna(0)
    state_dummies = pd.get_dummies(places_df.State_Name)
    places_df = pd.concat([places_df, state_dummies.set_axis(places_df.index)], axis=1)
    drop_cols = [
        'State_Abbr', 'State_Name', 'Type', 'All_Employers', 'All_Employees', 'All_Payroll',
        'Agriculture_Employers','Agriculture_Employees','Agriculture_Payroll','Agriculture_Revenue',
        'Construction_Employers','Construction_Employees','Construction_Payroll','Construction_Revenue',
        'Finance_Revenue',
        'Information_Revenue',
        'Management_Employers','Management_Employees','Management_Payroll','Management_Revenue',
        'Manufacturing_Employers','Manufacturing_Employees','Manufacturing_Payroll','Manufacturing_Revenue',
        'Mining_Employers','Mining_Employees','Mining_Payroll','Mining_Revenue',
        'Utilities_Revenue',
        'Wholesale_Employers','Wholesale_Employees','Wholesale_Payroll','Wholesale_Revenue',
        'Consumer_Total_Expense','Consumer_Expense_Alcohol','Consumer_Expense_Alcohol_Home','Consumer_Expense_Beer_Bar','Consumer_Expense_Wine_Bar','Consumer_Expense_Clothes','Consumer_Expense_Mens_Clothes',
        'Consumer_Expense_Womens_Clothes','Consumer_Expense_Childrens_Clothes','Consumer_Expense_Boys_Clothes','Consumer_Expense_Girls_Clothes','Consumer_Expense_Footwear','Consumer_Expense_Dining',
        'Consumer_Expense_Dining_Breakfast','Consumer_Expense_Dining_Lunch','Consumer_Expense_Dining_Dinner','Consumer_Expense_Education','Consumer_Expense_Entertainment','Consumer_Expense_Clubs',
        'Consumer_Expense_Dating','Consumer_Expense_Pet_Food','Consumer_Expense_Pet_Services','Consumer_Expense_Food_Home','Consumer_Expense_Bakery_Home','Consumer_Expense_Dairy_Home','Consumer_Expense_Fruits_Home',
        'Consumer_Expense_Meat_Home','Consumer_Expense_Nonalcohol_Home','Consumer_Expense_Snacks_Home','Consumer_Expense_Healthcare','Consumer_Expense_Mentalcare','Consumer_Expense_Drugcar','Consumer_Expense_House_Services',
        'Consumer_Expense_Eldercare','Consumer_Expense_Landscape','Consumer_Expense_Housekeeping','Consumer_Expense_PC','Consumer_Expense_Housing','Consumer_Expense_Home_Improvements','Consumer_Expense_Energy',
        'Consumer_Expense_Phone','Consumer_Expense_Water','Consumer_Expense_Insurance','Consumer_Expense_Pensions','Consumer_Expense_Personalcare','Consumer_Expense_Haircare','Consumer_Expense_Personalcare_Products',
        'Consumer_Expense_Transport','Consumer_Expense_Gas','Consumer_Expense_Vehicle_Repair','Consumer_Expense_Travel','Consumer_Expense_Airfare','Consumer_Expense_Auto_Rentals','Consumer_Expense_Travel_Lodging',
        'Consumer_Expense_Travel_Meals','Consumer_Expense_Travel_Entertainment',
        'All_Employee_Per_Employer','All_Revenue_Per_Employer','All_Avg_Payroll_Per_Employee','All_Population_Per_Employer',
        'Food_Services_Employee_Per_Employer','Food_Services_Revenue_Per_Employer','Food_Services_Avg_Payroll_Per_Employee','Food_Services_Population_Per_Employer','Waste_Management_Employee_Per_Employer',
        'Waste_Management_Revenue_Per_Employer','Waste_Management_Avg_Payroll_Per_Employee','Waste_Management_Population_Per_Employer','Agriculture_Employee_Per_Employer','Agriculture_Revenue_Per_Employer',
        'Agriculture_Avg_Payroll_Per_Employee','Agriculture_Population_Per_Employer','Arts_Employee_Per_Employer','Arts_Revenue_Per_Employer','Arts_Avg_Payroll_Per_Employee','Arts_Population_Per_Employer',
        'Construction_Employee_Per_Employer','Construction_Revenue_Per_Employer','Construction_Avg_Payroll_Per_Employee','Construction_Population_Per_Employer','Education_Employee_Per_Employer',
        'Education_Revenue_Per_Employer','Education_Avg_Payroll_Per_Employee','Education_Population_Per_Employer','Finance_Employee_Per_Employer','Finance_Revenue_Per_Employer','Finance_Avg_Payroll_Per_Employee',
        'Finance_Population_Per_Employer','Healthcare_Employee_Per_Employer','Healthcare_Revenue_Per_Employer','Healthcare_Avg_Payroll_Per_Employee','Healthcare_Population_Per_Employer','Information_Employee_Per_Employer',
        'Information_Revenue_Per_Employer','Information_Avg_Payroll_Per_Employee','Information_Population_Per_Employer','Management_Employee_Per_Employer','Management_Revenue_Per_Employer','Management_Avg_Payroll_Per_Employee',
        'Management_Population_Per_Employer','Manufacturing_Employee_Per_Employer','Manufacturing_Revenue_Per_Employer','Manufacturing_Avg_Payroll_Per_Employee','Manufacturing_Population_Per_Employer','Mining_Employee_Per_Employer',
        'Mining_Revenue_Per_Employer','Mining_Avg_Payroll_Per_Employee','Mining_Population_Per_Employer','Other_Employee_Per_Employer','Other_Revenue_Per_Employer','Other_Avg_Payroll_Per_Employee','Other_Population_Per_Employer',
        'Technical_Employee_Per_Employer','Technical_Revenue_Per_Employer','Technical_Avg_Payroll_Per_Employee','Technical_Population_Per_Employer','Real_Estate_Employee_Per_Employer','Real_Estate_Revenue_Per_Employer',
        'Real_Estate_Avg_Payroll_Per_Employee','Real_Estate_Population_Per_Employer','Retail_Employee_Per_Employer','Retail_Revenue_Per_Employer','Retail_Avg_Payroll_Per_Employee','Retail_Population_Per_Employer',
        'Transportation_Employee_Per_Employer','Transportation_Revenue_Per_Employer','Transportation_Avg_Payroll_Per_Employee','Transportation_Population_Per_Employer','Utilities_Employee_Per_Employer','Utilities_Revenue_Per_Employer',
        'Utilities_Avg_Payroll_Per_Employee','Utilities_Population_Per_Employer','Wholesale_Employee_Per_Employer','Wholesale_Revenue_Per_Employer','Wholesale_Avg_Payroll_Per_Employee','Wholesale_Population_Per_Employer',
        'Income_Per_Revenue',
        'Revenue_Per_Person','Profit_Per_Person',
        'Population_Range', 'Performance'
        ]
    places_df.drop(columns=drop_cols, inplace=True)
    places_df = places_df[places_df.All_Revenue < 20000000]

def load_scaler():
    global scaler
    scaler = MinMaxScaler()
    x = prep_df(places_df)
    print(x.shape)
    scaler.fit(x)

def prep_df(df):
    new_df = df.drop(columns=['Place_Name', 'GeoId', 'All_Revenue'])
    return new_df

if __name__ == "app":
    print(("* Loading PyTorch model and Flask starting server...please wait until server has fully started"))
    load_model()
    load_places()
    load_scaler()
    #app.run()
    app.run(debug=True)