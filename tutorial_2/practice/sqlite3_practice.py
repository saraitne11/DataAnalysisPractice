import sqlite3 as sql


def list_tables(conn: sql.Connection):
    curs = conn.cursor()
    curs.execute('SELECT name from sqlite_master where type="table"')
    tables = list(map(lambda x: x[0], curs.fetchall()))
    curs.close()
    return tables


def list_columns(conn: sql.Connection, table: str):
    curs = conn.cursor()
    curs.execute('SELECT * from %s' % table)
    description = curs.description
    names = list(map(lambda x: x[0], description))
    curs.close()
    return names


# actiontype: 문서 이용시 행동(OPEN, CLOSE, SAVE..)
# ismydoc: 내 문서 해당 여부
# ext: 문서 확장자
# sessionid: 유저 식별자
# documentposition: 문서 이용시 위치 정보(CLOUD, OTHERAPP)
# datetime: TimeStamp
# screen: 앱내 화면 이름


if __name__ == '__main__':
    conn = sql.connect('db/funnel.db')

    tables = list_tables(conn)
    table = tables[0]
    # print(tables)
    # ['log']

    columns = list_columns(conn, table)
    # ['index', 'Unnamed: 0', 'actiontype', 'ismydoc', 'ext', 'sessionid', 'documentposition', 'datetime', 'screen']
    # print(columns)
    columns = columns[2:]

    curs = conn.cursor()
    for col in columns:
        q = """
            SELECT %s,
                    count(%s) as cnt
            FROM %s
            GROUP BY %s
            ORDER BY cnt DESC
            """ % (col, col, table, col)
        print(curs.execute(q).fetchall())
