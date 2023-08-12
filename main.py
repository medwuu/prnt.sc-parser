import os
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

def checkConfig():
    global config
    config = configparser.ConfigParser()
    if not os.path.isfile('config.ini'):
        config.add_section('PATH')
        config.set('PATH', 'BROWSER_PATH', r'C:\Program Files\Mozilla Firefox\firefox.exe')
        config.set('PATH', 'RESULT_FOLDER', 'result')
        config.set('PATH', 'JSON_NAME', 'links')
        config.add('WORK')
        config.set('WORK', 'IMG_COUNT', '100')
        config.set('WORK', 'BACKUP_COUNT', '10')
        config.add_section('WINDOW')
        config.set('WINDOW', 'WIDTH', '1500')
        config.set('WINDOW', 'HEIGHT', '700')
        config.set('WINDOW', 'IS_VISIBLE', '0')
        with open('config.ini', 'w') as cfg_file:
            config.write(cfg_file)
    else:
        # TODO: проверка наличия всех ключей
        config.read('config.ini')
        for section in config.sections():
            for _, value in config.items(section):
                if not value or \
                section != 'PATH' and not value.isdigit():
                    return False
    return True


def init() -> None:
    """Инициализация окна и его настройка"""
    options = Options()
    options.binary_location = config['PATH']['BROWSER_PATH']
    options.page_load_strategy = 'eager'
    # TODO: прикрутить сюда прокси
    global browser
    browser = webdriver.Firefox(options=options)
    browser.install_addon('extensions\\browsec@browsec.com.xpi', True)
    browser.set_window_position(0, 0)
    # set_window_size позволяет передавать str значения, поэтому здесь нет преобразования в int
    browser.set_window_size(config['WINDOW']['WIDTH'], config['WINDOW']['HEIGHT'])
    global img_downloaded
    img_downloaded = 0
    
    

def getImgLinks() -> None:
    """Добавление ссылки в json, если она найдена (но не проверена)"""
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
            
        
        # FIXME: добавляются нерабочие ссылки
        if saveImg(img_link, postfix):
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




def main():
    if not checkConfig():
        print("Ошибка чтения config файла! Пожалуйста, проверьте правильность ввседённых данных")
        return
    tprint("PRNT.SC        PARSER")
    init()
    input("Включите VPN и нажмите Enter...")
    getImgLinks()
    browser.quit()
    print(f"Программа успешно завершена! Найдено и скачано {img_downloaded}/{config['WORK']['IMG_COUNT']} изображений")

if __name__ == '__main__':
    main()