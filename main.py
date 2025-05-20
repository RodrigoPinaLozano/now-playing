from fastapi import FastAPI, HTTPException
import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
import uvicorn

# Constant XML URL
XML_URL = "http://192.168.0.210:8410/iptv/xmltv.xml"

app = FastAPI(title="Now Playing API")

def get_config():
    """
    Load configuration.
    This function is kept for potential future configuration needs.
    """
    # Configuration dictionary
    config = {}
    
    return config

async def fetch_xml_data(url: str) -> str:
    """Fetch XML data from the provided URL."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.text
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch XML data: {str(e)}")

async def parse_programmes(xml_data: str, limit: int = 3) -> List[Dict[str, Optional[str]]]:
    """
    Parse XML data and extract programme titles.
    Returns a list of dictionaries with text and icon fields.
    """
    try:
        root = ET.fromstring(xml_data)
        programmes = root.findall(".//programme")
        
        results = []
        for i, programme in enumerate(programmes[:limit]):
            title_element = programme.find(".//title")
            title = title_element.text if title_element is not None else "No title available"
            
            results.append({
                "text": title,
                "icon": "7740"
            })
        
        return results
    except ET.ParseError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse XML data: {str(e)}")

@app.get("/nowplaying")
async def now_playing(xml_url: Optional[str] = None):
    """
    Endpoint that fetches current programme titles from IPTV XML data
    and returns them in the required JSON format.
    
    Parameters:
    - xml_url: Optional URL to fetch XML data from. If not provided, the default URL will be used.
    """
    # Use the provided URL if available, otherwise fall back to the constant
    url_to_use = xml_url if xml_url else XML_URL
    xml_data = await fetch_xml_data(url_to_use)
    programmes = await parse_programmes(xml_data)
    
    return {
        "frames": programmes
    }

@app.get("/")
async def root():
    """Root endpoint that provides API information."""
    return {
        "message": "Now Playing API is running",
        "endpoints": {
            "/nowplaying": "Get current programme information"
        }
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
