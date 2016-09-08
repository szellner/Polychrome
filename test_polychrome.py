import pytest
from scd import Polychrome


poly = Polychrome()


class TestPolychrome:
    # Naming hex values
    def test_valid_hex_in_magick(self):
        assert poly.name("magick", "#EE8262") and poly.name("magick", "EE8262")

    def test_valid_hex_notin_magick(self):
        assert not poly.name("magick", "#444EE2")

    def test_invalid_hex_magick(self):
        assert not poly.name("magick", "#EE822") and not poly.name(
            "magick", "EE822")

    # Naming RGB values
    def test_valid_rgb_in_magick(self):
    	assert poly.name("magick", (205,201,201))

    def test_valid_rgb_notin_magick(self):
    	assert not poly.name("magick", (40,40,40))

	# Testing that the correct maps are supported 
    def test_valid_supported_map(self):
    	assert poly.isSupportedMap("magick") == True
    def test_invalid_supported_map(self):
    	assert poly.isSupportedMap("mgik") == False
