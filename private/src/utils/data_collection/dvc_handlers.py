import datetime
import pytz

class RawDVC:
    """
    Generate a raw data version based on the current date and time.
    """
    @staticmethod
    def create_dir():
        # in future, this method will create a directory to store raw data. Nowdays, the directory is created by the scraper_main function
        pass

    @staticmethod
    def generate_raw_data_version_name():
        brazil_timezone = pytz.timezone('America/Sao_Paulo')
        now = datetime.datetime.now(brazil_timezone)
        timestamp = now.strftime('%Y%m%d-%H%M%S')
        
        raw_data_version_name = f'v{timestamp}-GMT3'
        return raw_data_version_name
