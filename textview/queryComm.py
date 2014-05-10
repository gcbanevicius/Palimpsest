#!/usr/bin/python

import sys, re, os
import psycopg2
import urlparse

def getDecimal(numString):
    return int(numString.split('.')[-1]) 

def getInteger(numString):
    return int(numString.split('.')[0]) 

def db_connect():
# Register database schemes in URLs.
    urlparse.uses_netloc.append('postgres')
    urlparse.uses_netloc.append('mysql')

    try:
        if 'DATBASES' not in locals():
            DATABASES = {}

        if 'DATABASE_URL' in os.environ:
            print os.environ['DATABASE_URL']
            url = urlparse.urlparse(os.environ['DATABASE_URL'])

            # Ensure default database exists.
            DATABASES['default'] = DATABASES.get('default', {})

            # Update with environment configuration.
            DATABASES['default'].update({
                'NAME': url.path[1:],
                'USER': url.username,
                'PASSWORD': url.password,
                'HOST': url.hostname,
                'PORT': url.port, 
                })
            if url.scheme == 'postgres':
                DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

            if url.scheme == 'mysql':
                DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'

            print DATABASES['default']

    except Exception:
        print 'Unexpected error:', sys.exc_info()
    
    try:
        #conn = psycopg2.connect("dbname='simple_ltree'") # user='gbanevic' host='localhost' password='password'")
        conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    except:
        print "Could not connect to database"
    curs = conn.cursor()

    #if conn:
    #    conn.close()
    return curs


def book(bk_start, view_mode, uid):
    curs = db_connect()
    query = (int(bk_start), uid)
    if view_mode == 1:
        curs.execute("""SELECT * FROM textview_comment WHERE book = %s AND public = 't' ORDER BY line;""", query)
    elif view_mode == 2:
        curs.execute("""SELECT * FROM textview_comment WHERE book = %s AND public = 'f' AND user_id = %s ORDER BY line;""", query)
    else:
        curs.execute("""SELECT * FROM textview_comment WHERE book = %s AND (public = 't' OR user_id = %s) ORDER BY line;""", query)
    lines = curs.fetchall()
    #print lines
    return lines

def line(ln_start, view_mode, uid):
    curs = db_connect()
    bk_start = int(ln_start.split('.')[0])
    ln_start = int(ln_start.split('.')[1])
    query = (bk_start, ln_start, uid)
    if view_mode == 1:
        curs.execute("""SELECT * FROM textview_comment WHERE book = %s AND line = %s AND public = 't';""", query)
    elif view_mode == 2:
        curs.execute("""SELECT * FROM textview_comment WHERE book = %s AND line = %s AND public = 'f' AND user_id = %s;""", query)
    else:
        curs.execute("""SELECT * FROM textview_comment WHERE book = %s AND line = %s AND (public = 't' OR user_id = %s);""", query)
    line = curs.fetchall()
    return line

def lineToLine(start, end, view_mode, uid):
    curs = db_connect()
    
    bk_start = getInteger(start)
    bk_end = getInteger(end)

    ln_start = getDecimal(start)
    ln_end = getDecimal(end) 

    if int(bk_start) > int(bk_end):
        print 'Starting position is greater than ending position'
        rspStr = 'Starting position is greater than ending position'
        return [('', '', rspStr, '', '')]

    print "Book range:", bk_start, bk_end
    print "Linerange:", ln_start, ln_end

    lines = []

    # get the first book
    query = (int(bk_start), int(ln_start), uid)
    if view_mode == 1:
        curs.execute("""SELECT * FROM textview_comment WHERE book = %s AND line >= %s AND public = 't' ORDER BY line;""", query)
    elif view_mode == 2:
        curs.execute("""SELECT * FROM textview_comment WHERE book = %s AND line >= %s AND public = 'f' AND user_id = %s ORDER BY line;""", query)
    else:
        curs.execute("""SELECT * FROM textview_comment WHERE book = %s AND line >= %s AND (public = 't' OR user_id = %s) ORDER BY line;""", query)

    lines.extend(curs.fetchall())

    # if the lines only span one book
    if bk_start == bk_end:
        # behold the CORRECT way to do things
        print lines
        lines = [ line for line in lines if line[2] <= ln_end ]
        return lines 

    # if there's at least one full book between them
    elif bk_end - bk_start > 1:
        for i in range(bk_start+1, bk_end):
            query = (str(i), uid)
            if view_mode == 1:
                curs.execute("""SELECT * FROM textview_comment WHERE book = %s AND comment_text IS NOT NULL AND public = 't' ORDER BY line;""", query)
            elif view_mode == 2:
                curs.execute("""SELECT * FROM textview_comment WHERE book = %s AND comment_text IS NOT NULL AND public = 'f' AND user_id = %s ORDER BY line;""", query)
            else:
                curs.execute("""SELECT * FROM textview_comment WHERE book = %s AND comment_text IS NOT NULL AND ( public = 't' OR user_id = %s) ORDER BY line;""", query)
            lines.extend(curs.fetchall())
            lines = [ line for line in lines if line[1] > bk_start or line[2] >= ln_start ]

            
    # now get the last book
    query = (str(bk_end), uid)
    if view_mode == 1:
        curs.execute("""SELECT * FROM textview_comment WHERE book = %s AND comment_text IS NOT NULL AND public = 't' ORDER BY line;""", query)
    elif view_mode == 2:
        curs.execute("""SELECT * FROM textview_comment WHERE book = %s AND comment_text IS NOT NULL AND public = 'f' AND user_id = %s ORDER BY line;""", query)
    else:
        curs.execute("""SELECT * FROM textview_comment WHERE book = %s AND comment_text IS NOT NULL AND (public = 't' OR user_id = %s) ORDER BY line;""", query)
    lines.extend(curs.fetchall()[:ln_end])
    lines = [ line for line in lines if line[1] < bk_end or line[2] <= ln_end ]
     
    #print lines
    return lines

def bookToBook(start, end, view_mode, uid):
    curs = db_connect()
    
    bk_start = int(start) #int(start.split('.')[0])
    bk_end = int(end) #int(end.split('.')[0])

    # equality OK; strange to query one book as a range, but acceptable
    if int(bk_start) > int(bk_end):
        print "Starting position is greater than ending position"
        return [('', '', '', '', '')]

    lines = []

    # get the first book
    query = (int(bk_start), int(bk_end), uid)
    if view_mode == 1:
        curs.execute("""SELECT * FROM textview_comment WHERE book >= %s AND book <= %s AND comment_text IS NOT NULL AND public = 't' ORDER BY book, line;""", query)
    elif view_mode == 2:
        curs.execute("""SELECT * FROM textview_comment WHERE book >= %s AND book <= %s AND comment_text IS NOT NULL AND public = 'f' AND user_id = %s ORDER BY book, line;""", query)
    else:
        curs.execute("""SELECT * FROM textview_comment WHERE book >= %s AND book <= %s AND comment_text IS NOT NULL AND (public = 't' OR user_id = %s) ORDER BY book, line;""", query)
    lines.extend(curs.fetchall())

    return linesp

def startQuery(queryStr, view_mode, uid):

    if not queryStr:
        print "Please input a single query or query range"
        return [('', '', '', '', '')]

    query = queryStr.replace('-', ' ')
    q_list = query.split() # no options will do any whitespace
    q_len = len(query.split())

    if q_len > 2:
        print "Please limit query to single index or range of two"
        return [('', '', '', '', '')]

    elif q_len == 2:
        match = re.match(r'^\s*\d+\s*\d+\s*$', query)
        if match:
            #print '1-1'
            q_result = bookToBook(q_list[0], q_list[1], view_mode, uid)

        match = re.match(r'^\s*\d+\.\d+\s*\d+\.\d+\s*$', query)
        if match:
            #print '2-2'
            q_result = lineToLine(q_list[0], q_list[1], view_mode, uid)
        
        match = re.match(r'^\s*\d+\s*\d+\.\d+\s*$', query)
        if match:
            #print '1-2'
            rspStr = 'Please input a valid query!'
            return [('', '', rspStr, '', '')]

        match = re.match(r'^\s*\d+\.\d+\s*\d+\s*$', query)
        if match:
            #print '2-1'
            rspStr = 'Please input a valid query!'
            return [('', '', rspStr, '', '')]

    elif q_len == 1:
        match = re.match(r'^\s*\d+\s*$', query)
        if match:
            #print '1'
            q_result = book(match.group(), view_mode, uid)

        match = re.match(r'^\s*\d+\.\d+\s*$', query)
        if match:
            #print '2'
            q_result = line(match.group(), view_mode, uid)

    else:
        print "Please input a query"
        return [('', '', 'Please input a query', '', '')]

    #print q_result    
    return q_result
 
def main():
    return startQuery(sys.argv[1], 1, 0)

if __name__ == "__main__":
    main()
