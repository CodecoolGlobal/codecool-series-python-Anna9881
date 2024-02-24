from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_most_rated_shows():
    return data_manager.execute_select(
        """ 
       SELECT title, TO_CHAR(year, 'YYYY') AS year, runtime, COALESCE(trailer, 'No URL') AS trailer, ROUND(rating, 2) AS rating, STRING_AGG(genres.name, ', ') AS genres, homepage FROM shows
        LEFT JOIN show_genres ON shows.id = show_genres.show_id
        LEFT JOIN genres ON genres.id = show_genres.genre_id
        GROUP BY shows.id
        ORDER BY shows.rating DESC
        LIMIT 15;
        """
)

