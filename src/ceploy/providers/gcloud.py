################################
# Copyright 2020
# Author: Thamir M. Qadah
################################

from ceploy import Cloud
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

    def getCloudName(self):
        return "Google Cloud"

    def list_instances(self, filter_str=''):
        print("{}Listing instances using GCloud API{}".format(OutputColors.COLOR_BLUE, OutputColors.COLOR_RESET))
        cmd = "{} instances list {} --format json -q".format(GCloud.COMPUTE_CMD, "" if filter_str == '' else "--filter={}".format(filter_str))
        _, output, err = self.utils.exec_cmd(cmd)

        json_out = json.loads(output)
        return json_out

    def create_instance(self, name, template):
        msg = "Creating a VM instance using name:{},  template: {}".format(name, template)
        print("{}{}{}".format(OutputColors.COLOR_GREEN, msg, OutputColors.COLOR_RESET))
        cmd_template = "{} instances create {} --format json -q --source-instance-template={}"
        cmd = cmd_template.format(GCloud.COMPUTE_CMD, name, template)
        _, output, err = self.utils.exec_cmd(cmd)
        if len(output) > 0:
            return json.loads(output)
        else:
            return {}

    def delete_instance(self, name):
        msg = "Deleteing a VM instance with name: {}".format(name)
        print("{}{}{}".format(OutputColors.COLOR_RED, msg, OutputColors.COLOR_RESET))
        cmd_template = "{} instances delete {} --format json -q"
        cmd = cmd_template.format(GCloud.COMPUTE_CMD, name)
        _, output, err = self.utils.exec_cmd(cmd)
        if len(output) > 0:
            return json.loads(output)
        else:
            return {}


