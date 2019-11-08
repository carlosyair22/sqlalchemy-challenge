
# import dependencies
import pandas as pd
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, desc
from flask import Flask, jsonify

###################################################################################################################################
#Queries code (done in Jupiter notebook)
engine = create_engine("sqlite:///./Resources/hawaii.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station
session = Session(engine)

###################################################################################################################################
#App code
app=Flask(__name__)

@app.route("/")
# List all routes that are available.
def welcome():
    return f'''
    <h1>Hawaii Weather API</h1>
    <h4>versions 1.0</h4>
    <hr>
    <h4>Available routes</h4>
    <ul>
        <li>/api/v1.0/precipitation    ...   Precipitation data of Last twelve months available</li>
        <li>/api/v1.0/stations         ...   List of measurement stations</li>
        <li>/api/v1.0/tobs             ...   Temperature data of Last twelve months available</li>
        <li>/api/v1.0/<start>          ...   Returns minimum, average, and the max temperature for a given start date</li>
        <li>/api/v1.0/<start>/<end>    ...   Returns minimum, average, and the max temperature between two dates</li>
    </ul>
    '''

@app.route("/api/v1.0/precipitation")
#Convert the query results to a Dictionary using date as the key and prcp as the value.
def prcp():
    sel = [measurement.date, measurement.prcp]
    precipitation=session.query(*sel).filter(measurement.date>= "2016-08-24").all()
    #Return the JSON representation of your dictionary.
    return jsonify([precipitation][0])

@app.route("/api/v1.0/stations")
#Return a JSON list of stations from the dataset
def stations():
    stations_query = session.query(station.station, station.name).all()
    return jsonify([stations_query][0])

@app.route("/api/v1.0/tobs")
#query for the dates and temperature observations from a year from the last data point.
def tobs():
    sel = [measurement.date, measurement.tobs]
    temperatures=session.query(*sel).filter(measurement.date>= "2016-08-24").all()
    #Return a JSON list of Temperature Observations (tobs) for the previous year.
    return jsonify([temperatures][0])

@app.route('/api/v1.0/<date>/')
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
def start_date(date):
    temp_stats = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= date).all()
    stats=temp_stats[0]
    return f'''
    <h4>Summary of temperature statistics after {date}</h4>
    <ul>
    <li>Min temperature: {stats[0]}</li>
    <li>Average temperature: {round(stats[1],1)}</li>
    <li>Max temperature: {stats[2]}</li>
    </ul>
    '''
@app.route('/api/v1.0/<start_date>/<end_date>/')
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
def range(start_date,end_date):
    temp_stats = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start_date,measurement.date <= end_date).all()
    stats=temp_stats[0]
    return f'''
    <h4>Summary of temperature statistics between {start_date} and {end_date}</h4>
    <ul>
    <li>Min temperature: {stats[0]}</li>
    <li>Average temperature: {round(stats[1],1)}</li>
    <li>Max temperature: {stats[2]}</li>
    </ul>
    '''

if __name__ == '__main__':
    app.run(debug=True)