# Scraping by Scrapy And save Data to the database

I made this project by [Scrapy](https://scrapy.org/) and [Django](https://www.djangoproject.com/) .

Screenshot :


![Screenshot](Screenshot.png)
## Run

### Create and activate virtual env

    python3 -m venv venv
    . ./venv/bin/activate

### Install dependencies

    pip install -r requirements.txt

### Run django
    python manage.py runserver
### create superuser
    python manage.py createsperuser

## Check spiders contracts

    scrapy check codal

### Scrap

    scrapy crawl codal
