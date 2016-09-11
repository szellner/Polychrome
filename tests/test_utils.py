import utils
import colour


class TestPolychromeUtils:
    def test_validHex(self):
        """Tests that valid hex values can be determined regardless of there being an octothorpe."""
        assert utils.validHex("#0066CC") and utils.validHex("01A368")

    def test_invalidHex_length(self):
        """Tests that hex values are invalid if they have more or less than six characters."""
        assert not utils.validHex("#0066C") and not utils.validHex(
            "#06CC") and not utils.validHex("#00666CC")

    def test_invalidHex_format(self):
        """Tests hex values that have alphanumeric characters outside the hexadecimal format's range (0-9 and A-F)."""
        assert not utils.validHex("#0066GG")

    def test_invalidHex_rgb(self):
        """Tests that valid RGB values are not valid hex values."""
        assert utils.validRGB(
            (38, 29, 103)) and not utils.validHex((38, 29, 103))

    def test_validRGB(self):
        assert utils.validRGB((70, 24, 250))

    def test_invalidRGB_length(self):
        """Tests that RGB values are invalid if they have more or less than three values."""
        assert not utils.validRGB(
            (42, 42)) and not utils.validRGB((42, 200, 100, 38))

    def test_invalidRGB_format(self):
        """Tests that RGB values are invalid if numbers fall outside the range 0-255 or are not integers."""
        assert not utils.validRGB((-1, 25, 70)) and not utils.validRGB((
            400, 50, 82)) and not utils.validRGB((25, 'a', 93)) and not utils.validRGB((4.2, 0, 16))

    def test_invalidRGB_hex(self):
        """Tests that valid hex values are not valid RGB values."""
        assert utils.validHex("#444ABC") and not utils.validRGB("#444ABC")
