#!/usr/bin/env python
# encoding: utf-8
"""
utilities.py

Accessory functions used in the community module.

Created by Kevin Brown on 2014-12-09.
"""

from numpy.random import randint

def random_choice(l):
    """
    Returns an element from list l chosen at random.
    """
    return l[randint(len(l))]
