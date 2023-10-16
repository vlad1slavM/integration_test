from loguru import logger


logger.add('Parser.log', level="INFO", format="{time} - {level} - {message}")