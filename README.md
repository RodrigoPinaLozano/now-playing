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

The IPTV XML source is currently hardcoded to `http://192.168.0.210:8410/iptv/xmltv.xml`. To change this, modify the `xml_url` variable in the `now_playing` function in `main.py`.

## License

MIT