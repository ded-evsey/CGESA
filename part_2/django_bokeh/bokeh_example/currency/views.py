import datetime
import pandas as pd
from bokeh.plotting import figure, output_file
from bokeh.palettes import Category20c
import math
from bokeh.transform import cumsum
from bokeh.embed import components
from django.views.generic import FormView
from django.shortcuts import render
from .models import Currency, CurrencyPerDate
from .forms import SelectCurForms
# Create your views here.


class MainView(FormView):
    template_name = 'base.html'
    form_class = SelectCurForms

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['max_data'] = datetime.date.today()
        context['min_data'] = datetime.date.today() - datetime.timedelta(weeks=1)
        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        pd_keys = [
            'date',
            'value',
            'nominal',
            'currency_id'
        ]
        data = pd.DataFrame(
            CurrencyPerDate.objects.filter(
                currency__in=[cleaned_data['main'], cleaned_data['sub']],
                date__gte=cleaned_data['date_from'],
                date__lte=cleaned_data['date_to'],
            ).values(
                *pd_keys
            )
        ).set_index(['currency_id', 'date'])
        x = list()
        y = list()
        for day in pd.date_range(cleaned_data['date_from'], cleaned_data['date_to']):
            date = day.date().strftime('%Y-%m-%d')
            try:
                main_data = data.loc[cleaned_data['main'].id].loc[date]
                sub_data = data.loc[cleaned_data['sub'].id].loc[date]
                val = float(main_data['value'].loc[date]) / float(sub_data['value'].loc[date])
                nominal = float(sub_data['nominal'].loc[date]) / float(main_data['nominal'].loc[date])
                y.append(
                    val * nominal * 100
                )
                x.append(date)
            except KeyError:
                continue
        plot = figure(
            title=f'Стоимость '
                  f'{cleaned_data["main"]} '
                  f'к {cleaned_data["sub"]} '
                  f'в переод с '
                  f'{cleaned_data["date_from"]} по '
                  f'{cleaned_data["date_to"]}',
            y_axis_label=f'Курс {cleaned_data["main"].code} при покупке 100 единиц валюты',
            x_axis_label='Даты',
            plot_width=900,
            plot_height=400,
            x_range=x
        )
        plot.line(x, y, line_width=4)
        plot_pie = figure(
            title=f'Стоимость '
                  f'{str(cleaned_data["main"])} '
                  f'к {str(cleaned_data["sub"])} '
                  f'в переод с '
                  f'{cleaned_data["date_from"]} по '
                  f'{cleaned_data["date_to"]}',
            plot_height=400,
            plot_width=900,
            tools="hover",
            tooltips="@date_str: @value",
        )
        data_pie = pd.Series(dict(zip(x, y))).reset_index(name='value').rename(columns={'index': 'date_str'})
        data_pie['angle'] = data_pie['value'] / data_pie['value'].sum() * 2 * math.pi

        plot_pie.wedge(x=0, y=1, radius=0.4,
                       start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                       line_color="blue", fill_color='green', legend_field='date_str', source=data_pie)
        plot_pie.axis.axis_label = None
        plot_pie.axis.visible = False
        plot_pie.grid.grid_line_color = None
        script, div = components(plot)
        script_pie, div_pie = components(plot_pie)
        return render(
            self.request,
            self.template_name,
            {
                'script': script,
                'div': div,
                'form': self.form_class(),
                'script_pie': script_pie,
                'div_pie': div_pie
            }
        )
