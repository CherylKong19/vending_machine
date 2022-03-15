import sqlite3

conn = sqlite3.connect('stats.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE stats
          (id INTEGER PRIMARY KEY ASC, 
           sanitizer_quantity INTEGER NOT NULL,
           sanitizer_price INTEGER NOT NULL,
           mask_quantity INTEGER NOT NULL,
           mask_price INTEGER NOT NULL,
           last_updated VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
