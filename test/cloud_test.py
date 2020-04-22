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
        gcloud = Cloud.make(Provider.GCLOUD)
        aws = Cloud.make(Provider.AWS)

        self.assertEqual(gcloud.code, Provider.GCLOUD)
        self.assertEqual(aws.code, Provider.AWS)

        self.assertEqual(gcloud.getCloudName(), "Google Cloud")
        self.assertEqual(aws.getCloudName(), "AWS Cloud")


if __name__ == '__main__':
    unittest.main()
