# -*- coding: utf-8 -*-
# copyright: aeon developers, BSD-3-Clause License (see LICENSE file)
"""Tests for parameter plugin transformers."""

__author__ = ["fkiraly"]

import pytest

from aeon.datasets import load_airline
from aeon.forecasting.naive import NaiveForecaster
from aeon.forecasting.param_est.fixed import FixedParams
from aeon.forecasting.param_est.plugin import PluginParamsForecaster
from aeon.forecasting.param_est.seasonality import SeasonalityACF
from aeon.transformations.series.difference import Differencer
from aeon.utils.validation._dependencies import _check_estimator_deps


@pytest.mark.skipif(
    not _check_estimator_deps(SeasonalityACF, severity="none"),
    reason="skip test if required soft dependencies not available",
)
def test_seasonality_acf():
    """Test PluginParamsForecaster on airline data. Same as docstring example."""
    y = load_airline()

    sp_est = Differencer() * SeasonalityACF()
    fcst = NaiveForecaster()
    sp_auto = PluginParamsForecaster(sp_est, fcst)
    sp_auto.fit(y, fh=[1, 2, 3])
    assert sp_auto.forecaster_.get_params()["sp"] == 12

    PluginParamsForecaster(
        FixedParams({"foo": 12}), NaiveForecaster(), params={"foo": "sp"}
    )
