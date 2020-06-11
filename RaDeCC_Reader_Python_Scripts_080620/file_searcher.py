#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 16:54:22 2018

@author: seanselzer
"""

"""
file_searcher takes one search term in the form of a string and then returns the first line that starts with that string.

"""

def file_searcher(string1, arg_file):
    f = open(arg_file, 'r')
    with open (arg_file) as f:
        for line in f:
            if line[0:len(string1)]== string1:
                return (line)			
