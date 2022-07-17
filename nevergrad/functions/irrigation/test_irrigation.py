# Copyright (c) Meta Platforms, Inc. and affiliates. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import numpy as np
import pytest
from nevergrad.functions.irrigation import Irrigation

func = Irrigation(symmetry=2)


@pytest.mark.ut
def test_irrigation_is_deterministic() -> None:
    # Given
    x = np.random.rand(func.dimension)

    # When
    value = func(x)
    value_2 = func(x)

    # Then
    np.testing.assert_almost_equal(value, value_2)


@pytest.mark.ut
def test_irrigation_is_not_flat() -> None:
    # Given
    x = np.random.rand(func.dimension)
    y = np.random.rand(func.dimension)

    # When
    value_x = func(x)
    value_y = func(y)

    # Then
    assert value_x != value_y


@pytest.mark.ut
def test_irrigation_is_non_positive() -> None:
    # Given
    x = np.random.rand(func.dimension)

    # When
    value = func(x)

    # Then
    assert value <= 0.0
