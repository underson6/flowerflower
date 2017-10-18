# -*- coding: utf-8 -*-
from nose.tools import with_setup, raises
import nose
from commons import validationUtil

class TestValidationUtil(object):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_validationUtil_success1(self):
        a = ""
        assert validationUtil.isEmpty(a) == True

    def test_validationUtil_success2(self):
        a = None
        assert validationUtil.isEmpty(a) == True

    def test_validationUtil_fail1(self):
        a = 1
        assert validationUtil.isEmpty(a) != True

    def test_validationUtil_fail2(self):
        a = "aaa"
        assert validationUtil.isEmpty(a) is False
