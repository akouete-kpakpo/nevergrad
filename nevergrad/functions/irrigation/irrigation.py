# Copyright (c) Meta Platforms, Inc. and affiliates. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
Approximate crop Simulation
Based on
https://raw.githubusercontent.com/purdue-orbital/pcse-simulation/master/Simulation2.py
"""


import json
import logging
import os
import urllib.request
from pathlib import Path

import nevergrad as ng
import numpy as np
import pandas as pd
import yaml
from nevergrad.functions.irrigation.common_path import IRRIGATION_DATA_DIR, IRRIGATION_DIR
from pcse.base import ParameterProvider
from pcse.db import NASAPowerWeatherDataProvider
from pcse.fileinput import CABOFileReader, YAMLCropDataProvider
from pcse.models import Wofost72_WLP_FD
from pcse.util import WOFOST72SiteDataProvider

from ..base import ArrayExperimentFunction

# pylint: disable=too-many-locals,too-many-statements
with open(IRRIGATION_DIR / "known_geoloc.json") as fhandle:
    KNOWN_GEOLOCS = json.load(fhandle)


class Irrigation(ArrayExperimentFunction):
    variant_choice = {}

    def __init__(self, symmetry: int, n_iterations: int = 1000) -> None:
        urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/ajwdewit/pcse_notebooks/master/data/soil/ec3.soil",
            Path(IRRIGATION_DATA_DIR, "soil/ec3.soil"),
        )
        self.soil = CABOFileReader(Path(IRRIGATION_DATA_DIR, "soil", "ec3.soil"))
        param = ng.p.Array(shape=(8,), lower=(0.0), upper=(1.0)).set_name("irrigation8")
        super().__init__(self.leaf_area_index, parametrization=param, symmetry=symmetry)
        if os.environ.get("CIRCLECI", False):
            raise ng.errors.UnsupportedExperiment("No HTTP request in CircleCI")

        self.cropd = YAMLCropDataProvider(
            repository="https://raw.githubusercontent.com/ajwdewit/WOFOST_crop_parameters/master/"
        )
        for k in range(n_iterations):
            if symmetry in self.variant_choice and k < self.variant_choice[symmetry]:
                continue
            self.weatherdataprovider = get_weather_data_provider("Lome")
            self.set_data(symmetry, k)
            v = [self.leaf_area_index(np.random.rand(8)) for _ in range(5)]
            if min(v) != max(v):
                break
            self.variant_choice[symmetry] = k
        logging.info(f"we work on {self.cropname} with variety {self.cropvariety} in {self.address}.")

    def set_data(self, symmetry: int, k: int):
        self.cropname = "rice"
        self.cropvariety = np.random.RandomState(symmetry + 3 * k + 2).choice(
            list(self.cropd.get_crops_varieties()[self.cropname])
        )
        # We check if the problem is challenging.
        # print(f"testing {symmetry}: {k} {self.address} {self.cropvariety}")
        site = WOFOST72SiteDataProvider(WAV=100)
        self.parameterprovider = ParameterProvider(soildata=self.soil, cropdata=self.cropd, sitedata=site)

    def leaf_area_index(self, x: np.ndarray):
        d0 = int(1.01 + 29.98 * x[0])
        d1 = int(1.01 + 30.98 * x[1])
        d2 = int(1.01 + 30.98 * x[2])
        d3 = int(1.01 + 29.98 * x[3])
        a0 = 15.0 * x[4] / (x[4] + x[5] + x[6] + x[7])
        a1 = 15.0 * x[5] / (x[4] + x[5] + x[6] + x[7])
        a2 = 15.0 * x[6] / (x[4] + x[5] + x[6] + x[7])
        a3 = 15.0 * x[7] / (x[4] + x[5] + x[6] + x[7])

        yaml_agro = f"""
        - 2006-01-01:
            CropCalendar:
                crop_name: {self.cropname}
                variety_name: {self.cropvariety}
                crop_start_date: 2006-03-31
                crop_start_type: emergence
                crop_end_date: 2006-10-20
                crop_end_type: harvest
                max_duration: 300
            TimedEvents:
            -   event_signal: irrigate
                name: Irrigation application table
                comment: All irrigation amounts in cm
                events_table:
                - 2006-06-{d0:02}: {{amount: {a0}, efficiency: 0.7}}
                - 2006-07-{d1:02}: {{amount: {a1}, efficiency: 0.7}}
                - 2006-08-{d2:02}: {{amount: {a2}, efficiency: 0.7}}
                - 2006-09-{d3:02}: {{amount: {a3}, efficiency: 0.7}}
            StateEvents: null
        """
        try:
            agromanagement = yaml.safe_load(yaml_agro)
            wofost = Wofost72_WLP_FD(self.parameterprovider, self.weatherdataprovider, agromanagement)
            wofost.run_till_terminate()
        except Exception as e:
            return float("inf")
            # assert (
            #    False
            # ), f"Problem!\n Dates: {d0} {d1} {d2} {d3},\n amounts: {a0}, {a1}, {a2}, {a3}\n  ({e}).\n"
            # raise e

        output = wofost.get_output()
        df = pd.DataFrame(output).set_index("day")
        df.tail()

        return -sum([float(o["LAI"]) for o in output if o["LAI"] is not None])


def get_weather_data_provider(address: str, known_geolocs: dict = KNOWN_GEOLOCS):
    if address not in known_geolocs:
        msg = f"{address} geoloc unknown"
        raise AssertionError(msg)
    geoloc = known_geolocs[address]
    return NASAPowerWeatherDataProvider(latitude=geoloc["latitude"], longitude=geoloc["longitude"])
