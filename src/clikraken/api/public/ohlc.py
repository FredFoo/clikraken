# -*- coding: utf8 -*-

"""
clikraken.api.public.ohlc

This module queries the OHLC method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

from collections import OrderedDict
from decimal import Decimal

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import asset_pair_short, humanize_timestamp
from clikraken.clikraken_utils import _tabulate as tabulate

import datetime
def _ts(timestamp):
    return datetime.datetime.fromtimestamp(
        int(timestamp)
    ).strftime('%Y-%m-%d %H:%M:%S')


def ohlc(args):
    """Get ohlc information."""

    # Parameters to pass to the API
    api_params = {
        'pair': args.pair,
    }

    if args.since:
        api_params['since'] = args.since

    if args.interval:
        api_params['interval'] = args.interval

    # initialize a list to store the parsed points
    plist = []

    res = query_api('public', 'OHLC', api_params, args)

    for point in res.get(args.pair):

        # Initialize an OrderedDict to garantee the column order
        # for later use with the tabulate function
        pdict = OrderedDict()
        pdict["Time"] = _ts(point[0])
        pdict["Open"] = point[1]
        pdict["High"] = point[2]
        pdict["Low"] = point[3]
        pdict["Close"] = point[4]
        pdict["Ywap"] = point[5]
        pdict["Volume"] = point[6]
        pdict["Count"] = point[7]
        plist.append(pdict)

    if not plist:
        return

    # <time>, <open>, <high>, <low>, <close>, <vwap>, <volume>, <count>
    # Reverse point list to have the most recent points at the top
    plist = plist[::-1]
    print(tabulate(plist[:args.count], headers="keys") + '\n')

    # asks_table = tabulate(depth_dict['asks'], headers="keys")
    # bids_table = tabulate(depth_dict['bids'], headers="keys")
    #
    # print("{}\n\n{}".format(asks_table, bids_table))
