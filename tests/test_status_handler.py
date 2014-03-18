""" Test for status_handler.py. """
from unittest import TestCase
from mcman.status_handler import StatusHandler


class TestStatusHandler(TestCase):

    """ Tests for StatusHandler. """

    def setUp(self):
        """ Set up. """
        self.handler = StatusHandler()

    def test_handler_tuple(self):
        """ Test StatusHandler with tuples. """
        def one(arguments):
            """ First handler. """
            assert arguments[0] == 'test'
            assert arguments[1] == 'tset'

        def two(arguments):
            """ Second handler. """
            assert arguments[0] == 'herp'
            assert arguments[1] == 'preh'

        self.handler.register_handler(2, two)
        self.handler.register_handler(1, one)

        hook = self.handler.get_hook()
        hook(1, ('test', 'tset'))
        hook(2, ('herp', 'preh'))


    def test_handler_single_value(self):
        """ Test StatusHandler with single value. """
        def one(arguments):
            """ First handler. """
            assert arguments == 'test'

        def two(arguments):
            """ Second handler. """
            assert arguments == 'herp'

        self.handler.register_handler(1, one)
        self.handler.register_handler(2, two)

        hook = self.handler.get_hook()
        hook(1, 'test')
        hook(2, 'herp')


    def test_handler_overwrite(self):
        """ Test StatusHandler with overwriting of handlers. """
        def overwritten(arguments):
            """ Handler that should be overwritten. """
            assert False

        success = lambda arguments: None

        self.handler.register_handler(1, overwritten)
        self.handler.register_handler(1, success)

        hook = self.handler.get_hook()
        hook(1, None)


    def test_handler_no_handler(self):
        """ Test StatusHandler with missing handler. """
        try:
            self.handler.get_hook()(1, None)
        except ValueError:
            assert True
        else:
            assert False
