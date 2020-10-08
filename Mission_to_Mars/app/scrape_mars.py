from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import time
import re


def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    article_title, article_para = mars_news(browser)

    # Run all scraping functions and store in dictionary.
    data = {
        "article_title": article_title,
        "article_para": article_para,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data




def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    pollo_soup = BeautifulSoup(html, 'html.parser')

    try:
        slide_elem = pollo_soup.select_one('ul.item_list li.slide')
        article_title = slide_elem.find("div", class_='content_title').get_text()
        article_para = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return article_title, article_para




def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    try:
        image = soup.find("img", class_="thumb")["src"]

    except AttributeError:
        return None

    featured_image_url = "https://www.jpl.nasa.gov" + image

    return featured_image_url




def mars_facts():
    try:
        df = pd.read_html("http://space-facts.com/mars/")[0]
    except BaseException:
        return None

    df.columns = ["description", "value"]
    df.set_index("description", inplace=True)

    return df.to_html(classes="table table-striped")




def hemispheres(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    links = browser.find_by_css("a.product-item h3")

    for item in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[item].click()
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()

    return hemisphere_image_urls


if __name__ == "__main__":

    print(scrape_all())




