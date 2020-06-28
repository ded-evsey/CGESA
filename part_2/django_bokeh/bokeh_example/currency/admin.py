from django.contrib import admin
from .models import Currency, CurrencyPerDate
import requests
import datetime
# Register your models here.


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', ]

    def sync_currency_name(self, request, queryset):
        req = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        if req.status_code != 200:
            return
        for item in req.json().get('Valute').values():
            obj = self.model
            obj.objects.get_or_create(name=item['Name'], code=item['CharCode'])

    actions = [sync_currency_name, ]


@admin.register(CurrencyPerDate)
class CurrencyPerDateAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ['currency', 'value', 'nominal', 'date']

    def sync_currency_value_per_week(self, request, queryset):
        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        day_sync = 0
        currency = Currency.objects.all()
        obj = self.model
        while day_sync != 7:
            req = requests.get(url)
            if req.status_code != 200:
                return
            for cur in currency:
                data = req.json()['Valute'].get(cur.code)
                if not data:
                    continue
                date = datetime.datetime.strptime(
                    req.json()['Date'].split('+')[0],
                    '%Y-%m-%dT%H:%M:%S'
                )
                cur_obj, created = obj.objects.get_or_create(
                    currency=cur,
                    date=date.date()
                )
                cur_obj.value = data['Value']
                cur_obj.nominal = data['Nominal']
                cur_obj.save()
                url = 'http:' + req.json()['PreviousURL']
            day_sync += 1

    actions = [sync_currency_value_per_week]
