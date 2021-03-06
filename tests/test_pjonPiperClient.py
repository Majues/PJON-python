import platform
from unittest import TestCase
from pjon_python import wrapper_client
from unittest2.compatibility import wraps
import mock
import time


def skip_if_condition(condition, reason):
    def deco(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            if condition:
                self.skipTest(reason)
            else:
                f(self, *args, **kwargs)
        return wrapper
    return deco


class TestPjonPiperClient(TestCase):
    def setUp(self):
        with mock.patch('pjon_python.wrapper_client.PjonPiperClient.get_coms', create=True) as get_coms_mock:
            get_coms_mock.return_value = ['COM1']
            self._pjon_wrapper_cli = wrapper_client.PjonPiperClient(com_port='COM1')

    @skip_if_condition('win' not in platform.platform(), 'skipping on non-windows')
    def test_is_string_valid_com_port_name__should_return_true_for_expected_com_names__windows(self):
        self.assertTrue(self._pjon_wrapper_cli.is_string_valid_com_port_name("COM1"))
        self.assertTrue(self._pjon_wrapper_cli.is_string_valid_com_port_name("COM99"))
        self.assertTrue(self._pjon_wrapper_cli.is_string_valid_com_port_name("COM11"))

    @skip_if_condition('win' not in platform.platform(), 'skipping on non-windows')
    def test_is_string_valid_com_port_name__should_return_false_for_wrong_com_names__windows(self):
        self.assertFalse(self._pjon_wrapper_cli.is_string_valid_com_port_name("COM1 "))
        self.assertFalse(self._pjon_wrapper_cli.is_string_valid_com_port_name("COM0"))
        self.assertFalse(self._pjon_wrapper_cli.is_string_valid_com_port_name("COM100"))
        self.assertFalse(self._pjon_wrapper_cli.is_string_valid_com_port_name("coom"))
        self.assertFalse(self._pjon_wrapper_cli.is_string_valid_com_port_name(" com"))
        self.assertFalse(self._pjon_wrapper_cli.is_string_valid_com_port_name(" com3"))
        self.assertFalse(self._pjon_wrapper_cli.is_string_valid_com_port_name(" com323"))

    def test_client_should_initialize_with_stdout_watchdog_disabled(self):
        self.assertEqual(self._pjon_wrapper_cli.is_piper_stdout_watchdog_enabled, False)

    def test_set_stdout_watchdog__should_change_enable_property(self):
        self._pjon_wrapper_cli.set_piper_stdout_watchdog(timeout_sec=0.250)
        self.assertEqual(self._pjon_wrapper_cli.is_piper_stdout_watchdog_enabled, True)

    def test_reset_piper_stdout_watchdog__should_set_received_ts_to_current_time(self):
        self._pjon_wrapper_cli.reset_piper_stdout_watchdog()
        self.assertLess(self._pjon_wrapper_cli._piper_stdout_last_received_ts - time.time(), 2)
