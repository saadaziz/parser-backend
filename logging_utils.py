import logging
import sys

def setup_logging():
    logger = logging.getLogger("parser-backend")
    logger.setLevel(logging.DEBUG)

    # Only add handlers if not already added!
    if not logger.hasHandlers():
        fh = logging.FileHandler("stderr.log")
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stderr)
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger

logger = setup_logging()
