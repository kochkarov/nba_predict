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

    @staticmethod
    def make_all_prediction():
        data = DataNba()
        data.init_data(forced_call=True)
        leagues = League.objects.all()
        events = Event.objects.all()

        for league in leagues:
            bot_list = league.members.filter(is_bot=1)
            for event in tqdm(events):
                champ, _ = Championship.objects.get_or_create(name=f'{event.__str__()} {league.name}',
                                                              league=league, event=event)
                game_list = event.games.all().values_list('game_id', flat=True)
                for predictor in bot_list:
                    predictor.restore_bot()
                    y_predict = predictor.bot.make_predict(game_list)
                    Moderator.save_prediction(y_predict, member=predictor, champ=champ)
        return

    def make_prediction(self):
        data = DataNba()
        data.init_data(forced_call=True)
        bot_list = self.championship.league.members.filter(is_bot=1)
        game_list = self.championship.event.games.all().values_list('game_id', flat=True)
        for predictor in tqdm(bot_list):
            predictor.restore_bot()
            y_predict = predictor.bot.make_predict(game_list)
            self.save_prediction(y_predict, member=predictor, champ=self.championship)
        return

    @staticmethod
    def save_prediction(prediction_list: list[dict], member: Member, champ: Championship):
        for element in prediction_list:
            element['game'] = Game.objects.get(game_id=element['game_id'])
            element['member'] = member
            predict, _ = Prediction.objects.update_or_create(game=element['game'], member=element['member'],
                                                             defaults=element)
            score, _ = Score.objects.update_or_create(prediction=predict)
            champ.scoreboard.add(score)
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
            rate = 1 - game_scores.aggregate(rate=Avg('result'))['rate']
            game_scores.filter(result=1).update(rate=rate)
        return

    @staticmethod
    def create_events():
        min_games = 20
        games = Game.objects.filter(game_date__gte=datetime.date(2021, 3, 8))
        dates = games.values_list('game_date', flat=True).order_by('game_date').distinct()
        total_games = 0
        date_list = []
        for cur_date in dates:
            total_games += len(games.filter(game_date=cur_date))
            date_list.append(cur_date)
            if total_games >= min_games:
                event, _ = Event.objects.get_or_create(name=str(cur_date))
                event.games.add(*games.filter(game_date__in=date_list))
                total_games = 0
                date_list = []
