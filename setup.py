from setuptools import setup

setup(
    name='myhello',
    version='1.0',
    py_modules=['hello'],
    install_requires=[
        'Click',
        ],
    entry_points='''
[console_script]
myhello=hello:cli
''',
    )
