from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from textblob import TextBlob


def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.2:
        return "positive"
    elif polarity < -0.2:
        return "negative"
    else:
        return "neutral"


def scrape_amazon(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.page_load_strategy = 'eager'   # ⚡ fast load

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(url)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "productTitle"))
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Product
    title = soup.find(id="productTitle")
    product_name = title.get_text(strip=True) if title else "N/A"

    price = soup.find("span", {"class": "a-price-whole"})
    product_price = price.get_text(strip=True) if price else "N/A"

    rating = soup.find("span", {"class": "a-icon-alt"})
    product_rating = rating.get_text().split()[0] if rating else "N/A"

    # Image
    image = soup.find("img", {"id": "landingImage"})
    product_image = image["src"] if image else ""

    # Reviews
    reviews = []
    review_elements = soup.find_all("span", {"data-hook": "review-body"}, limit=15)

    for r in review_elements:
        text = r.get_text(strip=True)
        if text:
            sentiment = analyze_sentiment(text)
            reviews.append({
                "review_text": text,
                "sentiment": sentiment
            })

    # Summary
    positive = sum(1 for r in reviews if r["sentiment"] == "positive")
    negative = sum(1 for r in reviews if r["sentiment"] == "negative")
    neutral = sum(1 for r in reviews if r["sentiment"] == "neutral")

    summary = {
        "positive": positive,
        "negative": negative,
        "neutral": neutral
    }

    driver.quit()

    return {
        "product_name": product_name,
        "price": product_price,
        "rating": product_rating,
        "image": product_image,
        "summary": summary,
        "reviews": reviews
    }