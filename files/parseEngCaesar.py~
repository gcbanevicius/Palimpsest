#!/usr/bin/python

import sys

def parseText(fileName):
    import xml.etree.ElementTree as ET
    tree = ET.parse(fileName)
    root = tree.getroot()

    books_raw = root.findall('text/body/div1')

    books = []
    book_idx = 0
    chap_idx = 0
    for book_raw in books_raw:
        book_idx += 1
        chap_idx = 0
        tags = book_raw.findall('*')
        book = []
        for tag in tags:
            if tag.tag == 'p': # only <p> tags have useful data	
                chap_idx += 1 # new <p> tag means new chapter
                lines = tag.itertext()
                chap_text = ''
                for line in lines:
					chap_text += line	
                idx = str(book_idx) + '.' + str(chap_idx)
                book.append( (chap_text, idx) )
        books.append(book)

    import psycopg2
    try:
        conn = psycopg2.connect("dbname='simple_ltree' user='gbanevic' host='localhost' password='password'")
    except:
        print "Could not connect to DB 'simple_ltree'"
    curs = conn.cursor()

    b_idx = 0
    chap_num = 0
        
    for b in books:
        b_idx += 1
        c_idx = 0
        for c in b:
            c_idx += 1
            chap_num += 1
            path = str(b_idx)+'.'+str(c_idx)
            text = c 
            data = (path, chap_num, c[0], chap_num, 'gallic_war')
            curs.execute("""INSERT INTO english VALUES (%s, %s, %s, %s, %s);""", data)

    conn.commit()
    if conn:
        conn.close()

def main():
        
    fileName = 'Gallic_War_English.xml'
    parseText(fileName)

if __name__ == '__main__':
    main()
