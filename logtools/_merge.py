#!/usr/bin/env python
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#  
#      http://www.apache.org/licenses/LICENSE-2.0 
#     
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 
"""
logtools._merge
Logfile merging utilities.
These typically help in streaming multiple 
input logfiles through, outputting them in
combined sorted order (typically by date field)
"""
import os
import re
import sys
import logging
from itertools import imap
from optparse import OptionParser
from heapq import heappush, heappop, merge

from _config import logtools_config, interpolate_config

__all__ = ['logmerge_parse_args', 'logmerge', 'logmerge_main']

def logmerge_parse_args():
    usage = "%prog -f <field> -d <delimiter> filename1 filename2 ..."
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--field", dest="field", default=None, type=int,
                    help="Field index to use as key for sorting by (1-based)")
    parser.add_option("-d", "--delimiter", dest="delimiter", default=None, 
                    help="Delimiter character for fields in logfile")
    parser.add_option("-n", "--numeric", dest="numeric", default=None, action="store_true",
                    help="Parse key field value as numeric and sort accordingly")
    
    parser.add_option("-P", "--profile", dest="profile", default='logmerge',
                      help="Configuration profile (section in configuration file)")
    
    options, args = parser.parse_args()
    
    # Interpolate from configuration
    options.field = interpolate_config(options.field, 
                                    options.profile, 'field', type=int)
    options.delimiter = interpolate_config(options.delimiter, 
                                    options.profile, 'delimiter')
    options.numeric = interpolate_config(options.numeric, options.profile, 
                                    'numeric', default=False, type=bool)    

    return options, args

def logmerge(options, args):
    """Perform merge on multiple input logfiles
    and emit in sorted order using a priority queue"""
    
    delimiter = options.delimiter
    field = options.field-1
    
    iters = (imap(lambda x: (x.split(delimiter)[field], x), open(filename, "r")) \
                  for filename in args)
    
    for k, line in merge(*iters):
        print line.strip()            
    
def logmerge_main():
    """Console entry-point"""
    options, args = logmerge_parse_args()
    logmerge(options, args)
    return 0