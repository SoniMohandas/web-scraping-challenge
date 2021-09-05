# Dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars
from bson.codec_options import CodecOptions
from flask import redirect


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
    
    # Run the scrape function
    mars_collection = scrape_mars.scrape()
    
    # Update mongo database using update and upsert = True
    mongo.db.mars_data.update({},mars_collection, upsert=True)
    
    # Redirect to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

