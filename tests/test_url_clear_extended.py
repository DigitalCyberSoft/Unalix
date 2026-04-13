"""
Test cases for the unalix_extended.json ruleset — tracking parameters and
redirect services NOT covered by the upstream ClearURLs data.min.json.
"""
from unalix import clear_url


class TestExtendedGlobalParams:
    """Tests for new global tracking params in unalix_extended.json"""

    def test_gbraid(self):
        assert clear_url("https://example.com/?gbraid=abc") == "https://example.com/"

    def test_wbraid(self):
        assert clear_url("https://example.com/?wbraid=abc") == "https://example.com/"

    def test_gad_source(self):
        assert clear_url("https://example.com/?gad_source=1") == "https://example.com/"

    def test_gad_campaignid(self):
        assert clear_url("https://example.com/?gad_campaignid=2000") == "https://example.com/"

    def test_gad_source_and_campaignid(self):
        url = "https://example.com/?gad_source=1&gad_campaignid=2000"
        assert clear_url(url) == "https://example.com/"

    def test_msclkid(self):
        assert clear_url("https://example.com/?msclkid=abc") == "https://example.com/"

    def test_msclkid_preserves_legit(self):
        url = "https://example.com/?msclkid=abc&page=1"
        assert clear_url(url) == "https://example.com/?page=1"

    def test_ttclid(self):
        assert clear_url("https://example.com/?ttclid=abc") == "https://example.com/"

    def test_twclid(self):
        assert clear_url("https://example.com/?twclid=abc") == "https://example.com/"

    def test_li_fat_id(self):
        assert clear_url("https://example.com/?li_fat_id=abc") == "https://example.com/"

    def test_hsenc(self):
        assert clear_url("https://example.com/?_hsenc=abc") == "https://example.com/"

    def test_hsmi(self):
        assert clear_url("https://example.com/?_hsmi=123") == "https://example.com/"

    def test_hsenc_and_hsmi(self):
        url = "https://example.com/?_hsenc=abc&_hsmi=123"
        assert clear_url(url) == "https://example.com/"

    def test_mc_cid(self):
        assert clear_url("https://example.com/?mc_cid=abc") == "https://example.com/"

    def test_mc_eid(self):
        assert clear_url("https://example.com/?mc_eid=def") == "https://example.com/"

    def test_mc_cid_and_eid(self):
        url = "https://example.com/?mc_cid=abc&mc_eid=def"
        assert clear_url(url) == "https://example.com/"

    def test_ck_subscriber_id(self):
        assert clear_url("https://example.com/?ck_subscriber_id=abc") == "https://example.com/"

    def test_vero_conv(self):
        assert clear_url("https://example.com/?vero_conv=abc") == "https://example.com/"

    def test_vero_id(self):
        assert clear_url("https://example.com/?vero_id=def") == "https://example.com/"

    def test_sr_share(self):
        assert clear_url("https://example.com/?sr_share=abc") == "https://example.com/"

    def test_nr_email_referer(self):
        assert clear_url("https://example.com/?nr_email_referer=abc") == "https://example.com/"

    def test_ke(self):
        assert clear_url("https://example.com/?_ke=abc") == "https://example.com/"

    def test_kx(self):
        assert clear_url("https://example.com/?_kx=def") == "https://example.com/"

    def test_epik(self):
        assert clear_url("https://example.com/?epik=abc") == "https://example.com/"

    def test_ef_id(self):
        assert clear_url("https://example.com/?ef_id=abc") == "https://example.com/"

    def test_dm_i(self):
        assert clear_url("https://example.com/?dm_i=abc") == "https://example.com/"

    def test_srsltid(self):
        assert clear_url("https://example.com/?srsltid=abc") == "https://example.com/"

    def test_bta_c(self):
        assert clear_url("https://example.com/?_bta_c=abc") == "https://example.com/"

    def test_bta_tid(self):
        assert clear_url("https://example.com/?_bta_tid=def") == "https://example.com/"

    def test_bta_c_and_tid(self):
        url = "https://example.com/?_bta_c=abc&_bta_tid=def"
        assert clear_url(url) == "https://example.com/"


class TestExtendedPlatformParams:
    """Tests for new platform-specific params in unalix_extended.json"""

    def test_youtube_si(self):
        url = "https://www.youtube.com/watch?v=abc&si=xyz"
        assert clear_url(url) == "https://www.youtube.com/watch?v=abc"

    def test_twitch_tv_tracking(self):
        url = "https://www.twitch.tv/videos/123?tt_medium=redt&tt_content=post"
        assert clear_url(url) == "https://www.twitch.tv/videos/123"


class TestExtendedRedirects:
    """Tests for new redirect services in unalix_extended.json"""

    def test_slack_redir(self):
        url = "https://slack-redir.net/link?url=https%3A%2F%2Fexample.com"
        assert clear_url(url) == "https://example.com"

    def test_redirectingat(self):
        url = "https://www.redirectingat.com/?url=https%3A%2F%2Fexample.com"
        assert clear_url(url) == "https://example.com"

    def test_cj_affiliate_tkqlhce(self):
        url = "https://www.tkqlhce.com/click?url=https%3A%2F%2Fexample.com"
        assert clear_url(url) == "https://example.com"

    def test_cj_affiliate_anrdoezrs(self):
        url = "https://www.anrdoezrs.net/click?url=https%3A%2F%2Fexample.com"
        assert clear_url(url) == "https://example.com"

    def test_impact_radius(self):
        url = "https://www.ojrq.net/p/?return=https%3A%2F%2Fexample.com"
        assert clear_url(url) == "https://example.com"

    def test_connexity(self):
        url = "https://rd.connexity.net/rd?t=https%3A%2F%2Fexample.com"
        assert clear_url(url) == "https://example.com"

    def test_commission_factory(self):
        url = "https://t.cfjump.com/abc?Url=https%3A%2F%2Fexample.com"
        assert clear_url(url) == "https://example.com"
