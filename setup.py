from setuptools import setup

setup(
    name='fedal_cli',
    version='1.0',
    py_modules=['api_cli', 'spanglish', 'services.logger', 'services/requester'],
    install_requires=[
        'Click',
        'certifi',
        'coverage', 'get', 'httpie', 'idna', 'nose', 'post', 'post', 'public', 'pyaml', 'Pygments', 'PyYAML', 'query-string', 'redis', 'requests'
        ],
    entry_points='''
[console_script]
''',
    )
