import os
import time
import locale
import requests
import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from tempfile import mkdtemp

# URL de CSSBattle
CSSBATTLE_URL = "https://cssbattle.dev"

# En local, on charge .env s'il existe
if os.path.exists('.env'):
    from dotenv import load_dotenv
    load_dotenv()

# Récupération de la variable
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "https://default-or-none")

locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")


def get_daily_battle():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument(f"--user-data-dir={mkdtemp()}")
    chrome_options.add_argument(f"--data-path={mkdtemp()}")
    chrome_options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    chrome_options.add_argument("--remote-debugging-pipe")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--log-path=/tmp")
    chrome_options.binary_location = "/opt/chrome/chrome-linux64/chrome"

    service = Service(
        executable_path="/opt/chrome-driver/chromedriver-linux64/chromedriver",
        service_log_path="/tmp/chromedriver.log",
    )

    driver = webdriver.Chrome(service=service, options=chrome_options)
    # Open a webpage
    driver.get("https://cssbattle.dev")
    time.sleep(2)  # Attendre que le JavaScript charge la page

    # Récupérer le HTML rendu
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    battle = soup.find("div", lambda x: x and "target-today" in x)

    if not battle:
        return None

    battle_link = CSSBATTLE_URL + battle.find("a")["href"]
    battle_image = battle.find("img")["src"]

    return battle_link, battle_image


def send_slack_message():
    """Envoie le défi du jour sur Slack"""
    battle = get_daily_battle()
    print(battle)
    if battle:
        battle_link, battle_image = battle
        message = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"🔥 Défi CSSBattle du {datetime.date.today().strftime('%A %d %B %Y')}! 🎯\n👉 {battle_link}",
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": battle_image,
                        "alt_text": "CSSBattleOfTheDay",
                    },
                }
            ]
        }
        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        print(f"Message envoyé avec statut: {response.status_code}")
        return message
    else:
        print("Impossible de récupérer le défi du jour.")


def lambda_handler(event, context):
    return send_slack_message()
