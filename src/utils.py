import logging
import sys


class SparkLikeFormatter(logging.Formatter):
    """
    Matches the pattern in log4j2.properties:
    %d{yy/MM/dd HH:mm:ss} %highlight{%p} %style{%c{1}}{cyan}: %m%n
    """

    # ANSI escape sequences for Spark-like colors
    COLORS = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[1;91m",  # Bold Red
    }
    CYAN = "\033[96m"
    RESET = "\033[0m"

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        timestamp = self.formatTime(record, "%y/%m/%d %H:%M:%S")

        # Build the formatted string
        # [Timestamp] [LEVEL] [LoggerName]: Message
        return (
            f"{timestamp} {log_color}{record.levelname:<5}{self.RESET} "
            f"{self.CYAN}{record.name}{self.RESET}: {record.getMessage()}"
        )


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(SparkLikeFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


# Pre-defined colors for simple UI elements if needed
class Colors:
    BOLD = "\033[1m"
    BLUE = "\033[94m"
    END = "\033[0m"
