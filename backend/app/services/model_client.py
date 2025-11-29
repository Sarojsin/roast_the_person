"""
AI model client for generating roasts using vision models.
Supports both Gemini and OpenAI.
"""

import base64
import os
from typing import Optional, Dict
from app.config import settings

# Import Gemini SDK
try:
    import google.generativeai as genai
except ImportError:
    genai = None


class ModelClient:
    """Client for interacting with AI vision models."""
    
    def __init__(self):
        """Initialize the model client based on configured provider."""
        self.provider = settings.AI_PROVIDER
        
        if self.provider == "gemini":
            if not genai:
                raise ImportError("google-generativeai package not installed")
            if not settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not set")
            
            genai.configure(api_key=settings.GEMINI_API_KEY)
            # Use gemini-2.0-flash which is available for this API key
            self.model = genai.GenerativeModel("gemini-2.0-flash")
        
        elif self.provider == "openai":
            # OpenAI implementation can be added here
            raise NotImplementedError("OpenAI provider not yet implemented")
        
        else:
            raise ValueError(f"Unknown AI provider: {self.provider}")
    
    def analyze_image(self, image_bytes: bytes, prompt: str) -> str:
        """
        Analyze an image using the vision model.
        
        Args:
            image_bytes: Raw image bytes
            prompt: Analysis prompt
            
        Returns:
            Model's analysis as text
        """
        if self.provider == "gemini":
            return self._analyze_with_gemini(image_bytes, prompt)
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented")
    
    def _analyze_with_gemini(self, image_bytes: bytes, prompt: str) -> str:
        """
        Analyze image using Gemini.
        
        Args:
            image_bytes: Raw image bytes
            prompt: Analysis prompt
            
        Returns:
            Gemini's analysis
        """
        from PIL import Image
        import io
        
        # Convert bytes to PIL Image (preferred by Gemini SDK)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Generate content with image
        response = self.model.generate_content([prompt, image])
        
        # Extract text from response
        if response.text:
            return response.text
        else:
            raise ValueError("No response from model")
    
    def generate_roast(
        self, 
        image_bytes: bytes, 
        vision_prompt: str, 
        roast_prompt: str
    ) -> Dict[str, str]:
        """
        Generate a roast in two steps:
        1. Analyze the image
        2. Generate witty roast based on analysis
        
        Args:
            image_bytes: Raw image bytes
            vision_prompt: Prompt for image analysis
            roast_prompt: Prompt for roast generation
            
        Returns:
            Dictionary with 'analysis' and 'roast' keys
        """
        # Step 1: Analyze the image
        analysis = self.analyze_image(image_bytes, vision_prompt)
        
        # Step 2: Generate roast based on analysis
        # For Gemini, we can do this in a single call with both image and roast instructions
        full_prompt = f"{roast_prompt}\n\nImage Analysis:\n{analysis}\n\nNow generate a witty roast:"
        
        if self.provider == "gemini":
            roast = self._generate_roast_gemini(image_bytes, full_prompt)
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented")
        
        return {
            "analysis": analysis,
            "roast": roast
        }
    
    def _generate_roast_gemini(self, image_bytes: bytes, prompt: str) -> str:
        """
        Generate roast using Gemini with both image and prompt context.
        
        Args:
            image_bytes: Raw image bytes
            prompt: Full roast generation prompt
            
        Returns:
            Generated roast text
        """
        from PIL import Image
        import io
        
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Generate roast
        response = self.model.generate_content([prompt, image])
        
        if response.text:
            return response.text.strip()
        else:
            raise ValueError("No roast generated")


# Global model client instance
def get_model_client() -> ModelClient:
    """Get or create model client instance."""
    return ModelClient()
