"""
External real-world test cases for clear_url(), harvested from open-source
URL cleaning projects:
  - clean-url (Chrome extension)
  - url-tracking-stripper (Chrome extension)
  - Link Cleaner+ (Firefox extension)
  - link-cleaner-pro (Chrome extension)

Each test case has been verified against Unalix's rulesets
(data.min.json + unalix.json + unalix_extended.json).
"""
from unalix import clear_url


class TestGlobalTrackingParams:
    """Tests for parameters handled by the globalRules provider (urlPattern: .*)"""

    def test_utm_params_stripped(self):
        url = "https://example.com/page?utm_source=google&utm_medium=cpc&utm_campaign=spring"
        assert clear_url(url) == "https://example.com/page"

    def test_fbclid_stripped(self):
        url = "https://example.com/article?fbclid=IwAR0abc123"
        assert clear_url(url) == "https://example.com/article"

    def test_gclid_stripped_preserves_legit(self):
        url = "https://example.com/?gclid=abc123&page=1"
        assert clear_url(url) == "https://example.com/?page=1"

    def test_ga_and_gl_stripped(self):
        url = "https://example.com/?_ga=1.2.3&_gl=abc"
        assert clear_url(url) == "https://example.com/"

    def test_dclid_stripped(self):
        url = "https://example.com/?dclid=xyz"
        assert clear_url(url) == "https://example.com/"

    def test_yclid_stripped(self):
        url = "https://example.com/?yclid=123"
        assert clear_url(url) == "https://example.com/"

    def test_spm_stripped(self):
        url = "https://example.com/?spm=a2g0o.detail"
        assert clear_url(url) == "https://example.com/"

    def test_mkt_tok_stripped(self):
        url = "https://example.com/?mkt_tok=abc"
        assert clear_url(url) == "https://example.com/"

    def test_ref_stripped_preserves_legit(self):
        url = "https://example.com/?ref=sidebar&id=5"
        assert clear_url(url) == "https://example.com/?id=5"

    def test_referrer_stripped_preserves_legit(self):
        url = "https://example.com/?referrer=google&q=test"
        assert clear_url(url) == "https://example.com/?q=test"

    def test_gclsrc_stripped(self):
        url = "https://example.com/?gclsrc=aw.ds"
        assert clear_url(url) == "https://example.com/"

    def test_twitter_impression_stripped(self):
        url = "https://example.com/?__twitter_impression=true"
        assert clear_url(url) == "https://example.com/"


class TestPlatformSpecificParams:
    """Tests for parameters handled by platform-specific providers"""

    def test_instagram_igshid(self):
        url = "https://www.instagram.com/p/B7ToSDrg44K/?igshid=36gmy2rkwpsg"
        assert clear_url(url) == "https://www.instagram.com/p/B7ToSDrg44K/"

    def test_youtube_feature(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtu.be"
        assert clear_url(url) == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    def test_youtube_gclid(self):
        url = "https://www.youtube.com/watch?v=abc&gclid=xyz"
        assert clear_url(url) == "https://www.youtube.com/watch?v=abc"

    def test_spotify_si(self):
        url = "https://open.spotify.com/track/abc?si=xyz"
        assert clear_url(url) == "https://open.spotify.com/track/abc"

    def test_linkedin_trk(self):
        url = "https://www.linkedin.com/jobs/view/123/?trk=public_jobs"
        assert clear_url(url) == "https://www.linkedin.com/jobs/view/123/"

    def test_ebay_tracking_params(self):
        url = "https://www.ebay.com/itm/123?_trkparms=abc&_trksid=def"
        assert clear_url(url) == "https://www.ebay.com/itm/123"

    def test_etsy_click_tracking(self):
        url = "https://www.etsy.com/listing/123?click_key=abc&click_sum=def"
        assert clear_url(url) == "https://www.etsy.com/listing/123"

    def test_tiktok_u_code(self):
        url = "https://www.tiktok.com/@user/video/123?u_code=abc"
        assert clear_url(url) == "https://www.tiktok.com/@user/video/123"

    def test_twitch_com_tracking(self):
        url = "https://www.twitch.com/videos/123?tt_medium=redt&tt_content=post"
        assert clear_url(url) == "https://www.twitch.com/videos/123"

    def test_netflix_tracking(self):
        url = "https://www.netflix.com/title/123?trackId=abc&tctx=def"
        assert clear_url(url) == "https://www.netflix.com/title/123"

    def test_amazon_tag_referral(self):
        url = "https://www.amazon.com/dp/B00005N5PF?tag=affiliate-20"
        assert clear_url(url) == "https://www.amazon.com/dp/B00005N5PF"

    def test_amazon_pd_rd_params(self):
        url = "https://www.amazon.com/dp/B00005N5PF?pd_rd_w=abc&pd_rd_r=def"
        assert clear_url(url) == "https://www.amazon.com/dp/B00005N5PF"

    def test_bing_tracking(self):
        url = "https://www.bing.com/search?q=test&toWww=1&redig=abc"
        assert clear_url(url) == "https://www.bing.com/search?q=test"

    def test_facebook_hc_ref(self):
        url = "https://www.facebook.com/page?hc_ref=ARRabc"
        assert clear_url(url) == "https://www.facebook.com/page"

    def test_reddit_correlation_id(self):
        url = "https://www.reddit.com/r/sub/comments/abc?correlation_id=xyz"
        assert clear_url(url) == "https://www.reddit.com/r/sub/comments/abc"

    def test_snapchat_sc_referrer(self):
        url = "https://www.snapchat.com/add/user?sc_referrer=abc"
        assert clear_url(url) == "https://www.snapchat.com/add/user"

    def test_aliexpress_tracking(self):
        url = "https://www.aliexpress.com/item/123.html?srcSns=sns_Copy&tid=abc"
        assert clear_url(url) == "https://www.aliexpress.com/item/123.html"


class TestRedirectUnwrapping:
    """Tests for redirect URL extraction from wrapper/tracking URLs"""

    def test_google_url_redirect(self):
        url = "https://www.google.com/url?q=https://example.com&sa=D"
        assert clear_url(url) == "https://example.com"

    def test_google_amp(self):
        url = "https://www.google.com/amp/s/www.example.com/article"
        assert clear_url(url) == "http://www.example.com/article"

    def test_google_aclk_adurl(self):
        url = "https://www.google.com/aclk?sa=L&adurl=https://example.com"
        assert clear_url(url) == "https://example.com"

    def test_facebook_redirect(self):
        url = "https://l.facebook.com/l.php?u=https%3A%2F%2Fexample.com&h=abc"
        assert clear_url(url) == "https://example.com"

    def test_reddit_redirect(self):
        url = "https://out.reddit.com/?url=https%3A%2F%2Fexample.com&token=abc"
        assert clear_url(url) == "https://example.com"

    def test_instagram_redirect(self):
        url = "https://l.instagram.com/?u=https%3A%2F%2Fexample.com&e=abc"
        assert clear_url(url) == "https://example.com"

    def test_youtube_redirect(self):
        url = "https://www.youtube.com/redirect?q=https%3A%2F%2Fexample.com&v=abc"
        assert clear_url(url) == "https://example.com"

    def test_steam_linkfilter(self):
        url = "https://steamcommunity.com/linkfilter/?url=https://example.com"
        assert clear_url(url) == "https://example.com"

    def test_messenger_redirect(self):
        url = "https://l.messenger.com/l.php?u=https%3A%2F%2Fexample.com"
        assert clear_url(url) == "https://example.com"

    def test_pocket_redirect(self):
        url = "https://getpocket.com/redirect?url=https%3A%2F%2Fexample.com"
        assert clear_url(url) == "https://example.com"

    def test_vk_redirect(self):
        url = "https://vk.com/away.php?to=https%3A%2F%2Fexample.com"
        assert clear_url(url) == "https://example.com"

    def test_duckduckgo_redirect(self):
        url = "https://duckduckgo.com/l/?uddg=https%3A%2F%2Fexample.com"
        assert clear_url(url) == "https://example.com"

    def test_deviantart_outgoing(self):
        url = "https://www.deviantart.com/users/outgoing?https://example.com"
        assert clear_url(url) == "https://example.com"

    def test_ebay_rover_redirect(self):
        url = "https://rover.ebay.com/rover/1/123/4?mpre=https%3A%2F%2Fwww.ebay.com%2Fitm%2F456"
        assert clear_url(url) == "https://www.ebay.com/itm/456"


class TestRawRules:
    """Tests for path-based tracking element removal"""

    def test_amazon_ref_in_path(self):
        url = "https://www.amazon.com/dp/B08CH7RHDP/ref=sr_1_1"
        assert clear_url(url) == "https://www.amazon.com/dp/B08CH7RHDP"

    def test_primevideo_ref_in_path(self):
        url = "https://www.primevideo.com/detail/abc/ref=atv_dp"
        assert clear_url(url) == "https://www.primevideo.com/detail/abc"


class TestEdgeCases:
    """Tests for interaction edge cases: fragments, ports, mixed params, exceptions"""

    def test_fragment_preserved(self):
        url = "https://example.com/page?utm_source=news#section"
        assert clear_url(url) == "https://example.com/page#section"

    def test_port_preserved(self):
        url = "https://localhost:3000/app?utm_source=local&port=3000"
        assert clear_url(url) == "https://localhost:3000/app?port=3000"

    def test_legit_params_preserved(self):
        url = "https://shop.example.com/products?category=shoes&utm_source=newsletter&color=red&fbclid=123"
        assert clear_url(url) == "https://shop.example.com/products?category=shoes&color=red"

    def test_clean_url_unchanged(self):
        url = "https://www.google.com/search?q=test"
        assert clear_url(url) == "https://www.google.com/search?q=test"

    def test_github_ref_exception(self):
        url = "https://github.com/user/repo?ref=main"
        assert clear_url(url) == "https://github.com/user/repo?ref=main"

    def test_multiple_trackers_removed(self):
        url = "https://news.example.com/article?fbclid=fb123&gclid=gc456&utm_source=social"
        assert clear_url(url) == "https://news.example.com/article"
