from livetribe.utils.version import StandardVersion, VersionRange


def test_std_init():
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


def test_std_equals():
    """ test equals override for StandardVersion """

    version1 = StandardVersion.parse('1.2.3-YOKO')
    version2 = StandardVersion.parse('1.2.3-YOKO')

    assert version1 is not version2, 'Two instances of StandardVersion are not the same'
    assert version1 == version2


def test_std_not_equals():
    """ test not equals override for StandardVersion """

    assert StandardVersion.parse('1.2.3-YOKO') != StandardVersion.parse('1.2.3-NOBU'), 'Two instances of StandardVersion are equal'
    assert not (StandardVersion.parse('1.2.3-YOKO') != StandardVersion.parse('1.2.3-YOKO')), 'Two instances of StandardVersion are equal'


def test_std_hash():
    """ test hash override for StandardVersion """

    assert hash(StandardVersion.parse('1.2.3-YOKO')) != 0, 'StdVersions have non-zero hashes'
    assert hash(StandardVersion.parse('1.2.3-YOKO')) == hash(StandardVersion.parse('1.2.3-YOKO'))


def test_std_set():
    """ test set usage for StandardVersion """

    test = set()

    test.add(StandardVersion.parse('1.2.3-YOKO'))
    test.add(StandardVersion.parse('1.2.3-YOKO'))

    assert len(test) == 1
    assert StandardVersion.parse('1.2.3-YOKO') in test


def test_std_string():
    """ test string usage for StandardVersion """

    assert str(StandardVersion.parse('1.2.3-YOKO')) == '1.2.3-YOKO'
    assert str(StandardVersion.parse('1.2.3')) == '1.2.3'
    assert str(StandardVersion.parse('1.2')) == '1.2'
    assert str(StandardVersion.parse('1')) == '1.0'


def test_std_repr():
    """ test repr usage for StandardVersion """

    assert repr(StandardVersion.parse('1.2.3-YOKO')) == "StandardVersion(1, 2, 3, 'YOKO')"
    assert repr(StandardVersion.parse('1.2.3')) == "StandardVersion(1, 2, 3, None)"
    assert repr(StandardVersion.parse('1.2')) == "StandardVersion(1, 2, 0, None)"
    assert repr(StandardVersion.parse('1')) == "StandardVersion(1, 0, 0, None)"


def test_std_cmp():
    """ test cmp usage for StandardVersion """

    assert StandardVersion.parse('0') < StandardVersion.parse('1')
    assert StandardVersion.parse('2') < StandardVersion.parse('10')
    assert StandardVersion.parse('0.9') < StandardVersion.parse('1.0')
    assert StandardVersion.parse('0.0.9') < StandardVersion.parse('1.0.0')
    assert StandardVersion.parse('1.0.0-A') < StandardVersion.parse('1.0.0-B')
    assert StandardVersion.parse('1.0.0-A') < StandardVersion.parse('1.0.0'), 'Version with qualifier should be less than one without'


def test_range_parse():
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


def test_range_checking():
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


def test_range_equals():
    """ test equals override for VersionRange """

    assert VersionRange.parse('(1.0, 2.0)') is not VersionRange.parse('(1.0, 2.0)'), 'Two instances of StandardVersion are not the same'
    assert VersionRange.parse('(1.0, 2.0)') == VersionRange.parse('(1.0, 2.0)')


def test_range_not_equals():
    """ test not equals override for VersionRange """

    assert not (VersionRange.parse('(1.0, 2.0)') != VersionRange.parse('(1.0, 2.0)')), 'Two instances of VersionRange are equal'


def test_range_hash():
    """ test hash override for VersionRange """

    assert hash(VersionRange.parse('(1.0, 2.0)')) != 0, 'VersionRanges have non-zero hashes'
    assert hash(VersionRange.parse('(1.0, 2.0)')) == hash(VersionRange.parse('(1.0, 2.0)'))


def test_range_set():
    """ test set usage for StandardVersion """

    test = set()
    test.add(VersionRange.parse('(1.0, 2.0)'))
    test.add(VersionRange.parse('(1.0, 2.0)'))

    assert len(test) == 1
    assert VersionRange.parse('(1.0, 2.0)') in test


def test_range_string():
    """ test string usage for VersionRange """

    assert str(VersionRange.parse('( 1.0,   2.0 )')) == '(1.0, 2.0)'
    assert str(VersionRange.parse('[ 1.0,   2.0 )')) == '[1.0, 2.0)'
    assert str(VersionRange.parse('( 1.0,   2.0 ]')) == '(1.0, 2.0]'
    assert str(VersionRange.parse('[ 1.0,   2.0 ]')) == '[1.0, 2.0]'


def test_range_repr():
    """ test repr usage for VersionRange """

    assert repr(VersionRange.parse('(1.0, 2.0)')) == "VersionRange(StandardVersion(1, 0, 0, None), False, StandardVersion(2, 0, 0, None), False)"
    assert repr(VersionRange.parse('(1.0, 2.0]')) == "VersionRange(StandardVersion(1, 0, 0, None), False, StandardVersion(2, 0, 0, None), True)"
    assert repr(VersionRange.parse('[1.0, 2.0)')) == "VersionRange(StandardVersion(1, 0, 0, None), True, StandardVersion(2, 0, 0, None), False)"
    assert repr(VersionRange.parse('[1.0, 2.0]')) == "VersionRange(StandardVersion(1, 0, 0, None), True, StandardVersion(2, 0, 0, None), True)"
