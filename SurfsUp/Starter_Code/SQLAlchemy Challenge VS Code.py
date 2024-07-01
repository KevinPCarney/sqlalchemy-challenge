# Import the dependencies.

import pandas as pd
import numpy as np
import datetime

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, func

# 1 import flask
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# define properties
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

Base.prepare(autoload_with=engine)

# Base = automap_base() - reference previous code

# Use the Base class to reflect the database tables

# Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)


# 2 create an app
app = Flask(__name__)

#################################################
# Flask Setup
#################################################


#################################################
# Flask Routes
#################################################


#4 establish home page
@app.route("/")
def home():
    return (f"The following are the potential links you can follow from this homepage - NOTE: All links are JSON files.<br/>"
            f"<br/>"
            f"/api/v1.0/precipitation - will give the data for the last 12 months of precipitation for station USC00519281.<br/>"
            f"/api/v1.0/stations - will list all the stations in the database.<br/>"
            f"/api/v1.0/tobs - will give the data for the last 12 months of temperature for station USC00519281.<br/>"
            f"/api/v1.0/temp/start - will give the variable (min, max, and average) temp data for all dates after 2016-06-01.<br/>"
            f"/api/v1.0/temp/start/end - will give the variable (min, max, and average) temp data for all dates during June 2016 for all stations.<br/>"
        )


#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#

#5 establish a route for precipitation
@app.route("/api/v1.0/precipitation")
#def precipitation():
#    print("Request received to gain access to precipitation")

def query_precipitation():
    # Query for the last 12 months of station USC00519281: 
    query = """
            SELECT
                date,
                station,
                prcp
            FROM
                measurement
            WHERE
                station = "USC00519281"
                AND date >= '2016-08-23'
            ORDER BY
                date ASC;
            """
    df = pd.read_sql(text(query), con=engine)
    data = df.to_dict(orient="records")
    return jsonify(data)

#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#


#6 establish a route for stations
@app.route("/api/v1.0/stations")

def query_station():
    # Query all stations 
    query = """
            SELECT
                station
            FROM
                measurement
            GROUP BY
                station
            ORDER BY
                station ASC;
            """
    df = pd.read_sql(text(query), con=engine)
    data = df.to_dict(orient="records")
    return jsonify(data)

#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#

          
#7 establish a route for Temperature
@app.route("/api/v1.0/tobs")

def query_tobs():
    # Query all temperature
    # print("Request received to gain access to tobs")
    query = """
            SELECT
                date,
                station,
                tobs
            FROM
                measurement
            WHERE
                station = "USC00519281"
                AND date >= '2016-08-23'
            ORDER BY
                date ASC;
            """
    df = pd.read_sql(text(query), con=engine)
    data = df.to_dict(orient="records")
    return jsonify(data)


#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#


#8 establish a route for Start
@app.route("/api/v1.0/temp/start")

def start_tobs():
    # Query min, max, and average temperature for June of 2016
    # print("Request received to gain access to tobs")
    query = """
            SELECT
                date,
                station,
                min(tobs) as min_temp,
                avg(tobs) as avg_temp,
                max(tobs) as max_temp
            FROM
                measurement
            WHERE
                date >= '2016-06-01'
            GROUP BY
                station
            ORDER BY
                date ASC;
            """
    df = pd.read_sql(text(query), con=engine)
    data = df.to_dict(orient="records")
    return jsonify(data)

#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#

#9 establish a route for Start and End
@app.route("/api/v1.0/temp/start/end")

def tobs_range():
    # Query min, max, and average temperature for June of 2016
    print("Request received to gain access to tobs")
    query = """
            SELECT
                date,
                station,
                min(tobs) as min_temp,
                avg(tobs) as avg_temp,
                max(tobs) as max_temp
            FROM
                measurement
            WHERE
                date <= '2016-06-30'
                AND date >= '2016-06-01'
            GROUP BY
                station
            ORDER BY
                date ASC;
            """
    df = pd.read_sql(text(query), con=engine)
    data = df.to_dict(orient="records")
    return jsonify(data)

#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#


if __name__ == "__main__":
    app.run(debug=True)