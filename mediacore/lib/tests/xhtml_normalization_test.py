# -*- coding: utf-8 -*-
# This file is a part of MediaDrop (http://www.mediadrop.net),
# Copyright 2009-2013 MediaCore Inc., Felix Schwarz and other contributors.
# For the exact contribution history, see the git revision log.
# The source code contained in this file is licensed under the GPLv3 or
# (at your option) any later version.
# See LICENSE.txt in the main project directory, for more information.

from mediacore.lib.helpers import clean_xhtml, line_break_xhtml
from mediacore.lib.xhtml import cleaner_settings
from mediacore.lib.test.pythonic_testcase import *


class XHTMLNormalizationTest(PythonicTestCase):

    def test_text_do_not_change_after_a_clean_xhtml_and_line_break_xhtml_cycle(self):
        """Mimics the input -> clean -> display -> input... cycle of the
        XHTMLTextArea widget.
        """
        expected_html = '<p>first line<br>second line</p>'
        htmlified_text = clean_xhtml('first line\n\nsecond line')
        assert_equals(expected_html, htmlified_text)

    def test_adds_nofollow_attribute_to_links(self):
        original = '<a href="http://example.com">link</a>'
        cleaned = clean_xhtml(original)
        assert_equals(cleaned, '<p><a href="http://example.com" rel="nofollow">link</a></p>')

    def _test_removes_follow_attribute_from_links(self):
        original = '<a href="http://example.com" rel="follow">link</a>'
        cleaned = clean_xhtml(original)
        assert_equals(cleaned, '<a href="http://example.com" rel="nofollow">link</a>')

    def test_makes_automatic_links_nofollow(self):
        original = 'http://example.com'
        cleaned = clean_xhtml(original)
        assert_equals(cleaned, '<p><a href="http://example.com" rel="nofollow">http://example.com</a></p>')

    def test_adds_target_blank_to_links(self):
        original = '<a href="http://example.com">link</a>'
        from copy import deepcopy
        settings = deepcopy(cleaner_settings)
        settings['add_target_blank'] = True
        cleaned = clean_xhtml(original, _cleaner_settings=settings)
        assert_equals(cleaned, '<p><a href="http://example.com" rel="nofollow" target="_blank">link</a></p>')

import unittest
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(XHTMLNormalizationTest))
    return suite
