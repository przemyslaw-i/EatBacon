#!/usr/bin/env python

"""
Module for Parsing Beacon and providing it in OBS readable format.
"""

__author__ = "Przemyslaw I."
__copyright__ = "Copyright 2022, Przemyslaw I."
__license__ = "MIT"
__version__ = "0.1.0"

import os
import json
import time
import datetime
import requests

class EatBacon:
    """
    Parses Beacon data.
    """

    @classmethod
    def parse_datapoint(cls, dtp):
        """
        Parses one datapoint.
        """
        try:
            dp_prs = json.loads(dtp)
            return (
                dp_prs.get('status', 0),
                dp_prs.get('stats', {}).get('distance', 0.0),
                dp_prs.get('stats', {}).get('distance', 0.0) / 1000,
                int(dp_prs.get('stats', {}).get('distance', 0.0) / 1000),
                dp_prs.get('stats', {}).get('moving_time', 0),
                dp_prs.get('stats', {}).get('elapsed_time', 0),
                dp_prs.get('battery_level', 0)
            )
        except json.decoder.JSONDecodeError:
            return ('Error', 0.0, 0, 0, 0)

    @classmethod
    def write(cls, flme, data):
        """
        Writes data to file.
        """
        with open(flme, "w", encoding="utf-8") as fle:
            fle.write(data)

    @classmethod
    def make_timestamp(cls):
        """
        Creates UTC time zoned timestamp.
        """
        dt_utc = datetime.datetime.now(datetime.timezone.utc)
        utc_time = dt_utc.replace(tzinfo=datetime.timezone.utc)
        return int(utc_time.timestamp())

    def __init__(self, url, cfg='config.json'):
        """
        Initializes class. Reads config and prepares output directory.
        """
        # Read config
        with open(cfg, "r", encoding="utf-8") as cfg_obj:
            self._cfg = json.load(cfg_obj)
            self._hdr = {
                'user-agent': self._cfg['ua']
            }
        # Create output directory
        self._dir = os.path.dirname(os.path.realpath(__file__)) + "/out"
        os.makedirs(self._dir, exist_ok=True)
        # Save url in config
        self._cfg['url'] = url

    def manage_cookie(self, req):
        """
        Updates stored cookie value in order to make further requests.
        If cookie is not available, removes old value.
        """
        if req.status_code == 200:
            if 'set-cookie' in req.headers:
                self._hdr['cookie'] = req.headers['set-cookie'].split(";")[0]
            else:
                del self._hdr['cookie']

    def get_init_call(self):
        """
        Creates initial call to get cookie for further requests.
        Returns true if success.
        """
        req = requests.get(self._cfg['url'], headers=self._hdr)
        self.manage_cookie(req)
        return req.status_code == 200

    def get_datapoint(self):
        """
        Calls for newest datapoint and returns it.
        """
        # Prepare additional headers
        ext_hdr = self._hdr.copy()
        ext_hdr['referer'] = self._cfg['url']
        ext_hdr['x-requested-with'] = 'XMLHttpRequest'
        # Create timestamp for request
        tms = EatBacon.make_timestamp()
        # Get beacon datapoint and return it
        req = requests.get(
            f"{self._cfg['url']}?minimum_timestamp={tms}",
            headers=ext_hdr
        )
        self.manage_cookie(req)
        if req.status_code == 200:
            return req.text
        return '{}'

    def sleep(self):
        """
        Sleeps for desired amount of time.
        """
        time.sleep(self._cfg['sleep'])

    def get_status(self, num):
        """
        Returns string status from provided status number.
        """
        return self._cfg['statuses'][str(num)]

    def make_output(self, pdp):
        """
        Write datapoint on desired outputs (defined in config file).
        """
        # For each defined output
        for out, cfg in self._cfg['outputs'].items():
            # File output - Write 5 metrics to 5 different files
            if out == "file":
                EatBacon.write(
                    f"{self._dir}/{cfg['fn_prefix']}status.txt",
                    self._cfg['statuses'][str(pdp[0])]
                )
                EatBacon.write(
                    f"{self._dir}/{cfg['fn_prefix']}distance.txt",
                    f"{pdp[1]:.2f}"
                )
                EatBacon.write(
                    f"{self._dir}/{cfg['fn_prefix']}distance_km.txt",
                    f"{pdp[2]:.2f}"
                )
                EatBacon.write(
                    f"{self._dir}/{cfg['fn_prefix']}distance_km_only.txt",
                    f"{pdp[3]:.2f}"
                )
                EatBacon.write(
                    f"{self._dir}/{cfg['fn_prefix']}moving_time.txt",
                    f"{pdp[4]}"
                )
                EatBacon.write(
                    f"{self._dir}/{cfg['fn_prefix']}elapsed_time.txt",
                    f"{pdp[5]}"
                )
                EatBacon.write(
                    f"{self._dir}/{cfg['fn_prefix']}battery.txt",
                    f"{pdp[6]}"
                )
            # Stdout output - Write metrics in nice form on stdout
            elif out == "stdout":
                print(', '.join([
                    f"Status: {self._cfg['statuses'][str(pdp[0])]}",
                    f"Distance: {pdp[1]:.2f}m",
                    f"Distance KM: {pdp[2]:.2f}m",
                    f"Moving time: {pdp[4]}s",
                    f"Elapsed time: {pdp[5]}s",
                    f"Battery: {pdp[6]}%"
                ]))
