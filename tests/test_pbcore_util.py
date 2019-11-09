from __future__ import absolute_import, division, print_function

from builtins import round

import pytest
import sys

from pbcore.util import Process
from pbcore.util.statistics import accuracy_as_phred_qv


class TestBackticks(object):
    def test_errCode(self):
        output, errCode, errMsg = Process.backticks("exit 42")
        assert 42 == errCode

    def test_output(self):
        output, errCode, errMsg = Process.backticks("echo Me stdout")
        assert ["Me stdout"] == output

    @pytest.mark.linux
    def test_errMsg(self):
        output, errCode, errMsg = Process.backticks("grep -l . /proc/cpuinfo /dev/foo/bar")
        assert "/proc/cpuinfo\ngrep: /dev/foo/bar: No such file or directory" == errMsg

    @pytest.mark.linux
    def test_errMsgMerge(self):
        output, errCode, errMsg = Process.backticks("grep -l . /proc/cpuinfo /dev/foo/bar", merge_stderr=False)
        assert output == ["/proc/cpuinfo"] and errMsg == "grep: /dev/foo/bar: No such file or directory"


class TestStatistics(object):

    def test_accuracy_as_phred_qv(self):
        qv = accuracy_as_phred_qv(0.999)
        assert int(round(qv)) == 30
        qv = accuracy_as_phred_qv(1.0, max_qv=60)
        assert int(round(qv)) == 60
        qv = accuracy_as_phred_qv([0.95, 1.0, 0.99999])
        qvs = [int(round(x)) for x in qv]
        assert qvs == [13, 60, 50]
