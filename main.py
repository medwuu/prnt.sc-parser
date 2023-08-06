import json
import string
import random
import configparser
import requests
from tqdm import tqdm
from art import tprint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


def init() -> None:
    """Инициализация окна и его настройка"""
    options = Options()
    options.binary_location = config['PATH']['BROWSER_PATH']
    if not config['WINDOW']['IS_VISIBLE']:
        options.add_argument('--headless')
    options.page_load_strategy = 'eager'
    # TODO: прикрутить сюда прокси
    global browser
    browser = webdriver.Firefox(options=options)
    browser.set_window_position(0, 0)
    # аргумент set_window_size позволяет передавать str значения, поэтому здесь нет преобразования в int
    browser.set_window_size(config['WINDOW']['WIDTH'], config['WINDOW']['HEIGHT'])
    
    

def getImgLinks() -> None:
    """При (USE_FAST_METHOD == 0) добавление проверенной сслыки в json и загрузка изображения.\n
    При (USE_FAST_METHOD != 0) только добавление ссылки в json, если она найдена"""
    letters = string.ascii_lowercase + string.digits
    links_dict = {}
    for iter in tqdm(range(int(config['WORK']['IMG_COUNT']))):
        postfix = ''.join([random.choice(letters) for _ in range(6)])
        link = f'https://prnt.sc/{postfix}'
        browser.get(link)
        # Позволяет приступить к проверке фото сразу после того, как на странице полностью загрузится <body>
        WebDriverWait(browser, 10).until(expected_conditions.visibility_of_element_located((By.TAG_NAME, 'body')))
        img_link = checkImg(browser.page_source)
        # Изображение: не найдено на странице || не загружается || удалено
        if not img_link:
            continue
        
        # В первом случае добавляется в json любая найденная сслылка
        # Во втором случае сохранятся и заносится в json, только если существует
        # FIXME: в первом случае добавляются нерабочие ссылки
        if int(config['WORK']['USE_FAST_METHOD']) or saveImg(img_link, postfix):
            links_dict[postfix] = img_link


        if iter % int(config['WORK']['BACKUP_COUNT']) == 0:
            writeIntoJSON(links_dict)
    writeIntoJSON(links_dict)


def writeIntoJSON(links_dict: dict) -> None:
    """Запись словаря links_dict в json"""
    with open(f'{config["PATH"]["JSON_NAME"]}.json', 'w') as f:
        json.dump(links_dict, f, indent=4, ensure_ascii=False)

def checkImg(html: str) -> str:
    """Проверка страницы на наличие небитого и неудалённого изображения.\n
    Output: сслыка, если она подходит, и '', если нет"""
    soup = BeautifulSoup(html, 'lxml')
    img_section = soup.find('img', id='screenshot-image')
    if img_section and not img_section.has_attr('attempt'):
        img_link = img_section.get_attribute_list('src')[0]
        if not '//st.prntscr.com' in img_link:
            return img_link
    return ''
    

def saveImg(url: str, postfix: str) -> bool:
    """Скачивание изображения, если оно существует и не удалено.\n
    Output: было ли изображение сохранено (bool)"""
    r = requests.get(url)
    if r.url != 'https://i.imgur.com/removed.png' and \
    '404 Not Found' not in r.text:
        with open(f'{config["PATH"]["RESULT_FOLDER"]}\\{postfix}.png', 'wb') as f:
            f.write(r.content)
        global img_downloaded
        img_downloaded += 1
        return True
    return False

def saveImgFast() -> None:
    """Чтение проверенных ссылок из json и скачивание изображений"""
    with open(f'{config["PATH"]["JSON_NAME"]}.json', 'r') as f:
        file_links = json.load(f)
    postfixes = list(file_links.keys())
    links = list(file_links.values())
    for x in tqdm(range(len(links))):
        saveImg(links[x], postfixes[x])



def main():
    global config
    config = configparser.ConfigParser()
    config.read('config.ini')
    global img_downloaded
    img_downloaded = 0
    tprint("PRNT.SC        PARSER")
    input("Включите VPN и нажмите Enter...")
    init()
    getImgLinks()
    browser.quit()
    if int(config['WORK']['USE_FAST_METHOD']):
        input("Для скачивания картинок отключите VPN и нажмите Enter...")
        saveImgFast()
    print(f"Программа успешно завершена! Найдено и скачано {img_downloaded}/{config['WORK']['IMG_COUNT']} изображений")

if __name__ == '__main__':
    main()