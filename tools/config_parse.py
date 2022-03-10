#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2022 anqi.huang@outlook.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import sys
import re

from utils import TYPE_INT, TYPE_BOOLEAN, TYPE_STRING


class ConfigParse:
    mFeatureDict = {}

    def __init__(self):
        pass

    def sys_exit(self):
        sys.exit(-2)

    def get_features(self):
        return self.mFeatureDict

    def check_key_legally(self, key, path):
        _key = re.sub("[A-Z]", "", key)
        _key = re.sub("[a-z]", "", _key)
        _key = re.sub("[0-9]", "", _key)
        _key = re.sub("_", "", _key)
        if len(_key) > 0:
            print('Found illegal feature key: =', key, ', file =', path)
            self.sys_exit()

    def check_value_legally(self, val, path):
        if val == 'true' or val == 'false':
            return TYPE_BOOLEAN

        _val = re.sub("[0-9]", "", val)
        if len(_val) <= 0:
            return TYPE_INT

        _val = re.sub("\".*\"", "", val)
        if len(_val) <= 0:
            return TYPE_STRING
        _val = re.sub("\'.*\'", "", val)
        if len(_val) <= 0:
            return TYPE_STRING

        print('Found illegal feature value: =', val, ', file =', path)
        self.sys_exit()

    def parse_file_impl(self, def_file_path):
        with open(def_file_path, 'r') as f:
            line = "_"
            comment = ""
            for line in f:
                line = line.strip()
                if line.startswith('#'):
                    comment += line[1:] + "\n"
                    continue
                pos = line.find('=')
                if pos < 0:
                    continue

                key = str(line[0:pos]).strip()
                value = str(line[pos + 1:]).strip()
                self.check_key_legally(key, def_file_path)
                type = self.check_value_legally(value, def_file_path)

                self.mFeatureDict[key] = (value, type, comment)
                comment = ""
            f.close()

    def parse(self, common_file_path, product_file_path):
        # collect key:value from common_file_path
        if os.path.exists(common_file_path):
            self.parse_file_impl(common_file_path)

        # collect key:value from product_file_path
        # same key in common_file_path will be updated
        if os.path.exists(product_file_path):
            self.parse_file_impl(product_file_path)

        return True
