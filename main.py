from flask import Flask, render_template, url_for, request
from data import queries
import math
from dotenv import load_dotenv

from data.queries import get_shows, get_pages_num

load_dotenv()
app = Flask('codecool_series')


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/shows/most-rated')
@app.route('/shows/most-rated/<int:page_num>')
@app.route('/shows', defaults={'page_num': 1})
def shows_most_rated(page_num=1):
    sort_by = request.args.get('sort_by', 'rating')
    sort_order = request.args.get('sort_order', 'desc')
    shows = queries.get_most_rated_shows(page_num, sort_by, sort_order)
    num = queries.get_pages_num()['num']
    from_num = page_num - 2 if (page_num > 3) else 1
    to_num = page_num + 2 if (page_num < num - 2) else num
    if page_num > num - 2:
        from_num = num - 4
    if page_num < 3:
        to_num = 5
    return render_template('most_rated_shows.html',
                           page_title="Most rated shows",
                           shows=shows,
                           num=num,
                           current_page=page_num,
                           from_num=from_num,
                           to_num=to_num)



if __name__ == '__main__':
    app.run(debug=True)


def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()
