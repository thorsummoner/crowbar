import os
from setuptools import setup

setup(
    name = "vpk_scape",
    version = "0.0.0",
    author = "Dylan Grafmyre",
    author_email = "thorsummoner0@gmail.com",
    description = "A graphical PGK Browser/Extractor Utillity",
    license = "GPL v3.0",
    keywords = "sourcesdk, valve, vpk, valve pack file",
    # url = "",
    packages=['vpk_scape', 'tests'],
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),

    package_data = {
        'vpk_scape': ['data/*'],
    },

    # classifiers=[
    #     "Development Status :: 3 - Alpha",
    #     "Topic :: Utilities",
    #     "License :: OSI Approved :: GPL License",
    # ],
    entry_points={
        # 'console_scripts': [
        #     'foo = my_package.some_module:main_func',
        #     'bar = other_module:some_func',
        # ],
        'gui_scripts': [
            'vpk_scape = vpk_scape.__main__:main',
        ]
    }
)
