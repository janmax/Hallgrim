# -*- coding: utf-8 -*-

from .context import hallgrim

import unittest

class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_markdown(self):
        markdown = hallgrim.custom_markdown.get_markdown()
        assert markdown("** BOLD **") == "<p><strong> BOLD </strong></p>\n"


if __name__ == '__main__':
    unittest.main()
