import logging
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, JobQueue
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

URL = "https://app.testcenter.kz/profile/applications/2"
current_content = ""

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Бот запущен и начал отслеживание изменений на странице.')
    context.job_queue.run_repeating(check_page, interval=300, first=0, context=update.message.chat_id)

def get_page_content():
    options = Options()
    options.add_argument("--headless=new")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL)
    content = driver.find_element(By.TAG_NAME, "body").text
    driver.quit()
    return content


def check_page(context: CallbackContext) -> None:
    job = context.job
    global current_content
    new_content = get_page_content()

    if new_content != current_content:
        if current_content != "":
            context.bot.send_message(chat_id=job.context, text='Обнаружены изменения на странице!')
        current_content = new_content
        print(current_content)


def main() -> None:
    token = '7007694957:AAGiz6Diu3kOQo4ue0Q_Rqps4uOWTJP9gnc'
    bot = Bot(token)
    updater = Updater(bot=bot, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()