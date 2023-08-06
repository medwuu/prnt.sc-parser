import os
import json
import string
import random
import dotenv
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def init():
    options = Options()
    options.binary_location = os.getenv("BROWSER_PATH")
    # TODO: в конце, чтобы окно не открывалось
    # options.add_argument("--headless")
    options.page_load_strategy = 'eager'
    global browser
    browser = webdriver.Firefox(options=options)
    browser.set_window_position(0, 0)
    browser.set_window_size(1500, 700)
    

def getImgLinks():
    letters = string.ascii_lowercase + string.digits
    links_list = []
    for iter in tqdm(range(50)):
        postfix = ''.join([random.choice(letters) for _ in range(6)])
        link = f"https://prnt.sc/{postfix}"
        browser.get(link)
        img_link = checkImg(browser.page_source)
        if not img_link:
            continue

        if saveImg(img_link, postfix):
            links_list.append({postfix: img_link})


        if iter % 10 == 0:
            writeIntoJSON(links_list)
    writeIntoJSON(links_list)


def writeIntoJSON(links_list=[], filename="links"):
    with open(f"{filename}.json", "w") as f:
        json.dump(links_list, f, indent=4, ensure_ascii=False)

def checkImg(html):
    soup = BeautifulSoup(html, "lxml")
    img_section = soup.find("img", id="screenshot-image")
    if img_section and not img_section.has_attr("attempt"):
        img_link = img_section.get_attribute_list("src")[0]
        if not "//st.prntscr.com" in img_link:
            return img_link
    return ""
    

def saveImg(url, postfix):
    r = requests.get(url)
    if r.url != "https://i.imgur.com/removed.png" and \
    "404 Not Found" not in r.text:
        with open(f"result\\{postfix}.png", "wb") as f:
            f.write(r.content)
            return True
    return False



def main():
    dotenv.load_dotenv()
    init()
    getImgLinks()
    browser.quit()

if __name__ == "__main__":
    main()