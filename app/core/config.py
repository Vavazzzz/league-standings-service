from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Dict, Optional


class Settings(BaseSettings):
    app_name: str = "Standings Service"
    debug: bool = False
    
    model_config = ConfigDict(
        env_file=".env",
        extra="allow"  # Allow extra fields from env vars
    )
    
    def get_team_config(self, team_id: str) -> Dict[str, str]:
        """
        Retrieve configuration for a specific team.
        
        Args:
            team_id: Team identifier (e.g., "1", "2")
            
        Returns:
            Dictionary with base_url, category_id, and main_url_path
            
        Raises:
            ValueError: If team configuration is not found
        """
        team_id = str(team_id).upper()
        
        base_url = self._get_env_var(f"TEAM{team_id}_BASE_URL")
        category_id = self._get_env_var(f"TEAM{team_id}_CATEGORY_ID")
        main_url_path = self._get_env_var(f"TEAM{team_id}_MAIN_URL_PATH")
        
        if not all([base_url, category_id, main_url_path]):
            raise ValueError(
                f"Team configuration for TEAM{team_id} is incomplete. "
                f"Required env vars: TEAM{team_id}_BASE_URL, TEAM{team_id}_CATEGORY_ID, TEAM{team_id}_MAIN_URL_PATH"
            )
        
        return {
            "base_url": base_url,
            "category_id": category_id,
            "main_url_path": main_url_path
        }
    
    def _get_env_var(self, var_name: str) -> Optional[str]:
        """Retrieve environment variable from loaded settings"""
        # Convert to lowercase for attribute access (pydantic lowercases env var names)
        attr_name = var_name.lower()
        return getattr(self, attr_name, None)


settings = Settings()


if __name__ == "__main__":
    env_var = settings._get_env_var("TEAM1_BASE_URL")
    print(f"TEAM1_BASE_URL: {env_var}")