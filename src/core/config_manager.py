"""
Core Configuration Manager
Centralized configuration management for all Gaia components
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """
    Centralized configuration management system
    """
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.config_data: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
            else:
                self.create_default_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration"""
        self.config_data = {
            "azure": {
                "key": "",
                "region": "eastus",
                "voice": "en-US-AriaNeural"
            },
            "llm": {
                "model": "llama3",
                "temperature": 0.7
            },
            "hotel": {
                "name": "Boutique Hotel",
                "rooms": 8
            },
            "audio": {
                "input_device": None,
                "sample_rate": 16000
            },
            "gui": {
                "theme": "dark",
                "window_size": [1000, 700]
            }
        }
        self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        current = self.config_data
        
        try:
            for k in keys:
                current = current[k]
            return current
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key.split('.')
        current = self.config_data
        
        # Navigate to the parent of the final key
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Set the final key
        current[keys[-1]] = value
        self.save_config()
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section"""
        return self.config_data.get(section, {})
    
    def update_section(self, section: str, data: Dict[str, Any]):
        """Update entire configuration section"""
        if section not in self.config_data:
            self.config_data[section] = {}
        self.config_data[section].update(data)
        self.save_config()
