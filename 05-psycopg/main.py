import psycopg2


def create_db(cur):
    cur.execute("""
    		    DROP TABLE phones;
                DROP TABLE clients;
    	    """)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS clients(
                    client_id SERIAL PRIMARY KEY,
                    first_name VARCHAR(10),
                    last_name VARCHAR(20),
                    email VARCHAR(30) UNIQUE
                );
            """)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS phones(
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER REFERENCES clients(client_id),
                    phone VARCHAR(12)
                );
            """)


def add_client(cur, client_id, first_name, last_name, email, phones=None):
    cur.execute("""
                INSERT INTO clients(client_id, first_name, last_name, email) VALUES(%s, %s, %s, %s);
                """, (client_id, first_name, last_name, email))

    cur.execute("""
                INSERT INTO phones(client_id, phone) VALUES(%s, %s);
                """, (client_id, phones))


def add_phone(cur, client_id, phone):
    cur.execute("""
                INSERT INTO phones(client_id, phone) VALUES(%s, %s);
                """, (client_id, phone))


def change_client(cur, client_id, first_name=None, last_name=None, email=None, phone=None):
    if first_name:
        cur.execute("""
                UPDATE clients SET first_name=%s WHERE client_id=%s;
                """, (first_name, client_id))
    if last_name:
        cur.execute("""
                UPDATE clients SET last_name=%s WHERE client_id=%s;
                """, (last_name, client_id))
    if email:
        cur.execute("""
                UPDATE clients SET email=%s WHERE client_id=%s;
                """, (email, client_id))
    cur.execute("""
            SELECT last_name, first_name, email FROM clients WHERE client_id=%s;
            """, (client_id,))

    cur.execute("""
            UPDATE phones SET phone=%s WHERE client_id=%s;
            """, (phone, client_id))


def delete_phone(cur, client_id, phone):
    cur.execute("""
                DELETE FROM phones WHERE client_id=%s AND phone=%s;
                """, (client_id, phone))


def delete_client(cur, client_id):
    cur.execute("""
                DELETE FROM phones WHERE client_id=%s;
                """, (client_id))
    cur.execute("""DELETE FROM clients WHERE client_id=%s;
                """, (client_id))


def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    conditions = []
    params = []

    if not any([first_name, last_name, email, phone]):
        print('Введите данные для поиска:\nИмя, Фамилию, Email или номер телефона.')
        return

    if first_name:
        conditions.append("first_name ILIKE %s")
        params.append(f'%{first_name}%')

    if last_name:
        conditions.append("last_name ILIKE %s")
        params.append(f'%{last_name}%')

    if email:
        conditions.append("email ILIKE %s")
        params.append(f'%{email}%')

    if phone:
        conditions.append("phone LIKE %s")
        params.append(f'%{phone}%')

    query = f"""
    SELECT clients.client_id, first_name, last_name, email, phone 
    FROM clients 
    JOIN phones ON clients.client_id = phones.client_id
    WHERE {' AND '.join(conditions)}
    """
    cur.execute(query, params)
    print(cur.fetchall())


if __name__ == "__main__":
    with psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost',
                          port='5432') as conn:
        with conn.cursor() as cur:
            create_db(cur)
            add_client(cur, 1, 'Сергей', 'Уткин', 'bigduc@mail.ru')
            add_client(cur, 2, 'Элина', 'Пунина', 'e.punina@mail.ru', 89111111111)
            add_client(cur, 3, 'Сергей', 'Пунин', 's.punin@mail.ru', 89333333333)
            add_client(cur, 4, 'Оля', 'Пунина', 'o.punina@mail.ru', 89444444444)
            add_phone(cur, 1, 89222222222)
            add_phone(cur, 1, 89222223333)
            change_client(cur, 4, first_name='Ольга', last_name='Punya')
            # change_client(cur, 3, 'Сергей', 'Пунин', 's.punin@gmail.com', 89666666666)
            # delete_phone(cur, 1, '89555555555')
            # delete_client(cur,'1')
            # delete_client(cur,'2')
            find_client(cur,phone="89222222222")
            find_client(cur, first_name='Ольга')
            find_client(cur, )
    conn.close()
