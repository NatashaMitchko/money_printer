import bs4
import lxml
import requests
import concurrent.futures

page = requests.get("https://en.wikipedia.org/wiki/Category:Euro_images")

soup = bs4.BeautifulSoup(page.content, "lxml")
data = soup.findAll("div", attrs={"class": "mw-category-group"})

decsription_pages = []

for div in data:
    links = div.findAll("a")
    for a in links:
        decsription_pages.append(f"https://en.wikipedia.org{a['href']}")

print(len(decsription_pages))

# for each page, get the file path

def get_file_path(description_path):
    page = requests.get(description_path)
    soup = bs4.BeautifulSoup(page.content, "lxml")
    div = soup.find("div", attrs={"class": "fullImageLink"})
    return div.find("a").get("href")

results = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(get_file_path, url) for url in decsription_pages]
    for future in concurrent.futures.as_completed(futures):
        results.append("https:" + future.result())


print(len(results))
print(results)