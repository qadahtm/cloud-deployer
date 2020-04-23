################################
# Copyright 2020
# Author: Thamir M. Qadah
################################

from ceploy import Cloud
"""
Class for AWS specific implementation
"""
class AWSCloud(Cloud):

    def __init__(self, conf_file):
        super().__init__(conf_file)
        from ceploy.constants import Provider
        self.code = Provider.AWS

    def getCloudName(self):
        return "AWS Cloud"

    def list_instances(self):
        print("Listing instances using AWS CLI")
