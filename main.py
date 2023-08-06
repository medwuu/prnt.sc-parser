import os
import json
import string
import random
import dotenv
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import selenium.common.exceptions

def init():
    options = Options()
    options.binary_location = os.getenv("BROWSER_PATH")
    # Чтобы окно не открывалось
    # options.add_argument("--headless")
    options.page_load_strategy = 'eager'
    global browser
    browser = webdriver.Firefox(options=options)
    browser.set_window_position(0, 0)
    browser.set_window_size(1500, 700)
    

def getImgLinks():
    letters = string.ascii_lowercase + string.digits
    links_list = []
    for iter in tqdm(range(10)):
        postfix = ''.join([random.choice(letters) for _ in range(6)])
        link = f"https://prnt.sc/{postfix}"
        browser.get(link)

        try:
            img_section = browser.find_element(By.ID, "screenshot-image")
        except selenium.common.exceptions.NoSuchElementException:
            continue

        if img_section.get_attribute("attempt"):
            continue

        img_link = img_section.get_attribute("src")
        browser.get(img_link)
        try:
            if "//st.prntscr.com/" not in img_link and \
            browser.current_url != "https://i.imgur.com/removed.png" and \
            not browser.find_element(By.TAG_NAME, "h1"):
                links_list.append({postfix: img_link})
        except selenium.common.exceptions.NoSuchElementException:
            links_list.append({postfix: img_link})


        if iter % 10 == 0:
            writeIntoJSON(links_list)
    writeIntoJSON(links_list)


def writeIntoJSON(links_list=[], filename="links"):
    with open(f"{filename}.json", "w") as f:
        json.dump(links_list, f, indent=4, ensure_ascii=False)






def main():
    dotenv.load_dotenv()
    init()
    getImgLinks()
    browser.quit()

if __name__ == "__main__":
    main()