"""Central brand configuration for LexCraft AI.

Every user-visible product name, tagline, and asset path lives here so the
application can be rebranded from a single file.
"""

APP_NAME = "LexCraft AI"
APP_TAGLINE = "AI-Powered Legal Document Studio"
APP_SHORT = "LexCraft"
FOOTER_NOTICE = (
    "LexCraft AI drafts are AI-generated information and must be reviewed by a "
    "qualified legal professional before use."
)
EXPORT_FOOTER = "LexCraft AI - AI-generated draft | Review before use"
DISCLAIMER_TITLE = "Important Notice"

# Document type presets shown in the UI and in the template gallery.
DOCUMENT_TYPES = [
    "Employment Contract",
    "NDA (Non-Disclosure Agreement)",
    "Lease Agreement",
    "Freelance Work Contract",
    "Service Agreement",
    "General Agreement",
    "Custom",
]

ASSET_DIR_NAME = "assets"
LOGO_FILENAME = "lexcraft_logo.png"


def logo_path():
    """Return the Path of the brand logo (may not exist)."""
    from pathlib import Path

    return Path(__file__).resolve().parents[1] / ASSET_DIR_NAME / LOGO_FILENAME


def legacy_logo_path():
    """Original reference-repo logo, used only as a fallback asset."""
    from pathlib import Path

    return Path(__file__).resolve().parents[1] / ASSET_DIR_NAME / "logo.png"
