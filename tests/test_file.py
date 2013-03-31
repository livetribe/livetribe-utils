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
import os

from livetribe.utils.file import temp_directory


def test_temp_directory():
    with temp_directory() as tmpdir:
        assert tmpdir
        assert os.path.isdir(tmpdir)

        test_file = os.path.join(tmpdir, 't.txt')
        with open(test_file, 'w') as fp:
            fp.write('zzz')

        assert os.path.exists(test_file)

    assert not os.path.exists(test_file)
    assert not os.path.exists(tmpdir)
