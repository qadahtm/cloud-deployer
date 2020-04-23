#  Copyright (c) 2020.
#  Author: Thamir M. Qadah

################################
################################

import sys
#append src modules
#TODO(tq): find a better way to import source
sys.path.append("src") # when running at the root project directory
sys.path.append("../src") # when running inside the test directory

from ceploy.cloud import Cloud
from ceploy.constants import Provider

def main():
    gcloud = Cloud.make(Provider.GCLOUD, '../gcloud_conf.json')




if __name__ == '__main__':
    main()

