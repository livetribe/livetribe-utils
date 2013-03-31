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
from unittest import TestCase

from livetribe.utils.version import StandardVersion, VersionRange


class TestStandardVersion(TestCase):
    def test_std_init(self):
        """ create StandardVersion from string """
        version = StandardVersion.parse('1.2.3-YOKO')

        assert version.version[0] == 1
        assert version.version[1] == 2
        assert version.version[2] == 3
        assert version.qualifier == 'YOKO'

        version = StandardVersion.parse('1.2.1102-RC2.4622')

        assert version.version[0] == 1
        assert version.version[1] == 2
        assert version.version[2] == 1102
        assert version.qualifier == 'RC2.4622'


    def test_std_equals(self):
        """ test equals override for StandardVersion """

        version1 = StandardVersion.parse('1.2.3-YOKO')
        version2 = StandardVersion.parse('1.2.3-YOKO')

        assert version1 is not version2, 'Two instances of StandardVersion are not the same'
        assert version1 == version2


    def test_std_not_equals(self):
        """ test not equals override for StandardVersion """

        assert StandardVersion.parse('1.2.3-YOKO') != StandardVersion.parse('1.2.3-NOBU'), 'Two instances of StandardVersion are equal'
        assert not (StandardVersion.parse('1.2.3-YOKO') != StandardVersion.parse('1.2.3-YOKO')), 'Two instances of StandardVersion are equal'


    def test_std_hash(self):
        """ test hash override for StandardVersion """

        assert hash(StandardVersion.parse('1.2.3-YOKO')) != 0, 'StdVersions have non-zero hashes'
        assert hash(StandardVersion.parse('1.2.3-YOKO')) == hash(StandardVersion.parse('1.2.3-YOKO'))


    def test_std_set(self):
        """ test set usage for StandardVersion """

        test = set()

        test.add(StandardVersion.parse('1.2.3-YOKO'))
        test.add(StandardVersion.parse('1.2.3-YOKO'))

        assert len(test) == 1
        assert StandardVersion.parse('1.2.3-YOKO') in test


    def test_std_string(self):
        """ test string usage for StandardVersion """

        assert str(StandardVersion.parse('1.2.3-YOKO')) == '1.2.3-YOKO'
        assert str(StandardVersion.parse('1.2.3')) == '1.2.3'
        assert str(StandardVersion.parse('1.2')) == '1.2'
        assert str(StandardVersion.parse('1')) == '1.0'


    def test_std_repr(self):
        """ test repr usage for StandardVersion """

        assert repr(StandardVersion.parse('1.2.3-YOKO')) == "StandardVersion(1, 2, 3, 'YOKO')"
        assert repr(StandardVersion.parse('1.2.3')) == "StandardVersion(1, 2, 3, None)"
        assert repr(StandardVersion.parse('1.2')) == "StandardVersion(1, 2, 0, None)"
        assert repr(StandardVersion.parse('1')) == "StandardVersion(1, 0, 0, None)"


    def test_std_cmp(self):
        """ test cmp usage for StandardVersion """

        assert StandardVersion.parse('0') < StandardVersion.parse('1')
        assert StandardVersion.parse('2') < StandardVersion.parse('10')
        assert StandardVersion.parse('0.9') < StandardVersion.parse('1.0')
        assert StandardVersion.parse('0.0.9') < StandardVersion.parse('1.0.0')
        assert StandardVersion.parse('1.0.0-A') < StandardVersion.parse('1.0.0-B')
        assert StandardVersion.parse('1.0.0-A') < StandardVersion.parse('1.0.0'), 'Version with qualifier should be less than one without'


class TestVersionRange(TestCase):
    def test_range_parse(self):
        try:
            VersionRange.parse('{1.0, 2.0)')
            assert False, 'Should have raised an exception for bad version range'
        except Exception:
            pass
        try:
            VersionRange.parse('[Z.0, 2.0)')
            assert False, 'Should have raised an exception for bad version range'
        except Exception:
            pass

        assert VersionRange.parse('[1.0, 2.0)') == VersionRange(StandardVersion(1), True, StandardVersion(2), False)
        assert VersionRange.parse('(1.0, 2.0]') == VersionRange(StandardVersion(1), False, StandardVersion(2), True)
        assert VersionRange.parse('[1.0, 2.0]') == VersionRange(StandardVersion(1), True, StandardVersion(2), True)
        assert VersionRange.parse('(1.0, 2.0)') == VersionRange(StandardVersion(1), False, StandardVersion(2), False)


    def test_range_checking(self):
        """ test version range checking """

        assert not VersionRange.parse('[1.0, 2.0)').contains(StandardVersion.parse('0.1'))
        assert VersionRange.parse('[1.0, 2.0)').contains(StandardVersion.parse('1'))
        assert VersionRange.parse('[1.0, 2.0)').contains(StandardVersion.parse('1.5'))
        assert not VersionRange.parse('[1.0, 2.0)').contains(StandardVersion.parse('2'))
        assert not VersionRange.parse('[1.0, 2.0)').contains(StandardVersion.parse('5'))

        assert not VersionRange.parse('(1.0, 2.0)').contains(StandardVersion.parse('0.1'))
        assert not VersionRange.parse('(1.0, 2.0]').contains(StandardVersion.parse('1'))
        assert VersionRange.parse('(1.0, 2.0]').contains(StandardVersion.parse('1.5'))
        assert VersionRange.parse('(1.0, 2.0]').contains(StandardVersion.parse('2'))
        assert not VersionRange.parse('(1.0, 2.0)').contains(StandardVersion.parse('5'))


    def test_range_equals(self):
        """ test equals override for VersionRange """

        assert VersionRange.parse('(1.0, 2.0)') is not VersionRange.parse('(1.0, 2.0)'), 'Two instances of StandardVersion are not the same'
        assert VersionRange.parse('(1.0, 2.0)') == VersionRange.parse('(1.0, 2.0)')


    def test_range_not_equals(self):
        """ test not equals override for VersionRange """

        assert not (VersionRange.parse('(1.0, 2.0)') != VersionRange.parse('(1.0, 2.0)')), 'Two instances of VersionRange are equal'


    def test_range_hash(self):
        """ test hash override for VersionRange """

        assert hash(VersionRange.parse('(1.0, 2.0)')) != 0, 'VersionRanges have non-zero hashes'
        assert hash(VersionRange.parse('(1.0, 2.0)')) == hash(VersionRange.parse('(1.0, 2.0)'))


    def test_range_set(self):
        """ test set usage for StandardVersion """

        test = set()
        test.add(VersionRange.parse('(1.0, 2.0)'))
        test.add(VersionRange.parse('(1.0, 2.0)'))

        assert len(test) == 1
        assert VersionRange.parse('(1.0, 2.0)') in test


    def test_range_string(self):
        """ test string usage for VersionRange """

        assert str(VersionRange.parse('( 1.0,   2.0 )')) == '(1.0, 2.0)'
        assert str(VersionRange.parse('[ 1.0,   2.0 )')) == '[1.0, 2.0)'
        assert str(VersionRange.parse('( 1.0,   2.0 ]')) == '(1.0, 2.0]'
        assert str(VersionRange.parse('[ 1.0,   2.0 ]')) == '[1.0, 2.0]'


    def test_range_repr(self):
        """ test repr usage for VersionRange """

        assert repr(VersionRange.parse('(1.0, 2.0)')) == "VersionRange(StandardVersion(1, 0, 0, None), False, StandardVersion(2, 0, 0, None), False)"
        assert repr(VersionRange.parse('(1.0, 2.0]')) == "VersionRange(StandardVersion(1, 0, 0, None), False, StandardVersion(2, 0, 0, None), True)"
        assert repr(VersionRange.parse('[1.0, 2.0)')) == "VersionRange(StandardVersion(1, 0, 0, None), True, StandardVersion(2, 0, 0, None), False)"
        assert repr(VersionRange.parse('[1.0, 2.0]')) == "VersionRange(StandardVersion(1, 0, 0, None), True, StandardVersion(2, 0, 0, None), True)"
