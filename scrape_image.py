import bs4
import lxml
import requests
import concurrent.futures
import shutil
import urllib.parse
import time

page = requests.get("https://en.wikipedia.org/wiki/Category:Euro_images")

soup = bs4.BeautifulSoup(page.content, "lxml")
data = soup.findAll("div", attrs={"class": "mw-category-group"})

decsription_pages = []
for div in data:
    links = div.findAll("a")
    for a in links:
        decsription_pages.append(f"https://en.wikipedia.org{a['href']}")

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

def extract_filename(url):
    file = url.split("/")[-1]
    return urllib.parse.unquote(file)

def save_file_from_url(url):
    r = requests.get(url, stream=True)
    time.sleep(.3)
    if r.status_code == 200:
        filename = extract_filename(url)
        with open("euro_coins/" + filename, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        return "Success"
    else:
        return url

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(save_file_from_url, url) for url in results]
    for future in concurrent.futures.as_completed(futures):
        print(future.result())