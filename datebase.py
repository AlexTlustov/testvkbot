import psycopg2 as pg
# from config import host, user, password, db_name

with pg.connect(
    database='dataclients', 
    user='postgres', 
    password='7753191qq'
    ) as conn:
    conn.autocommit = True


def create_table_seen_person(): 
    pass


def insert_data_seen_person(id_vk):
    pass


def check():
    pass


def delete_table_seen_person():
    pass

