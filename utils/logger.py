import logging


def log(level: str, message: str, exc_info: bool = False) -> None:
    """
    Sets the Logger and Writes Logs to File.
    Args:
        level (str): Log Level to File.
        message (str): Log Message to Write to File.
        exc_info (bool): Exception Info to Write to File, False by Default.
    """
    FORMAT = "%(asctime)s %(message)s"
    logging.basicConfig(
        format=FORMAT, filename="compare.log", filemode="w", level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    log_levels = {
        "info": logger.info,
        "warning": logger.warning,
        "error": logger.error,
    }
    level = level.lower()

    write_log = log_levels.get(level, logger.info)
    write_log(message, exc_info=exc_info)
