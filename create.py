import psycopg2
from psycopg2 import Error

try:
    # Подключиться к существующей базе данных
    connection = psycopg2.connect(user="postgres",
                                  password="1234",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="pbz_2")

    cur = connection.cursor()



    cur.execute('''CREATE TABLE ORGANIZATION 
        (ID INT PRIMARY KEY NOT NULL,
        NAME TEXT NOT NULL)''')

    cur.execute('''CREATE TABLE EMPLOYEE 
        (ID INT PRIMARY KEY NOT NULL,
        NAME TEXT NOT NULL,
        POST TEXT NOT NULL,
        EMAIL TEXT NOT NULL,
        ORGANIZATION_ID INT not null,
        FOREIGN KEY (ORGANIZATION_ID) REFERENCES ORGANIZATION(ID) ON DELETE CASCADE);''')

    cur.execute('''CREATE TABLE DOCUMENT 
        (ID INT PRIMARY KEY NOT NULL,
        REG_DATE TEXT NOT NULL,
        ADRESAT INT NOT NULL,
        ADRESANT INT NOT NULL,
        RESOLUTION_ID INT NOT NULL,
        CONTROLLER_ID INT NOT NULL,
        FOREIGN KEY (ADRESAT) REFERENCES ORGANIZATION(ID) ON DELETE CASCADE,
        FOREIGN KEY (ADRESANT) REFERENCES ORGANIZATION(ID) ON DELETE CASCADE,
        FOREIGN KEY (RESOLUTION_ID) REFERENCES EMPLOYEE(ID) ON DELETE CASCADE,
        FOREIGN KEY (CONTROLLER_ID) REFERENCES EMPLOYEE(ID) ON DELETE CASCADE);''')

    cur.execute('''CREATE TABLE TASK 
        (ID INT PRIMARY KEY NOT NULL,
        NAME TEXT NOT NULL,
        EXPLORER_ID INT NOT NULL,
        EXP_DATE TEXT NOT NULL,
        DOC_ID INT NOT NULL, 
        FOREIGN KEY (DOC_ID) REFERENCES DOCUMENT(ID) ON DELETE CASCADE,
        FOREIGN KEY (EXPLORER_ID) REFERENCES EMPLOYEE(ID) ON DELETE CASCADE);''')



    cur.execute('''CREATE TABLE WORKER
         (ID INT PRIMARY KEY NOT NULL,
         NAME TEXT NOT NULL,
         WORK_POSITION TEXT NOT NULL,
         RANK INT NOT NULL,
         BASE_SALARY FLOAT,
         EXTRA_SALARY FLOAT,
         MINUS_SALARY FLOAT,
         ITOG_SALARY FLOAT,
         MONTH TEXT);''')

    cur.execute('''CREATE TABLE COEFF
             (RANK INT PRIMARY KEY NOT NULL,
             COEFFICIENT FLOAT,
             MONTH TEXT);''')

    connection.commit()

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cur.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")

