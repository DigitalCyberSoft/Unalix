"""
Tests for the custom_rulesets API: rulesets_from_dict() and the
custom_rulesets parameter on clear_url().
"""
import os
import json
import tempfile

from unalix import clear_url, rulesets_from_dict, rulesets_from_files


class TestRulesetsFromDict:
    """Tests for rulesets_from_dict() compilation"""

    def test_compiles_valid_ruleset(self):
        ruleset = rulesets_from_dict({
            "providers": {
                "test": {
                    "urlPattern": ".*",
                    "rules": ["my_param"]
                }
            }
        })
        assert len(ruleset.base_list) == 1
        assert ruleset.base_list[0].providerName == "test"

    def test_empty_providers(self):
        ruleset = rulesets_from_dict({"providers": {}})
        assert len(ruleset.base_list) == 0

    def test_ignored_providers(self):
        ruleset = rulesets_from_dict(
            {"providers": {"keep": {"urlPattern": ".*"}, "drop": {"urlPattern": ".*"}}},
            ignored_providers=["drop"]
        )
        assert len(ruleset.base_list) == 1
        assert ruleset.base_list[0].providerName == "keep"


class TestCustomRulesetsParam:
    """Tests for clear_url() with custom_rulesets parameter"""

    def test_custom_rules_applied(self):
        custom = rulesets_from_dict({
            "providers": {
                "test": {
                    "urlPattern": ".*",
                    "rules": ["my_tracking"]
                }
            }
        })
        url = "https://example.com/?my_tracking=abc"
        assert clear_url(url, custom_rulesets=custom) == "https://example.com/"

    def test_custom_rules_do_not_affect_default(self):
        url = "https://example.com/?my_tracking=abc"
        assert clear_url(url) == "https://example.com/?my_tracking=abc"

    def test_custom_redirect_extraction(self):
        custom = rulesets_from_dict({
            "providers": {
                "myredirect": {
                    "urlPattern": "^https?:\\/\\/redir\\.example\\.com",
                    "redirections": [
                        "^https?:\\/\\/redir\\.example\\.com\\/go\\?.*dest=([^&]*)"
                    ]
                }
            }
        })
        url = "https://redir.example.com/go?dest=https%3A%2F%2Ftarget.com"
        assert clear_url(url, custom_rulesets=custom) == "https://target.com"

    def test_custom_raw_rules(self):
        custom = rulesets_from_dict({
            "providers": {
                "myraw": {
                    "urlPattern": "^https?:\\/\\/shop\\.example\\.com",
                    "rawRules": ["\\/tracking_[a-z]+"]
                }
            }
        })
        url = "https://shop.example.com/product/tracking_abc/details"
        assert clear_url(url, custom_rulesets=custom) == "https://shop.example.com/product/details"

    def test_builtin_rules_still_apply_with_custom(self):
        custom = rulesets_from_dict({
            "providers": {
                "extra": {
                    "urlPattern": ".*",
                    "rules": ["custom_param"]
                }
            }
        })
        url = "https://example.com/?utm_source=test&custom_param=abc"
        assert clear_url(url, custom_rulesets=custom) == "https://example.com/"

    def test_custom_rulesets_from_file(self):
        ruleset_data = {
            "providers": {
                "filtest": {
                    "urlPattern": ".*",
                    "rules": ["file_param"]
                }
            }
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(ruleset_data, f)
            tmp_path = f.name

        try:
            custom = rulesets_from_files((tmp_path,))
            url = "https://example.com/?file_param=abc"
            assert clear_url(url, custom_rulesets=custom) == "https://example.com/"
        finally:
            os.unlink(tmp_path)
