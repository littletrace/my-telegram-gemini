import os
import google.generativeai as genai
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 환경 변수 설정 (Render에서 입력할 예정)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
app = Flask(__name__)

# /ask 명령어를 처리하는 함수
async def ask_gemini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = " ".join(context.args)
    if not user_query:
        await update.message.reply_text("질문을 함께 입력해주세요! 예: /ask 안녕?")
        return
    
    response = model.generate_content(user_query)
    await update.message.reply_text(response.text)

# 봇 구동 설정
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("ask", ask_gemini))

@app.route('/webhook', methods=['POST'])
def webhook():
    # 텔레그램으로부터 메시지를 받는 통로
    return "OK"

if __name__ == "__main__":
    # 포트 설정 (Render 기본값)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
