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

import types

from notify.all import *



class AllTestCase (unittest.TestCase):

    def assert_is_class (self, _class):
        self.assert_(isinstance (_class, (type, types.ClassType)), _class)


    def test_base (self):
        self.assert_is_class (AbstractValueObject)


    def test_bind (self):
        self.assert_is_class (Binding)
        self.assert_is_class (WeakBinding)
        self.assert_is_class (RaisingWeakBinding)

        for type in BindingCompatibleTypes:
            self.assert_is_class (type)

        self.assert_is_class (CannotWeakReferenceError)
        self.assert_is_class (GarbageCollectedError)


    def test_condition (self):
        self.assert_is_class (AbstractCondition)
        self.assert_is_class (Condition)
        self.assert_is_class (PredicateCondition)
        self.assert_is_class (WatcherCondition)


    def test_mediator (self):
        self.assert_is_class (AbstractMediator)
        self.assert_is_class (BooleanMediator)
        self.assert_is_class (FunctionalMediator)


    def test_signal (self):
        self.assert_is_class (Signal)


    def test_variable (self):
        self.assert_is_class (AbstractVariable)
        self.assert_is_class (Variable)



if __name__ == '__main__':
    unittest.main ()



# Local variables:
# mode: python
# python-indent: 4
# indent-tabs-mode: nil
# fill-column: 90
# End: