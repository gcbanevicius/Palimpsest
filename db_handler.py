#!/usr/bin/python

import psycopg2

conn = psycopg2.connect('dbname=simple_postgres user=gbanevic')

cur = conn.cursor()

# open files for reading
gweFile = open('./files/Gallic_War_English.txt', 'r')
gweString = gweFile.read()
#print gweString

cur.execute("INSERT INTO texts_text (title, text_field) VALUES (%s, %s)",
                ('Gallic_War_English', gweString))


# commit, close cursor, close connection
conn.commit()
cur.close()
conn.close()
