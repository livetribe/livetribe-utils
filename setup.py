#!/usr/bin/env python

#
# Copyright 2013 the original author or authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from io import open
import subprocess
import sys

from setuptools import find_packages, setup, Command, os


VERSION = '1.0'

class doc(Command):
    description = 'generate or test documentation'
    user_options = [('test', 't', 'run doctests instead of generating documentation')]
    boolean_options = ['test']

    def initialize_options(self):
        self.test = False

    def finalize_options(self):
        pass

    def run(self):
        if self.test:
            path = 'docs/build/doctest'
            mode = 'doctest'
        else:
            path = 'docs/build/%s' % VERSION
            mode = 'html'

        try:
            os.makedirs(path)
        except OSError:
            pass

        status = subprocess.call(['sphinx-build', '-E', '-b', mode, '-d', 'docs/build/doctrees', 'docs/source', path])

        if status:
            raise RuntimeError('documentation step "%s" failed' % (mode,))

        sys.stdout.write('\nDocumentation step "%s" performed, results here:\n'
                         '   %s/\n' % (mode, path))


class test(Command):
    description = 'run nosetests'
    user_options = [('verbose', 'v', 'run nosetests with -v option')]
    boolean_options = ['verbose']

    def initialize_options(self):
        self.verbose = False

    def finalize_options(self):
        pass

    def run(self):
        if self.verbose:
            verbose = '-v'
        else:
            verbose = ''

        status = subprocess.call(['nosetests', verbose])

        if status:
            raise RuntimeError('nosetests step failed')


with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

tests_requires = install_requires + [
    'nose >= 1.2',
]

setup(
    name='livetribe-utils',
    version=VERSION,
    url='http://github.com/livetribe/livetribe-utils/',
    license='Apache Software License (http://www.apache.org/licenses/LICENSE-2.0)',
    author='Alan D. Cabrera',
    author_email='dev@livetribe.codehaus.org',
    description='Shared utilities.',
    # don't ever depend on refcounting to close files anywhere else
    long_description=open('README.rst', encoding='utf-8').read(),

    namespace_packages=['livetribe'],
    package_dir={'': 'src'},
    packages=find_packages('src'),

    zip_safe=False,
    platforms='any',
    install_requires=install_requires,

    tests_require=tests_requires,
    test_suite='nose.collector',

    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    cmdclass={'doc': doc, 'test': test},
)
