from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# flask_pymongo to setup mongo connection
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017"
mongo = PyMongo(app)

@app.route("/")
def index():
    data = mongo.db.mars_facts.find_one()
    return render_template("index.html")
    
    
@app.route("/scrape")    
def scrape():
    
    mars_data = scrape_mars.scrape_info()
    
    # Update mongo database using update and upsert = True
    mongo.db.mars_facts.update({}, mars_data, upsert = True)
    
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)

