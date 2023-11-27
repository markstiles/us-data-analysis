import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import flask
import pandas as pd

from flask import Flask
from flask import render_template
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

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
props = ['Population','Median_Age','Average_Income','Percent_High_School','Percent_Bachelors','Housing_Units_Total',
    'Housing_Units_Single_Family','Percent_In_Poverty','Food_Services_Employers','Waste_Management_Employers',
    'Arts_Employers','Education_Employers','Finance_Employers','Healthcare_Employers','Information_Employers',
    'Technical_Employers','Real_Estate_Employers','Retail_Employers',
    'Transportation_Employers','Utilities_Employers']
drop_final_cols = ['Place_Name', 'GeoId', 'All_Revenue', 'State_Abbr']
drop_cols = [
    'State_Name','Type','All_Employers','All_Employees','All_Payroll',
    'Agriculture_Employers','Agriculture_Employees','Agriculture_Payroll','Agriculture_Revenue',
    'Construction_Employers','Construction_Employees','Construction_Payroll','Construction_Revenue',
    'Finance_Revenue','Information_Revenue','Management_Employers','Management_Employees','Management_Payroll','Management_Revenue',
    'Manufacturing_Employers','Manufacturing_Employees','Manufacturing_Payroll','Manufacturing_Revenue',
    'Mining_Employers','Mining_Employees','Mining_Payroll','Mining_Revenue','Utilities_Revenue',
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
    'Income_Per_Revenue','Revenue_Per_Person','Profit_Per_Person','Population_Range', 'Performance']

@app.route("/")
def home():
    return render_template(
        "home.html",
        date=datetime.now()
    )

@app.route("/location/<placename>", methods=["GET"])
def location(placename):
    places = places_df[places_df.Place_Name.str.contains(placename, na=False, case=False)][['Place_Name', 'State_Abbr', 'GeoId', 'All_Revenue']]
    data = {"places": places.to_json(orient="records")}
    return flask.jsonify(data)

@app.route("/geolocation/<geoid>", methods=["GET"])
def geolocation(geoid):
    places = places_df[places_df.GeoId==int(geoid)][props]
    data = {"place": places.to_json(orient="records")}
    return flask.jsonify(data)

@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary
    data = {"success": False}

    if flask.request.method == "POST":
        #lookup values
        place = places_df[places_df.GeoId==int(flask.request.form.get("geoid"))].iloc[0]
        actual = place.All_Revenue
        data["name"] = place.Place_Name
        
        # update values
        place.Population = flask.request.form.get("population")
        place.Median_Age = flask.request.form.get("medianage")
        place.Average_Income = flask.request.form.get("avgincome")
        place.Percent_High_School = flask.request.form.get("perhighschool")
        place.Percent_Bachelors = flask.request.form.get("perbach")
        place.Housing_Units_Total = flask.request.form.get("housingtotal")
        place.Housing_Units_Single_Family = flask.request.form.get("housingsingle")
        place.Percent_In_Poverty = flask.request.form.get("perpoverty")
        place.Food_Services_Employers = flask.request.form.get("foodemp")
        place.Waste_Management_Employers = flask.request.form.get("wasteemp")
        place.Arts_Employers = flask.request.form.get("artsemp")
        place.Education_Employers = flask.request.form.get("edemp")
        place.Finance_Employers = flask.request.form.get("finemp")
        place.Healthcare_Employers = flask.request.form.get("healthemp")
        place.Information_Employers = flask.request.form.get("infoemp")
        place.Technical_Employers = flask.request.form.get("techemp")
        place.Real_Estate_Employers = flask.request.form.get("reemp")
        place.Retail_Employers = flask.request.form.get("retailemp")
        place.Transportation_Employers = flask.request.form.get("transemp")
        place.Utilities_Employers = flask.request.form.get("utilityemp")

        # scale and predict
        place_scaled = scaler.transform(prep_series(place))
        prediction = model(torch.tensor(place_scaled, dtype=torch.float32)).item()
        
        # return data
        data["actual"] = f'{int(actual):,}'
        data["prediction"] = f'{int(prediction):,}'
        diff = int(prediction-actual)
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
    places_df = pd.read_csv('../places_data.csv')
    places_df.drop(places_df.columns[[0]], axis=1, inplace=True)
    places_df = places_df.fillna(0)
    state_dummies = pd.get_dummies(places_df.State_Name)
    places_df = pd.concat([places_df, state_dummies.set_axis(places_df.index)], axis=1)
    places_df.drop(columns=drop_cols, inplace=True)
    places_df = places_df[places_df.All_Revenue < 20000000]

def load_scaler():
    global scaler
    scaler = MinMaxScaler()
    x = prep_df(places_df)
    scaler.fit(x)

def prep_df(df):
    new_df = df.drop(columns=drop_final_cols)
    return new_df

def prep_series(series):
    new_series = series.drop(labels=drop_final_cols).values.reshape(1,-1)
    return new_series

if __name__ == "app":
    load_model()
    load_places()
    load_scaler()
    #app.run()
    app.run(debug=True)