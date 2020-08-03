# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispehere_images": hemis(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def hemis(browser):
    # declare the variable that will contain a list of dicts having the title and urls appended 
    hemi_data = []

    # Scrape the photos of Mars Hemispheres
    # Visit the site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # Convert the browser html to a soup object 
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    
    # Go to parent div & grab all 4 hemisphere info
    hemis = hemi_soup.find('div', class_="collapsible results")
    items = hemis.find_all('div', class_="item")
    
    # loop thru items to get a list of hemisphere names then use to find click path to enhanced 
    hemispheres = []
    for item in items:
        x = item.find("h3").text
        hemispheres.append(x)

    # Go to each hemisphere page, one at a time
    for hemi in hemispheres:
        browser.visit(url)
        browser.is_element_present_by_text(hemi, wait_time=1)
        enhanced_image_elem = browser.links.find_by_partial_text(hemi)
        enhanced_image_elem.click()
        
        # Convert the browser html to a soup object 
        html = browser.html
        hemi_soup = soup(html, 'html.parser')

        # get title of enhanced image
        hemi_title = hemi_soup.find("h2", class_="title").text
        # get url of enhanced image
        hemi_url = hemi_soup.find("a", text="Original").get("href")
        # append to dictionary
        hemi_dict = {'title':hemi_title, 'img_url': hemi_url}
        # append to list of dictionaries
        hemi_data.append(hemi_dict)
        # return list of dictionaries
        return hemi_data

    
    # 1. click thumbnail
    # 2. click filename link
    # 3. grab filename & url to store in dict
    # 4. append dict to a list, list contains a dict for each hemisphere

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')


# Scrape Mars News
def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# Scrape Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
   
    return img_url

# Scrape Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())