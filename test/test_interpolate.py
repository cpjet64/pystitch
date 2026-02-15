from __future__ import print_function

from pystitch import *
from test.pattern_for_tests import *


class TestInterpolate:

    def test_interpolate_color_stop(self):
        """Full circle STOP/color conversion"""
        pattern = get_fractal_pattern()
        pattern.fix_color_count()
        p2 = pattern.copy()
        assert pattern.count_stitch_commands(STOP) == 1
        pattern.interpolate_stop_as_duplicate_color()
        assert pattern.count_stitch_commands(STOP) == 0
        pattern.interpolate_duplicate_color_as_stop()
        assert pattern.count_stitch_commands(STOP) == 1

        assert pattern == p2

    def test_interpolate_to_stop(self):
        """Duplicate color to STOP"""
        pattern = EmbPattern()
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern += "red"
        pattern += (100, 0), (0, 100)
        assert pattern.count_stitch_commands(STOP) == 0
        pattern.interpolate_duplicate_color_as_stop()
        assert pattern.count_stitch_commands(STOP) == 1

    def test_interpolate_to_stop_multi(self):
        """Multiple duplicate color to multiple STOP"""
        pattern = EmbPattern()
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern += "red"
        pattern += (100, 0), (0, 100)
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern += "red"
        pattern += (100, 0), (0, 100)
        assert pattern.count_stitch_commands(STOP) == 0
        pattern.interpolate_duplicate_color_as_stop()
        assert pattern.count_stitch_commands(STOP) == 3

    def test_interpolate_to_stop_interleave(self):
        """interleaved colors do not become STOP"""
        pattern = EmbPattern()
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern += "blue"
        pattern += (100, 0), (0, 100)
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern += "blue"
        pattern += (100, 0), (0, 100)
        assert pattern.count_stitch_commands(STOP) == 0
        pattern.interpolate_duplicate_color_as_stop()
        assert pattern.count_stitch_commands(STOP) == 0

    def test_interpolate_to_stop_mismatch(self):
        """if the threadlist and color_changes are mismatched"""
        pattern = EmbPattern()
        pattern += "red"
        pattern += "red"
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern += COLOR_CHANGE
        pattern += (100, 0), (0, 100)
        pattern += COLOR_CHANGE
        pattern += (0, 0), (100, 100)
        pattern += COLOR_CHANGE
        pattern += (100, 0), (0, 100)
        assert pattern.count_stitch_commands(STOP) == 0
        pattern.interpolate_duplicate_color_as_stop()
        assert pattern.count_stitch_commands(STOP) == 2
        assert pattern.count_stitch_commands(COLOR_CHANGE) == 1

    def test_interpolate_stop_no_threads(self):
        """No threads, cannot duplicate."""
        pattern = EmbPattern()
        pattern += (0, 0), (100, 100)
        pattern += STOP
        pattern += (100, 0), (0, 100)
        pattern += STOP
        pattern += (0, 0), (100, 100)
        pattern += STOP
        pattern += (100, 0), (0, 100)
        assert pattern.count_stitch_commands(STOP) == 3
        pattern.interpolate_stop_as_duplicate_color()
        assert pattern.count_stitch_commands(STOP) == 3

    def test_interpolate_to_stop_intermix(self):
        """intermixed colors become intermixed STOP"""
        pattern = EmbPattern()
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern += "red"
        pattern += (100, 0), (0, 100)
        pattern += "blue"
        pattern += (0, 0), (100, 100)
        pattern += "blue"
        pattern += (100, 0), (0, 100)
        assert pattern.count_stitch_commands(STOP) == 0
        pattern.interpolate_duplicate_color_as_stop()
        assert pattern.count_stitch_commands(STOP) == 2

    def test_interpolate_stop_intermix(self):
        """intermixed STOP become intermixed colors"""
        pattern = EmbPattern()
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern += STOP
        pattern += (100, 0), (0, 100)
        pattern += "blue"
        pattern += (0, 0), (100, 100)
        pattern += STOP
        pattern += (100, 0), (0, 100)
        assert pattern.count_stitch_commands(STOP) == 2
        pattern.interpolate_stop_as_duplicate_color()
        assert pattern.count_stitch_commands(STOP) == 0
        assert len(pattern.threadlist) == 4
        assert pattern.threadlist[0] == pattern.threadlist[1]
        assert pattern.threadlist[1] != pattern.threadlist[2]
        assert pattern.threadlist[2] == pattern.threadlist[3]

    def test_interpolate_stop_duplicate(self):
        """multiple STOP become multiple duplicate"""
        pattern = EmbPattern()
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern += STOP
        pattern += STOP
        pattern += STOP
        pattern += STOP
        pattern += (100, 0), (0, 100)
        assert pattern.count_stitch_commands(STOP) == 4
        pattern.interpolate_stop_as_duplicate_color()
        assert pattern.count_stitch_commands(STOP) == 0
        assert len(pattern.threadlist) == 5

    def test_interpolate_stop_duplicate_break(self):
        """changing colors, in a stop series works"""
        pattern = EmbPattern()
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern += STOP
        pattern += STOP
        pattern += "blue"
        pattern += STOP
        pattern += STOP
        pattern += (100, 0), (0, 100)
        assert pattern.count_stitch_commands(STOP) == 4
        pattern.interpolate_stop_as_duplicate_color()
        assert pattern.count_stitch_commands(STOP) == 0
        assert len(pattern.threadlist) == 6
        assert pattern.threadlist[0] == pattern.threadlist[1]
        assert pattern.threadlist[1] == pattern.threadlist[2]
        assert pattern.threadlist[2] != pattern.threadlist[3]
        assert pattern.threadlist[3] == pattern.threadlist[4]
        assert pattern.threadlist[4] == pattern.threadlist[5]

    def test_interpolate_frame_eject(self):
        """FRAME_EJECTs are interpolated"""
        pattern = EmbPattern()
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern.move_abs(200, 0)
        pattern.stop()
        pattern.move_abs(100, 100)
        pattern += (100, 0), (0, 100)
        assert pattern.count_stitch_commands(FRAME_EJECT) == 0
        assert pattern.count_stitch_commands(STOP) == 1
        pattern.interpolate_frame_eject()
        assert pattern.count_stitch_commands(FRAME_EJECT) == 1
        assert pattern.count_stitch_commands(STOP) == 0

    def test_interpolate_frame_eject_multijums(self):
        """FRAME_EJECTs are interpolated"""
        pattern = EmbPattern()
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern.move_abs(100, 0)
        pattern.move_abs(200, 0)
        pattern.stop()
        pattern.move_abs(100, 0)
        pattern.move_abs(101, 0)
        pattern.move_abs(100, 100)
        pattern += (100, 0), (0, 100)
        assert pattern.count_stitch_commands(JUMP) == 5
        assert pattern.count_stitch_commands(FRAME_EJECT) == 0
        assert pattern.count_stitch_commands(STOP) == 1
        pattern.interpolate_frame_eject()
        assert pattern.count_stitch_commands(JUMP) == 0
        assert pattern.count_stitch_commands(FRAME_EJECT) == 1
        assert pattern.count_stitch_commands(STOP) == 0

    def test_interpolate_frame_eject_end(self):
        """FRAME_EJECTs are interpolated"""
        pattern = EmbPattern()
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern.move_abs(200, 0)
        pattern.stop()
        assert pattern.count_stitch_commands(FRAME_EJECT) == 0
        assert pattern.count_stitch_commands(STOP) == 1
        pattern.interpolate_frame_eject()
        assert pattern.count_stitch_commands(FRAME_EJECT) == 1
        assert pattern.count_stitch_commands(STOP) == 0
