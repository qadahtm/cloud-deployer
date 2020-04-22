################################
# Copyright 2020
# Author: Thamir M. Qadah
################################

from ceploy import Provider

class Cloud:

    def __init__(self):
        self.code = -1

    def list_instances(self):
        pass

    def getCloudCode(self):
        return self.code

    def getCloudName(self):
        return "Invalid cloud instance"

    def make(provider_code):

        if provider_code == Provider.GCLOUD:
            from ceploy.providers.gcloud import GCloud
            return GCloud()

        elif provider_code == Provider.AWS:
            from ceploy.providers.aws import AWSCloud
            return AWSCloud()
        else:
            raise ValueError("Provider not supported")

