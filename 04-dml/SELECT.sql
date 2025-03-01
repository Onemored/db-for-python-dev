-- Задание 2
-- Название и продолжительность самого длительного трека.
SELECT name, duration 
FROM tracks 
WHERE duration
IN (SELECT MAX(duration) FROM tracks);

-- Название треков, продолжительность которых не менее 3,5 минут.
SELECT name 
FROM tracks
WHERE duration>='00:03:30';

-- Названия сборников, вышедших в период с 2018 по 2020 год включительно.
SELECT name 
FROM compilations
WHERE release_year BETWEEN 2018 AND 2020;

-- Исполнители, чьё имя состоит из одного слова.
SELECT *
FROM artists
WHERE name NOT LIKE '% %';

-- Название треков, которые содержат слово «мой» или «my».
SELECT name 
FROM tracks
WHERE string_to_array(lower(name), ' ') && ARRAY['мой', 'мой %', '% мой', '%мой%', 'my', '% my', 'my %', '%my%'];

-- Задание 3
-- Количество исполнителей в каждом жанре.
SELECT genre_id, COUNT(*) 
FROM artist_genres
GROUP BY genre_id
ORDER BY COUNT(*);

-- Количество треков, вошедших в альбомы 2019–2020 годов.
SELECT a.name, COUNT(s.name) 
FROM albums a JOIN tracks s ON s.album_id = a.album_id
WHERE release_year IN (2019, 2020)
GROUP BY a.name;

-- Средняя продолжительность треков по каждому альбому.
SELECT album_id, AVG(duration) avg_dur 
FROM tracks
GROUP BY album_id
ORDER BY avg_dur;

-- Все исполнители, которые не выпустили альбомы в 2020 году.
SELECT distinct "name" 
FROM artists
WHERE name NOT IN (SELECT DISTINCT m.name FROM artists m
LEFT JOIN artist_albums am ON am.artist_id = m.artist_id
LEFT JOIN albums a ON am.album_id = a.album_id
WHERE release_year=2020);

-- Названия сборников, в которых присутствует конкретный исполнитель (выберите его сами).
SELECT DISTINCT c.name FROM compilations c
LEFT JOIN compilation_tracks sc ON c.compilation_id = sc.compilation_id  
LEFT JOIN tracks s ON sc.track_id = s.track_id 
LEFT JOIN albums a ON s.album_id = a.album_id
LEFT JOIN artist_albums am ON am.album_id = a.album_id 
LEFT JOIN artists m ON am.artist_id = m.artist_id 
WHERE m.name LIKE '%Krek%'
ORDER BY c.name;

-- Задание 4
-- Названия альбомов, в которых присутствуют исполнители более чем одного жанра.
SELECT a.name FROM albums a 
LEFT JOIN artist_albums am ON a.album_id = am.album_id
LEFT JOIN artists m ON m.artist_id = am.artist_id
LEFT JOIN artist_genres gm ON m.artist_id = gm.artist_id
LEFT JOIN genres g ON g.genre_id = gm.genre_id
GROUP BY a.name
HAVING COUNT(DISTINCT g.name) > 1
ORDER BY a.name;

-- Наименования треков, которые не входят в сборники.
SELECT s.name FROM tracks s
LEFT JOIN compilation_tracks sc ON sc.track_id  = s.track_id
WHERE sc.track_id IS null;


--Исполнитель или исполнители, написавшие самый короткий по продолжительности трек, — теоретически таких треков может быть несколько.
SELECT DISTINCT m.name FROM artists m 
LEFT JOIN artist_albums am ON m.artist_id  = am.artist_id 
LEFT JOIN albums a ON am.album_id = a.album_id
LEFT JOIN tracks s ON a.album_id = s.album_id
WHERE duration = (SELECT MIN(duration) FROM tracks);

-- Названия альбомов, содержащих наименьшее количество треков.
SELECT DISTINCT a.name FROM albums a
LEFT JOIN tracks s ON s.album_id = a.album_id
WHERE s.album_id IN (SELECT album_id FROM tracks
GROUP BY album_id
HAVING COUNT(album_id)=(SELECT COUNT(album_id) FROM tracks
GROUP BY album_id
ORDER BY COUNT
LIMIT 1))
ORDER BY a.name;