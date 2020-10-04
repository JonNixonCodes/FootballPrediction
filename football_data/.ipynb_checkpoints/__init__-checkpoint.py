import os
from football_data.schema import *
from football_data.extract import *
from football_data.ingest import *

__this_dir, __this_filename = os.path.split(__file__)
DATA_CONFIG_PATH = os.path.join(__this_dir, "config", "data-config.json")