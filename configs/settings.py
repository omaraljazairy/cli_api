URL='http://0.0.0.0:8000'

CACHE={
    'REDIS':
        {
            'URL': '192.168.192.26',
            'PASSWORD': 'mytestpass',
            'TTL': 3600,
        },
    'CACHTOOLS':
        {
            'TTL': 30,
            'MAXSIZE': 128,
        },
    }


API={
    'token':
        {
            'token': '/api/token/',
            'refresh': '/api/token/refresh/',
            'verify': '/api/token/verify/',
        },
    'spanglish':
        {
            'words': '/spanglish/words/',
            'word': '/spanglish/word/',
            'verb': '/spanglish/verbs/',
            'sentence': '/spanglish/sentences/',
            'category': '/spanglish/categories/',
            'language': '/spanglish/languages/',
        },
    }

AUTH= {
    'user': 'foobar',
    'password': 'mytest',
    }
