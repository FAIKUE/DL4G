# HSLU
#
# Created by Ruedi Arnold on 18.01.2018
#

import unittest

from jass.player_service.player_service import *


class PlayerServiceTest(unittest.TestCase):

    def test_convert_camel_to_snake(self):
        self.assertEqual("this_is_it", convert_camel_to_snake("ThisIsIt"))
        self.assertEqual("t", convert_camel_to_snake("T"))
        self.assertEqual("sbb_test", convert_camel_to_snake("SBBTest"))
        self.assertEqual("123_hallo", convert_camel_to_snake("123Hallo"))
        self.assertEqual("", convert_camel_to_snake(""))


if __name__ == '__main__':
    unittest.main()
