# -*- coding: utf-8 -*-
"""Test Truncator transformer."""

from aeon.datasets import load_basic_motions
from aeon.datatypes import get_examples
from aeon.transformations.panel.truncation import TruncationTransformer


def test_truncation_transformer():
    """Test truncation to the shortest series length."""
    # load data
    X_train, y_train = load_basic_motions(split="train")
    n_cases, n_channels, _ = X_train.shape
    truncated_transformer = TruncationTransformer(5)
    Xt = truncated_transformer.fit_transform(X_train)

    # when we tabularize the data it has 6 dimensions
    # and we've truncated them all to 5 long.
    assert Xt.shape == (n_cases, n_channels, 5)


def test_truncation_paramterised_transformer():
    """Test truncation to the a user defined length."""
    # load data
    X_train, y_train = load_basic_motions(split="train")
    n_cases, n_channels, _ = X_train.shape

    truncated_transformer = TruncationTransformer(2, 10)
    Xt = truncated_transformer.fit_transform(X_train)

    assert Xt.shape == (n_cases, n_channels, 8)


def test_truncation_pd_multiindex():
    """Test that column and index names in a pd-multiindex container are preserved."""
    # get a multiindex dataframe, ensure instance levels are string, not int
    X = get_examples("pd-multiindex")[0].copy()
    X.index = X.index.set_levels(["a", "b", "c"], level=0)

    t = TruncationTransformer(1, 2)
    Xt = t.fit_transform(X)

    # assert that column names and index names are preserved
    assert (X.index.get_level_values(0).unique().values == ["a", "b", "c"]).all()
    assert (Xt.columns == X.columns).all()
