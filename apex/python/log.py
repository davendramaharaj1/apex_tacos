import logging
import time

class message:
    def __init__(self):
        self.start_time = time.time()
        logging.basicConfig(filename="apex_tacos.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s", level=logging.INFO)
        logging.info("Starting Logger..")

    def display_info(self, s:str) ->None:
        logging.info("At t = %0.5f seconds, %s", time.time() - self.start_time, s)

    def display_warning(self, s:str)->None:
        logging.warning("At t = %0.5f seconds, %s", time.time() - self.start_time, s)

    def display_error(self, s:str)->None:
        logging.error("At t = %0.5f seconds, %s", time.time() - self.start_time, s)

    def __del__(self):
        print("Logger file saved as apex_tacos.log under apex/python")