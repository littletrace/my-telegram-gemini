import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 환경 변수 불러오기
TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")
PORT = int(os.environ.get('PORT', 10000))
# Render가 자동으로 발급하는 본인 서버 주소입니다.
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL") 

# 제미나이 설정
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# /ask 명령어 처리 함수
async def ask_gemini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 사용자가 입력한 질문 추출
    user_query = " ".join(context.args)
    
    # 질문이 비어있을 경우 안내
    if not user_query:
        await update.message.reply_text("질문을 함께 입력해주세요! 예: /ask 오늘 서울 날씨 어때?")
        return
    
    # 봇이 "입력 중..." 상태를 표시하게 만듦 (선택사항)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    # 제미나이에게 질문하고 답변 받기
    response = model.generate_content(user_query)
    
    # 텔레그램 그룹에 답변 전송
    await update.message.reply_text(response.text)

if __name__ == "__main__":
    # 봇 어플리케이션 생성
    application = Application.builder().token(TOKEN).build()
    
    # /ask 명령어 핸들러 추가
    application.add_handler(CommandHandler("ask", ask_gemini))
    
    # 수동 설정 없이 봇이 알아서 웹훅을 연결하고 실행합니다.
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{RENDER_URL}/webhook"
    )
