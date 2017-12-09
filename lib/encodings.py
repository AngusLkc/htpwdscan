#!/usr/bin/env python
# encoding=utf-8

import sys

def system_encode(s):
    charset = sys.stdout.encoding
    return s.encode(charset, 'ignore')

def system_decode(s):
    charset = sys.stdout.encoding
    return s.decode(charset, 'ignore')
