
from src.Clients.superclient import SuperClient
from logger import icarus_logger

from telegram.ext import Updater, Filters, MessageHandler
BOT_TOKEN = "839599567:AAHy91zA1ePG4vbwlwz-_9prlsPJ1dnkteE"


class TelegramClient(SuperClient):

    updater = None
    dispatcher = None
    CONTEXT_IDENT = "context"

    def run(self):
        # init connection
        self.updater = Updater(token=BOT_TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher

        # append handler
        echo_handler = MessageHandler(Filters.text, self.incoming_message_handler)
        self.dispatcher.add_handler(echo_handler)

        # start responding
        self.updater.start_polling()

    def incoming_message_handler(self, sender):
        # old implementation: self._queue_new_message(context.message.text, {self.CONTEXT_IDENT: context})
        self._queue_new_message(sender.message.text, {self.CONTEXT_IDENT: sender})

    def send(self, message: str, client_attr):
        context = client_attr[self.CONTEXT_IDENT]
        context.message.reply_text(message)

    def stop(self):
        icarus_logger.info("stopping telegram client")
        self.updater.stop()

