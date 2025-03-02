# Работа с БД из python с помощью драйвера psycopg2
import psycopg2

conn = psycopg2.connect(dbname='postgres', user='postgres', password='@Nton199010', host='192.168.90.14', port='5432')

# Создание таблиц. CRUD


with conn.cursor() as cur:
	# cur.execute("""
    # 		DROP TABLE test;
    # 	""")

	# cur.execute("""
    #     	CREATE TABLE IF NOT EXISTS public.albums(
    #             album_id serial NOT NULL,
    #             name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    #             release_year INTEGER NOT NULL,
    #             CONSTRAINT albums_pkey PRIMARY KEY (album_id)
    #     	);
    #     	""")
	# cur.execute("""
    #     	CREATE TABLE IF NOT EXISTS public.artist_albums(
    #             artist_id integer NOT NULL,
    #             album_id integer NOT NULL,
    #             CONSTRAINT artist_albums_pkey PRIMARY KEY (artist_id, album_id)
    #     	);
    #     	""")
	# cur.execute("""
    #     	CREATE TABLE IF NOT EXISTS public.artist_genres(
    #             artist_id integer NOT NULL,
    #             genre_id integer NOT NULL,
    #             CONSTRAINT artist_genres_pkey PRIMARY KEY (artist_id, genre_id)
    #     	);
    #     	""")

	# cur.execute("""
    #     	CREATE TABLE IF NOT EXISTS public.artists(
    #             artist_id serial NOT NULL,
    #             name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    #             CONSTRAINT artists_pkey PRIMARY KEY (artist_id)
    #     	);
    #     	""")

	# cur.execute("""
    #     	CREATE TABLE IF NOT EXISTS public.compilation_tracks(
    #             compilation_id integer NOT NULL,
    #             track_id integer NOT NULL,
    #             CONSTRAINT compilation_tracks_pkey PRIMARY KEY (compilation_id, track_id)
    #     	);
    #     	""")

	# cur.execute("""
    #     	CREATE TABLE IF NOT EXISTS public.compilations(
    #             compilation_id serial NOT NULL,
    #             name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    #             release_year INTEGER NOT NULL,
    #             CONSTRAINT compilations_pkey PRIMARY KEY (compilation_id)
    #     	);
    #     	""")

	# cur.execute("""
    #     	CREATE TABLE IF NOT EXISTS public.genres(
    #             genre_id serial NOT NULL,
    #             name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    #             CONSTRAINT genres_pkey PRIMARY KEY (genre_id)
    #     	);
    #     	""")

	# cur.execute("""
    #     	CREATE TABLE IF NOT EXISTS public.tracks(
    #             track_id serial NOT NULL,
    #             name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    #             duration TIME NOT NULL,
    #             album_id INTEGER NOT NULL,
    #             CONSTRAINT tracks_pkey PRIMARY KEY (track_id)
    #     	);
    #     	""")

	# cur.execute("""
    #     	ALTER TABLE IF EXISTS public.artist_albums
    #             ADD CONSTRAINT artist_albums_album_id_fkey FOREIGN KEY (album_id)
    #             REFERENCES public.albums (album_id) MATCH SIMPLE
    #             ON UPDATE NO ACTION
    #             ON DELETE NO ACTION;
    #     	""")

	# cur.execute("""
    #     	ALTER TABLE IF EXISTS public.artist_albums
    #             ADD CONSTRAINT artist_albums_artist_id_fkey FOREIGN KEY (artist_id)
    #             REFERENCES public.artists (artist_id) MATCH SIMPLE
    #             ON UPDATE NO ACTION
    #             ON DELETE NO ACTION;
    #     	""")

	# cur.execute("""
    #     	ALTER TABLE IF EXISTS public.artist_genres
    #             ADD CONSTRAINT artist_genres_artist_id_fkey FOREIGN KEY (artist_id)
    #             REFERENCES public.artists (artist_id) MATCH SIMPLE
    #             ON UPDATE NO ACTION
    #             ON DELETE NO ACTION;
    #         """)

	# cur.execute("""
    #     	ALTER TABLE IF EXISTS public.artist_genres
    #             ADD CONSTRAINT artist_genres_genre_id_fkey FOREIGN KEY (genre_id)
    #             REFERENCES public.genres (genre_id) MATCH SIMPLE
    #             ON UPDATE NO ACTION
    #             ON DELETE NO ACTION;
    #     	""")
    
	# cur.execute("""
    #     	ALTER TABLE IF EXISTS public.compilation_tracks
    #             ADD CONSTRAINT compilation_tracks_compilation_id_fkey FOREIGN KEY (compilation_id)
    #             REFERENCES public.compilations (compilation_id) MATCH SIMPLE
    #             ON UPDATE NO ACTION
    #             ON DELETE NO ACTION;
    #     	""")
    
	# cur.execute("""
    #     	ALTER TABLE IF EXISTS public.compilation_tracks
    #             ADD CONSTRAINT compilation_tracks_track_id_fkey FOREIGN KEY (track_id)
    #             REFERENCES public.tracks (track_id) MATCH SIMPLE
    #             ON UPDATE NO ACTION
    #             ON DELETE NO ACTION;
    #     	""")
    
	# cur.execute("""
    #     	ALTER TABLE IF EXISTS public.tracks
    #             ADD CONSTRAINT tracks_album_id_fkey FOREIGN KEY (album_id)
    #             REFERENCES public.albums (album_id) MATCH SIMPLE
    #             ON UPDATE NO ACTION
    #             ON DELETE NO ACTION;
    #         """)
	# conn.commit()

	cur.execute("""
			SELECT * FROM tracks;
			""")
	print('fetchall', cur.fetchall())
    

	cur.execute("""
			SELECT * FROM albums;
			""")
	print(cur.fetchone())
	
	cur.execute("""
			SELECT * FROM albums;
			""")
	print(cur.fetchmany(2))

# Выбор данных из таблицы.
	cur.execute("""
			SELECT name FROM tracks WHERE track_id=%s;
			""", (3,))
	print(cur.fetchone())

# Функция для извлечения данных (Выдает имя по track_id)
	def get_track_name(cursor, track_id: str) -> int:
		cursor.execute("""
				 SELECT name FROM tracks where track_id=%s
				 """, (track_id,))
		return cur.fetchone()[0]
	
	track_name = get_track_name(cur, '5')
	print('track_name', track_name)
					

conn.close()
