#!/usr/bin/env python
#
# Copyright (C) 2015 Michael Brown 
#
# This file is part of YouCompleteMe.
#
# YouCompleteMe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# YouCompleteMe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with YouCompleteMe.  If not, see <http://www.gnu.org/licenses/>.

import logging
logging.debug("htmldjango:init")
from ycmd.completers.completer import Completer
import sys, os

sys.path.append(os.getcwd())

try:
    from django_completeme.parser import TemplateInspector
except ImportError as e:
    logging.info("htmldjango:parser_load_fail")
    logging.info(sys.path)
    logging.info(e)
    raise ImportError(
        'Error importing django_completeme. Make sure the django_completeme '
        'submodule has been checked out In the YouCompleteMe folder, '
        'run "git submodule update --init --recursive"')


# TODO really can be anything. normally set ft=htmldjango handles this
HTMLDJANGO_FILETYPES = set(['htmldjango'])


logging.debug("htmldjango:parser_loaded")


class HtmlDjangoCompleter(Completer):

    def SupportedFiletypes(self):
        return HTMLDJANGO_FILETYPES

    def _GetDjangoInspector(self, request_data):
        filename = request_data['filepath']
        contents = request_data['file_data'][filename]['contents']
        line = request_data['line_num']
        column = request_data['column_num'] - 1
        return TemplateInspector(filename, line, column, contents)

    def _GetExtraData(self, completion):
        location = {}
        if completion.module_path:
            location['filepath'] = (completion.module_path)
        if completion.line:
            location['line_num'] = completion.line
        if completion.column:
            location['column_num'] = completion.column + 1

        if location:
            extra_data = {}
            extra_data['location'] = location
            return extra_data
        else:
            return None

    def ComputeCandidatesInner(self, request_data):
        script = self._GetDjangoInspector(request_data)
        return script.completions()

    def ShouldUseNow(self, request_data):
        script = self._GetDjangoInspector(request_data)
        return script.in_django_tag()
