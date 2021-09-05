# Dependencies
import pandas as pd
from splinter import Browser
from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

# Set executable path and initialize chrome browser
executable_path = {"executable_path": r"C:\Users\Soni Mohandas\.wdm\drivers\chromedriver\win32\92.0.4515.107\chromedriver.exe"}

# executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def marsNews(browser):
    # visit browser url
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")
    
    # Scrate all news
    news=soup.select_one("div", id_='news')

    # Find first news title using beautifulsoup
    news_title = news.find("div", class_="content_title").get_text()
        
    # Find first news title paragraph using beautifulsoup
    news_para = news.find("div", class_="article_teaser_body").get_text()
    
    # Return news title and news para
    return news_title, news_para

def marsImage(browser):
    # splinter to navigate the site and find the image url
    browser.visit("https://spaceimages-mars.com")

    featured_image_url = browser.find_by_css('.headerimage')['src']
    
    # Return featured image
    return featured_image_url
    
def marsFacts():
    # Pandas to scrape the table containing facts about Mars Diameter, mass, etc
    url = "https://galaxyfacts-mars.com"
    tables = pd.read_html(url)
    
    # Access 2nd table content
    mars_facts_df = tables[1]
    
    # Adding column names
    mars_facts_df.columns = ["Mars_Features", "Values"]
    
    # Return table values
    return mars_facts_df.to_html()

def marsHemispheres(browser):
    # Obtain high resolution images for each of Mar's hemispheres
    # Visit url
    browser.visit("https://marshemispheres.com/")

    hemisphere_image_urls = []

    # Find the links of hemisphere texts
    links = browser.find_by_css('a.itemLink h3')

    # Loop through the links to get all the hemisphere mages
    for txt in range(len(links)-1):   
        hemisphere_image_title = {}
        
        browser.find_by_css('a.itemLink h3')[txt].click()
    
        # Find the title of the hemisphere and store in a dictionary
        hemisphere_image_title["title"] = browser.find_by_css('h2.title').text
    
        # Find the high resolution image link and store in the dictionary
        hemisphere_image_title["image_url"] = browser.find_by_css('img.wide-image')['src']
    
        # Append the dictionary in the list
        hemisphere_image_urls.append(hemisphere_image_title)
    
        # Navigate back to get other hemisphere details
        browser.back()

    # Return values
    return hemisphere_image_urls

def scrape():
    
#     executable_path = {'executable_path': ChromeDriverManager().install()}
    executable_path = {"executable_path": r"C:\Users\Soni Mohandas\.wdm\drivers\chromedriver\win32\92.0.4515.107\chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)
        
    news_title, news_para = marsNews(browser)
    
    featured_image_url = marsImage(browser)
    
    mars_facts_df = marsFacts()
    
    hemisphere_image_urls = marsHemispheres(browser)
    
    # Create a dictionary for mars data
    mars_data = {
        "news_title": news_title,
        "news_para": news_para,
        "featured_image_url": featured_image_url,
        "mars_facts_df": mars_facts_df,
        "hemisphere_image_url": hemisphere_image_urls
    }
    # Close the browser after scraping
    browser.quit()
    
    # Return results
    return mars_data

if __name__=="__main__":
    app.run(debug=True)