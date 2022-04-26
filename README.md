# Instagram Image Scraper
Скрапер для скачивания картинок из Instagram'а по тэгам.

## Installation
```
$ pip install -r requirements.txt
```
Также в папке `imagescraper/` должен находиться `chromedriver`.

## Usage
Для первого запуска понадобится войти в аккаунт Instagram:
```
$ scrapy crawl instagram -a is_login=True -a username=<username> -a password=<password> -a tags=<tag1>,<tag2>,<tag3>
```
После первого запуска сохранится файл cookies.pkl. Поэтому можно запускать скрапер таким образом:
```
$ scrapy crawl instagram -a is_login=False -a tags=<tag1>,<tag2>,<tag3>
```
В папке `imagescraper/images/` будет сохранен результат работы скрапера.