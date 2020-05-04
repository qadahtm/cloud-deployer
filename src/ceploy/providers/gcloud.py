################################
# Copyright 2020
# Author: Thamir M. Qadah
################################

from ceploy import Cloud
from ceploy.cloud import VmInstance
import json
from ceploy.constants import OutputColors

"""
Class for Google Cloud specific implementation
"""


class GCloud(Cloud):
    CMD = 'gcloud'
    COMPUTE_CMD = 'gcloud compute'

    def __init__(self, conf_file):
        super().__init__(conf_file)
        from ceploy.constants import Provider
        self.code = Provider.GCLOUD
        self.conf = self.utils.secrets

        cmd = "gcloud auth activate-service-account \
          --key-file={} --project={}".format(self.conf['gcloud_key_file'], self.conf['gcloud_project_name'])
        self.utils.exec_cmd(cmd)

    def get_cloud_name(self):
        return "Google Cloud"

    def list_instances(self, filter_str=''):
        print("{}Listing instances using GCloud API{}".format(OutputColors.COLOR_BLUE, OutputColors.COLOR_RESET))
        cmd = "{} instances list {} --format json -q".format(GCloud.COMPUTE_CMD, "" if filter_str == '' else "--filter={}".format(filter_str))
        _, output, err = self.utils.exec_cmd(cmd)

        json_out = json.loads(output)
        return json_out

    def create_instance(self, name, template, zone):
        msg = "Creating a VM instance using name:{},  template: {}, zone={}".format(name, template, zone)
        print("{}{}{}".format(OutputColors.COLOR_GREEN, msg, OutputColors.COLOR_RESET))
        cmd_template = "{} instances create {} --format json -q --source-instance-template={} --zone={}"
        cmd = cmd_template.format(GCloud.COMPUTE_CMD, name, template, zone)
        _, output, err = self.utils.exec_cmd(cmd)
        if len(output) > 0:
            return json.loads(output)
        else:
            return {}

    def delete_instance(self, name, zone):
        msg = "Deleteing a VM instance with name: {}, zone: {}".format(name, zone)
        print("{}{}{}".format(OutputColors.COLOR_RED, msg, OutputColors.COLOR_RESET))
        cmd_template = "{} instances delete {} --format json -q --zone={}"
        cmd = cmd_template.format(GCloud.COMPUTE_CMD, name, zone)
        _, output, err = self.utils.exec_cmd(cmd)
        if len(output) > 0:
            return json.loads(output)
        else:
            return {}

    def vm_to_str(self, vm: dict) -> str:
        # print(json.dumps(vm, indent=2))
        name = vm['name']
        zone = get_zone(vm['zone'])
        extIP = "" if 'natIP' not in dict(vm['networkInterfaces'][0]).keys() else vm['networkInterfaces'][0]['natIP']
        intIP = vm['networkInterfaces'][0]['networkIP']
        vm_status = vm['status']
        return "name: {}, zone: {}, extIP: {}, intIP: {}, status: {}".format(name, zone, extIP, intIP, vm_status)

class GCVM(VmInstance):

    def __init__(self, vm):
        super().__init__(vm)
        self.name = vm['name']
        self.ext_ip = "" if 'natIP' not in dict(vm['networkInterfaces'][0]['accessConfigs'][0]).keys() else vm['networkInterfaces'][0]['accessConfigs'][0]['natIP']
        self.zone = get_zone(vm['zone'])
        self.int_ip = vm['networkInterfaces'][0]['networkIP']
        self.status = vm['status']

# Module functions
def get_zone(zone_attr : str) -> str:
    return zone_attr.split('/zones/')[1]


