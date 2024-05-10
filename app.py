# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# # Create our session (link) from Python to the DB
# session = Session(engine)

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
        f"/api/v1.0/start_date/<br/>"
        f"/api/v1.0/start_date/end_date/"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of date and prcp for the last 12 months"""
    # Query
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        all()

    session.close()

    # Dictionary
    precipitation_dict = {}
    for date, prcp in results:
        precipitation_dict[date] = prcp
      
    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query
    results = session.query(Station.name).all()
    session.close()

    # List
    all_stations = []
    for name in results:
        all_stations.append(name[0])
    
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Dates and temperature observations of the most-active station for the previous year"""
    # Query
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-23').\
        all()
    session.close()

    # List
    all_temperatures = []
    for temp in results:
        all_temperatures.append(temp[0])
    
    return jsonify(all_temperatures)


@app.route("/api/v1.0/start_date/<start_date>")
def temp_stats(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """The minimum, average, and the maximum temperature for all the dates greater than or equal to the start date."""
    # Query
    results = session.query(func.min(Measurement.tobs),
                       func.round(func.avg(Measurement.tobs),0),
                       func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date).\
                        all()
    session.close()

    # List
    all_stats = []
    for minimum, average, maximum in results:
        # Dictionary
        stat_dict = {}
        stat_dict["Minimum Temperature"] = minimum
        stat_dict["Average Temperature"] = average
        stat_dict["Maximum Temperature"] = maximum
        all_stats.append(stat_dict)
    
    return jsonify(all_stats)


@app.route("/api/v1.0/start_date/end_date/<start_date>/<end_date>")
def temp_stats2(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """The minimum, average, and the maximum temperature for the dates from the start date to the end date, inclusive."""
    # Query
    results = session.query(func.min(Measurement.tobs),
                       func.round(func.avg(Measurement.tobs),0),
                       func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date).\
                        filter(Measurement.date <= end_date).\
                        all()
    session.close()

    # List
    all_stats2 = []
    for minimum, average, maximum in results:
        # Dictionary
        stat_dict2 = {}
        stat_dict2["Minimum Temperature"] = minimum
        stat_dict2["Average Temperature"] = average
        stat_dict2["Maximum Temperature"] = maximum
        all_stats2.append(stat_dict2)
    
    return jsonify(all_stats2)


if __name__ == '__main__':
    app.run(debug=True)