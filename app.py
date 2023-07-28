import os.path
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from recalendar import YearProperties


app = Flask(__name__)
app.config['SECRET_KEY'] = '4926Oe720$'


@app.route('/', methods=('GET', 'POST'))
def calendar():

    if request.method == 'POST':
        phase_tolerance_input = request.form['phase_tolerance']
        if not phase_tolerance_input:
            flash('Please enter a phase tolerance!')
        else:
            phase_tolerance = float(phase_tolerance_input)

    else:
        phase_tolerance = 3.5  # default to 3.5 days

    year_list = []
    for year_int in range(1940, 2084):
        year = YearProperties(year_int)
        year_past = []
        year_future = []
        for year_other in range(1940, 2084):
            if year_other != year.year:
                comparison = year.compare_years(YearProperties(year_other))
                if comparison['leap'] and comparison['start_doy']:
                    if year_other < year.year:
                        year_past.append([year_other, comparison])
                    else:
                        year_future.append([year_other, comparison])
        year_list.append([year, year_past, year_future])
    return render_template('calendar.html', year_rows=year_list, phase_tolerance=phase_tolerance)


if __name__ == '__main__':
    app.run()
