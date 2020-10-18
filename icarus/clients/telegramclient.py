
from icarus.clients.superclient import SuperClient
from icarus.logging import icarus_logger

from telegram.ext import Updater, Filters, MessageHandler
from telegram.error import InvalidToken, TelegramError

import speech_recognition as sr
BOT_TOKEN = ""


class TelegramClient(SuperClient):

    updater = None
    dispatcher = None
    CONTEXT_IDENT = "context"

    def run(self):
        try:
            # init connection
            self.updater = Updater(token=self.persistence.get_config('Telegram', 'token'), use_context=True)
            self.dispatcher = self.updater.dispatcher
        except InvalidToken:
            icarus_logger.error("Telegram Token invalid")
            return

        # append handler
        text_handler = MessageHandler(Filters.text, self.incoming_message_handler)
        voice_handler = MessageHandler(Filters.voice, self.incoming_voice_handler)
        self.dispatcher.add_handler(text_handler)
        self.dispatcher.add_handler(voice_handler)

        # start responding
        self.updater.start_polling()

    def incoming_message_handler(self, sender, more):
        # old implementation: self._queue_new_message(context.message.text, {self.CONTEXT_IDENT: context})
        self._queue_new_message(sender.message.text, {self.CONTEXT_IDENT: sender})

    def incoming_voice_handler(self, sender, more):
        # process audio
        try:
            link = sender.message.voice.get_file()
            link.download("telegram.opus")
        except TelegramError:
            print("Could not load file")
        processed_text = ""

        # todo: does not work, must be wav or flac
        try:
            r = sr.Recognizer()
            with sr.AudioFile("telegram.opus") as source:
                processed_text = r.recognize_google(source)

            print(f"recognized: {processed_text}")
            self._queue_new_message(processed_text, {self.CONTEXT_IDENT: sender})
        except:
            self.send("I do not support voice messages - yet", {self.CONTEXT_IDENT: sender})


    def send(self, message: str, client_attr):
        context = client_attr[self.CONTEXT_IDENT]
        context.message.reply_text(message)

    def stop(self):
        icarus_logger.info("stopping telegram client")
        self.updater.stop()

