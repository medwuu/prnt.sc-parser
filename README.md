# prnt.sc-parser

## Содержание:
- [Что это и зачем?](#что-это-и-зачем)
- [Пример работы](#пример-работы)
- [Установка](#установка)
- [P. S.](#ps)

---
### Что это и зачем?
Существует приложение для ПК и одноимённый сайт [prnt.sc](https://prnt.sc/) (недоступен из РФ), на который люди могут загружать свои скрины и делиться ссылками на эти самые фотографии. Но далеко не все осознают, что их (возможно) персональные данные можно раздобыть незамысловатым перебором ссылок в браузере, ведь сайт не шифрует и не проверяет авторизацию перед просмотром материалов

Данный скрипт позволит вам узнать, какие фотографии люди добровольно предоставляют в открытый доступ, даже не заботясь о своей ИБ

\* Данный скрипт не распространяет ПД третьих лиц, т. к. все материалы взяты из открытого доступа

---
### Пример работы
Во время работы:
![Пример работы](https://github.com/medwuu/prnt.sc-parser/assets/91782808/eb3aaf00-8bdc-47aa-b267-77aeadbc731a)

Конец работы:
![Конец работы](https://github.com/medwuu/prnt.sc-parser/assets/91782808/8dea79ae-0b10-4614-8769-ee27f8f1ff21)

---
### Установка:
1. Убедиться, что стоит [Python 3.11](https://www.python.org/downloads/) и [Firefox последней версии](https://www.mozilla.org/ru/firefox/new/)
2. Прописать в консоли `pip install -r requitements.txt`
3. При необходимости изменить файл `config.ini`
4. Запустить скрипт

---
### P. S.
Если вы знаете, как адекватно подключить VPN к 4 версии Selenium, киньте Pull request

В будущем возможно будет добвлена асинхронная работа кода