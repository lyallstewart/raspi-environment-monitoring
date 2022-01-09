# Generic imports -------------------------------------
import logging 
import sys
import time


# Setup sensors ---------------------------------------
# LTR559 light sensor
try:
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559
    
# BME280 weather sensor
from smbus2 import SMBus
from bme280 import BME280

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

# MICS6814 analog gas sensor
from enviroplus import gas

# LCD screen
import ST7735
from PIL import Image, ImageDraw, ImageFont


# Setup logging --------------------------------------
logger = logging.getLogger(__name__)

logging.basicConfig(
    handlers=[
        logging.FileHandler('output.log'),
        logging.StreamHandler(sys.stdout)
    ],
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# Gather data ---------------------------------------

def log_data():
    while True:
        # Get data values
        temp = bme280.get_temperature()
        pressure = bme280.get_pressure()
        humidity = bme280.get_humidity()
        light = ltr559.get_lux()
        gas_readings = gas.read_all()
        gas_reducing = gas_readings.reducing
        gas_oxidising = gas_readings.oxidising
        gas_nh3 = gas_readings.nh3
        
        logger.log(logging.INFO, "Temp: {:0.2f}   Pressure: {:0.2f}   Humidity: {:0.2f}    Light: {:0.2f}    Gas: Ox:{:0.2f} Reducing: {:0.2f} NH3: {:0.2f}".format(
            temp,
            pressure,
            humidity,
            light,
            gas_reducing,
            gas_oxidising,
            gas_nh3
        ))
        
        time.sleep(1)
    
    
try:
    logger.log(logging.INFO, "Logging Started")
    log_data()
except KeyboardInterrupt:
    logger.log(logging.WARNING, "Logging Ended - Keyboard Interrupt")
    sys.exit(1)
except Exception as err:
    logger.log(logging.ERROR, f"Logging Ended - Error - {err}", exc_info=True)
    sys.exit(1)
