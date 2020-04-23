################################
# Copyright 2020
# Author: Thamir M. Qadah
################################

from ceploy import Provider

class Cloud:

    def __init__(self, conf_file):
        self.code = -1
        from ceploy.utils import Utils
        self.utils = Utils(conf_file)

    def list_instances(self):
        pass

    def getCloudCode(self):
        return self.code

    def getCloudName(self):
        return "Invalid cloud instance"

    def make(provider_code, conf_file=''):

        if provider_code == Provider.GCLOUD:
            from ceploy.providers.gcloud import GCloud
            return GCloud(conf_file)

        elif provider_code == Provider.AWS:
            from ceploy.providers.aws import AWSCloud
            return AWSCloud(conf_file)
        else:
            raise ValueError("Provider not supported")

