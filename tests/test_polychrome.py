from polychrome import Polychrome

poly = Polychrome()


class TestPolychrome:
    # Naming hex values
    def test_valid_hex_in_magick(self):
        """Tests that a valid hex value in the magick map can be found by isInMap."""
        assert poly.isInMap("#EE8262", "magick") and poly.isInMap(
            "EE8262", "magick")

    def test_valid_hex_notin_magick(self):
        """Tests that a valid hex value not in the magick map cannot be found by isInMap."""
        assert not poly.isInMap("#444EE2", "magick")

    def test_invalid_hex_magick(self):
        """Tests that an invalid hex value cannot be found by isInMap."""
        assert not poly.isInMap("#EE822", "magick") and not poly.isInMap(
            "EE822", "magick", )

    # Naming RGB values
    def test_valid_rgb_in_magick(self):
        """Tests that a valid RGB value in the magick map can be found by isInMap."""
        assert poly.isInMap((205, 201, 201), "magick")

    def test_valid_rgb_notin_magick(self):
        """Tests that a valid RGB value not in the magick map cannot be found by isInMap."""
        assert not poly.isInMap((40, 40, 40), "magick")

    def test_invalid_rgb_magick(self):
        """Tests that an invalid RGB value cannot be found by isInMap."""
        assert not poly.isInMap((40, 40), "magick") and not poly.isInMap((40, 40, 40, 40), "magick") and not poly.isInMap(('a', 40, 40), "magick")  and not poly.isInMap((40, 40, 400), "magick") 

        # Testing that the correct maps are supported
    def test_valid_supported_map(self):
        """Tests that a valid colormap has been successfully created and is usable."""
        assert poly.isSupportedMap("magick")

    def test_invalid_supported_map(self):
        """Tests that an invalid colormap has been unsuccessfully created or doesn't exist."""
        assert not poly.isSupportedMap("mgik")
