from bnx.database.utils import SelfFillClass
import datetime

class User(SelfFillClass):

    fields = ['id', 'login', 'password', 'email', 'rights', 'reg_time', 'rec_time']
    types = [int, str, str, str, int, None, None]

