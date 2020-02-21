import sqlite3 as sql

con = sql.connect('db/doc_use_log.db')

curs = con.cursor()

q = """
    SELECT *
    FROM log
    WHERE ext = 'PDF'
    AND ismydoc = '0'
    LIMIT 20
    """

rows = curs.execute(q)
for row in rows:
    print(row)