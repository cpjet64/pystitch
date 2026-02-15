from __future__ import print_function

from test.cleanup_case import CleanupTestCase

from test.pattern_for_tests import *
from pystitch import *


class TestWrites(CleanupTestCase):

    def position_equals(self, stitches, j, k):
        assert stitches[j][:1] == stitches[k][:1]

    def test_write_png(self):
        file1 = "file.png"
        write_png(get_shift_pattern(), file1, {"background": "#F00", "linewidth": 5})
        self.addCleanup(os.remove, file1)

    def test_write_fancy_png(self):
        file1 = "file-fancy.png"
        write_png(get_shift_pattern(), file1, {"background": "#F00", "linewidth": 5, "fancy": True})
        self.addCleanup(os.remove, file1)

    def test_write_guides_png(self):
        file1 = "file-guides.png"
        write_png(
            get_shift_pattern(), file1, {"background": "#F00", "linewidth": 5, "guides": True}
        )
        self.addCleanup(os.remove, file1)

    def test_write_fancy_guides_png(self):
        file1 = "file-fancy-guides.png"
        write_png(
            get_shift_pattern(),
            file1,
            {"background": "#F00", "linewidth": 5, "fancy": True, "guides": True},
        )
        self.addCleanup(os.remove, file1)

    def test_write_dst_read_dst(self):
        file1 = "file.dst"
        write_dst(get_big_pattern(), file1)
        dst_pattern = read_dst(file1)
        assert len(dst_pattern.threadlist) == 0
        assert dst_pattern.count_stitch_commands(COLOR_CHANGE) == 15
        assert dst_pattern is not None
        assert dst_pattern.count_stitch_commands(STITCH) == 5 * 16
        self.position_equals(dst_pattern.stitches, 0, -1)
        print("dst: ", dst_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_exp_read_exp(self):
        file1 = "file.exp"
        write_exp(get_big_pattern(), file1)
        exp_pattern = read_exp(file1)
        assert len(exp_pattern.threadlist) == 0
        assert exp_pattern.count_stitch_commands(COLOR_CHANGE) == 15
        assert exp_pattern is not None
        assert exp_pattern.count_stitch_commands(STITCH) == 5 * 16
        self.position_equals(exp_pattern.stitches, 0, -1)
        print("exp: ", exp_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_vp3_read_vp3(self):
        file1 = "file.vp3"
        write_vp3(get_big_pattern(), file1)
        vp3_pattern = read_vp3(file1)
        assert len(vp3_pattern.threadlist) == vp3_pattern.count_stitch_commands(COLOR_CHANGE) + 1
        assert vp3_pattern.count_stitch_commands(COLOR_CHANGE) == 15
        assert vp3_pattern is not None
        assert vp3_pattern.count_stitch_commands(STITCH) == 5 * 16
        self.position_equals(vp3_pattern.stitches, 0, -1)
        print("vp3: ", vp3_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_jef_read_jef(self):
        file1 = "file.jef"
        write_jef(get_big_pattern(), file1)
        jef_pattern = read_jef(file1)
        assert len(jef_pattern.threadlist) == jef_pattern.count_stitch_commands(COLOR_CHANGE) + 1
        assert jef_pattern.count_stitch_commands(COLOR_CHANGE) == 15
        assert jef_pattern is not None
        assert jef_pattern.count_stitch_commands(STITCH) == 5 * 16
        self.position_equals(jef_pattern.stitches, 0, -1)
        print("jef: ", jef_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_pec_read_pec(self):
        file1 = "file.pec"
        write_pec(get_big_pattern(), file1)
        pec_pattern = read_pec(file1)
        assert len(pec_pattern.threadlist) == pec_pattern.count_stitch_commands(COLOR_CHANGE) + 1
        assert pec_pattern.count_stitch_commands(COLOR_CHANGE) == 15
        assert pec_pattern is not None
        assert pec_pattern.count_stitch_commands(STITCH) == 5 * 16
        self.position_equals(pec_pattern.stitches, 0, -1)
        print("pec: ", pec_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_pes_read_pes(self):
        file1 = "file.pes"
        write_pes(get_big_pattern(), file1)
        pes_pattern = read_pes(file1)
        assert len(pes_pattern.threadlist) == pes_pattern.count_stitch_commands(COLOR_CHANGE) + 1
        assert pes_pattern.count_stitch_commands(COLOR_CHANGE) == 15
        assert pes_pattern is not None
        assert pes_pattern.count_stitch_commands(STITCH) == 5 * 16
        self.position_equals(pes_pattern.stitches, 0, -1)
        print("pes: ", pes_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_xxx_read_xxx(self):
        file1 = "file.xxx"
        write_xxx(get_big_pattern(), file1)
        pattern = read_xxx(file1)
        assert len(pattern.threadlist) == pattern.count_stitch_commands(COLOR_CHANGE) + 1
        assert pattern.count_stitch_commands(COLOR_CHANGE) == 15
        assert pattern is not None
        assert pattern.count_stitch_commands(STITCH) == 5 * 16
        self.position_equals(pattern.stitches, 0, -1)
        print("xxx: ", pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_u01_read_u01(self):
        file1 = "file.u01"
        write_u01(get_big_pattern(), file1)
        u01_pattern = read_u01(file1)
        assert len(u01_pattern.threadlist) == 0
        assert u01_pattern.count_stitch_commands(NEEDLE_SET) == 16
        assert u01_pattern is not None
        assert u01_pattern.count_stitch_commands(STITCH) == 5 * 16
        self.position_equals(u01_pattern.stitches, 0, -1)
        print("u01: ", u01_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_csv_read_csv(self):
        file1 = "file.csv"
        write_csv(get_big_pattern(), file1, {"encode": True})
        csv_pattern = read_csv(file1)
        assert csv_pattern is not None
        assert len(csv_pattern.threadlist) == csv_pattern.count_stitch_commands(COLOR_CHANGE) + 1
        assert csv_pattern.count_stitch_commands(COLOR_CHANGE) == 15
        assert csv_pattern.count_stitch_commands(STITCH) == 5 * 16
        self.position_equals(csv_pattern.stitches, 0, -1)
        print("csv: ", csv_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_gcode_read_gcode(self):
        file1 = "file.gcode"
        write_gcode(get_big_pattern(), file1)
        gcode_pattern = read_gcode(file1)
        assert gcode_pattern is not None
        thread_count = len(gcode_pattern.threadlist)
        change_count = gcode_pattern.count_stitch_commands(COLOR_CHANGE) + 1
        print(thread_count)
        print(change_count)

        assert thread_count == change_count
        assert gcode_pattern.count_stitch_commands(COLOR_CHANGE) == 15
        assert gcode_pattern.count_stitch_commands(STITCH) == 5 * 16
        self.position_equals(gcode_pattern.stitches, 0, -1)
        self.addCleanup(os.remove, file1)

    def test_write_txt(self):
        file1 = "file.txt"
        write_txt(get_big_pattern(), file1)
        write_txt(get_big_pattern(), file1, {"mimic": True})
        self.addCleanup(os.remove, file1)

    def test_write_pes_mismatched(self):
        file1 = "file.pes"
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
        write_pes(pattern, file1, {"version": "6t"})
        write_pes(pattern, file1)
        self.addCleanup(os.remove, file1)

    def test_pes_writes_stop(self):
        """Test if pes can read/write a stop command."""
        file1 = "file.pes"
        pattern = EmbPattern()
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern += STOP
        pattern += (100, 0), (0, 100)
        pattern += "blue"
        pattern += (0, 0), (100, 100)
        pattern += STOP
        pattern += (100, 0), (0, 100)
        write_pes(pattern, file1, {"version": "6t"})
        loaded = read_pes(file1)
        assert pattern.count_stitch_commands(STOP) == 2
        assert pattern.count_stitch_commands(COLOR_CHANGE) == 1
        assert pattern.count_threads() == 2
        assert loaded.count_stitch_commands(STOP) == 2
        assert loaded.count_stitch_commands(COLOR_CHANGE) == 1
        assert loaded.count_threads() == 2
        self.addCleanup(os.remove, file1)
