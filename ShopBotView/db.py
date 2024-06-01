from mysql import establish_connection

def create_tables():
    connection = establish_connection()
    with connection:
        with connection.cursor() as cursor:
            create_table_article = """
                CREATE TABLE IF NOT EXISTS article (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(45) NOT NULL,
                    price VARCHAR(45) NOT NULL,
                    about VARCHAR(256) NOT NULL,
                    picture varchar(256) NOT NULL
                )
            """

            try:
                cursor.execute(create_table_article)
                print("[LOG] Tables was seccsessfuly created")
            except Exception as e:
                print("[ERROR]:", e)
        
if __name__ == '__main__':
	create_tables()