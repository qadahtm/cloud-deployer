################################
# Copyright 2020
# Author: Thamir M. Qadah
################################

from ceploy import Cloud

"""
Class for Google Cloud specific implementation
"""
class GCloud(Cloud):

    def __init__(self):
        super().__init__()
        from ceploy.constants import Provider
        self.code = Provider.GCLOUD

    def getCloudName(self):
        return "Google Cloud"

    def list_instances(self):
        print("Listing instances using GCloud API")