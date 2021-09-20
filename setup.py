#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'cookiecutter==1.7.3', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Stavros Kolometsos",
    author_email='stkolome@iit.demokritos.gr',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Evolved5G CLI prototype ",
    entry_points={
        'console_scripts': [
            'evolved5g=evolved5g.cli:cli',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='evolved5g',
    name='evolved5g',
    packages=find_packages(include=['evolved5g', 'evolved5g.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/skolome/evolved5g',
    version='0.1.5',
    zip_safe=False,
)
