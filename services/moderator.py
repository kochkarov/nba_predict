import datetime

from member.models import Member


def make_prediction(date: datetime.date):
    member_bots = Member.objects.filter(is_bot=1)
    for predictor in member_bots:
        predictor.restore_bot()
