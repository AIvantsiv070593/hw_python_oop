import datetime as dt
from datetime import timedelta as td

now_date = dt.datetime.now().date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, rec):
        self.records.append(rec)
        return self.records

    def get_today_stats(self):
        self.today_stats = 0
        for record in self.records:
            if record.date == now_date:
                self.today_stats += record.amount
        return self.today_stats

    def get_week_stats(self):
        self.week_stats = 0
        for record in self.records:
            if now_date >= record.date >= (now_date - td(days=7)):
                self.week_stats += record.amount
        return self.week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_remained = 0
        if self.limit > self.get_today_stats():
            calories_remained = self.limit - self.get_today_stats()
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{calories_remained} кКал')
        else:
            return ('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = 73.65
    EURO_RATE = 89.25

    def get_today_cash_remained(self, currency):
        cash_value_deafult = round((self.limit) - (self.get_today_stats()), 2)
        cash_value_usd = round((cash_value_deafult / self.USD_RATE), 2)
        cash_value_euro = round((cash_value_deafult / self.EURO_RATE), 2)
        if cash_value_deafult > 0:
            if currency == 'usd':
                return (f'На сегодня осталось {cash_value_usd} USD')
            elif currency == 'eur':
                return (f'На сегодня осталось {cash_value_euro} Euro')
            elif currency == 'rub':
                return (f'На сегодня осталось {cash_value_deafult} руб')
            else:
                return ('Введи валюту верно: usd, eur, rub')
        elif cash_value_deafult < 0:
            if currency == 'usd':
                return (f'Денег нет, держись: твой долг - '
                        f'{abs(cash_value_usd)} USD')
            elif currency == 'eur':
                return (f'Денег нет, держись: твой долг - '
                        f'{abs(cash_value_euro)} Euro')
            elif currency == 'rub':
                return (f'Денег нет, держись: твой долг - '
                        f'{abs(cash_value_deafult)} руб')
            else:
                return ('Введи валюту верно: usd, eur, rub')
        else:
            return ('Денег нет, держись')


class Record:
    def __init__(self, amount, comment, date=now_date):
        self.amount = amount
        self.comment = comment
        self.date = date
        if type(self.date) == str:
            self.date = dt.datetime.strptime(self.date, '%d.%m.%Y').date()
