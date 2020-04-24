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
    gcloud = Cloud.make(Provider.GCLOUD, '../gcloud_conf.yml')
    vm_list = gcloud.list_instances(filter_str="name~'c\\d\\-qcd\\-.'")
    for vm in vm_list:
        print(vm['name'])

    cmd_out = gcloud.create_instance("c8-qcd-test", "c8-qstore")
    print(cmd_out)

    vm_list = gcloud.list_instances(filter_str="name~'c\\d\\-qcd\\-.'")
    for vm in vm_list:
        print(vm['name'])

    cmd_out = gcloud.delete_instance("c8-qcd-test")
    print(cmd_out)

    vm_list = gcloud.list_instances(filter_str="name~'c\\d\\-qcd\\-.'")
    for vm in vm_list:
        print(vm['name'])





if __name__ == '__main__':
    main()

