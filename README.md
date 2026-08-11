## What is Querit.ai Search?

[Querit.ai](https://www.querit.ai/) Search is a retrieval system specifically designed for generative LLMs invocation scenarios, providing real-time search results.

Limited training data and local knowledge bases restrict LLMs, leading to hallucinations and timeliness issues when handling complex or real-time queries. To address this, AI search needs to provide retrieval services that are **real-time**, **authoritative**, **accurate**, **high-quality**, and **comprehensive**. Therefore, we offer a Web Search API that seamlessly integrates with your LLM applications, giving you access to authoritative, accurate, and high-quality information from across the web.

### Why Querit.ai?

- **Comprehensive Content**: Massive global index spanning nearly 20 countries and 10 languages with hundreds of billions of web pages.
  - Countries include: United States, India, United Kingdom, Canada, etc.
  - Languages include: English, Spanish, Portuguese, etc.
- **Strong Capabilities**: Flexible retrieval options allowing enterprises to customize results for specific scenarios.
- **Excellent Results**: Delivers accurate, authoritative, and high-quality content coverage.
- **High Performance**: Ensures enterprise-grade high availability with ultra-low latency.

---

## Description

This plugin integrates **Querit.ai** real-time search and retrieval services into **Dify** platform through standardized APIs, allowing agents to query external knowledge sources with natural language and obtain structured search results.

Querit.ai provides a global-scale multilingual indexing and semantic understanding engine for more reliable and precise results, with integrated filtering and ranking strategies to enhance LLM context support.

### Features

- Real-time web search for LLM applications
- Natural language query understanding
- Structured search results with URLs, images, and data
- Full-page content crawling for up to 10 URLs per request
- Text, Markdown, and HTML content output formats
- Optional page metadata, including title, publication time, site name, and site icon
- Global multi-language coverage
- Low-latency enterprise-grade API

---

## Installation

### Prerequisites

- Python 3.11+
- Dify platform (self-hosted or cloud)

### Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/querit-ai/dify-querit.git
   cd dify-querit
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the environment file and configure your API key:
   ```bash
   cp .env.example .env
   ```

4. Get your Querit API key from [Querit Dashboard](https://www.querit.ai/en/dashboard/api-keys) and add it to the `.env` file.

5. Run the plugin:
   ```bash
   python -m main
   ```

---

## Usage

### In Dify

1. Install the plugin in your Dify workspace
2. Configure the Querit API key in the plugin settings
3. Use the Querit Search or Querit Contents tool in your AI agents/workflows

### API Endpoints

#### Search API

Search the web with a natural language query and return structured results.

```
POST https://api.querit.ai/v1/search
```

**Parameters:**
- `query`: The natural language search query (required)
- `count`: The maximum number of search results to return (optional)
- `filters`: Additional conditions used to refine the search results (optional)
- `filters.language`: Restricts results to the specified language, such as `english` (optional)

Example request:

```json
{
  "query": "what does salesforce do",
  "count": 5,
  "filters": {
    "language": "english"
  }
}
```

#### Contents API

Crawl one or more web pages and return their contents with optional metadata.

```
POST https://api.querit.ai/v1/contents
```

**Parameters:**
- `urls`: URLs of pages to crawl. At least 1 and at most 10 URLs are supported
- `format`: Content output format. Supported values are `text`, `markdown`, and `html` (optional, defaults to `markdown`)
- `crawlTimeout`: Page crawl timeout in seconds, from 1 to 60 (optional, defaults to `10`)
- `extrasMeta`: Whether to include page metadata in each result (optional, defaults to `false`)

**Response:**
- `results`: Crawled page contents and optional metadata
- `statuses`: Per-URL crawl status (`success` or `failed`)
- `searchTime`: Server-side crawl time in seconds

Example request:

```json
{
  "urls": [
    "https://example.com"
  ],
  "format": "markdown",
  "crawlTimeout": 10,
  "extrasMeta": true
}
```

---

## Development

See [GUIDE.md](GUIDE.md) for detailed development documentation.

### Plugin Structure

```
dify-querit/
├── main.py                 # Plugin entry point
├── manifest.yaml           # Plugin manifest
├── provider/               # Provider configuration
│   ├── dify_querit.py
│   └── dify_querit.yaml
├── tools/                  # Tool definitions
│   ├── dify_querit.py
│   └── dify_querit.yaml
├── _assets/                # Icons and assets
├── README.md               # This file
├── GUIDE.md                # Development guide
└── requirements.txt        # Python dependencies
```

---

## Publishing to Dify Marketplace

This plugin follows the official Dify plugin publishing workflow:

1. **Develop & Test**: Make changes in this repository and test locally
2. **Create Release**: Publish a new release with a version tag (e.g., v0.0.1)
3. **Auto-Publish**: GitHub Actions will automatically:
   - Package the plugin
   - Create a branch in [dify-plugins](https://github.com/querit-ai/dify-plugins)
4. **Submit to Dify**: The branch will be merged into the official Dify plugin repository

For detailed publishing instructions, see [CONTRIBUTING.md](CONTRIBUTING.md#publishing-releases).

---

## License

See [LICENSE](LICENSE) for details.

---

## Support

- [GitHub Issues](https://github.com/querit-ai/dify-querit/issues)
- [Querit Website](https://www.querit.ai/)
- [Querit Dashboard](https://www.querit.ai/en/dashboard)
