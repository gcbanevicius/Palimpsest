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
    #sect_idx = 0 # this is just a running count of chapters
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
                #sect_idx += 1
                lines = tag.itertext()
                chap_text = ''
                for line in lines:
                    #sect_idx += 1
                    #print line, "!?!?"
                    #book.append( (ET.tostring(line, encoding='utf_8', method='text'), card_idx) )
					# WHY I STORE THE INDEX HERE ONLY TO NOT USE IT AND RECALC IT LATER IS A MYSTERY...
					
					# the new way (lol)... just get all the text
					chap_text += line				
                print chap_text
                idx = str(book_idx) + '.' + str(chap_idx)
                book.append( (chap_text, idx) )
            # a bit extreme...
            else:
                exit(1)
        books.append(book)
    
    #print books[0]
    #print books[1][1]
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
            chap_num += 1 # running count of comments
            path = str(b_idx)+'.'+str(c_idx)
            text = c[0]
            data = (path, chap_num, c[0], chap_num, 'gallic_war')

            #print '========================'
            #print data
            #print '========================'
            
            curs.execute("""INSERT INTO latin VALUES (%s, %s, %s, %s, %s);""", data)

    conn.commit()
    if conn:
    	conn.close()

def main():
    #if len(sys.argv) > 2:
    #    print 'Takes one argument: file name to parse'
        
    fileName = 'Gallic_War_Latin.xml' #sys.argv[1]
    parseText(fileName)

if __name__ == '__main__':
    main()
