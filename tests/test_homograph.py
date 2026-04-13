"""
Tests for IDN homograph attack detection.
"""
from unalix import detect_homograph


class TestHomographDetection:
    """Tests for detect_homograph() function"""

    def test_cyrillic_o_in_google(self):
        # Cyrillic 'о' (U+043E) looks identical to Latin 'o'
        result = detect_homograph("https://g\u043e\u043egle.com")
        assert result is not None
        assert result["target"] == "google.com"
        assert result["normalized"] == "google.com"
        assert len(result["confusable_chars"]) == 2
        assert result["confusable_chars"][0]["script"] == "CYRILLIC"
        assert result["confusable_chars"][0]["looks_like"] == "o"

    def test_cyrillic_a_in_amazon(self):
        # Cyrillic 'а' (U+0430) looks identical to Latin 'a'
        result = detect_homograph("https://\u0430mazon.com")
        assert result is not None
        assert result["normalized"] == "amazon.com"

    def test_cyrillic_c_in_facebook(self):
        # Cyrillic 'с' (U+0441) looks identical to Latin 'c'
        result = detect_homograph("https://fa\u0441ebook.com")
        assert result is not None
        assert result["normalized"] == "facebook.com"

    def test_cyrillic_e_in_paypal(self):
        # Cyrillic 'е' (U+0435) looks identical to Latin 'e'
        result = detect_homograph("https://payp\u0430l.\u0441om")
        assert result is not None
        assert result["normalized"] == "paypal.com"

    def test_greek_omicron_in_google(self):
        # Greek 'ο' (U+03BF) looks identical to Latin 'o'
        result = detect_homograph("https://g\u03bf\u03bfgle.com")
        assert result is not None
        assert result["normalized"] == "google.com"
        assert result["confusable_chars"][0]["script"] == "GREEK"

    def test_pure_ascii_safe(self):
        result = detect_homograph("https://google.com")
        assert result is None

    def test_pure_ascii_with_path(self):
        result = detect_homograph("https://google.com/search?q=test")
        assert result is None

    def test_ip_address_safe(self):
        result = detect_homograph("https://192.168.1.1/login")
        assert result is None

    def test_subdomain_with_homograph(self):
        # Homograph in main domain should still be detected
        result = detect_homograph("https://www.g\u043e\u043egle.com/search")
        assert result is not None
        assert result["normalized"] == "www.google.com"

    def test_url_with_port(self):
        result = detect_homograph("https://g\u043e\u043egle.com:443/path")
        assert result is not None
        assert result["normalized"] == "google.com"

    def test_no_scheme(self):
        result = detect_homograph("g\u043e\u043egle.com")
        assert result is not None
        assert result["normalized"] == "google.com"

    def test_unknown_target_still_flagged(self):
        # Mixed scripts in an unknown domain — suspicious but no target match
        result = detect_homograph("https://r\u0430ndom-site.com")
        assert result is not None
        assert result["target"] is None
        assert len(result["confusable_chars"]) > 0

    def test_confusable_chars_detail(self):
        result = detect_homograph("https://g\u043e\u043egle.com")
        assert result is not None
        char_info = result["confusable_chars"][0]
        assert "char" in char_info
        assert "position" in char_info
        assert "script" in char_info
        assert "looks_like" in char_info

    def test_multiple_protected_domains(self):
        for domain in ["apple", "microsoft", "paypal", "github"]:
            # Replace first vowel with Cyrillic equivalent
            spoofed = domain.replace("a", "\u0430", 1)
            if spoofed == domain:
                spoofed = domain.replace("o", "\u043e", 1)
            if spoofed == domain:
                spoofed = domain.replace("e", "\u0435", 1)
            if spoofed == domain:
                continue
            result = detect_homograph(f"https://{spoofed}.com")
            assert result is not None, f"Failed to detect homograph for {domain}"

    def test_fullwidth_chars_detected(self):
        # Fullwidth 'ａ' (U+FF41) in amazon
        result = detect_homograph("https://\uff41mazon.com")
        assert result is not None
        assert result["confusable_chars"][0]["script"] == "FULLWIDTH"
