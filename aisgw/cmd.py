#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python AIS Gateway Commands."""

import argparse
import datetime
import json
import socket
import time

import pyais
import requests

__author__ = 'Daniel J. Grinkevich'  # NOQA pylint: disable=R0801
__copyright__ = 'Copyright 2017 Daniel J. Grinkevich'  # NOQA pylint: disable=R0801
__license__ = 'GNU General Public License, Version 3'  # NOQA pylint: disable=R0801


def cli():
    """Command Line interface for AIS Gateway."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--host', help='TCP host', default='127.0.0.1')
    parser.add_argument(
        '--port', help='TCP Listen port', default=10110)
    parser.add_argument(
        '-p', '--password', help='APRS.FI AIS API Password', required=True)
    parser.add_argument(
        '-c', '--callsign', help='APRS.FI Login/Callsign', required=True)

    opts = parser.parse_args()

    api_url = 'http://aprs.fi/jsonais/post/' + opts.password
    path = {'name': opts.callsign, 'url': api_url}

    while 1:
        for msg in pyais.stream.TCPConnection(opts.host, port=int(opts.port)):
            rxtime = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S") #YYYYMMDDHHMMSS
            parsed = msg.decode().asdict()
            
            #print(parsed)

            ais = {
                'msgtype': parsed['msg_type'],
                'mmsi': parsed['mmsi'],
                'rxtime': rxtime
            }

            if 'lon' in parsed:
                ais['lon'] = parsed['lon']
            if 'lat' in parsed:
                ais['lat'] = parsed['lat']
            if 'speed' in parsed:
                ais['speed'] = parsed['speed']
            if 'course' in parsed:
                ais['course'] = parsed['course']
            if 'heading' in parsed:
                ais['heading'] = parsed['heading']
            if 'status' in parsed:
                ais['status'] = int(parsed['status'])
            if 'ship_type' in parsed:
                ais['shiptype'] = int(parsed['ship_type'])
            if 'part_num' in parsed:
                ais['partno'] = parsed['part_num']
            if 'callsign' in parsed:
                ais['callsign'] = parsed['callsign']

            if 'shipname' in parsed:
                ais['shipname'] = parsed['shipname']

            if 'vendor_id' in parsed:
                ais['vendorid'] = parsed['vendor_id']
            if 'dim_a' in parsed:
                ais['ref_front'] = parsed['dim_a']
            if 'dim_c' in parsed:
                ais['ref_left'] = parsed['dim_c']
            if 'draught' in parsed:
                ais['draught'] = parsed['draught']
            if 'length' in parsed:
                ais['length'] = parsed['length']
            if 'width' in parsed:
                ais['width'] = parsed['width']
            if 'destination' in parsed:
                ais['destination'] = parsed['destination']
            if 'persons' in parsed:
                ais['persons_on_board'] = parsed['persons']

            groups = {'path': [path], 'msgs':[ais]}

            output = {
                'encodetime': rxtime,
                'protocol': 'jsonais',
                'groups':  [groups]
            }

            post = json.dumps(output)
            r = requests.post(api_url, files={'jsonais': (None, post)})
            #print(ais)

if __name__ == '__main__':
    cli()
