# VaccineBotTO
VaccineBotTO on Twitter

[![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/to_vaccine.svg?style=social&label=Follow%20%40to_vaccine)](https://twitter.com/to_vaccine)

Project page: https://lindayi.me/vaccinebotto/

## Dependencies
- python (tested on 3.7.4)
- selenium (tested on 3.141.0)
- undetected_chromedriver (tested on 2.2.1)
- tweepy (tested on 3.10.0)
- gspread (tested on 3.7.0)
- pytz (tested on 2019.3)

## Setup
- For the detailed process of obtaining credentials for your Twitter account, please see https://realpython.com/twitter-bot-python-tweepy/#creating-twitter-api-authentication-credentials
- For the detailed process of obtaining credentials for your Google service account, please see https://docs.gspread.org/en/latest/oauth2.html

1. Update the following storage-related variables in `config.py`: `BASE_PATH`, `SHEET_URL_ID`, and optionally, `CRAWLER_FILE`.
2. Update the following credential variables in `config.py`: `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`, `TWITTER_ACCESS_KEY`, `TWITTER_ACCESS_SECRET`, `SHEET_KEY_FILE`.
3. Update the `CAPTCHA_KEY` for Verto Health API in `config.py`. The Key can be obtained by going to the Verto Health booking site, solve the CAPTCHA once, land on the date selection page and inspect the network request to the `availability` endpoint when you select any date. It is the string value in the `authorization` request header, in the format of `Bearer ...`. You only need to put what's after `Bearer` into the `CAPTCHA_KEY` variable in `config.py`.
4. (Optional) Modify any other configurations of interest in `config.py` to adjust the scope, behavior, and Tweet template.
5. Set up cron job to run the bot periodically. For example, `*/5 * * * * python3 /projects/vacbot/vacbot.py >> /projects/vacbot/output.log`
