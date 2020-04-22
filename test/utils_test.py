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

    def test_Utils_init(self):
        utils_test = Utils('{}utils_test_config_sample.json'.format('./' if (os.getcwd().find('test') > 0) else "./test/"), 'from@test.com', 'to@test.com')
        secrets = utils_test.secrets
        self.assertEqual(secrets['uname'], 'uname_test')


    def test_Utils_exec_cmd(self):
        utils_test = Utils()
        cmd = 'echo Hello Test'
        p = utils_test.exec_cmd(cmd)



if __name__ == '__main__':
    unittest.main()
