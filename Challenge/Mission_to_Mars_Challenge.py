#!/usr/bin/env python
# coding: utf-8

import pandas as pd
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)
html = browser.html

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# Parse HTML with Beautiful Soup
hemi_soup = soup(html, 'html.parser')
# Retrieve all elements that contain Hemisphere Info
hemispheres = hemi_soup.find_all('div', class_='item')


# Iterate through each
for hemisphere in hemispheres:
    hemisphere_dict ={}
    try:
        click_lnk = hemisphere.find('h3').text
        browser.links.find_by_partial_text(click_lnk).click()
        
        clicked_html = browser.html
        image_soup = soup(clicked_html, 'html.parser')
        
        full_image = image_soup.find('a',text='Sample').get('href')
        title_image = image_soup.find('h2', class_='title').get_text()
        
        
        img_url = f'{url}{full_image}'
        hemisphere_dict["title"]= title_image
        hemisphere_dict["img_url"]= img_url
    except:
        print(f'Scraping Error {clicked_html}' )
    
    #print(title_image)
    #print(full_image)
    
    hemisphere_image_urls.append(hemisphere_dict)
    browser.back() 


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()

