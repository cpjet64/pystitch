from __future__ import print_function

import pystitch


def test_catalog_files():
    for f in pystitch.supported_formats():
        assert "extensions" in f
        assert "extension" in f
        assert "description" in f
        assert "category" in f
