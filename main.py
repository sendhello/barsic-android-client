# -*- coding: utf-8 -*-

import os
import sys
import traceback
import platform

from sentry_sdk import init as senry_init, push_scope, capture_exception
senry_init('https://9e367e10d7a24038942dc7d20db5767c@o412552.ingest.sentry.io/5304929')


def send_sentry(error):
    with push_scope() as scope:
        scope.set_context('context', {
            'platform': platform.system(),
            'platform releas': platform.release(),
            'platform version': platform.version(),
            'module': 'barsic_android_client',
            'version': __version__
        })
        scope.set_tag('module', 'barsic_android_client')
        capture_exception(error)
        raise error


directory = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.join(directory, 'applibs'))

try:
    try:
        import six.moves.urllib
    except ImportError:
        pass

    import kivy
    kivy.require('1.11.0')

    from kivy.config import Config
    Config.set('kivy', 'keyboard_mode', 'system')
    Config.set('kivy', 'log_enable', 0)

except Exception as e:
    traceback.print_exc(file=open(os.path.join(directory, 'error.log'), 'w'))
    send_sentry(e)


__version__ = '3.0.0.0'


def main():
    try:
        from barsic import Barsic

        app = Barsic()
        app.run()
    except Exception as e:
        traceback.print_exc(file=open(os.path.join(directory, 'error.log'), 'w'))
        send_sentry(e)


if __name__ in ('__main__', '__android__'):
    main()
