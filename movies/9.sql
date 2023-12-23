SELECT DISTINCT name FROM people JOIN stars, movies ON movies.id = stars.movie_id AND people.id = stars.person_id WHERE year = 2004 ORDER BY birth;
