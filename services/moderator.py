import datetime

from game.models import Game
from member.models import Member
from services.database import DataNba


class Moderator:
    def __init__(self):
        pass

    @staticmethod
    def get_game_list(date: datetime.date):
        return list(Game.objects.filter(game_date=date).values_list('game_id', flat=True))

    def make_prediction(self, date: datetime.date):
        data = DataNba(forced_call=True)
        bot_list = Member.objects.filter(is_bot=1)
        game_list = self.get_game_list(date)
        for predictor in bot_list:
            predictor.restore_bot()
            predictor.bot.make_predict(game_list)
