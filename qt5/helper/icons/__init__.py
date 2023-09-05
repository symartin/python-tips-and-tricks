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

from collections.abc import Sequence
from typing import List

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

# to compile the qrc file, one needs pyrcc5 provided by the pyqt5-tools package
#  pyrcc5 icons.qrc > icons_rc.py
from . import icons_rc


class Icon(QIcon):
    """ Utility class to create QIcons easily from a library of icons """

    ICON_ROOT_PATH = ":icons/"

    ICON_PATH = {

        # edit ----------------------------------------------------------------------------------

        'paste': ICON_ROOT_PATH + "edit/paste.png",
        'copy': ICON_ROOT_PATH + "edit/copy.png",

        # folder ----------------------------------------------------------------------------------
        'folder': ((ICON_ROOT_PATH + "folder/folder_24px.png", QSize(24, 24)),),

        'root folder': ((ICON_ROOT_PATH + "folder/root_folder_16px.png", QSize(16, 16)),
                        (ICON_ROOT_PATH + "folder/root_folder_24px.png", QSize(24, 24)),
                        (ICON_ROOT_PATH + "folder/root_folder_32px.png", QSize(32, 32))),

        'explorer': ((ICON_ROOT_PATH + "folder/explorer_16px.png", QSize(16, 16)),
                     (ICON_ROOT_PATH + "folder/explorer_24px.png", QSize(24, 24)),
                     (ICON_ROOT_PATH + "folder/explorer_32px.png", QSize(32, 32))),

        'refresh': ((ICON_ROOT_PATH + "folder/refresh_16px.png", QSize(16, 16)),
                    (ICON_ROOT_PATH + "folder/refresh_24px.png", QSize(24, 24)),
                    (ICON_ROOT_PATH + "folder/refresh_32px.png", QSize(32, 32))),

        # file ------------------------------------------------------------------------------------
        'save file as': ((ICON_ROOT_PATH + "file/save_file_as_16px.png", QSize(16, 16)),
                         (ICON_ROOT_PATH + "file/save_file_as_24px.png", QSize(24, 24)),
                         (ICON_ROOT_PATH + "file/save_file_as_32px.png", QSize(32, 32))),

        'save file': ((ICON_ROOT_PATH + "file/save_file_16px.png", QSize(16, 16)),
                      (ICON_ROOT_PATH + "file/save_file_24px.png", QSize(24, 24)),
                      (ICON_ROOT_PATH + "file/save_file_32px.png", QSize(32, 32))),

        'save in folder': ((ICON_ROOT_PATH + "file/save_in_folder_16px.png", QSize(16, 16)),
                           (ICON_ROOT_PATH + "file/save_in_folder_24px.png", QSize(24, 24)),
                           (ICON_ROOT_PATH + "file/save_in_folder_32px.png", QSize(32, 32))),

        'load file': ((ICON_ROOT_PATH + "file/load_file_16px.png", QSize(16, 16)),
                      (ICON_ROOT_PATH + "file/load_file_24px.png", QSize(24, 24)),
                      (ICON_ROOT_PATH + "file/load_file_32px.png", QSize(32, 32))),

        'open': ((ICON_ROOT_PATH + "file/open_16px.png", QSize(16, 16)),
                 (ICON_ROOT_PATH + "file/open_24px.png", QSize(24, 24)),
                 (ICON_ROOT_PATH + "file/open_32px.png", QSize(32, 32))),

        'new': ((ICON_ROOT_PATH + "file/new_16px.png", QSize(16, 16)),
                (ICON_ROOT_PATH + "file/new_24px.png", QSize(24, 24)),
                (ICON_ROOT_PATH + "file/new_32px.png", QSize(32, 32)),),

        'save': ((ICON_ROOT_PATH + "/file/save_16px.png", QSize(16, 16)),
                 (ICON_ROOT_PATH + "/file/save_24px.png", QSize(24, 24)),
                 (ICON_ROOT_PATH + "/file/save_32px.png", QSize(32, 32))),

        'settings file': ((ICON_ROOT_PATH + "file/settings_file_16px.png", QSize(16, 16)),
                          (ICON_ROOT_PATH + "file/settings_file_24px.png", QSize(24, 24)),
                          (ICON_ROOT_PATH + "file/settings_file_32px.png", QSize(32, 32))),

        # app ------------------------------------------------------------------------------------------

        'collapse': (
            (ICON_ROOT_PATH + "app/collapse_16px.png", QSize(16, 16), QIcon.Normal, QIcon.Off),
            (ICON_ROOT_PATH + "app/expand_16px.png", QSize(16, 16), QIcon.Normal, QIcon.On),

            (ICON_ROOT_PATH + "app/collapse_24px.png", QSize(24, 24), QIcon.Normal, QIcon.Off),
            (ICON_ROOT_PATH + "app/expand_24px.png", QSize(24, 24), QIcon.Normal, QIcon.On),

            (ICON_ROOT_PATH + "app/collapse_32px.png", QSize(32, 32), QIcon.Normal, QIcon.Off),
            (ICON_ROOT_PATH + "app/expand_32px.png", QSize(32, 32), QIcon.Normal, QIcon.On),
        ),

        # misc ------------------------------------------------------------------------------------------

        'wrench': ((ICON_ROOT_PATH + "misc/wrench_16px.png", QSize(16, 16)),
                   (ICON_ROOT_PATH + "misc/wrench_24px.png", QSize(24, 24)),
                   (ICON_ROOT_PATH + "misc/wrench_32px.png", QSize(32, 32))),

        'lightning': ((ICON_ROOT_PATH + "misc/lightning_16px.png", QSize(16, 16)),
                      (ICON_ROOT_PATH + "misc/lightning_24px.png", QSize(24, 24)),
                      (ICON_ROOT_PATH + "misc/lightning_24px.png", QSize(32, 32))),

    }

    def __init__(self, name, **kwargs):
        if name in Icon.ICON_PATH:
            if isinstance(Icon.ICON_PATH[name], str):
                super().__init__(Icon.ICON_PATH[name], **kwargs)  # type: ignore

            elif isinstance(Icon.ICON_PATH[name], Sequence):
                super().__init__(**kwargs)  # type: ignore
                for arg in Icon.ICON_PATH[name]:
                    self.addFile(arg[0], *arg[1:])

        else:
            print("icon %s not found" % name)
            super().__init__(name, **kwargs)  # type: ignore

    @staticmethod
    def buildFromList(arg_list: List, **kwargs) -> QIcon:

        icon = QIcon(**kwargs)
        for arg in arg_list:
            icon.addFile(arg[0], *arg[1:])

        return icon
