from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'C:/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

def scrape_mars():
    browser = init_browser()
    
    mars_data = {}
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide",wait_time = 1)
    time.sleep(3)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    tag = soup.select_one("ul.item_list li.slide")


    title = tag.find("div",class_ = "content_title").get_text()
    print(title)

    paragraph = tag.find("div",class_ = "article_teaser_body").get_text()
    print(paragraph)
    article = {
        "title":title,
        "paragraph":paragraph
    }
    mars_data["news"] = article 

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    full_image = browser.find_by_id("full_image")
    full_image.click()

    browser.is_element_present_by_text("more info",wait_time = 1)
    tag_2 = browser.find_link_by_partial_text("more info")
    tag_2.click()

    html = browser.html
    soup = bs(html, "html.parser")

    image = soup.select_one("figure.lede a img").get("src")
    print(image)

    img_url = "https://www.jpl.nasa.gov"+image
    img_url
    mars_data["image"] = img_url


    url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    tweet_containers = soup.find_all("div", class_="js-tweet-text-container")
    mars_weather = tweet_containers[0].text
    print(mars_weather)
    #I had trouble reading these values using BeautifulSoup and it looks like Twitter may have updated its site. 
    #So I worked with Dominic LaBella to come up with a workaround
    mars_data["weather"] = mars_weather


    table = pd.read_html("https://space-facts.com/mars/")[0]
    table.columns = ["desc","data"]
    table = table.set_index("desc")
    table = table.to_html()
    mars_data["table"] = table



    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    img_titles = []
    links = browser.find_by_css("a.product-item h3")
    for i in range(len(links)):
        images = {}
        browser.find_by_css("a.product-item h3")[i].click()
        element = browser.find_link_by_text("Sample").first
        images["image_url"] = element["href"]
        images["title"] = browser.find_by_css("h2.title").text
        img_titles.append(images)
        print(img_titles)
        browser.back()

    print(img_titles)

    mars_data["hemispheres"] = img_titles
    return mars_data


