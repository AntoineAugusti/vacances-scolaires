#!/usr/bin/env python

from argparse import ArgumentParser
from datetime import date
from datetime import timedelta

parser = ArgumentParser()
parser.add_argument('target_year', help='Year we need to generate', type=int)
args = parser.parse_args()

target_year = args.target_year

current_date = date(target_year, 1, 1)

while current_date.year == target_year:
    date = current_date.strftime('%Y-%m-%d')
    print(date + ',False,False,False,')
    current_date = current_date + timedelta(days=1)
