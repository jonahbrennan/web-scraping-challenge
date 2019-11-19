from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from flask import Flask, jsonify, render_template, redirect
import pandas as pd


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
    # Scrape the weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "lxml")
    mars_weather = soup.body.find('p', class_="TweetTextSize").text  
    
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
    mars_facts_df = tables[0]   # [0] sets it to pull from the first table 
    mars_facts_df.columns = ['Mars', 'Fact',]
    mars_facts_html_table = mars_facts_df.to_html()
    # mars_facts_html_table = mars_facts_html_table.replace('\n', '')

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # time.sleep(3)
    html = browser.html
    soup = bs(html, 'lxml')
    time.sleep(1)

    # Retrieve all div elements
    # articles = soup.find_all('div', class_='item') 
    clickers = []
    articles = soup.find_all('div', class_='item')
    # articles = soup.find_all('div', class_="description")

#     print(articles)
    img_urls = []
    titles = []
    for article in articles:
        title = []
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        title = article.find('h3').text
        link = article.find('a')
        titles.append(title)
#         print(article)
#         try:
        browser.click_link_by_partial_text(title)
#             time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_url = soup.find('a', target='_blank').get('href')
        img_urls.append(img_url)
        browser.back()
        # except:
        #     print(f'"Exception! - Scraping Aborted"{url}')
            
        #     browser.back()
        
    

        # browser.quit()

    # Store data in a dictionary
    mars_data = {
        "headline": results1,
        "teaser": results2,
        "featured_image": mars_hires_img,
        "mars_facts_table": mars_facts_html_table,
        "mars_weather": mars_weather,
        "Cerberus": img_urls[0],
        "Schiaparelli": img_urls[1],
        "Syrtis": img_urls[2],
        "Valles": img_urls[3],
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
