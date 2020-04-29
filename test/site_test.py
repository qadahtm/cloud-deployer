#  Copyright (c) 2020.
#  Author: Thamir M. Qadah

import yaml

with open("test/site_conf_test.yml") as conf_file:
    conf = yaml.load(conf_file, Loader=yaml.FullLoader)
    print(conf)