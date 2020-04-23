################################
# Copyright 2020
# Author: Thamir M. Qadah
################################

from ceploy import Cloud

"""
Class for Google Cloud specific implementation
"""
class GCloud(Cloud):

    def __init__(self, conf_file):
        super().__init__(conf_file)
        from ceploy.constants import Provider
        self.code = Provider.GCLOUD
        conf = self.utils.secrets

        cmd = "gcloud auth activate-service-account {} \
          --key-file={} --project={}".format(conf['gcloud_user'],conf['gcloud_key_file'], conf['gcloud_project_name'])
        print(cmd)
        # self.utils.exec_cmd("gcloud init")

    def getCloudName(self):
        return "Google Cloud"

    def list_instances(self):
        print("Listing instances using GCloud API")