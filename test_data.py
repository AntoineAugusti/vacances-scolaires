# -*- coding: utf-8 -*-
import unittest
import datetime

import pandas as pd


class DataTest(unittest.TestCase):
    START_YEAR, END_YEAR = 1990, 2020
    HOLIDAY_NAMES = [
        "Vacances de la Toussaint",
        "Vacances de Noël",
        "Vacances d'hiver",
        "Vacances de printemps",
        "Vacances d'été",
    ]
    ZONES = ["A", "B", "C"]

    def data(self):
        return pd.read_csv("data.csv", parse_dates=["date"])

    def col_zone(self, zone):
        if zone not in self.ZONES:
            raise ValueError
        return "vacances_zone_" + zone.lower()

    def data_with_holiday(self):
        def on_holiday(row):
            res = False
            for zone in self.ZONES:
                res = res or row[self.col_zone(zone)]
            return res

        df = self.data()
        df["on_holiday"] = df.apply(lambda row: on_holiday(row), axis=1)

        return df

    def test_columns(self):
        expected = [
            "date",
            "vacances_zone_a",
            "vacances_zone_b",
            "vacances_zone_c",
            "nom_vacances",
        ]

        self.assertEquals(list(self.data().columns), expected)

    def test_no_missing_dates(self):
        start = datetime.datetime(self.START_YEAR, 1, 1)
        end = datetime.datetime(self.END_YEAR, 12, 31)

        pd.testing.assert_series_equal(
            self.data().date,
            pd.Series(pd.date_range(start=start, end=end)),
            check_names=False,
            check_exact=True,
        )

    def test_nom_vacances(self):
        self.assertEquals(
            sorted(list(self.data().nom_vacances.dropna().unique())),
            sorted(self.HOLIDAY_NAMES + ["Pont de l'Ascension"]),
        )

    def test_boolean_values(self):
        cols = map(self.col_zone, self.ZONES)

        for col in cols:
            self.assertEquals(self.data()[col].dtype, bool)

            self.assertEquals(set(self.data()[col].unique()), set([False, True]))

    def test_holiday_name_set_but_not_on_holiday(self):
        df = self.data_with_holiday()

        impossible = df[~df.on_holiday & ~df.nom_vacances.isna()]

        self.assertEquals(impossible.shape, (0, 6), impossible)

    def test_on_holiday_without_holidayname(self):
        df = self.data_with_holiday()

        impossible = df[df.on_holiday & df.nom_vacances.isna()]

        self.assertEquals(impossible.shape, (0, 6), impossible)

    def test_ascension(self):
        df = self.data()

        holidays = df.loc[df.nom_vacances == "Pont de l'Ascension", "date"]

        self.assertEquals(
            list(holidays.apply(lambda d: d.date())),
            list(
                pd.date_range("2019-05-30", "2019-06-02")
                .union(pd.date_range("2020-05-21", "2020-05-24"))
                .to_series()
                .apply(lambda d: d.date())
            ),
        )

    def test_fresh_data(self):
        the_date = datetime.datetime.utcnow().date()

        # Assume school holidays are published more than a year
        # in advance in July
        if the_date.month <= 7:
            target_year = the_date.year + 1
        else:
            target_year = the_date.year + 2

        self.assertEquals(target_year, self.END_YEAR, "Data is not fresh enough")

    def test_no_gap_in_holidays(self):
        df = self.data()
        # Remove Ascension holidays
        df.loc[
            df.nom_vacances == "Pont de l'Ascension",
            ["vacances_zone_a", "vacances_zone_b", "vacances_zone_c"],
        ] = False
        df.loc[df.nom_vacances == "Pont de l'Ascension", "nom_vacances"] = None

        df_shifted = df.shift(periods=1)

        # Count number of times we start and end holidays.
        # It counts for each holiday the change from False to True and
        # True to False
        nb_years = self.END_YEAR - self.START_YEAR + 1
        nb_missing_holidays = 5
        nb_holidays = nb_years * len(self.HOLIDAY_NAMES) - nb_missing_holidays
        expected = nb_holidays * 2

        for zone in self.ZONES:
            diff = df_shifted[self.col_zone(zone)] - df[self.col_zone(zone)]

            self.assertEquals(
                diff.abs().sum(),
                expected,
                "Zone {zone} seems to have a gap".format(zone=zone),
            )

        # Detect a faulty sequence for nom_vacances like:
        # ['Vacances d'hiver', 'Vacances d'hiver', 'Vacances de la Toussaint']
        diff = df_shifted["nom_vacances"].fillna("") != df["nom_vacances"].fillna("")

        self.assertEquals(diff.sum(), expected)


if __name__ == "__main__":
    unittest.main()
