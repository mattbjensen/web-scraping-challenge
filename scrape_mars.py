# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    browser=init_browser()
    mars_dict={}

    # ### NASA Mars News (https://redplanetscience.com/)

    # URL for NASA news page to be scraped
    news_url = 'https://redplanetscience.com/'
    browser.visit( news_url)

    # Create HTML object
    html = browser.html

    # Parse HTML with BeautifulSoup
    soup = bs( html, 'html.parser')


    # Retrieve the latest news title
    title = soup.find_all( 'div', class_ = 'content_title')[0].text

    # Retrieve the latest news paragraph
    paragraph = soup.find_all( 'div', class_ = 'article_teaser_body')[0].text
    print( title)
    print( '-------------------')
    print( paragraph)


    # ### JPL Mars Space Images - Featured Image (https://spaceimages-mars.com/)

    # URL for JPL Featured Image
    space_images_url = 'https://spaceimages-mars.com/'
    browser.visit( space_images_url)

    # Create HTML object
    html = browser.html

    # Parse HTML with BeautifulSoup
    soup = bs( html, 'html.parser')

    # Find featured image and print source url
    featured_image = soup.find_all( 'img', class_ = 'headerimage fade-in')[0]['src']
    featured_image_url = space_images_url + featured_image
    print(featured_image_url)


    # ### Mars Facts (https://galaxyfacts-mars.com/)

    #URL for Mars Facts Website
    facts_url = 'https://galaxyfacts-mars.com/'

    # Use pandas to read table of facts comparing Mars and Earth
    facts_table = pd.read_html(facts_url, header=0)
    facts_table[0]

    # Use pandas to read table of Mars facts
    facts_table = pd.read_html(facts_url)
    facts_df = facts_table[1]
    facts_df.columns =['Description', 'Value']
    facts_df

    # Convert to HTML
    facts_html = facts_df.to_html()
    print(facts_html)


    # ### Mars Hemispheres (https://marshemispheres.com/)

    # URL for JPL Featured Image
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit( hemispheres_url)

    # Create HTML object
    html = browser.html

    # Parse HTML with BeautifulSoup
    soup = bs( html, 'html.parser')

    items = soup.find_all('div', class_='item')

    mars_hemi_urls = []
    mars_hemi_titles = []

    for item in items:
        mars_hemi_urls.append( hemispheres_url + item.find('a')['href'])
        mars_hemi_titles.append( item.find('h3').text.strip())

    print( mars_hemi_urls)
    mars_hemi_titles

    hemi_img_urls = []

    for url in mars_hemi_urls:
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        
        # Find image urls and append to list
        source_url = hemispheres_url + soup.find('img',class_='wide-image')['src']
        hemi_img_urls.append( source_url)
        
    hemi_img_urls

    hemi_img_list = []

    for i in range( len( mars_hemi_titles)):
        hemi_img_list.append({ 'title':mars_hemi_titles[i], 'img_url':hemi_img_urls[i]})

    hemi_img_list

    mars_dict = {
        "news_title":title,
        "news_p":paragraph,
        "featured_image_url":featured_image_url,
        "fact_table":facts_html,
        "hemisphere_images":hemi_img_list
    }

    mars_dict

    # Close the browser after scraping
    browser.quit()
    return mars_dict