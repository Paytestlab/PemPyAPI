#!/usr/bin/python3

"""
Setup module based on setuptools.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Ax Robot Integration Layer',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.5.51',

    description='Integration layer for the AX robot, Ax Mux and Ax Magstripe probe',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # The project's main homepage.
    url='https://github.com/plutonij/PemPyAPI',

    # Author details
    author='Matija Mazalin',
    author_email='matija.mazalin@abrantix.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Users of the Ax Robot',
        'Topic :: Robot integration layer :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='mapping gcode-abstraction pos-testing',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    py_modules=['MultiRobotRest'],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['netifaces'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    #extras_require={
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    #},

    python_requires='>=3',
    
    package_data={
        'ConfigRest': [
            'CardMagstriper.xml',
            'CardMultiplexer.xml',
            'ICP.xml'
            'Ingenico-IPP350.xml',
            'Ingenico-IPP320.xml',
            'Ingenico-IWL250.xml',
            'Ingenico-Move5000.xml',
            'Miura-010.xml',
            'Miura-020.xml',
            'Pax-S920.xml'
            'Verifone-E355.xml'
            'Verifone-MX915.xml'
            'Verifone-MX925.xml'
            'Verifone-P400.xml'
            'Verifone-VX820.xml',
            'Yomani.xml',
            'Yoximo.xml'
            ],
        'Assets' : ['EntryConfiguration.xml']
    },
    include_package_data=True,
   
    data_files=[
        ('ConfigRest', [ 'ConfigRest/CardMagstriper.xml']),
        ('ConfigRest', [ 'ConfigRest/CardMultiplexer.xml']),
        ('ConfigRest', [ 'ConfigRest/ICP.xml']),
        ('ConfigRest', [ 'ConfigRest/Ingenico-IPP350.xml']),
        ('ConfigRest', [ 'ConfigRest/Ingenico-IPP320.xml']),
        ('ConfigRest', [ 'ConfigRest/Ingenico-IWL250.xml']),
        ('ConfigRest', [ 'ConfigRest/Ingenico-Move5000.xml']),
        ('ConfigRest', [ 'ConfigRest/Miura-010.xml']),
        ('ConfigRest', [ 'ConfigRest/Miura-020.xml']),
        ('ConfigRest', [ 'ConfigRest/Pax-S920.xml']),
        ('ConfigRest', [ 'ConfigRest/Verifone-E355.xml']),
        ('ConfigRest', [ 'ConfigRest/Verifone-MX915.xml']),
        ('ConfigRest', [ 'ConfigRest/Verifone-MX925.xml']),
        ('ConfigRest', [ 'ConfigRest/Verifone-P400.xml']),
        ('ConfigRest', [ 'ConfigRest/Verifone-VX820.xml']),
        ('ConfigRest', [ 'ConfigRest/Yomani.xml']),
        ('ConfigRest', [ 'ConfigRest/Yoximo.xml']),
        ( 'Assets',    [ 'Assets/EntryConfiguration.xml'])
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'MultiRobotRest=MultiRobotRest:main',
        ],
    },
)
