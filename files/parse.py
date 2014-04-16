#!/usr/bin/python

def parseText(fileName):
    import xml.etree.ElementTree as ET
    tree = ET.parse(fileName) #('Aeneid_Latin.xml')
    root = tree.getroot()

    books_raw = root.findall('text/body/div1')
    
    books = []
    card_idx = 0
    for book_raw in books_raw:
        lines = book_raw.findall('*')
        book = []
    #card = []
        for line in lines:
            if line.find('milestone') is not None or line.tag == 'milestone':
                card_idx += 1
            if line.text:  #line.tag == "l":
            #print line.text
            #card.append(line)
                book.append( (ET.tostring(line, encoding='utf_8', method='text'), card_idx) )
            #book.append(line)
        #elif len(card) > 0:
        #    book.append(card)
        #    card = []
        books.append(book)
    
#print book[1]
#print book[1][1]
    import psycopg2
    try:
        conn = psycopg2.connect("dbname='simple_ltree' user='gbanevic' host='localhost' password='password'")
    except:
        print "Could not connect to DB 'simple_ltree'"
    curs = conn.cursor()

    b_idx = 0
    
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

        l_idx = 0
        for l in b:
            l_idx += 1
        #print c.find('l').text
        #print l.text
            path = str(b_idx)+'.'+str(l_idx)
            text = l[0]
            data = (path, l[0], l[1])
            curs.execute("""INSERT INTO aen_lat VALUES (%s, %s, %s);""", data) # % (path, text))

# let's see if we can get our data back...
    curs.execute("""SELECT * FROM aen_lat WHERE path <@ '2.7' """)
    rows = curs.fetchall()
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
    parseText(fileName):

if __name__ == '__main__':
    main()
