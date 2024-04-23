from typing import List, Optional
from datetime import datetime
import src

from dateutil import parser

current_time: int = 0
update_queue: List[int] = []


class TimeKeeper:
    """ A class that counts the days and
    catalyzes the updating of accounts according to their tariffs. """

    def add(self, account: int):
        update_queue.append(account)

    def current_time(self):
        ct = current_time
        return ct

    def increase(self):
        for account in update_queue:
            src.SingleDO.DO().get(account, "Account").update()
            src.SingleDO.DO().done_with(account, "Account")
        global current_time
        current_time += 1

    def get(self) -> int:
        global current_time
        return current_time

    def update(self):
        print("\nUpdating accounts...\n")
        dm = __import__("src.miptpaydj.mainapp.models").DiaryModel
        am = __import__("src.miptpaydj.mainapp.models").AccountModel
        diary = dm.objects.get(parameter="Date")
        print(diary.value)
        dt = parser.parse(str(diary.value))
        print(dt)
        print(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        print(datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second))
        delta = datetime.now() - datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        match src.TIME:
            case "SECOND":
                delta = delta.days * 24 * 3600 + delta.seconds
            case "MINUTE":
                delta = delta.days * 24 * 60 + delta.seconds // 60
            case "HOUR":
                delta = delta.days * 24 + delta.seconds // 3600
            case "DAY":
                delta = delta.days
        print("Delta is", delta)
        for account_ in am.objects.all():
            account = src.SingleDO.DO().get(account_.id, "Account")
            account.update(delta)
            src.SingleDO.DO().done_with(account_.id, "Account")
        diary.value = datetime.now()
        diary.save()


class SingleTK:
    """Singleton wrapper for TimeKeeper class"""
    __timekeeper: Optional[TimeKeeper] = None

    def __init__(self):
        pass

    @classmethod
    def timekeeper(cls) -> TimeKeeper:
        if SingleTK.__timekeeper is None:
            SingleTK.__timekeeper = TimeKeeper()
        return SingleTK.__timekeeper
