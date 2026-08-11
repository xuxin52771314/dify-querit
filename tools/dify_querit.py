from collections.abc import Generator
from typing import Any, Dict, List, Optional
import os
import requests
from datetime import datetime
import json

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class DifyQueritTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            # Get API key from runtime credentials
            credential = self.runtime.credentials["querit_api_key"]
            
            # Required parameter
            query = tool_parameters.get("query")
            if not query:
                raise ValueError("Search query is required")

            # Remove None values from payload
            payload = {"query": query}
            
            
            # Make API request
            headers = {
                "Authorization": f"Bearer {credential}",
                "Content-Type": "application/json"
            }
            print("Payload being sent to Querit API:")
            print(json.dumps(payload, indent=2))
            response = requests.post(
                "https://api.querit.ai/v1/search",
                json=payload,
                headers=headers
            )

            response.raise_for_status()
            result_data = response.json()
            
            # Yield the raw JSON response first
            yield self.create_json_message(result_data)

            # Extract urls and images from results
            urls = []
            images = []
            raw_resultss = result_data.get("results", [])
            raw_results = raw_resultss.get("result", [])
            for result in raw_results:
                if url := result.get("url"):
                    urls.append(url)
                # Handle image extraction with proper validation
                if "image" in result:
                    image = result["snippet"]
                    if isinstance(image, str) and image.strip():  # Ensure non-empty string
                        if image.startswith(('http://', 'https://')):  # Basic URL validation
                            images.append(image)

            # Debug output
            print("\n===== EXTRACTED URLS AND IMAGES =====")
            print("URLs:", urls)
            print("Images:", images)
            print("===== END OF EXTRACTION =====\n")

            # Yield urls and images as separate variables
            yield self.create_variable_message("urls", urls)
            yield self.create_variable_message("images", images)

            # yield self.create_json_message({
            #     "result": "Hello, world!"
            # })
        except requests.RequestException as e:
            error_message = f"Error when calling Querit Search API: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                error_message += f" - Status code: {e.response.status_code}"
                if hasattr(e.response, 'text'):
                    error_message += f" - Response: {e.response.text}"
            
            yield self.create_json_message({
                "status": "error",
                "error": error_message
            })
            
            yield self.create_text_message(f"Error: {error_message}")
        except Exception as e:
            error_message = f"Error: {str(e)}"
            
            yield self.create_json_message({
                "status": "error",
                "error": error_message
            })
            
            yield self.create_text_message(f"Error: {error_message}")
