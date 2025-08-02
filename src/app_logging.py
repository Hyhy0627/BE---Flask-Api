import logging

def setup_logging(app=None):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )
    if app:
        app.logger.setLevel(logging.INFO)

setup_logging()