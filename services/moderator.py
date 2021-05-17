import datetime

from game.models import Game
from member.models import Member
from prediction.models import Prediction
from services.database import DataNba


class Moderator:
    def __init__(self):
        pass

    @staticmethod
    def get_game_list(date: datetime.date):
        return list(Game.objects.filter(game_date=date).values_list('game_id', flat=True))

    @staticmethod
    def save_prediction(prediction_list: list[dict], member: Member):
        for element in prediction_list:
            element['game'] = Game.objects.get(game_id=element['game_id'])
            element['game_date'] = element['game'].game_date
            element['member'] = member
            Prediction.objects.update_or_create(game=element['game'], member=element['member'],
                                                defaults=element)
        return

    def make_prediction(self, date: datetime.date):
        data = DataNba()
        data.init_data(forced_call=True)

        bot_list = Member.objects.filter(is_bot=1)
        game_list = self.get_game_list(date)
        for predictor in bot_list:
            predictor.restore_bot()
            y_predict = predictor.bot.make_predict(game_list)
            self.save_prediction(y_predict, member=predictor)
