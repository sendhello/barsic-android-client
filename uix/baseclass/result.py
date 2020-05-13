# -*- coding: utf-8 -*-

from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable


class Result(Screen):
    app = ObjectProperty()
    custom_dialog = None

    def __init__(self, **kwargs):
        super(Result, self).__init__(**kwargs)
        self.data = None

    def convert_to_tuple(self, data):
        table = []
        for service_type, groups in data.items():
            table.append((service_type, '', ''))
            for group, services in groups.items():
                table.append((f"<<<{group[:group.find('-')].upper()}>>>", '', ''))
                for service, numbers in services.items():
                    table.append((service, numbers['count'], f"{numbers['sum']:.2f} ₽"))
        return table

    def open_table(self, use_checkbox_state=False, use_pagination_state=False):
        if self.data.get('report_type') == 'total_report':
            data_tables = MDDataTable(
                size_hint=(0.9, 0.9),
                use_pagination=use_pagination_state,
                check=use_checkbox_state,
                rows_num=1000,
                column_data=[
                    ("Услуга", dp(70)),
                    ("Кол-во", dp(30)),
                    ("Стоимость", dp(30)),
                ],
                row_data=self.convert_to_tuple(self.data.get('data').get('report')),
            )
            data_tables.open()
