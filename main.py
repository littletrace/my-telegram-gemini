import os
from google import genai
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 환경 변수 불러오기
TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")
PORT = int(os.environ.get('PORT', 10000))
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL") 

# 제미나이 클라이언트 설정 (최신 패키지 방식)
client = genai.Client(api_key=GEMINI_KEY)

# /ask 명령어 처리 함수
async def ask_gemini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = " ".join(context.args)
    
    if not user_query:
        await update.message.reply_text("질문을 함께 입력해주세요! 예: /ask 오늘 서울 날씨 어때?")
        return
    
    # 봇이 "입력 중..." 상태를 표시
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    try:
        # 제미나이에게 질문하고 답변 받기 (최신 패키지 문법)
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=user_query
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    # 봇 어플리케이션 생성
    application = Application.builder().token(TOKEN).build()
    
    # /ask 명령어 핸들러 추가
    application.add_handler(CommandHandler("ask", ask_gemini))
    
    # 웹훅 실행 (requirements.txt의 [webhooks] 옵션이 있어야 정상 작동)
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{RENDER_URL}/webhook"
    )
