
#Craw
import os
import Response as R
import json
import sys
import News
import datetime
import pytz
# telegram
import logging
from telegram import __version__ as TG_VER
from telegram import  Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters,Defaults
baseUrl = "https://vnexpress.net/"  
TOKEN = os.environ.get('BOT_TOKEN')
#////////////////////$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$========================================

print("Bot Starting....")
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

QUEUE_DATA = ['duy','quang hùng','quang huy','quang sang']
INDEX = -1
# Định nghĩa đối tượng timezone cho múi giờ ICT (GMT+7)
ict_tz = pytz.timezone('Asia/Ho_Chi_Minh')
defaults = Defaults(tzinfo=ict_tz)
DAILY_TIME = datetime.time(hour=22, minute=0, second=0,tzinfo=ict_tz)
#################### handle #################
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text(f'Chào {update.effective_user.full_name}')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text("Bạn muốn tôi giúp gì? \n \
  1. Đọc báo -> /news <số lượng>\n \
  2. thời gian -> time?\n \
  3. ok -> ok, hi")


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  try:
    limit_news = int(context.args[0]) # Lấy tham số từ input truyền vào -> cào về bao nhiêu tin
    news = News.GetNews(limit_news)
    for x in range(0, len(news)): # Deserialize dữ liệu json trả về từ file News.py lúc nãy
      message = json.loads(news[x])
      await update.message.reply_text(message['title'] + "\n" 
        + message['link'] + "\n" + message['description'])
  except (IndexError, ValueError):
    await update.message.reply_text('Vui lòng chọn số lượng tin hiển thị!!')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  text = str(update.message.text).lower()
  response = R.sample_response(text)
  await update.message.reply_text(response)

 # Function dùng để xác định lỗi gì khi có thông báo lỗi
def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
  print(f"Update {update} cause error {context.error}")


##########################T____I____M____E##########
async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    global INDEX
    job = context.job
    output = []
    for i in range(2):
        output.append(job.data[INDEX])
        INDEX = (INDEX +2) % (len(job.data))
    await context.bot.send_message(job.chat_id, text=f"Quét vệ sinh!\n {[i for i in output]}")

def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global INDEX
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    try:
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_daily(alarm, time=DAILY_TIME, days=tuple(range(7)),chat_id=chat_id, name=str(chat_id), data=QUEUE_DATA)

        text = "Timer successfully set!"
        if job_removed:     # khi set 2 lan lien tuc thi cai sau se thay the cai trc
            text += " Old one was removed."
        await  update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <seconds>")  

async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
    await update.message.reply_text(text)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("news", news_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    ## set timmer
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()