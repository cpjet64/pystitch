from __future__ import print_function

from test.cleanup_case import CleanupTestCase
from pystitch import *


class TestMatrix(CleanupTestCase):

    def test_matrix(self):
        matrix = EmbMatrix()
        matrix.post_rotate(90, 100, 100)
        p = matrix.point_in_matrix_space(50, 50)
        assert round(abs(p[0] - 150), 7) == 0
        assert round(abs(p[1] - 50), 7) == 0

    def test_matrix_2(self):
        matrix = EmbMatrix()
        matrix.reset()
        matrix.post_scale(2, 2, 50, 50)
        p = matrix.point_in_matrix_space(50, 50)
        assert round(abs(p[0] - 50), 7) == 0
        assert round(abs(p[1] - 50), 7) == 0

        p = matrix.point_in_matrix_space(25, 25)
        assert round(abs(p[0] - 0), 7) == 0
        assert round(abs(p[1] - 0), 7) == 0
        matrix.post_rotate(45, 50, 50)

        p = matrix.point_in_matrix_space(25, 25)
        assert round(abs(p[0] - 50), 7) == 0

    def test_matrix_3(self):
        matrix = EmbMatrix()
        matrix.reset()
        matrix.post_scale(0.5, 0.5)
        p = matrix.point_in_matrix_space(100, 100)
        assert round(abs(p[0] - 50), 7) == 0
        assert round(abs(p[1] - 50), 7) == 0
        matrix.reset()
        matrix.post_scale(2, 2, 100, 100)
        p = matrix.point_in_matrix_space(50, 50)
        assert round(abs(p[0] - 0), 7) == 0
        assert round(abs(p[1] - 0), 7) == 0

    def test_matrix_rotate(self):
        pattern = EmbPattern()
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "red")
        pattern.add_command(MATRIX_ROTATE, 45)
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "blue")
        pattern.add_command(MATRIX_ROTATE, 45)
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "aqua")
        pattern = pattern.get_normalized_pattern()
        print("rotate:", pattern.stitches)
        assert round(abs(pattern.stitches[4][0] - pattern.stitches[6][0]), 7) == 0
        assert round(abs(pattern.stitches[4][1] - pattern.stitches[6][1]), 7) == 0
        assert round(abs(pattern.stitches[10][0] - pattern.stitches[12][0]), 7) == 0
        assert round(abs(pattern.stitches[10][1] - pattern.stitches[12][1]), 7) == 0
        assert round(abs(pattern.stitches[4][0] - pattern.stitches[12][0]), 7) == 0
        assert round(abs(pattern.stitches[4][1] - pattern.stitches[12][1]), 7) == 0
        file1 = "file.svg"
        write_svg(pattern, file1)
        self.addCleanup(os.remove, file1)

    def test_matrix_translate(self):
        pattern = EmbPattern()
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "red")
        pattern.add_command(MATRIX_TRANSLATE, 20, 40)
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "blue")
        pattern.add_command(MATRIX_TRANSLATE, -20, -40)
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "aqua")
        pattern = pattern.get_normalized_pattern()
        print("translate:", pattern.stitches)
        assert pattern.stitches is not None
        assert pattern.count_stitch_commands(MATRIX_TRANSLATE) == 0

        assert round(abs(pattern.stitches[4][0] - pattern.stitches[12][0]), 7) == 0
        assert round(abs(pattern.stitches[4][1] - pattern.stitches[12][1]), 7) == 0
        file1 = "file2.svg"
        write_svg(pattern, file1)
        self.addCleanup(os.remove, file1)

    def test_matrix_translate_rotate(self):
        pattern = EmbPattern()
        pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "red")
        pattern.add_command(MATRIX_TRANSLATE, 20, 40)
        pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "blue")
        pattern.add_command(MATRIX_ROTATE, -90)
        pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "aqua")
        pattern = pattern.get_normalized_pattern()
        print("transrot:", pattern.stitches)
        assert pattern.stitches is not None
        assert pattern.count_stitch_commands(MATRIX_TRANSLATE) == 0
        assert pattern.count_stitch_commands(MATRIX_ROTATE) == 0
        assert round(abs(pattern.stitches[14][0] - 140), 7) == 0
        assert round(abs(pattern.stitches[14][1] - -120), 7) == 0
        file1 = "file3.svg"
        write_svg(pattern, file1)
        self.addCleanup(os.remove, file1)

    def test_matrix_translate_scale(self):
        pattern = EmbPattern()
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "red")
        pattern.add_command(MATRIX_TRANSLATE, 20, 40)
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "blue")
        pattern.add_command(MATRIX_SCALE, 2, 2)
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "aqua")
        pattern = pattern.get_normalized_pattern()
        print("transcale:", pattern.stitches)
        assert pattern.stitches is not None
        assert pattern.count_stitch_commands(MATRIX_TRANSLATE) == 0
        assert pattern.count_stitch_commands(MATRIX_SCALE) == 0
        assert round(abs(pattern.stitches[13][0] - 50), 7) == 0
        assert round(abs(pattern.stitches[13][1] - 290), 7) == 0
        file1 = "file4.svg"
        write_svg(pattern, file1)
        self.addCleanup(os.remove, file1)
