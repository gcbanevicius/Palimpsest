#!/usr/bin/python

import sys

def parseText(fileName):
    import xml.etree.ElementTree as ET
    tree = ET.parse(fileName) #'Aeneid_English.xml')
    root = tree.getroot()

    books_raw = root.findall('text/body/div1')

    books = []
    book_idx = 0
    chap_idx = 0
    for book_raw in books_raw:
        book_idx += 1
        chap_idx = 0
        tags = book_raw.findall('*')
        #print tags, len(tags)
        book = []
        for tag in tags:
            if tag.tag == 'p': # only <p> tags have useful data	
                chap_idx += 1 # new <p> tag means new chapter
                lines = tag.itertext()
                chap_text = ''
                for line in lines:
                    #print line, "!?!?"
                    #book.append( (ET.tostring(line, encoding='utf_8', method='text'), card_idx) )
					# WHY I STORE THE INDEX HERE ONLY TO NOT USE IT AND RECALC IT LATER IS A MYSTERY...
					
					# the new way (lol)... just get all the text
					chap_text += line				
                print chap_text
                idx = str(book_idx) + '.' + str(chap_idx)
                book.append( (chap_text, idx) )
            # a bit extreme...
            #else:
            #    exit(1)
        books.append(book)

	### OLD WAY ###
    #books = []
    #card_idx = 0
    #for book_raw in books_raw:
    #    lines = book_raw.findall('*')
    #    book = []
    ##card = []
    #    for line in lines:
    #        if line.tag == 'milestone':
    #            card_idx += 1
    #        elif line.find('milestone') is not None:
    #            card_idx += 1
    #        #print ET.tostring(line, encoding='utf_8', method='text')
    #            book.append( (ET.tostring(line, encoding='utf_8', method='text'), card_idx) )
    #        elif line.text:  #line.tag == "l":
    #            book.append( (ET.tostring(line, encoding='utf_8', method='text'), card_idx) )
    #    books.append(book)

	

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
    #path = str(b_idx)
    #data = (path,)
    #curs.execute("""INSERT INTO aen_lat (path) VALUES (%s);""", data)

    #c_idx = 0
    #for c in b:
    #    c_idx += 1
    #    path = str(b_idx)+'.'+str(c_idx)
    #    data = (path,)
    #    curs.execute("""INSERT INTO aen_lat (path) VALUES (%s);""", data)

        c_idx = 0
        for c in b:
            c_idx += 1
            chap_num += 1
        #print c.find('l').text
        #print l.text
            path = str(b_idx)+'.'+str(c_idx)
            text = c #.text
            data = (path, chap_num, c[0], chap_num, 'gallic_war')
            curs.execute("""INSERT INTO english VALUES (%s, %s, %s, %s, %s);""", data)

    conn.commit()
    if conn:
        conn.close()

def main():
    #if len(sys.argv) > 2:
    #    print 'Takes one argument: file name to parse'
        
    fileName = 'Gallic_War_English.xml' #sys.argv[1]
    parseText(fileName)

if __name__ == '__main__':
    main()
