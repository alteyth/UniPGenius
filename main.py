from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import lib

# TOKEN: Final = "TELEGRAM TOKEN HERE"
# openai.api_key = "OPENAI TOKEN HERE"

# Messaggio placeholder di attesa una volta ricevuta una richiesta
must_delete: Update.message


# Comando /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    if message_type == "private":
        await update.message.reply_text(lib.benvenuto)

    if message_type == "group" or message_type == "supergroup":
        # Il messaggio di benvenuto nei gruppi/supergruppi viene inviato solo se il tag è presente nel comando
        if lib.BOT_USERNAME in text:
            await update.message.reply_text(lib.benvenuto_gruppo)


# Funzione che gestisce i messaggi ricevuti dal bot
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global must_delete
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Gestione dei messaggi in chat privata
    if message_type == "private":
        # Controllo per i comandi non validi
        if "/" in text:
            await update.message.reply_text(lib.command_error_message)
            return

        must_delete = await update.message.reply_text(lib.placeholder)

        response = create_response(text)

        # Richiesta è andata a buon fine, il messaggio di attesa è eliminato e sostituito dalla risposta generata
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=must_delete.message_id)
        await update.message.reply_text(response)

    # Gestione dei messaggi in gruppi o supergruppi
    if message_type == "group" or message_type == "supergroup":
        # Verifica della presenza del tag del bot nel messaggio
        if lib.BOT_USERNAME in text:
            # Controllo per i comandi non validi
            if "/" in text:
                await update.message.reply_text(lib.command_error_message)
                return

            must_delete = await update.message.reply_text(lib.placeholder)

            # Viene rimosso il tag del bot dalla richiesta
            new_text: str = text.replace(lib.BOT_USERNAME, "").strip()

            response = create_response(new_text)

            # Richiesta è andata a buon fine, il messaggio di attesa è eliminato e sostituito dalla risposta generata
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=must_delete.message_id)
            await update.message.reply_text(response)
        else:
            # Se il tag non è presente nel messaggio la richiesta viene ignorata
            return


# Funzione che si occupa dell'invio e completamento della richiesta tramite le API di OpenAI
def create_response(text: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Rispondi solamente in italiano"},
                  {"role": "user", "content": text}],
        temperature=1
    )
    # "Response" è un dizionario con al suo interno altre strutture dati, in questo modo accedo alla risposta
    return response["choices"][0]["message"]["content"]


# Gestore degli errori
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"{update}\n{context.error}")

    # Se sono state effettuate più di 3 richieste in un minuto viene restituito un messaggio di errore
    if openai.error.RateLimitError:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=must_delete.message_id)
        await update.message.reply_text(lib.rate_limit_error_message)


if __name__ == '__main__':
    print("Avviando il Bot...")
    # Istanziamento del Bot
    app = Application.builder().token("---TELEGRAM TOKEN HERE---").build()

    # Gestione dei comandi
    app.add_handler(CommandHandler("start", start_command))

    # Gestione dei messaggi
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Gestione degli errori
    app.add_error_handler(error)

    # Avvio del polling
    print("Polling...")
    app.run_polling(poll_interval=1)
