"""Content keys for LawlerAI site - used by dashboard and templates."""
from .default_content import DEFAULT_CONTENT

CONTENT_KEYS = list(DEFAULT_CONTENT.keys())

CONTENT_GROUPS = {
    "Hero": ["hero.tagline", "hero.headline_line1", "hero.headline_line2", "hero.subheadline", "hero.cta_label"],
    "What's Happening": ["happening.headline_line1", "happening.headline_line2", "happening.context", "happening.closing_statement"],
    "Outcome": ["outcome.label", "outcome.headline", "outcome.benefit_1", "outcome.benefit_2", "outcome.benefit_3", "outcome.tagline_1", "outcome.tagline_2"],
    "Clarity to Strategy": ["clarity.label", "clarity.headline", "clarity.intro", "clarity.closing_tagline"],
    "CTA Section": ["cta.label", "cta.headline_line1", "cta.headline_line2", "cta.subheadline", "cta.button_label"],
    "Footer": ["footer.tagline", "footer.logo_url"],
    "Site": ["site.title", "site.meta_description"],
}

# Image keys for the Images dashboard (separate from text content)
IMAGE_KEYS = [
    ("nav.logo_url", "Nav logo"),
    ("footer.logo_url", "Footer logo"),
    ("hero.background_image", "Hero background image"),
    ("hero.background_video_url", "Hero background video (YouTube embed URL)"),
    ("cta.background_image", "CTA background image"),
    ("cta.background_video_url", "CTA background video (YouTube embed URL)"),
    ("built_for_sports.image_url", "Built for Sports (Nancy photo)"),
]
