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
        print(gcloud.vm_to_str(vm))


    cmd_out = gcloud.create_instance("n8-qcd-test-1", "n8-qstore", "us-east1-b")
    cmd_out = gcloud.create_instance("n8-qcd-test-2", "n8-qstore", "us-west1-a")

    vm_list = gcloud.list_instances(filter_str="name~'(c|n)?\\d?\\-?qcd\\-.'")
    for vm in vm_list:
        print(gcloud.vm_to_str(vm))

    cmd_out = gcloud.delete_instance("n8-qcd-test-1", zone='us-east1-b')
    cmd_out = gcloud.delete_instance("n8-qcd-test-2", zone='us-west1-a')

    vm_list = gcloud.list_instances(filter_str="name~'c\\d\\-qcd\\-.'")
    for vm in vm_list:
        print(gcloud.vm_to_str(vm))


if __name__ == '__main__':
    main()

