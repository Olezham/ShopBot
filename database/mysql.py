import pymysql
import uuid

import time, datetime
import os

from config import host, username, password, db

current_data = datetime.datetime.now()
joindata = time.mktime(current_data.timetuple())
#salt = bcrypt.gensalt()


def establish_connection():
    connection = pymysql.connect(
        host=host,
        user=username,
        password=password,
        database=db,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def generate_uid():
    return str(uuid.uuid4())



def get_all_articles():
    connection = establish_connection()
    with connection:
        with connection.cursor() as cursor:
            insert_query = "SELECT * FROM article"
            cursor.execute(insert_query)
            result = cursor.fetchall()
            return result
        
def get_all_articles_eu():
    connection = establish_connection()
    with connection:
        with connection.cursor() as cursor:
            insert_query = "SELECT * FROM article_eu"
            cursor.execute(insert_query)
            result = cursor.fetchall()
            return result

def delete_article(image):
    connection = establish_connection()
    with connection:
        with connection.cursor() as cursor:
            insert_query = "DELETE FROM article WHERER image = %s"
            cursor.execute(insert_query, (image))
            connection.commit()

def add_article(title, price, about, picture):
    connection = establish_connection()
    with connection:
        with connection.cursor() as cursor:
            insert_query = "INSERT INTO `article` (title,price,about,picture) VALUES (%s,%s,%s,%s)"
            cursor.execute(insert_query, (title, price, about, picture))
            connection.commit()

def add_article_eu(title, price, about, picture):
    connection = establish_connection()
    with connection:
        with connection.cursor() as cursor:
            insert_query = "INSERT INTO `article_eu` (title,price,about,picture) VALUES (%s,%s,%s,%s)"
            cursor.execute(insert_query, (title, price, about, picture))
            connection.commit()