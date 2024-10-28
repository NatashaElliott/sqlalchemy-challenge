# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Query all precipitation data and dates and convert to JSON    
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session
    session = Session(engine)
    # Query all precipitation data and dates
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    # Create a dictionary from the results
    precipitation_results = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        precipitation_results.append(precipitation_dict)
    return jsonify(precipitation_results)

# Query all stations data and convert to JSON    
@app.route("/api/v1.0/stations")
def stations():
    # Create our session
    session = Session(engine)
    # Query all stations data
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()
    # Create a dictionary from the results
    stations_results = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name
        station_dict['latitude'] = latitude
        station_dict['longitude'] = longitude
        station_dict['elevation'] = elevation
        stations_results.append(station_dict)
    return jsonify(stations_results)
    
# Returning data for the most active station over the last 12 months  
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session
    session = Session(engine)
    # Query all stations data
    last_date = '2016-08-23'
    stations_active = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station==stations_active[0][0]).filter(Measurement.date > last_date).all()
    session.close()
    # Create a dictionary from the results
    tobs_results = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_results.append(tobs_dict)
    return jsonify(tobs_results)
    
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range  
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session
    session = Session(engine)
    # Calculating the data
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date > start).all()
    session.close()
    # Create a dictionary from the results
    start_date_results = []
    for min_date, max_date, avg_date in results:
        start_date_results_dict = {}
        start_date_results_dict['min_date'] = min_date
        start_date_results_dict['max_date'] = max_date
        start_date_results_dict['avg_date'] = avg_date
        start_date_results.append(start_date_results_dict)
    return jsonify(start_date_results_dict)

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range  
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create our session
    session = Session(engine)
    # Calculating the data
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date < end).all()
    session.close()
    # Create a dictionary from the results
    start_date_results = []
    for min_date, max_date, avg_date in results:
        start_date_results_dict = {}
        start_date_results_dict['min_date'] = min_date
        start_date_results_dict['max_date'] = max_date
        start_date_results_dict['avg_date'] = avg_date
        start_date_results.append(start_date_results_dict)
    return jsonify(start_date_results_dict)
    
if __name__ == "__main__":
    app.run(debug=True)
