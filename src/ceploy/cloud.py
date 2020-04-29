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

## Instances methods
    def list_instances(self):
        pass

    def create_instance(self, name, template):
        pass

    def delete_instance(self, name):
        pass

    def getCloudCode(self):
        return self.code

    def get_cloud_name(self):
        return "Invalid cloud instance"

    def vm_to_str(self, vm) -> str:
        return str(vm)

    def make(provider_code, conf_file=''):

        if provider_code == Provider.GCLOUD:
            from ceploy.providers.gcloud import GCloud
            return GCloud(conf_file)

        elif provider_code == Provider.AWS:
            from ceploy.providers.aws import AWSCloud
            return AWSCloud(conf_file)
        else:
            raise ValueError("Provider not supported")

class Site:

    def __init__(self, yml_conf):
        import yaml
        with open(yml_conf) as conf_file:
            self.conf = yaml.load(conf_file, Loader=yaml.FullLoader)