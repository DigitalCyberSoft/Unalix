# Unalix

Unalix is a dependency-free Python library for removing tracking fields from URLs, following the [ClearURLs](https://github.com/ClearURLs/Addon) specification.

This is an actively maintained fork of [AmanoTeam/Unalix](https://github.com/AmanoTeam/Unalix), which has been unmaintained since February 2022. This fork adds extended tracking parameter coverage, a custom rules API, IDN homograph attack detection, SSRF protections, and automated ruleset updates.

## What's new in this fork

- **Extended ruleset** (`unalix_extended.json`) -- 25 additional tracking parameters (Google Ads, Microsoft, TikTok, LinkedIn, HubSpot, MailChimp, etc.) and 7 redirect services (Slack, Skimlinks, CJ Affiliate, etc.) not covered by ClearURLs
- **Custom rules API** -- `rulesets_from_dict()` and `custom_rulesets` parameter on `clear_url()` for user-defined rulesets
- **Homograph detection** -- `detect_homograph()` identifies IDN homograph attacks using Cyrillic/Greek/fullwidth lookalike characters
- **Security hardening** -- SSRF protection in `unshort_url()`, capped Retry-After sleep, fixed IPv6 parsing, forward-secret-only TLS ciphers, proper cookie policy subclasses
- **Automated updates** -- GitHub Actions for weekly ClearURLs ruleset and CA bundle updates via PR
- **Updated data** -- ClearURLs rules updated from 173 to 206 providers, CA bundle updated to 2026
- **Comprehensive tests** -- 116 tests (up from 2), covering real-world URLs from clean-url, url-tracking-stripper, Link Cleaner+, and link-cleaner-pro

## Installation

Install from this fork:

```bash
pip install 'https://codeload.github.com/DigitalCyberSoft/Unalix/tar.gz/refs/heads/master'
```

_**Note**: Unalix requires Python 3.8 or higher._

## Usage

### Removing tracking fields

```python
import unalix

url = "https://example.com/page?utm_source=google&fbclid=abc&gclid=xyz"
result = unalix.clear_url(url)

assert result == "https://example.com/page"
```

### Resolving shortened URLs

```python
import unalix

url = "https://bitly.is/Pricing-Pop-Up"
result = unalix.unshort_url(url)

assert result == "https://bitly.com/pages/pricing"
```

_**Tip**: `unshort_url()` strips tracking fields from every URL before following a redirect, so you don't need to call `clear_url()` separately on its return value._

### Custom rules

```python
import unalix

custom = unalix.rulesets_from_dict({
    "providers": {
        "myapp": {
            "urlPattern": ".*",
            "rules": ["my_tracking_param"]
        }
    }
})

url = "https://example.com/?my_tracking_param=abc&page=1"
result = unalix.clear_url(url, custom_rulesets=custom)

assert result == "https://example.com/?page=1"
```

### Homograph attack detection

```python
import unalix

# Cyrillic 'о' (U+043E) masquerading as Latin 'o'
result = unalix.detect_homograph("https://g\u043e\u043egle.com")

assert result is not None
assert result["normalized"] == "google.com"
assert result["target"] == "google.com"
```

## Contributing

If you have discovered a bug in this library and know how to fix it, fork this repository and open a Pull Request.

## Third party software

Unalix includes some third party software in its codebase. See them below:

- **ClearURLs**
  - Author: Kevin Röbert
  - Repository: [ClearURLs/Rules](https://github.com/ClearURLs/Rules)
  - License: [GNU Lesser General Public License v3.0](https://gitlab.com/ClearURLs/Rules/blob/master/LICENSE)

- **Requests**
  - Author: Kenneth Reitz
  - Repository: [psf/requests](https://github.com/psf/requests)
  - License: [Apache v2.0](https://github.com/psf/requests/blob/master/LICENSE)

- **Pyrogram**
  - Author: Dan
  - Repository: [pyrogram/pyrogram](https://github.com/pyrogram/pyrogram)
  - License: [LGPL-3.0](https://github.com/pyrogram/pyrogram/blob/master/COPYING)
