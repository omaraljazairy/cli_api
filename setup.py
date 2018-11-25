from setuptools import setup

setup(
    name = "fedal_cli",
    version = "1.0",
    author = "Omar Aljazairy",
    author_email = "omar@fedal.nl",
    description = ("command line application for my fedal.net api"),
    license = "BSD",
    keywords = "fedal command line",
    url = "https://github.com/omaraljazairy/fedal_cli.git",
    packages=['fedal_cli', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
