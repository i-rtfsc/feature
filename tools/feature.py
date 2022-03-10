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
import optparse

from config_parse import ConfigParse
from generator_java import GeneratorJava
from generator_makefile import GeneratorMakeFile
from generator_header import GeneratorHeader


def parseargs():
    usage = "usage: %prog [options] arg1 arg2"
    parser = optparse.OptionParser(usage=usage)

    option_group = optparse.OptionGroup(parser, "auto generated jos-feature options")

    option_group.add_option("-p", "--product", dest="product", type='string',
                            help="build product", default="mars")
    option_group.add_option("-r", "--root", dest="root", type='string',
                            help="root dir", default="vendor/journeyOS/feature")
    option_group.add_option("-o", "--out", dest="out", type='string',
                            help="out dir", default="vendor/journeyOS/feature/build_out")

    parser.add_option_group(option_group)

    (options, args) = parser.parse_args()

    return (options, args)


def main():
    (options, args) = parseargs()
    product = options.product.strip()
    out_dir = options.out.strip()
    root_dir = options.root.strip()
    print('product =', product, ', out_dir =', out_dir, ', root_dir =', root_dir)

    # 1. get config file path
    name_file = "features.cof"
    common_file_path = os.path.join(root_dir, "device", "common", name_file)
    # TODO
    # get global config...
    product_file_path = os.path.join(root_dir, "device", product, name_file)
    # print('common_file_path =', common_file_path, ', product_file_path =', product_file_path)

    # 2. parser config file
    parser = ConfigParse()
    if not parser.parse(common_file_path, product_file_path):
        raise Exception('Failed to parse definitions!')

    features = parser.get_features()

    # 3. generate java
    java = GeneratorJava(out_dir)
    java.generate(features)

    # 4. generate make file
    mk = GeneratorMakeFile(out_dir)
    mk.generate(features)

    # 5. generate c/c++ header
    header = GeneratorHeader(out_dir)
    header.generate(features)

    return 0


if __name__ == "__main__":
    main()
