#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as file:
    INSTALL_REQUIERES = file.read().splitlines()

test_requirements = ['pytest>=3', ]

setup(
    author="EVOLVED5G project",
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
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
            'cli_helper= evolved5g.cli:cli_helper',
        ],
    },
    install_requires=INSTALL_REQUIERES,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='evolved5g',
    name='evolved5g',
    packages=find_packages(include=['evolved5g', 'evolved5g.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/EVOLVED-5G/SDK-CLI',
    version='0.8.2',
    zip_safe=False,
)
