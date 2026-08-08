import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import requests

# Reemplaza esto con el token que te dio BotFather
TOKEN = "8647748276:AAFoEw5TmEp5fJTDctxAyeiNHR93C23k_Ak"
FLASK_URL = "http://localhost:5000/chat"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pregunta_usuario = update.message.text
    
    # Opcional: Indicar que el bot está escribiendo
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # Hacemos la petición a tu API de Flask existente
        payload = {
            "pregunta": pregunta_usuario,
            "rol": 5 # Puedes definir un rol por defecto o extraerlo del usuario
        }
        response = requests.post(FLASK_URL, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            respuesta_rag = data.get("respuesta", "No se obtuvo respuesta.")
        else:
            respuesta_rag = "Hubo un error al comunicarse con el servidor del RAG."
            
    except Exception as e:
        respuesta_rag = f"Error de conexión: {str(e)}"

    # Responder al usuario en Telegram
    await update.message.reply_text(respuesta_rag)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # Escoger cualquier mensaje de texto que no sea un comando
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot de Telegram iniciado...")
    app.run_polling()