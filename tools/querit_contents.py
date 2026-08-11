"""Dify tool implementation for Querit Contents API requests."""

import json
from collections.abc import Generator
from typing import Any
from urllib.parse import urlparse

import requests

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class QueritContentsTool(Tool):
    """Crawl web pages through Querit's Contents API."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            credential = self.runtime.credentials["querit_api_key"]
            urls = self._parse_urls(tool_parameters.get("urls"))
            content_format = tool_parameters.get("format") or "markdown"
            crawl_timeout = self._parse_crawl_timeout(
                tool_parameters.get("crawl_timeout")
            )
            extras_meta = self._parse_boolean(
                tool_parameters.get("extras_meta"), default=False
            )

            if content_format not in {"text", "markdown", "html"}:
                raise ValueError("Format must be one of: text, markdown, html")

            payload = {
                "urls": urls,
                "format": content_format,
                "crawlTimeout": crawl_timeout,
                "extrasMeta": extras_meta,
            }
            headers = {
                "Authorization": f"Bearer {credential}",
                "Content-Type": "application/json",
            }

            response = requests.post(
                "https://api.querit.ai/v1/contents",
                json=payload,
                headers=headers,
                timeout=crawl_timeout + 10,
            )
            response.raise_for_status()
            result_data = response.json()
            if not isinstance(result_data, dict):
                raise ValueError("Querit Contents API returned an invalid JSON response")

            yield self.create_json_message(result_data)

            results = result_data.get("results", [])
            if not isinstance(results, list):
                results = []

            contents = []
            result_urls = []
            metadata = []
            for result in results:
                if not isinstance(result, dict):
                    continue
                if isinstance(result.get("content"), str):
                    contents.append(result["content"])
                if isinstance(result.get("url"), str):
                    result_urls.append(result["url"])
                if isinstance(result.get("extrasMeta"), dict):
                    metadata.append(result["extrasMeta"])

            statuses = result_data.get("statuses", [])
            if not isinstance(statuses, list):
                statuses = []

            yield self.create_variable_message("contents", contents)
            yield self.create_variable_message("urls", result_urls)
            yield self.create_variable_message("metadata", metadata)
            yield self.create_variable_message("statuses", statuses)
        except requests.RequestException as exc:
            error_message = f"Error when calling Querit Contents API: {exc}"
            if exc.response is not None:
                error_message += f" - Status code: {exc.response.status_code}"
                if exc.response.text:
                    error_message += f" - Response: {exc.response.text}"
            yield self.create_json_message(
                {"status": "error", "error": error_message}
            )
            yield self.create_text_message(f"Error: {error_message}")
        except (TypeError, ValueError, KeyError, json.JSONDecodeError) as exc:
            error_message = f"Error: {exc}"
            yield self.create_json_message(
                {"status": "error", "error": error_message}
            )
            yield self.create_text_message(error_message)

    @staticmethod
    def _parse_urls(value: Any) -> list[str]:
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("At least one URL is required")
            if value.startswith("["):
                parsed_value = json.loads(value)
                if not isinstance(parsed_value, list):
                    raise ValueError("URLs JSON input must be an array")
                urls = parsed_value
            else:
                urls = [line.strip() for line in value.splitlines() if line.strip()]
        elif isinstance(value, list):
            urls = value
        else:
            raise ValueError("URLs must be a string or an array of strings")

        if not 1 <= len(urls) <= 10:
            raise ValueError("Provide between 1 and 10 URLs")

        normalized_urls = []
        for url in urls:
            if not isinstance(url, str) or not url.strip():
                raise ValueError("Each URL must be a non-empty string")
            normalized_url = url.strip()
            parsed_url = urlparse(normalized_url)
            if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
                raise ValueError(f"Invalid HTTP(S) URL: {normalized_url}")
            normalized_urls.append(normalized_url)

        return normalized_urls

    @staticmethod
    def _parse_crawl_timeout(value: Any) -> int:
        if value in (None, ""):
            return 10
        if isinstance(value, bool):
            raise ValueError("Crawl timeout must be an integer from 1 to 60")
        if isinstance(value, float) and not value.is_integer():
            raise ValueError("Crawl timeout must be an integer from 1 to 60")
        try:
            timeout = int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("Crawl timeout must be an integer from 1 to 60") from exc
        if isinstance(value, str) and value.strip() != str(timeout):
            raise ValueError("Crawl timeout must be an integer from 1 to 60")
        if not 1 <= timeout <= 60:
            raise ValueError("Crawl timeout must be between 1 and 60 seconds")
        return timeout

    @staticmethod
    def _parse_boolean(value: Any, default: bool) -> bool:
        if value in (None, ""):
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized_value = value.strip().lower()
            if normalized_value == "true":
                return True
            if normalized_value == "false":
                return False
        raise ValueError("Extras metadata must be true or false")
