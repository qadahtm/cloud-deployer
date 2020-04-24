################################
# Copyright 2020
# Author: Thamir M. Qadah
################################

import unittest
import sys
import os

#append src modules
#TODO(tq): find a better way to import source
sys.path.append("src") # when running at the root project directory
sys.path.append("../src") # when running inside the test directory

from ceploy.utils import Utils

class BasicTests(unittest.TestCase):

    def test_Utils_JSON_init(self):
        utils_test = Utils('{}utils_test_config_sample.json'.format('./' if (os.getcwd().find('test') > 0) else "./test/"))
        secrets = utils_test.secrets
        self.assertEqual(secrets['uname'], 'uname_test')

    def test_Utils_YAML_init(self):
        utils_test = Utils('{}utils_test_config_sample.yml'.format('./' if (os.getcwd().find('test') > 0) else "./test/"))
        secrets = utils_test.secrets
        self.assertEqual(secrets['uname'], 'uname_test')


    def test_Utils_exec_cmd(self):
        utils_test = Utils()
        cmd = 'echo Hello Test'
        p, output, err = utils_test.exec_cmd(cmd)
        self.assertEqual(len(output), 11)
        self.assertEqual(len(err), 0)

if __name__ == '__main__':
    unittest.main()
