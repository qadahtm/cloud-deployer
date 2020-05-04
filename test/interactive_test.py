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

from pprint import pprint

def main():
    ## Create cloud context for GCloud
    gcloud = Cloud.make(Provider.GCLOUD, '../gcloud_conf.yml')

    ## Test list instance function
    vm_list = gcloud.list_instances(filter_str="name~'n\\d\\-qcd\\-.'")
    for vm in vm_list:
        print(gcloud.vm_to_str(vm))


    ## Test create instance function
    rc, cmd_out, err = gcloud.create_instance("n8-qcd-test-1", "n8-qstore", "us-east1-b")
    if rc:
        pprint(cmd_out[0])
        ## Test VMInstance
        from ceploy.providers.gcloud import GCVM
        vm = GCVM(cmd_out[0])
        print("name={}, zone={}, ext_ip={}, int_ip={}, status={}".format(vm.name, vm.zone, vm.ext_ip, vm.int_ip,
                                                                         vm.status))
    else:
        pprint(err)



    # Create another VM instance
    rc, cmd_out, err = gcloud.create_instance("n8-qcd-test-2", "n8-qstore", "us-west1-a")
    if rc:
        pprint(cmd_out[0])
    else:
        pprint(err)

    # List created instances
    vm_list = gcloud.list_instances(filter_str="name~'n\\d\\-qcd\\-.'")
    for vm in vm_list:
        print(gcloud.vm_to_str(vm))

    # Delete created instances
    rc, cmd_out, err = gcloud.delete_instance("n8-qcd-test-1", zone='us-east1-b')
    rc, cmd_out, err = gcloud.delete_instance("n8-qcd-test-2", zone='us-west1-a')

    # List (should be empty)
    vm_list = gcloud.list_instances(filter_str="name~'c\\d\\-qcd\\-.'")
    for vm in vm_list:
        print(gcloud.vm_to_str(vm))


if __name__ == '__main__':
    main()

