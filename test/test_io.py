import pytest

from test.pattern_for_tests import *
import pystitch


class TestExplicitIOErrors:
    def test_read_non_file(self):
        """
        1.5.0 adds explicit error raising.
        We test that now.
        """
        file1 = "nosuchfile.dst"
        with pytest.raises(IOError):
            pystitch.read(file1)

    def test_write_non_supported(self):
        """
        1.5.0 adds explicit error raising.
        We test that now.
        """
        pattern = get_simple_pattern()
        file1 = "nosuchfile.pdf"
        with pytest.raises(IOError):
            pystitch.write(pattern, file1)

    def test_write_no_writer(self):
        """
        1.5.0 adds explicit error raising.
        We test that now.
        """
        pattern = get_simple_pattern()
        file1 = "nosuchfile.dat"
        with pytest.raises(IOError):
            pystitch.write(pattern, file1)
