# -*- coding: utf-8 -*-

#--------------------------------------------------------------------#
# This file is part of Py-notify.                                    #
#                                                                    #
# Copyright (C) 2007 Paul Pogonyshev.                                #
#                                                                    #
# This library is free software; you can redistribute it and/or      #
# modify it under the terms of the GNU Lesser General Public License #
# as published by the Free Software Foundation; either version 2.1   #
# of the License, or (at your option) any later version.             #
#                                                                    #
# This library is distributed in the hope that it will be useful,    #
# but WITHOUT ANY WARRANTY; without even the implied warranty of     #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU  #
# Lesser General Public License for more details.                    #
#                                                                    #
# You should have received a copy of the GNU Lesser General Public   #
# License along with this library; if not, write to the Free         #
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor,        #
# Boston, MA 02110-1301 USA                                          #
#--------------------------------------------------------------------#


if __name__ == '__main__':
    import os
    import sys

    sys.path.insert (0, os.path.join (sys.path[0], os.pardir))


import unittest

import gc

from notify.bind import *



gc.set_threshold (0, 0, 0)



class Dummy (object):

    def identity_function (self, *arguments):
        return self.static_identity (*arguments)


    def static_identity (*arguments):
        if len (arguments) == 1:
            return arguments[0]
        else:
            return arguments


    static_identity = staticmethod (static_identity)



DUMMY = Dummy ()



class BindingTestCase (unittest.TestCase):

    def test_creation (self):
        Binding            (DUMMY.identity_function)
        WeakBinding        (DUMMY.identity_function)
        RaisingWeakBinding (DUMMY.identity_function)


    def test_invocation (self):
        self.assertEqual (Binding            (DUMMY.identity_function) (33, 'test'), (33, 'test'))
        self.assertEqual (WeakBinding        (DUMMY.identity_function) (33, 'test'), (33, 'test'))
        self.assertEqual (RaisingWeakBinding (DUMMY.identity_function) (33, 'test'), (33, 'test'))


    def test_unreferencable_object_method_failure (self):
        class Test (object):
            __slots__ = ()
            def test (self):
                pass

        self.assertRaises (CannotWeakReferenceError, lambda: WeakBinding        (Test ().test))
        self.assertRaises (CannotWeakReferenceError, lambda: RaisingWeakBinding (Test ().test))


    def test_garbage_collection_1 (self):
        object = Dummy ()
        method = WeakBinding (object.identity_function)

        self.assertEqual (method (15), 15)

        del object
        gc.collect ()

        self.assertEqual (method (15), None)


    def test_garbage_collection_2 (self):
        object = Dummy ()
        method = RaisingWeakBinding (object.identity_function)

        self.assertEqual (method (15), 15)

        del object
        gc.collect ()

        self.assertRaises (GarbageCollectedError, method)



class BindingWrapTestCase (unittest.TestCase):

    def test_wrap_1 (self):
        callable = lambda: None

        self.assert_(Binding           .wrap (callable) is callable)
        self.assert_(WeakBinding       .wrap (callable) is callable)
        self.assert_(RaisingWeakBinding.wrap (callable) is callable)


    def test_wrap_2 (self):
        callable = open

        self.assert_(Binding           .wrap (callable) is callable)
        self.assert_(WeakBinding       .wrap (callable) is callable)
        self.assert_(RaisingWeakBinding.wrap (callable) is callable)


    def test_wrap_3 (self):
        callable = Dummy.identity_function

        self.assert_(Binding           .wrap (callable) is callable)
        self.assert_(WeakBinding       .wrap (callable) is callable)
        self.assert_(RaisingWeakBinding.wrap (callable) is callable)


    def test_wrap_4 (self):
        callable = Dummy.static_identity

        self.assert_(Binding           .wrap (callable) is callable)
        self.assert_(WeakBinding       .wrap (callable) is callable)
        self.assert_(RaisingWeakBinding.wrap (callable) is callable)


    def test_wrap_5 (self):
        callable = DUMMY.identity_function

        for _class in (Binding, WeakBinding, RaisingWeakBinding):
            if issubclass (_class, WeakBinding):
                self.assert_(_class.wrap (callable) is not callable)

            self.assertEqual (_class.wrap (callable),        callable)
            self.assertEqual (_class.wrap (callable),        _class.wrap (callable))
            self.assertEqual (bool (_class.wrap (callable)), bool (callable))
            self.assertEqual (bool (_class.wrap (callable)), bool (_class.wrap (callable)))
            self.assertEqual (hash (_class.wrap (callable)), hash (callable))
            self.assertEqual (hash (_class.wrap (callable)), hash (_class.wrap (callable)))


    def test_wrap_6 (self):
        callable = DUMMY.identity_function

        self.assert_(Binding.wrap (callable).im_self  is callable.im_self)
        self.assert_(Binding.wrap (callable).im_func  is callable.im_func)
        self.assert_(Binding.wrap (callable).im_class is callable.im_class)



if __name__ == '__main__':
    unittest.main ()



# Local variables:
# mode: python
# python-indent: 4
# indent-tabs-mode: nil
# fill-column: 90
# End: