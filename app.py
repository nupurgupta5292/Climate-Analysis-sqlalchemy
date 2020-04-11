# Importing dependancies
import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# reflected an existing database into a new model
Base = automap_base()

# reflected the tables
Base.prepare(engine, reflect=True)

# Saved references to both the tables
measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

# Flask Routes

#Homepage
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welome to Hawaii Climate API!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation</br>  - Returns all precipitation data with dates<br/>"
        f"<br/>"
        f"/api/v1.0/stations</br>  - Returns the list of all stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs</br>  - Returns a list of temperature observations (TOBs) for the previous year for the most active station<br/>"
        f"<br/>"
        f"/api/v1.0/start_date</br>  - Calculates and returns the TMIN, TAVG, and TMAX for all dates greater than and equal to the start date<br/>"
        f"<br/>"
        f"/api/v1.0/start_date/end_date</br>  - Calculates and returns the TMIN, TAVG, and TMAX for dates between the start and end date inclusive<br/>"
    )

# First Path
@app.route("/api/v1.0/precipitation")
def prcpn():
    """Return a list of date wise precipitation data"""
    # Query all precipitation data
    results = session.query(measurement.date, measurement.prcp).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    precipitation_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precipitation_data.append(prcp_dict)

    return jsonify(precipitation_data)

#Second path
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations in the dataset"""
    # Query all passengers
    results = session.query(station.station,station.name).all()

    # Converting query results into a list
    station_names = []
    for station, name in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_names.append(station_dict)   

    return jsonify(station_names)

#Third Path
@app.route("/api/v1.0/tobs")
def tobs():
    """List of Temperature Observations (tobs) for the previous year for the most active station"""

    #Identifying most active station
    sel = [measurement.station,func.count(measurement.station)]
    station_count = session.query(*sel).group_by(measurement.station).order_by(func.count(measurement.station).desc())
    #Since the results are arrabged in descending order, the most active station would be the first one, i.e. the one with max count
    for station in station_count[:1]:
        most_active_station = station.station
    

    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first().scalar
    #From the above query, we know the last date data point is 2017-08-23
    one_year_ago = last_date - dt.timedelta(days=365)
    tobs = session.query(measurement.station,measurement.date, measurement.tobs).\
        filter(measurement.date >= one_year_ago).\
        filter(measurement.station == most_active_station).\
        order_by(measurement.date).all()

    # Creating list returning TOBs for previous year for most active station
    tobs_list = []
    for result in tobs:
        tob_row = {}
        tob_row["date"] = result[1]
        tob_row["tobs"] = result[2]
        tobs_list.append(tob_row)

    return jsonify(tobs_list)

#Fourth Path
@app.route("/api/v1.0/<start>")
def tstats(start):
    """When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""
    sel = [func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)]

    temp_stats = session.query(*sel).filter(measurement.date >= start).all()
    
    temp = []
    for result in temp_stats:
        temp_row = {}
        temp_row["TMIN"] = result[0]
        temp_row["TMAX"] = result[1]
        temp_row["TAVG"] = result[2]
        temp.append(temp_row)

    return jsonify(temp)

#Fifth Path
@app.route("/api/v1.0/<start>/<end>")
def tstats(start,end):
    """When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
    sel = [func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)]

    temp_stats = session.query(*sel).filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    temp = []
    for result in temp_stats:
        temp_row = {}
        temp_row["TMIN"] = result[0]
        temp_row["TMAX"] = result[1]
        temp_row["TAVG"] = result[2]
        temp.append(temp_row)

    return jsonify(temp)


if __name__ == "__main__":
    app.run(debug=True)



