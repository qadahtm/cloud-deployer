################################
# Copyright 2020
# Author: Thamir M. Qadah
################################

import unittest
import sys

#append src modules
#TODO(tq): find a better way to import source
sys.path.append("src") # when running at the root project directory
sys.path.append("../src") # when running inside the test directory

from ceploy import Cloud
from ceploy.constants import Provider

class BasicTests(unittest.TestCase):
    def test_classes(self):
        gcloud = Cloud.make(Provider.GCLOUD, 'test/utils_test_config_sample.yml')
        aws = Cloud.make(Provider.AWS, 'test/utils_test_config_sample.json')

        self.assertEqual(gcloud.code, Provider.GCLOUD)
        self.assertEqual(aws.code, Provider.AWS)

        self.assertEqual(gcloud.get_cloud_name(), "Google Cloud")
        self.assertEqual(aws.get_cloud_name(), "AWS Cloud")


if __name__ == '__main__':
    unittest.main()
