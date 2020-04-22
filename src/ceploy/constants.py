################################
# Copyright 2020
# Author: Thamir M. Qadah
################################

# Provider names
from enum import Enum

class Provider(Enum):
    GCLOUD = 1
    AWS = 2
    MSA = 3

# Color codes used when printing to STD OUTPUT
class OutputColors:
    COLOR_RED = '\x1b[31m'
    COLOR_GREEN = '\x1b[32m'
    COLOR_YELLOW = '\x1b[33m'
    COLOR_BLUE = '\x1b[34m'
    COLOR_MAGENTA = '\x1b[35m'
    COLOR_CYAN ='\x1b[36m'
    COLOR_RESET = '\x1b[0m'
