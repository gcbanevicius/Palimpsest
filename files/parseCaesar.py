#!/usr/bin/python

import sys

def parseText(fileName):
    import xml.etree.ElementTree as ET
    tree = ET.parse(fileName) #('Aeneid_Latin.xml')
    root = tree.getroot()

    books_raw = root.findall('text/body/div1')

    books = []
    book_idx = 0
    chap_idx = 0
    sect_idx = 0
    for book_raw in books_raw:
        book_idx += 1
        chap_idx = 0
        tags = book_raw.findall('*')
        book = []
        for tag in tags:
            if tag.tag == 'head':
                pass
            elif tag.tag == 'p': # assuming it's a <head> or a <p>
                chap_idx += 1 # new <p> tag means new chapter
                lines = tag.itertext()
                for line in lines:
                    sect_idx += 1
                    #print line, "!?!?"
                    #book.append( (ET.tostring(line, encoding='utf_8', method='text'), card_idx) )
                    idx = str(book_idx) + '.' + str(chap_idx) + '.' + str(sect_idx)
                    book.append( (line, idx) )
            # a bit extreme...
            else:
                exit(1)
        books.append(book)
    
    print books[0]
    print books[1][1]
    import psycopg2
    try:
        conn = psycopg2.connect("dbname='simple_ltree' user='gbanevic' host='localhost' password='password'")
    except:
        print "Could not connect to DB 'simple_ltree'"
    curs = conn.cursor()

    b_idx = 0
    line_num = 0
    
    for b in books:
        b_idx += 1
        l_idx = 0
        for l in b:
            l_idx += 1
            line_num += 1
            path = str(b_idx)+'.'+str(l_idx)
            text = l[0]
            data = (path, line_num, l[0], l[1], 'gallic_war')
            print data
            #curs.execute("""INSERT INTO latin VALUES (%s, %s, %s, %s, %s);""", data) # % (path, text))

# let's see if we can get our data back...
    #curs.execute("""SELECT * FROM aen_lat WHERE path <@ '2.7' """)
    #rows = curs.fetchall()
#print rows
    for row in rows:
        if row[1]:
            print row[1]

    conn.commit()
    if conn:
        conn.close()

def main():
    if len(sys.argv) > 2:
        print 'Takes one argument: file name to parse'
        
    fileName = sys.argv[1]
    parseText(fileName)

if __name__ == '__main__':
    main()
