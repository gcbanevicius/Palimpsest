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


    except Exception:
        print 'Unexpected error:', sys.exc_info()
    
    try:
        #conn = psycopg2.connect("dbname='simple_ltree'") # COMMENT BACK IN FOR LOCALHOST
        conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    except:
        print "Could not connect to database"
    curs = conn.cursor()

    return curs


def startQuery(card_start, card_end, text_name):

    curs = db_connect()
    query = (card_start, card_end, text_name)
    try:
        curs.execute("""SELECT * FROM english WHERE card >= %s AND card <= %s AND text_name = %s ORDER BY line_num;""", query)
    except:
        return [('', '', 'No English lines returned...', '')]
    lines = curs.fetchall()
    return lines

def main():
    sys.argv[1] = card_start
    sys.argv[2] = card_end
    startQuery(card_start, card_end, 'aeneid')

if __name__ == '__main__':
    main()
