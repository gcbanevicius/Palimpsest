#!/usr/bin/python

import sys, re
import psycopg2


def db_connect():
    try:
        conn = psycopg2.connect("dbname='simple_ltree'") # user='gbanevic'")  #host='localhost' password='password'")
    except:
        print "Could not connect to database"
    curs = conn.cursor()

    #if conn:
    #    conn.close()
    return curs


def book(bk_start):
    curs = db_connect()
    query = (str(bk_start), )
    curs.execute("""SELECT * FROM aen_lat WHERE path <@ %s""", query)
    lines = curs.fetchall()
    #print lines

def line(ln_start):
    curs = db_connect()
    query = (str(ln_start), )
    curs.execute("""SELECT * FROM aen_lat WHERE path <@ %s""", query)
    line = curs.fetchall()
    print line

def lineToLine(start, end):
    curs = db_connect()
    
    bk_start = int(start.split('.')[0])
    bk_end = int(end.split('.')[0])

    ln_start = int(start.split('.')[1])
    ln_end = int(end.split('.')[1])

    if int(bk_start) > int(bk_end):
        print "Starting position is greater than ending position"
        exit(1)

    print "Book range:", bk_start, bk_end
    print "Linerange:", ln_start, ln_end

    lines = []

    # get the first book
    query = (str(bk_start), )
    curs.execute("""SELECT * FROM aen_lat WHERE path <@ %s;""", query)
    lines.extend(curs.fetchall())
    
    # if the lines only span one book
    if bk_start == bk_end:
        lines = lines[ln_start-1 : ln_end]
        #print lines
        return lines 

    # if there's at least one full book between them
    elif bk_end - bk_start > 1:
        for i in range(bk_start+1, bk_end):
            query = (str(i), )
            curs.execute("""SELECT * FROM aen_lat WHERE path <@ %s;""", query)
            lines.extend(curs.fetchall())
            
    # now get the last book
    query = (str(bk_end), )
    curs.execute("""SELECT * FROM aen_lat WHERE path <@ %s;""", query)
    lines.extend(curs.fetchall()[:ln_end])
    
    #print lines
    return lines

def bookToBook(start, end):
    curs = db_connect()
    
    bk_start = int(start) #int(start.split('.')[0])
    bk_end = int(end) #int(end.split('.')[0])

    #ln_start = int(start.split('.')[1])
    #ln_end = int(end.split('.')[1])

    # equality OK; strange to query one book as a range, but acceptable
    if int(bk_start) > int(bk_end):
        print "Starting position is greater than ending position"
        exit(1)

    print "Book range:", bk_start, bk_end
    #print "Linerange:", ln_start, ln_end

    lines = []

    # get the first book
    query = (str(bk_start), )
    curs.execute("""SELECT * FROM aen_lat WHERE path <@ %s;""", query)
    lines.extend(curs.fetchall())
    
    # if the lines only span one book
    if bk_start == bk_end:
        #lines = lines[ln_start-1 : ln_end]
        #print lines
        return lines 

    # if there's at least one full book between them
    elif bk_end - bk_start > 1:
        for i in range(bk_start+1, bk_end):
            query = (str(i), )
            curs.execute("""SELECT * FROM aen_lat WHERE path <@ %s;""", query)
            lines.extend(curs.fetchall())
            
    # now get the last book
    query = (str(bk_end), )
    curs.execute("""SELECT * FROM aen_lat WHERE path <@ %s;""", query)
    lines.extend(curs.fetchall())
    
    #print lines
    return lines

def bookToLine(start, end):
    curs = db_connect()
    
    bk_start = int(start) #int(start.split('.')[0])
    bk_end = int(end.split('.')[0])

    ln_start = 1; #int(start.split('.')[1])
    ln_end = int(end.split('.')[1])

    if int(bk_start) > int(bk_end):
        print "Starting position is greater than ending position"
        exit(1)

    print "Book range:", bk_start, bk_end
    print "Linerange:", ln_start, ln_end

    lines = []

    # get the first book
    query = (str(bk_start), )
    curs.execute("""SELECT * FROM aen_lat WHERE path <@ %s;""", query)
    lines.extend(curs.fetchall())
    
    # if the lines only span one book
    if bk_start == bk_end:
        lines = lines[: ln_end]
        #print lines
        return lines 

    # if there's at least one full book between them
    elif bk_end - bk_start > 1:
        for i in range(bk_start+1, bk_end):
            query = (str(i), )
            curs.execute("""SELECT * FROM aen_lat WHERE path <@ %s;""", query)
            lines.extend(curs.fetchall())
            
    # now get the last book
    query = (str(bk_end), )
    curs.execute("""SELECT * FROM aen_lat WHERE path <@ %s;""", query)
    lines.extend(curs.fetchall()[:ln_end])
    
    #print lines
    return lines

def lineToBook(start, end):
    curs = db_connect()
    
    bk_start = int(start.split('.')[0])
    bk_end = int(end) #int(end.split('.')[0])

    ln_start = int(start.split('.')[1])
    #ln_end = int(end.split('.')[1])

    # note special case that even equality means start pos is too large
    if int(bk_start) >= int(bk_end):
        print "Starting position is greater than ending position"
        exit(1)

    print "Book range:", bk_start, bk_end
    print "Linerange:", ln_start, "end" #ln_end

    lines = []

    # get the first book
    query = (str(bk_start), )
    curs.execute("""SELECT * FROM aen_lat WHERE path <@ %s;""", query)
    lines.extend(curs.fetchall())
    
    # if the lines only span one book
    if bk_start == bk_end:
        lines = lines[ln_start-1 : ]
        #print lines
        return lines 

    # if there's at least one full book between them
    elif bk_end - bk_start > 1:
        for i in range(bk_start+1, bk_end):
            query = (str(i), )
            curs.execute("""SELECT * FROM aen_lat WHERE path <@ %s;""", query)
            lines.extend(curs.fetchall())
            
    # now get the last book
    query = (str(bk_end), )
    curs.execute("""SELECT * FROM aen_lat WHERE path <@ %s;""", query)
    lines.extend(curs.fetchall())
    
    #print lines
    return lines
    

def main():
    #print len(sys.argv)
    if len(sys.argv) < 2:
        print "Please input a single query or query range"
        exit(1)

    query = sys.argv[1]      
    query = query.replace('-', ' ')
    print query
    q_list = query.split() # no options will do any whitespace
    print q_list
    q_len = len(query.split())

    if q_len > 2:
        print "Please limit query to single index or range of two"
        exit(1)

    elif q_len == 2:
        match = re.match(r'^\s*\d+\s*\d+\s*$', query)
        if match:
            print '1-1'
            q_result = bookToBook(q_list[0], q_list[1])

        match = re.match(r'^\s*\d+\.\d+\s*\d+\.\d+\s*$', query)
        if match:
            print '2-2'
            q_result = lineToLine(q_list[0], q_list[1])
        
        match = re.match(r'^\s*\d+\s*\d+\.\d+\s*$', query)
        if match:
            print '1-2'
            q_result = bookToLine(q_list[0], q_list[1])

        match = re.match(r'^\s*\d+\.\d+\s*\d+\s*$', query)
        if match:
            print '2-1'
            print match.group()
            print q_list[0] + ' and ' + q_list[1]
            q_result = lineToBook(q_list[0], q_list[1])


    elif q_len == 1:
        match = re.match(r'^\s*\d+\s*$', query)
        if match:
            print '1'
            print match.group()
            q_result = book(match.group())

        match = re.match(r'^\s*\d+\.\d+\s*$', query)
        if match:
            print '2'
            print match.group()
            q_result = line(match.group())

    else:
        print "Please input a query"
        exit(1) 

    # all done!
    print q_result    
    return q_result
    


if __name__ == "__main__":
    main()
