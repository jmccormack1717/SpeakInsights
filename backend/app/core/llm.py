"""LLM client wrapper for OpenAI"""
import json
from typing import Dict, Any, Optional
from openai import OpenAI
from app.config import settings


class LLMClient:
    """Wrapper for OpenAI API"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    async def chat_completion(
        self,
        messages: list[Dict[str, str]],
        temperature: float = 0.3,
        response_format: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Make a chat completion request
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            response_format: Optional JSON schema for structured output
            
        Returns:
            Response content as string
        """
        try:
            kwargs = {
                "model": self.model,
                "messages": messages,
            }
            
            # Some models (like gpt-5-nano) only support default temperature (1)
            # Check if model name contains 'nano' and skip temperature parameter
            if 'nano' not in self.model.lower():
                kwargs["temperature"] = temperature
            
            if response_format:
                kwargs["response_format"] = response_format
            
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"LLM API error: {str(e)}")
    
    async def generate_json(
        self,
        messages: list[Dict[str, str]],
        temperature: float = 0.3
    ) -> Dict[str, Any]:
        """
        Generate and parse JSON response
        
        Args:
            messages: List of message dicts
            temperature: Sampling temperature
            
        Returns:
            Parsed JSON as dict
        """
        response_format = {"type": "json_object"}
        response = await self.chat_completion(messages, temperature, response_format)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract JSON from response if it's wrapped in text
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            raise Exception("Failed to parse JSON response from LLM")

