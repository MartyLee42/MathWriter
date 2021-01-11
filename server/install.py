import pymysql

con = pymysql.connect('localhost', 'root','rootroot')
cur = con.cursor()

try:
    cur.execute("CREATE DATABASE MathWriter")
except BaseException as er:
    print(er)


con = pymysql.connect('localhost', 'root','rootroot', "MathWriter")
cur = con.cursor()

try:
    cur.execute("""CREATE TABLE conspect
                   (conspect_id INT NOT NULL AUTO_INCREMENT,
                    title TEXT,
                    prev_title TEXT,
                    CONSTRAINT conspect_id PRIMARY KEY (conspect_id)
                   );""")
except BaseException as er:
    print(er)



try:
    cur.execute("""CREATE TABLE conspect_text
                   (text_id INT NOT NULL AUTO_INCREMENT,
                    conspect_id INT,
                    content TEXT,
                    CONSTRAINT text_id PRIMARY KEY (text_id)
                   );""")
except BaseException as er:
    print(er)
