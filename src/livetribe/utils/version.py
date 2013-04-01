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
""" Version handling classes & methods. """

import re
import pkg_resources


def version_for_package(package):
    """ Return the version for a given Python package name. """

    return pkg_resources.get_distribution(package).version


def ensure_version(given, expected):
    """
      Helper to check a version against an expected version.

      :param given: A `str` version.
      :param expected: A `str` version.
      :returns: A `tuple` of (True or False, expected_version)
    """

    given_version = StandardVersion.parse(given)
    expected_version = StandardVersion.parse(expected)

    if given_version < expected_version:
        return False, str(expected_version)
    return True, str(expected_version)


class Version(object):
    """
      Abstract base class for version numbering classes.  Just provides
      __init__ and __repr__, because those seem to be the same for all version
      numbering classes.
    """
    pass


class StandardVersion(Version):
    """ Represents a standard version. """

    _version_re = re.compile(r'^(\d+) (\. (\d+) (\. (\d+))?)? (-([a-zA-Z0-9_\.\-]+))?$', re.VERBOSE)

    def __init__(self, major, minor=None, patch=None, qualifier=None):
        self.version = (major, minor or 0, patch or 0)
        self.qualifier = qualifier

    @classmethod
    def parse(cls, version_string):
        match = cls._version_re.match(version_string)
        if not match:
            raise ValueError("Invalid version number '%s'" % version_string)

        (major, minor, patch, qualifier) = match.group(1, 3, 5, 7)

        return cls(int(major or 0), int(minor or 0), int(patch or 0), qualifier)

    def increment_major(self):
        self._inc_ver(0)

    def increment_minor(self):
        self._inc_ver(1)

    def increment_micro(self):
        self._inc_ver(2)

    def _inc_ver(self, ver_part):
        self.version = tuple([self.version[i] + (1 if i == ver_part else 0) for i in range(len(self.version))])


    @property
    def tuple(self):
        return self.version[0], self.version[1], self.version[2], self.qualifier

    def __str__(self):
        major, minor, micro = self.version
        string = str(major) + '.' + str(minor)
        if micro:
            string += '.' + str(micro)
        if self.qualifier:
            string += '-' + str(self.qualifier)
        return string

    def __repr__(self):
        return 'StandardVersion(%r, %r, %r, %r)' % self.tuple

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __cmp__(self, other):
        if isinstance(other, str):
            other = StandardVersion.parse(other)

        # numeric versions don't match -- qualifier stuff doesn't matter
        if self.version < other.version:
            return -1
        elif self.version > other.version:
            return 1

        # case 1: neither has qualifier; they're equal
        # case 2: self has qualifier, other doesn't; other is greater
        # case 3: self doesn't have qualifier, other does: self is greater
        # case 4: both have qualifier: must compare them!

        if not self.qualifier and not other.qualifier:
            return 0
        elif self.qualifier and not other.qualifier:
            return -1
        elif not self.qualifier and other.qualifier:
            return 1
        elif self.qualifier and other.qualifier:
            if self.qualifier < other.qualifier:
                return -1
            elif self.qualifier > other.qualifier:
                return 1
            else:
                return 0

    def __hash__(self):
        return hash(self.tuple)


class VersionRange(object):
    _range_re = re.compile(r'^([\[\(])\s*(\d+) (\. (\d+) (\. (\d+))?)? (-([a-zA-Z0-9_\.\-]+))?\s*,\s*(\d+) (\. (\d+) (\. (\d+))?)? (-([a-zA-Z0-9_\.\-]+))?\s*([\]\)])$', re.VERBOSE)

    def __init__(self, start, start_include, end, end_include):
        self.start = start
        self.start_include = start_include
        self.end = end
        self.end_include = end_include

    @classmethod
    def parse(cls, range_string):
        match = cls._range_re.match(range_string)
        if not match:
            raise ValueError("Invalid version range '%s'" % range_string)

        start, start_major, start_minor, start_patch, start_qualifier, end_major, end_minor, end_patch, end_qualifier, end = match.group(1, 2, 4, 6, 8, 9, 11, 13, 15, 16)

        start_version = StandardVersion(int(start_major or 0), int(start_minor or 0), int(start_patch or 0), start_qualifier)
        end_version = StandardVersion(int(end_major or 0), int(end_minor or 0), int(end_patch or 0), end_qualifier)
        return cls(start_version, start == '[', end_version, end == ']')

    def contains(self, version):
        if self.start:
            if version < self.start:
                return False
            if not self.start_include and version == self.start:
                return False
        if self.end:
            if version > self.end:
                return False
            if not self.end_include and version == self.end:
                return False
        return True

    @property
    def tuple(self):
        return self.start.tuple, self.start_include, self.end.tuple, self.end_include

    def __str__(self):
        string = '[' if self.start_include else '('
        string += str(self.start) if self.start else ''
        string += ', '
        string += str(self.end) if self.end else ''
        string += ']' if self.end_include else ')'
        return string

    def __repr__(self):
        return 'VersionRange(%r, %r, %r, %r)' % (self.start, self.start_include, self.end, self.end_include)

    def __eq__(self, other):
        return self.tuple == other.tuple

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.tuple)
