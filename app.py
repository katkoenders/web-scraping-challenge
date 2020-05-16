from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    Mars_Data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars=Mars_Data)


# Route that will trigger the scrape function
@app.route("/test")
def scrape():

    # Run the scrape function
    mars_info = Mars.scrape_mars()
    

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_info, upsert=True)

    # Redirect back to home page
    return redirect("/")
    #return jsonify(mars_info)

if __name__ == "__main__":
    app.run(debug=True)
