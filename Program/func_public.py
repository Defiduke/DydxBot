from constants import RESOLUTION
from func_utils import get_ISO_times
import pandas as pd
import numpy as np
import time
from pprint import pprint

#Get relevant ISO times
ISO_times= get_ISO_times()
pprint(ISO_times)
#Construct market prices

def construct_market_prices(client):
    pass