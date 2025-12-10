"""
moderation.py
Content moderation service for images and text.
Ensures roasts are funny but not harmful.
"""

from typing import Dict, List
from PIL import Image
import io


class ModerationService:
    """Service for moderating image uploads and roast content."""
    
    # Keywords that indicate potentially harmful content in roasts
    HARMFUL_KEYWORDS = {
        # Extreme insults
        "kill", "die", "suicide", "harm yourself",
        # Slurs and hate speech (add carefully)
        # Personal attacks beyond roasting
        "worthless", "pathetic loser", "waste of space",
    }
    
    # Minimum dimensions for profile images
    MIN_IMAGE_WIDTH = 100
    MIN_IMAGE_HEIGHT = 100
    
    # Maximum dimensions (to prevent memory issues)
    MAX_IMAGE_WIDTH = 4000
    MAX_IMAGE_HEIGHT = 4000
    
    @staticmethod
    def validate_image(image_bytes: bytes) -> Dict[str, any]:
        """
        Validate that the uploaded image is appropriate.
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Dictionary with 'valid' (bool) and 'reason' (str) keys
        """
        try:
            # Try to open image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Check dimensions
            width, height = image.size
            
            if width < ModerationService.MIN_IMAGE_WIDTH or height < ModerationService.MIN_IMAGE_HEIGHT:
                return {
                    "valid": False,
                    "reason": f"Image too small. Minimum size: {ModerationService.MIN_IMAGE_WIDTH}x{ModerationService.MIN_IMAGE_HEIGHT}px"
                }
            
            if width > ModerationService.MAX_IMAGE_WIDTH or height > ModerationService.MAX_IMAGE_HEIGHT:
                return {
                    "valid": False,
                    "reason": f"Image too large. Maximum size: {ModerationService.MAX_IMAGE_WIDTH}x{ModerationService.MAX_IMAGE_HEIGHT}px"
                }
            
            # Check if image has valid format
            if image.format not in ['JPEG', 'PNG', 'WEBP']:
                return {
                    "valid": False,
                    "reason": f"Unsupported format: {image.format}. Please use JPEG, PNG, or WEBP."
                }
            
            # Basic validation passed
            return {
                "valid": True,
                "reason": "Image validation passed",
                "metadata": {
                    "width": width,
                    "height": height,
                    "format": image.format,
                    "mode": image.mode
                }
            }
            
        except Exception as e:
            return {
                "valid": False,
                "reason": f"Invalid image file: {str(e)}"
            }
    
    @staticmethod
    def moderate_roast(roast_text: str) -> Dict[str, any]:
        """
        Check if the roast content is appropriate.
        Filters out extremely harmful content while keeping it funny.
        
        Args:
            roast_text: The generated roast text
            
        Returns:
            Dictionary with 'approved' (bool) and 'reason' (str) keys
        """
        if not roast_text or len(roast_text.strip()) == 0:
            return {
                "approved": False,
                "reason": "Empty roast content"
            }
        
        # Convert to lowercase for checking
        roast_lower = roast_text.lower()
        
        # Check for harmful keywords (whole word matching)
        import re
        for keyword in ModerationService.HARMFUL_KEYWORDS:
            # Create regex for whole word matching
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, roast_lower):
                return {
                    "approved": False,
                    "reason": f"Contains harmful content: '{keyword}'"
                }
        
        # Check length (roasts should be substantial but not essays)
        if len(roast_text) < 50:
            return {
                "approved": False,
                "reason": "Roast too short"
            }
        
        if len(roast_text) > 2000:
            return {
                "approved": False,
                "reason": "Roast too long"
            }
        
        # Passed all checks
        return {
            "approved": True,
            "reason": "Roast content approved"
        }
    
    @staticmethod
    def sanitize_roast(roast_text: str) -> str:
        """
        Sanitize roast text by removing any potentially harmful content.
        
        Args:
            roast_text: Raw roast text
            
        Returns:
            Sanitized roast text
        """
        # For now, just return the original
        # In production, you might want to:
        # - Remove specific words
        # - Apply additional filtering
        # - Use ML-based toxicity detection
        return roast_text.strip()


# Global moderation service instance
moderation = ModerationService()
