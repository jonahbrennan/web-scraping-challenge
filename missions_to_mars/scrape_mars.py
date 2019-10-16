from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    import pandas as pd
    browser = init_browser()

    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Find the headlines
    results1 = soup.find('div', class_='content_title').text
    results2 = soup.find('div', class_='article_teaser_body').text
    # browser.quit()
    # Scrape for the featured image
    # browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    jpl_img_route = soup.find('a', class_='fancybox').get('data-fancybox-href')
    # Form the url
    hires_img = jpl_img_route.replace("mediumsize","largesize")
    hires_img = hires_img.replace(hires_img[-6:],"hires.jpg")
    mars_hires_img = hires_img.replace("/spaceimages","https://www.jpl.nasa.gov/spaceimages")

    # browser.quit()
    # browser = init_browser()
    # Scrape for Mars facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_facts_df = tables[1]   # [0] sets it to pull from the first table 
    mars_facts_df.columns = ['Mars', 'Fact',]
    mars_facts_html_table = mars_facts_df.to_html()
    # mars_facts_html_table = mars_facts_html_table.replace('\n', '')

    browser.quit()

    # Store data in a dictionary
    mars_data = {
        "headline": results1,
        "teaser": results2,
        "featured_image": mars_hires_img,
        "mars_facts_table": mars_facts_html_table
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
