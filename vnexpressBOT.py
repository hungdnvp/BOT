
#Craw
import Response as R
import json
import sys
import News
# telegram
import logging
# from telegram import __version__ as TG_VER
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
baseUrl = "https://vnexpress.net/"  
TOKEN = '6018262692:AAFZU5Pm05WeNlO5xRhhO15-yujLnLYaxmg'
#////////////////////$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$========================================

print("Bot Starting....")
# try:
#     from telegram import __version_info__
# except ImportError:
#     __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

# if __version_info__ < (20, 0, 0, "alpha", 1):
#     raise RuntimeError(
#         f"This example is not compatible with your current PTB version {TG_VER}. To view the "
#         f"{TG_VER} version of this example, "
#         f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
#     )

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

#################### handle #################
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text(f'Chào {update.effective_user.full_name}')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text("Bạn muốn tôi giúp gì? \n 1. Đọc báo -> /news <số lượng>")


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

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()