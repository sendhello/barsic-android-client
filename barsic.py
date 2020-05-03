# -*- coding: utf-8 -*-

import os
import sys
from ast import literal_eval
from datetime import datetime, timedelta
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.logger import PY2
from kivy.clock import Clock
from kivy.utils import get_hex_from_color
from kivy.properties import ObjectProperty, StringProperty

from main import __version__
from uix.baseclass.translation import Translation
from uix.baseclass.startscreen import StartScreen
from uix.lists import Lists

from kivymd.app import MDApp
from kivymd.toast import toast

from applibs.dialogs.dialogs import card


class Barsic(MDApp):
    title = 'barsic'
    icon = 'icon.png'
    nav_drawer = ObjectProperty()
    action_bar = ObjectProperty()
    lang = StringProperty('ru')
    date_from = ObjectProperty()
    date_to = ObjectProperty()

    def __init__(self, **kvargs):
        super(Barsic, self).__init__(**kvargs)
        Window.bind(on_keyboard=self.events_program)
        Window.soft_input_mode = 'below_target'

        self.list_previous_screens = ['base']
        self.window = Window
        self.config = ConfigParser()
        self.manager = None
        self.window_language = None
        self.exit_interval = False
        self.dict_language = literal_eval(
            open(
                os.path.join(self.directory, 'data', 'locales', 'locales.txt')).read()
        )
        self.translation = Translation(
            self.lang, 'Ttest', os.path.join(self.directory, 'data', 'locales')
        )
        self.date_from = datetime.now().date()
        self.date_to = self.date_from

    def get_application_config(self):
        return super(Barsic, self).get_application_config(
                        '{}/%(appname)s.ini'.format(self.directory))

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'language', 'en')

    def set_value_from_config(self):
        self.config.read(os.path.join(self.directory, 'barsic.ini'))
        self.lang = self.config.get('General', 'language')

    def build(self):
        self.set_value_from_config()
        self.load_all_kv_files(os.path.join(self.directory, 'uix', 'kv'))
        self.screen = StartScreen()
        self.manager = self.screen.ids.manager
        self.nav_drawer = self.screen.ids.nav_drawer
        self.action_bar = self.screen.ids.action_bar

        return self.screen

    def load_all_kv_files(self, directory_kv_files):
        for kv_file in os.listdir(directory_kv_files):
            kv_file = os.path.join(directory_kv_files, kv_file)
            if os.path.isfile(kv_file):
                if not PY2:
                    with open(kv_file, encoding='utf-8') as kv:
                        Builder.load_string(kv.read())
                else:
                    Builder.load_file(kv_file)

    def events_program(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.nav_drawer.state == 'open':
                self.nav_drawer.toggle_nav_drawer()
            self.back_screen(event=keyboard)
        elif keyboard in (282, 319):
            pass

        return True

    def back_screen(self, event=None):
        if event in (1001, 27):
            if self.manager.current == 'base':
                self.dialog_exit()
                return
            try:
                self.manager.current = self.list_previous_screens.pop()
            except:
                self.manager.current = 'base'
            self.screen.ids.action_bar.title = self.title
            self.screen.ids.action_bar.left_action_items = \
                [['menu', lambda x: self.nav_drawer.toggle_nav_drawer()]]

    def show_about(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.screen.ids.about.ids.label.text = self.translation._(
            u'[size=20][b]barsic[/b][/size]\n\n'
            u'[b]Version:[/b] {version}\n'
            u'[b]License:[/b] MIT\n\n'
            u'[size=20][b]Developer[/b][/size]\n\n'
            u'[ref=SITE_PROJECT]'
            u'[color={link_color}]Ivan Bazhenov[/color][/ref]\n\n'
            u'[b]Source code:[/b] '
            u'[ref=https://github.com/sendhello/barsic-android-client]'
            u'[color={link_color}]GitHub[/color][/ref]').format(
            version=__version__,
            link_color=get_hex_from_color(self.theme_cls.primary_color)
        )
        self.manager.current = 'about'
        self.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.back_screen(27)]]

    def show_zones(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'zones'
        self.action_bar.title = 'zones'
        self.list_previous_screens.append('zones')
        self.screen.ids.action_bar.left_action_items = [['menu', lambda x: self.nav_drawer.toggle_nav_drawer()]]

    def show_short_report(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'short_report'
        self.action_bar.title = 'short_report'
        self.list_previous_screens.append('short_report')
        self.screen.ids.action_bar.left_action_items = [['menu', lambda x: self.nav_drawer.toggle_nav_drawer()]]

    def show_total_report(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'total_report'
        self.action_bar.title = 'total_report'
        self.list_previous_screens.append('total_report')
        self.screen.ids.action_bar.left_action_items = [['menu', lambda x: self.nav_drawer.toggle_nav_drawer()]]

    def show_reports(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'report'
        self.action_bar.title = 'report'
        self.list_previous_screens.append('report')
        self.screen.ids.action_bar.left_action_items = [['menu', lambda x: self.nav_drawer.toggle_nav_drawer()]]
        # Загрузка параметров из INI-файла
        self.load_checkbox()

    def show_license(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        if not PY2:
            self.screen.ids.license.ids.text_license.text = self.translation._('%s') % open(
                os.path.join(self.directory, 'LICENSE'), encoding='utf-8').read()
        else:
            self.screen.ids.license.ids.text_license.text = self.translation._('%s') % open(
                os.path.join(self.directory, 'LICENSE')).read()
        self.manager.current = 'license'
        self.action_bar.title = 'license'
        self.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.back_screen(27)]]
        self.screen.ids.action_bar.title = self.translation._('MIT LICENSE')

    def select_locale(self, *args):
        def select_locale(name_locale):
            for locale in self.dict_language.keys():
                if name_locale == self.dict_language[locale]:
                    self.lang = locale
                    self.config.set('General', 'language', self.lang)
                    self.config.write()

        dict_info_locales = {}
        for locale in self.dict_language.keys():
            dict_info_locales[self.dict_language[locale]] = \
                ['locale', locale == self.lang]

        if not self.window_language:
            self.window_language = card(
                Lists(
                    dict_items=dict_info_locales,
                    events_callback=select_locale, flag='one_select_check'
                ),
                size=(.85, .55)
            )
        self.window_language.open()

    def load_checkbox(self):
        """
        Установка чекбоксов в соответствии с настройками INI-файла
        """
        # self.root.ids.report.ids.split_by_days.active = self.split_by_days
        # self.root.ids.report.ids.finreport_xls.active = self.finreport_xls
        # self.root.ids.report.ids.check_client_count_total_xls.active = self.check_client_count_total_xls
        # self.root.ids.report.ids.check_cashreport_xls.active = self.check_cashreport_xls
        # self.root.ids.report.ids.check_itogreport_xls.active = self.check_itogreport_xls
        # self.root.ids.report.ids.agentreport_xls.active = self.agentreport_xls
        # self.root.ids.report.ids.use_yadisk.active = self.use_yadisk
        # self.root.ids.report.ids.finreport_google.active = self.finreport_google
        # self.root.ids.report.ids.finreport_telegram.active = self.finreport_telegram
        pass



    def click_date_switch(self):
        if self.root.ids.report.ids.date_switch.active:
            self.date_switch = True
            self.root.ids.report.ids.label_date.text = 'Дата:'
            self.set_date_to(self.date_from.date() + timedelta(1))
            self.root.ids.report.ids.date_to.theme_text_color = 'Secondary'
            self.root.ids.report.ids.split_by_days.active = False
            self.root.ids.report.ids.split_by_days.disabled = True
            self.root.ids.report.ids.split_by_days_text.theme_text_color = 'Secondary'
            self.change_checkbox('split_by_days', False)
            self.root.ids.report.ids.finreport_google_text.disabled = False
            self.root.ids.report.ids.finreport_google.disabled = False
        else:
            self.date_switch = False
            self.root.ids.report.ids.label_date.text = 'Период:'
            self.root.ids.report.ids.date_to.theme_text_color = 'Primary'
            self.root.ids.report.ids.split_by_days.disabled = False
            self.root.ids.report.ids.split_by_days.active = True
            self.root.ids.report.ids.split_by_days_text.theme_text_color = 'Primary'
            self.change_checkbox('split_by_days', True)

    def change_checkbox(self, name, checkbox):
        """
        Изменяет состояние элемента конфигурации и записывает в INI-файл
        :param name: Имя чекбокса
        :param checkbox: Состояние active чекбокса
        """
        self.config.set('General', name, str(checkbox))
        setattr(self, name, checkbox)
        self.config.write()
        if name == 'split_by_days' and not checkbox and not self.root.ids.report.ids.date_switch.active:
            self.root.ids.report.ids.finreport_google.active = False
            self.change_checkbox('finreport_google', False)
            self.root.ids.report.ids.finreport_google.disabled = True
            self.root.ids.report.ids.finreport_google_text.disabled = True
        elif name == 'split_by_days' and checkbox:
            self.root.ids.report.ids.finreport_google_text.disabled = False
            self.root.ids.report.ids.finreport_google.disabled = False

    def dialog_exit(self):
        def check_interval_press(interval):
            self.exit_interval += interval
            if self.exit_interval > 5:
                self.exit_interval = False
                Clock.unschedule(check_interval_press)

        if self.exit_interval:
            sys.exit(0)
            
        Clock.schedule_interval(check_interval_press, 1)
        toast(self.translation._('Press Back to Exit'))

    def on_lang(self, instance, lang):
        self.translation.switch_lang(lang)

    def show_example_alert_dialog(self):
        if not self.alert_dialog:
            self.alert_dialog = MDDialog(
                title="Reset settings?",
                text="This will reset your device to its default factory settings.",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        text_color=self.app.theme_cls.primary_color,
                    ),
                    MDFlatButton(
                        text="ACCEPT",
                        text_color=self.app.theme_cls.primary_color,
                    ),
                ],
            )
        self.alert_dialog.open()
