# -*- coding: utf-8 -*-
import unittest
import datetime

import pandas as pd


class DataTest(unittest.TestCase):
    START_YEAR, END_YEAR = 2008, 2020

    def data(self):
        return pd.read_csv(
            'data.csv',
            parse_dates=['date']
        )

    def test_columns(self):
        expected = [
            'date', 'vacances_zone_a', 'vacances_zone_b',
            'vacances_zone_c', 'nom_vacances'
        ]

        self.assertEquals(list(self.data().columns), expected)

    def test_no_missing_dates(self):
        start = datetime.datetime(self.START_YEAR, 1, 1)
        end = datetime.datetime(self.END_YEAR, 12, 31)

        pd.testing.assert_series_equal(
            self.data().date,
            pd.Series(pd.date_range(start=start, end=end)),
            check_names=False,
            check_exact=True
        )

    def test_nom_vacances(self):
        expected = [
            'Vacances de la Toussaint',
            'Vacances de Noël',
            "Vacances d'hiver",
            'Vacances de printemps',
            "Vacances d'été"
        ]

        self.assertEquals(
            list(self.data().nom_vacances.dropna().unique()),
            expected
        )

    def test_boolean_values(self):
        cols = ['vacances_zone_a', 'vacances_zone_b', 'vacances_zone_c']

        for col in cols:
            self.assertEquals(self.data()[col].dtype, bool)

            self.assertEquals(
                set(self.data()[col].unique()),
                set([False, True])
            )

    def test_holiday_name_set_but_not_on_holiday(self):
        def on_holiday(row):
            return row['vacances_zone_a'] or \
                row['vacances_zone_b'] or \
                row['vacances_zone_c']

        df = self.data()
        df['on_holiday'] = df.apply(lambda row: on_holiday(row), axis=1)

        impossible = df[~df.on_holiday & ~df.nom_vacances.isna()]

        self.assertEquals(
            impossible.shape,
            (0, 6),
            impossible
        )
