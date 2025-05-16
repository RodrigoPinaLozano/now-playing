# Now Playing API

A simple FastAPI application that fetches IPTV programme data and provides current programme information via a REST API.

## Features

- `/nowplaying` endpoint that fetches XML data from an IPTV source
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

The IPTV XML source URL can be configured in several ways:

1. **Environment Variable**: Set the `XML_URL` environment variable:
   ```
   export XML_URL="http://your-iptv-server/xmltv.xml"
   ```

2. **Config File**: Edit the `config.json` file in the project root:
   ```json
   {
       "xml_url": "http://your-iptv-server/xmltv.xml"
   }
   ```

3. **Docker Environment Variable**: When running with Docker, pass the environment variable:
   ```
   docker run -p 8000:8000 -e XML_URL="http://your-iptv-server/xmltv.xml" now-playing
   ```

The configuration priority is:
1. Environment variable (highest priority)
2. Config file
3. Default value: `http://192.168.0.210:8410/iptv/xmltv.xml` (lowest priority)

## License

MIT
