#!/usr/bin/python

import sys, re, os
import psycopg2
import urlparse

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


def startQuery(card_start, card_end):
    print 'Starting, ending cards:', card_start, card_end

    curs = db_connect()
    query = (card_start, card_end)
    try:
        curs.execute("""SELECT * FROM aen_eng WHERE card >= %s AND card <= %s ORDER BY line_num;""", query)
    except:
        return [('', '', 'No English lines returned...', '')]
    lines = curs.fetchall()
    print lines
    return lines

def main():
    sys.argv[1] = card_start
    sys.argv[2] = card_end
    startQuery(card_start, card_end)

if __name__ == '__main__':
    main()
