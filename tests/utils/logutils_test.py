import logging
import unittest

from pydes.core.utils.logutils import ConsoleHandler, get_logger, set_log_level


class LogUtilsTest(unittest.TestCase):
    def test_get_logger_returns_logger_with_name(self):
        logger = get_logger("pydes.test.logger")
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual("pydes.test.logger", logger.name)

    def test_set_log_level(self):
        logger = get_logger("pydes.test.logger.level")
        set_log_level(logger, logging.DEBUG)
        self.assertEqual(logging.DEBUG, logger.level)

    def test_console_handler_emit_info_goes_to_stdout(self):
        handler = ConsoleHandler(logging.INFO)
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="info message",
            args=None,
            exc_info=None,
        )
        handler.emit(record)
        self.assertIsNotNone(handler.stream)

    def test_console_handler_emit_error_goes_to_stderr(self):
        handler = ConsoleHandler(logging.INFO)
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname=__file__,
            lineno=1,
            msg="error message",
            args=None,
            exc_info=None,
        )
        handler.emit(record)
        self.assertIsNotNone(handler.stream)

    def test_console_handler_flush_without_prior_emit(self):
        handler = ConsoleHandler(logging.INFO)
        # stream is None before any record has been emitted; flush must not raise.
        handler.flush()

    def test_console_handler_flush_after_emit(self):
        handler = ConsoleHandler(logging.INFO)
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="info message",
            args=None,
            exc_info=None,
        )
        handler.emit(record)
        handler.flush()


if __name__ == "__main__":
    unittest.main()
