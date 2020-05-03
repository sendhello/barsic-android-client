# -*- coding: utf-8 -*-

from kivy.uix.screenmanager import Screen

import os

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.weakproxy import WeakProxy

from kivymd.uix.picker import MDDatePicker, MDLabel
from datetime import datetime, timedelta
from kivymd.uix.button import MDRectangleFlatIconButton

from uix.lists import (
    OneLineLeftAvatarItem,
)
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem
from kivy.metrics import dp
from kivy.properties import NumericProperty


class DateDialogsContent(BoxLayout):
    app = ObjectProperty()




class TotalReport(Screen):
    app = ObjectProperty()
    custom_dialog = None

    def set_date_from(self, date_obj):
        self.app.date_from = date_obj
        self.ids.date_from.text = date_obj.strftime('%d-%m-%Y')
        if self.ids.period.text == 'Период:' and self.app.date_to < self.app.date_from:
            self.set_date_to(date_obj)

    def set_date_to(self, date_obj):
        self.app.date_to = date_obj
        self.ids.date_to.text = date_obj.strftime('%d-%m-%Y')
        if self.app.date_to < self.app.date_from:
            self.set_date_from(date_obj)

    def show_date_from(self):
        pd = self.app.date_from
        try:
            MDDatePicker(self.set_date_from, pd.year, pd.month, pd.day).open()
        except AttributeError:
            MDDatePicker(self.set_date_from).open()

    def show_date_to(self):
        pd = self.app.date_to
        try:
            MDDatePicker(self.set_date_to, pd.year, pd.month, pd.day).open()
        except AttributeError:
            MDDatePicker(self.set_date_to).open()

    def clear_dates(self):
        if 'date_from' in self.ids:
            self.remove_widget(self.ids.date_from)
            self.ids.pop('date_from')
        if 'date_to' in self.ids:
            self.remove_widget(self.ids.date_to)
            self.ids.pop('date_to')

    def add_date_widgets(self, date_to=False):
        date_from_button = MDRectangleFlatIconButton(
            text=self.app.date_from.strftime('%d-%m-%Y'),
            icon="timetable",
            pos_hint={'center_x': .5, 'center_y': .8},
            size_hint=(0.8, 0.07),
            on_release=lambda x: self.show_date_from()
        )
        self.ids['date_from'] = WeakProxy(date_from_button)
        self.add_widget(date_from_button)
        self.app.date_to = self.app.date_from
        if date_to:
            date_to_button = MDRectangleFlatIconButton(
                text=self.app.date_to.strftime('%d-%m-%Y'),
                icon="timetable",
                pos_hint={'center_x': .5, 'center_y': .7},
                size_hint=(0.8, 0.07),
                on_release=lambda x: self.show_date_to()
            )
            self.ids['date_to'] = WeakProxy(date_to_button)
            self.add_widget(date_to_button)

    def set_today(self):
        self.ids.period.text = 'Сегодня'
        self.clear_dates()
        self.app.date_from = datetime.now().date()
        self.app.date_to = self.app.date_from

    def set_yesterday(self):
        self.ids.period.text = 'Вчера'
        self.clear_dates()
        self.app.date_from = datetime.now().date() - timedelta(days=1)
        self.app.date_to = self.app.date_from

    def set_date(self):
        self.ids.period.text = 'Число:'
        self.clear_dates()
        self.add_date_widgets()

    def set_period(self):
        self.ids.period.text = 'Период:'
        self.clear_dates()
        self.add_date_widgets(date_to=True)

    def bottom_sheet(self):
        from kivymd.uix.bottomsheet import MDListBottomSheet

        bs_menu_period = MDListBottomSheet()
        bs_menu_period.add_item(
            "Сегодня",
            lambda x: self.set_today(),
            icon="clipboard-account",
        )
        bs_menu_period.add_item(
            "Вчера",
            lambda x: self.set_yesterday(),
            icon="clipboard-account",
        )
        bs_menu_period.add_item(
            "Число",
            lambda x: self.set_date(),
            icon="clipboard-account",
        )
        bs_menu_period.add_item(
            "Период",
            lambda x: self.set_period(),
            icon="clipboard-account",
        )
        bs_menu_period.open()






