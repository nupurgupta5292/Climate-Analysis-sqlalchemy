# Importing Dependancies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

# Creating engine to SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflected an existing database into a new model
Base = automap_base()
# Reflected the tables
Base.prepare(engine, reflect=True)

# Saved references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

if __name__ == '__main__':
    app.run(debug=True)

