# Now Playing API

A simple FastAPI application that fetches IPTV programme data and provides current programme information via a REST API.

## Features

- `/nowplaying` endpoint that fetches XML data from an IPTV source
- **NEW**: Ability to specify a custom XML URL via query parameter (`?xml_url=...`)
- Parses XML to extract programme titles
- Returns data in a standardized JSON format
- Docker support for easy deployment

## Installation

### Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)

### Local Development

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/now-playing.git
   cd now-playing
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv nowPlaying
   source nowPlaying/bin/activate  # On Windows: nowPlaying\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   uvicorn main:app --reload
   ```

   The API will be available at http://localhost:8000

### Docker Deployment

1. Build the Docker image:
   ```
   docker build -t now-playing .
   ```

2. Run the container:
   ```
   docker run -p 8000:8000 now-playing
   ```

   The API will be available at http://localhost:8000

## API Endpoints

### GET /nowplaying

Returns the titles of up to three programmes currently playing on the IPTV service.

#### Query Parameters

- `xml_url` (optional): Custom URL to fetch XML data from. If not provided, the default URL defined in the application will be used.

Example with custom URL:
```
GET /nowplaying?xml_url=http://example.com/custom-xmltv.xml
```

#### Response Format

```json
{
    "frames": [
        {
            "text": "Programme Title 1",
            "icon": null
        },
        {
            "text": "Programme Title 2",
            "icon": null
        },
        {
            "text": "Programme Title 3",
            "icon": null
        }
    ]
}
```

### GET /

Root endpoint that provides API information.

## Configuration

The default IPTV XML source URL is defined as a constant `XML_URL` in the `main.py` file. This URL is used when no custom URL is provided in the request.

You can override the default URL by:
1. Providing a custom URL as a query parameter: `/nowplaying?xml_url=http://example.com/custom-xmltv.xml`
2. Modifying the `XML_URL` constant in the source code for a permanent change

Note: Previous versions used a config.json file and environment variables for configuration, but these have been removed in favor of a hardcoded constant with query parameter override capability.

## License

MIT
