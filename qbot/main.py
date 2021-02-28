import logging
import random
import uuid
from typing import Collection

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import CallbackContext, CommandHandler, InlineQueryHandler, Updater

logger: logging.Logger = logging.getLogger(__name__)


class QBot:
    def __init__(self, token: str, replies: Collection[str]) -> None:
        self.token = token
        self.replies = replies
        reply_factory = self._reply_factory()
        self.reply = reply_factory.__next__
        logger.info("QBot initialized, %d replies", len(replies))

    def _reply_factory(self) -> str:
        while True:
            replies = self.replies.copy()
            random.shuffle(replies)
            for reply in replies:
                yield reply

    def q_response(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(self.reply())

    def q_inline(self, update: Update, context: CallbackContext) -> None:
        reply = self.reply()
        results = [
            InlineQueryResultArticle(
                id=uuid.uuid4(),
                title=f"{reply[0:5]}...",
                input_message_content=InputTextMessageContent(reply),
            ),
        ]
        update.inline_query.answer(results)

    def start(self) -> None:
        updater = Updater(self.token)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("q", self.q_response))
        dispatcher.add_handler(InlineQueryHandler(self.q_inline))
        updater.start_polling()
        updater.idle()
