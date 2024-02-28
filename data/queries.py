from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_most_rated_shows(page_num=1, sort_by='rating', sort_order='desc'):
    sort_order_sql = 'ASC' if sort_order == 'asc' else 'DESC'
    valid_sort_columns = ['title', 'year', 'runtime', 'rating']
    if sort_by not in valid_sort_columns:
        sort_by = 'rating'
    return data_manager.execute_select(f"""
        SELECT title, 
               TO_CHAR(year, 'YYYY') AS year, 
               runtime,
               ROUND(rating, 2) AS rating, 
               COALESCE(trailer, 'No URL') AS trailer,
               STRING_AGG(genres.name, ', ') AS genres, 
               homepage FROM shows
        LEFT JOIN show_genres ON shows.id = show_genres.show_id
        LEFT JOIN genres ON genres.id = show_genres.genre_id
        GROUP BY shows.id
        ORDER BY {sort_by} {sort_order_sql}, shows.id {sort_order_sql}
        OFFSET (%(page_num)s-1)*15 LIMIT 15;
        """, {'page_num': page_num})

def get_show(show_id):
    return data_manager.execute_select("""
            SELECT
                title,
                runtime,
                CONCAT(ROUND(rating, 1)) AS rating,
                STRING_AGG(genres.name, ', ') AS genres,
                trailer,
                overview
            FROM shows
            LEFT JOIN show_genres ON shows.id = show_genres.show_id
            LEFT JOIN genres ON genres.id = show_genres.genre_id
            WHERE shows.id = %(show_id)s
            GROUP BY shows.id
        """, {"show_id":show_id}, fetchall=False)

def get_actors(show_id):
    return data_manager.execute_select("""
    SELECT actors.name AS actors FROM shows
            LEFT JOIN show_characters ON show_characters.show_id = shows.id
            LEFT JOIN actors ON actors.id = show_characters.actor_id
            WHERE shows.id = %(show_id)s
            ORDER BY actor_id
            LIMIT 3
    """, {"show_id": show_id})


def get_pages_num():
    return data_manager.execute_select("""
        SELECT count(*)/15 AS num FROM shows
        """, fetchall=False)