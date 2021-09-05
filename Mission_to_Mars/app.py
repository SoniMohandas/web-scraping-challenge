# Dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# flask_pymongo to setup mongo connection
# app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/MarsDB"
mongo = PyMongo(app, uri = "mongodb://127.0.0.1:27017/MarsDB")

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)
    
    
@app.route("/scrape")    
def scrape():
    
    mars_data = mongo.db.mars_data
    mars_collection = scrape_mars.scrape()
    
    # Update mongo database using update and upsert = True
    mars_data.update({}, mars_collection, upsert=True)
    return ('Scraping successful')

if __name__ == "__main__":
    app.run(debug=True)

