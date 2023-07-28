import calendar
import ephem


class YearProperties:
    def __init__(self, year_input):
        """ Initialize with basic year stats """
        self.year = year_input
        self.leap = calendar.isleap(self.year)
        self.start_doy = calendar.weekheader(3).split()[calendar.weekday(self.year, 1, 1)]
        self.previous_full_moon = ephem.previous_full_moon(str(self.year))
        self.next_full_moon = ephem.next_full_moon(str(self.year))

    def compare_years(self, other_year):
        """ Return a calendar comparison of two years """
        return {'leap': self.leap == other_year.leap,
                'start_doy': self.start_doy == other_year.start_doy,
                'moon_phase_delta': self.moon_phase_delta(other_year)
                }

    def moon_phase_delta(self, other_year):
        """ Return the difference in days between first full moons of two years"""

        # override year so month/day comparisons can be made
        other_year_next_full_moon = list(other_year.next_full_moon.tuple())
        other_year_next_full_moon[0] = self.year
        other_year_next_full_moon = ephem.Date(tuple(other_year_next_full_moon))

        other_year_previous_full_moon = list(other_year.previous_full_moon.tuple())
        other_year_previous_full_moon[0] = self.year - 1
        other_year_previous_full_moon = ephem.Date(tuple(other_year_previous_full_moon))

        return min([abs(self.next_full_moon - other_year_next_full_moon),
                    abs(self.next_full_moon - other_year_previous_full_moon)])


if __name__ == '__main__':

    moon_phase_tolerance = 3.5

    year = YearProperties(2023)
    print(year.year)
    print(year.leap)
    print(year.start_doy)
    print(year.previous_full_moon)
    print(year.next_full_moon)
    print()

    # Compare 2023 to other years in future
    print(f'Years matching {year.year} with moon phase tolerance of {moon_phase_tolerance} days:')
    for other_year in range(1940, 2083):
        if other_year != year.year:
            comparison = year.compare_years(YearProperties(other_year))
            if comparison['leap'] and comparison['start_doy'] and comparison['moon_phase_delta'] < moon_phase_tolerance:
                print(f'{other_year}: {year.compare_years(YearProperties(other_year))}')
