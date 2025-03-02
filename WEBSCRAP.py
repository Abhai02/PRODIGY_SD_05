import requests
from bs4 import BeautifulSoup
import pandas as pd

# Target website (Books to Scrape)
URL = "http://books.toscrape.com/"

# Send a request to the website
response = requests.get(URL)

# Check if the request was successful
if response.status_code != 200:
    print(f"❌ Failed to fetch the webpage. Status code: {response.status_code}")
    exit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Lists to store extracted data
book_titles = []
book_prices = []
book_ratings = []

# Find all book containers
books = soup.find_all("article", class_="product_pod")

for book in books:
    # Extract book title
    title = book.h3.a["title"].strip()

    # Extract book price
    price_tag = book.find("p", class_="price_color")
    price = price_tag.text.strip() if price_tag else "N/A"

    # Extract book rating (convert class to text)
    rating_classes = book.p["class"]
    rating = rating_classes[1] if len(rating_classes) > 1 else "No Rating"

    # Append extracted data to lists
    book_titles.append(title)
    book_prices.append(price)
    book_ratings.append(rating)

# Store data in a Pandas DataFrame
df = pd.DataFrame({
    "Title": book_titles,
    "Price": book_prices,
    "Rating": book_ratings
})

# Save to CSV
df.to_csv("books_data.csv", index=False, encoding="utf-8")

print("✅ Data scraped successfully and saved to 'books_data.csv'")
