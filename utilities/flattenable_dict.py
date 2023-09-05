#
# Copyright (c) 2023 Sylvain Martin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
Subclass of the dict class to allow a dictionary to be flattened and
unflattened as a list of lists

Classes:
 - FlattenableDict

"""
from collections import abc


class FlattenableDict(dict):
    """
    subclass the dictionary to allow a dictionary to be flattened and
    unflattened as a list of lists. It is also customize __str__ to return
    a string representation of a flatten directory
    """

    @classmethod
    def flatten(cls, d):
        ret = []
        if isinstance(d, dict):
            for k, v in sorted(d.items()):
                ret.append([k, cls.flatten(v)])
        else:
            return d
        return ret

    @classmethod
    def unflatten(cls, dict_list):
        ret = cls()

        def is_list(el):
            return isinstance(el, abc.Sequence) and not isinstance(el, str) and len(el) > 0

        def add_to_rootkey(value):
            if "" not in ret.keys():
                ret[""] = []

            ret[""].append(value)

        if is_list(dict_list):
            for sub_list in dict_list:
                if is_list(sub_list):
                    if len(sub_list) == 2:  # it key, value couple
                        try:
                            ret[sub_list[0]] = cls.unflatten(sub_list[1])
                        except TypeError:  # if not hashable, lest hash the repr
                            ret[repr(sub_list[0])] = cls.unflatten(sub_list[1])
                    else:  # it an other kind of list, let's put it in the root
                        add_to_rootkey(sub_list)
                else:
                    add_to_rootkey(sub_list)
        else:  # final condition of the recursion
            return dict_list

        return ret

    def __str__(self):
        return repr(self.flatten(self))
