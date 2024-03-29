import datetime as dt
from datetime import timedelta as td


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, rec):
        """Создает список записей."""
        self.records.append(rec)

    def get_today_stats(self):
        """Статистика за день."""
        self.today_stats = 0
        now_date = dt.date.today()
        self.today_stats = sum(
            [record.amount for record in self.records
                if record.date == now_date])
        return self.today_stats

    def get_week_stats(self):
        """Статистика за последние 7 дней."""
        self.week_stats = 0
        now_date = dt.date.today()
        next_days = (now_date - td(days=6))
        self.week_stats = sum(
            [record.amount for record in self.records
                if now_date >= record.date >= next_days])
        return self.week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """Получаем остаток по каллориям на день."""
        if self.limit > self.get_today_stats():
            calories_remained = self.limit - self.get_today_stats()
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{calories_remained} кКал')
        return ('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = 73.65
    EURO_RATE = 89.25
    RUB_RATE = 1

    def get_today_cash_remained(self, currency):
        """Получаем информацию об остатках денег на день."""

        dict = {'usd': {self.USD_RATE: 'USD'},
                'eur': {self.EURO_RATE: 'Euro'},
                'rub': {self.RUB_RATE: 'руб'}
                }
        cash_value_deafult = round((self.limit) - (self.get_today_stats()), 2)
        try:
            for key, value in dict[currency].items():
                cash_value = round(cash_value_deafult / key, 2)
                if cash_value > 0:
                    return (f'На сегодня осталось {cash_value} {value}')
                elif cash_value < 0:
                    return (f'Денег нет, держись: твой долг - '
                            f'{abs(cash_value)} {value}')
                else:
                    return ('Денег нет, держись')
        except KeyError:
            return ('Такой валюты нет')


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = date
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(self.date, '%d.%m.%Y').date()
