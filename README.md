cd tools
** pip install -r requirements.txt

test url: https://quotes.toscrape.com/


celery -A settings worker -l info
celery --app settings worker -l INFO