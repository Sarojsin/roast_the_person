"""
Tests for the moderation service.
"""

import pytest
from app.services.moderation import ModerationService
from PIL import Image
import io


@pytest.fixture
def valid_image_bytes():
    """Create valid image bytes for testing."""
    img = Image.new('RGB', (500, 500), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    return img_bytes.getvalue()


@pytest.fixture
def small_image_bytes():
    """Create too-small image bytes."""
    img = Image.new('RGB', (50, 50), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    return img_bytes.getvalue()


def test_validate_valid_image(valid_image_bytes):
    """Test validating a valid image."""
    result = ModerationService.validate_image(valid_image_bytes)
    assert result["valid"] is True
    assert "metadata" in result


def test_validate_small_image(small_image_bytes):
    """Test validating an image that's too small."""
    result = ModerationService.validate_image(small_image_bytes)
    assert result["valid"] is False
    assert "too small" in result["reason"].lower()


def test_validate_invalid_bytes():
    """Test validating invalid image bytes."""
    result = ModerationService.validate_image(b"not an image")
    assert result["valid"] is False
    assert "invalid" in result["reason"].lower()


def test_moderate_valid_roast():
    """Test moderating a valid roast."""
    roast = "Your profile pic looks like it was taken with a potato camera from 2005."
    result = ModerationService.moderate_roast(roast)
    assert result["approved"] is True


def test_moderate_harmful_roast():
    """Test moderating a roast with harmful content."""
    roast = "You should just kill yourself."
    result = ModerationService.moderate_roast(roast)
    assert result["approved"] is False


def test_moderate_empty_roast():
    """Test moderating an empty roast."""
    result = ModerationService.moderate_roast("")
    assert result["approved"] is False


def test_moderate_short_roast():
    """Test moderating a roast that's too short."""
    result = ModerationService.moderate_roast("Bad pic.")
    assert result["approved"] is False


def test_moderate_long_roast():
    """Test moderating a roast that's too long."""
    roast = "x" * 2500  # Way too long
    result = ModerationService.moderate_roast(roast)
    assert result["approved"] is False


def test_sanitize_roast():
    """Test roast sanitization."""
    roast = "  Your profile pic is hilarious  "
    sanitized = ModerationService.sanitize_roast(roast)
    assert sanitized == "Your profile pic is hilarious"
