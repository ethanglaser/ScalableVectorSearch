#
# Copyright (C) 2023-present, Intel Corporation
#
# You can redistribute and/or modify this software under the terms of the
# GNU Affero General Public License version 3.
#
# You should have received a copy of the GNU Affero General Public License
# version 3 along with this software. If not, see
# <https://www.gnu.org/licenses/agpl-3.0.en.html>.
#

# Tests for the Vamana index portion of the PySVS module.
import unittest
import itertools
import pysvs

# Local dependencies
from .common import \
    isapprox, \
    test_data_svs, \
    test_data_vecs, \
    test_data_dims

DEBUG = False;

class LoaderAPITester(unittest.TestCase):
    """
    Test routines for the various loader classes.
    """
    def _get_basic_loader(self):
        loader = pysvs.VectorDataLoader(test_data_vecs, data_type = pysvs.float32)
        self.assertEqual(loader.data_type, pysvs.float32)
        self.assertEqual(loader.dims, 128)
        return loader

    def test_lvq_loader(self):
        loader = self._get_basic_loader()

        # One Level LVQ - 4 bits.
        lvq = pysvs.LVQLoader(loader, primary = 4)
        self.assertEqual(lvq.dims, 128)
        self.assertEqual(lvq.primary_bits, 4)
        self.assertEqual(lvq.residual_bits, 0)
        self.assertEqual(lvq.strategy, pysvs.LVQStrategy.Auto)

        # One Level LVQ - 8 bits.
        lvq = pysvs.LVQLoader(
            loader, primary = 8, strategy = pysvs.LVQStrategy.Sequential
        )
        self.assertEqual(lvq.dims, 128)
        self.assertEqual(lvq.primary_bits, 8)
        self.assertEqual(lvq.residual_bits, 0)
        self.assertEqual(lvq.strategy, pysvs.LVQStrategy.Sequential)

        # Two level LVQ - 4x8 bits
        lvq = pysvs.LVQLoader(
            loader, primary = 4, residual = 8, strategy = pysvs.LVQStrategy.Turbo
        )
        self.assertEqual(lvq.dims, 128)
        self.assertEqual(lvq.primary_bits, 4)
        self.assertEqual(lvq.residual_bits, 8)
        self.assertEqual(lvq.strategy, pysvs.LVQStrategy.Turbo)


        # Two level LVQ - 8x8 bits
        lvq = pysvs.LVQLoader(loader, primary = 8, residual = 8)
        self.assertEqual(lvq.dims, 128)
        self.assertEqual(lvq.primary_bits, 8)
        self.assertEqual(lvq.residual_bits, 8)
        self.assertEqual(lvq.strategy, pysvs.LVQStrategy.Auto)

    def test_leanvec_loader(self):
        loader = self._get_basic_loader()

        kinds = [
            pysvs.LeanVecKind.lvq4,
            pysvs.LeanVecKind.lvq8,
            pysvs.LeanVecKind.float16,
            pysvs.LeanVecKind.float32,
        ]

        alignments = [0, 32]
        dims = [64, 96]

        for (p, s, a, d) in itertools.product(kinds, kinds, alignments, dims):
            leanvec = pysvs.LeanVecLoader(
                loader,
                d,
                primary_kind = p,
                secondary_kind = s,
                alignment = a
            )

            self.assertEqual(leanvec.dims, 128)
            self.assertEqual(leanvec.primary_kind, p)
            self.assertEqual(leanvec.secondary_kind, s)
            self.assertEqual(leanvec.alignment, a)

