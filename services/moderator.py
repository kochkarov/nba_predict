import datetime

from django.db.models import Avg
from tqdm.auto import tqdm

from game.models import Game
from member.models import Member
from services.database import DataNba
from championship.models import Championship, League, Score, Event, Prediction


class Moderator:
    def __init__(self, championship=None):
        self.championship = championship
        return

    @staticmethod
    def create_championship():
        members = Member.objects.all()
        league, _ = League.objects.get_or_create(name='Rusanovka')
        league.members.add(*members)

        games = Game.objects.filter(game_date__gte=datetime.date(2021, 5, 13))
        event, _ = Event.objects.get_or_create(name='LastWeek')
        event.games.add(*games)

        champ, _ = Championship.objects.get_or_create(name='Test championship', league=league, event=event)
        return champ

    def make_prediction(self):
        data = DataNba()
        data.init_data(forced_call=True)
        bot_list = self.championship.league.members.filter(is_bot=1)
        game_list = self.championship.event.games.all().values_list('game_id', flat=True)
        for predictor in tqdm(bot_list):
            predictor.restore_bot()
            y_predict = predictor.bot.make_predict(game_list)
            self.save_prediction(y_predict, member=predictor)
        return

    def save_prediction(self, prediction_list: list[dict], member: Member):
        for element in prediction_list:
            element['game'] = Game.objects.get(game_id=element['game_id'])
            element['member'] = member
            predict, _ = Prediction.objects.update_or_create(game=element['game'], member=element['member'],
                                                             defaults=element)
            score, _ = Score.objects.update_or_create(prediction=predict)
            self.championship.scoreboard.add(score)
        return

    def calc_result(self):
        scores = self.championship.scoreboard.all()
        for game in self.championship.event.games.filter(is_win__isnull=True):
            game.save()
        for score in scores:
            score.result = 1 if score.prediction.predict == score.prediction.game.is_win else 0
            score.save()
        for game in self.championship.event.games.all():
            game_scores = scores.filter(prediction__game=game)
            rate = game_scores.aggregate(rate=Avg('result'))['rate']
            game_scores.filter(result=1).update(rate=rate)
