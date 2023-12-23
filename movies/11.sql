SELECT title
FROM movies
JOIN stars, people, ratings
ON stars.movie_id = ratings.movie_id
AND movies.id = stars.movie_id
AND stars.person_id = people.id
WHERE name = 'Chadwick Boseman'
ORDER BY rating DESC
LIMIT 5;
