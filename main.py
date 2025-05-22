from fastapi import FastAPI, HTTPException
import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Any, Tuple
import uvicorn
from datetime import datetime, timedelta, timezone
import re
from zoneinfo import ZoneInfo

# Constant XML URL
XML_URL = "http://192.168.0.210:8410/iptv/xmltv.xml"

# Define CET timezone
CET = ZoneInfo("Europe/Berlin")

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

def parse_xmltv_time(time_str: str) -> datetime:
    """
    Parse XMLTV time format (YYYYMMDDHHMMSS +HHMM) to datetime in CET.
    """
    # Extract the datetime part and timezone part
    match = re.match(r'(\d{14})\s*([+-]\d{4})?', time_str)
    if not match:
        raise ValueError(f"Invalid time format: {time_str}")
    
    dt_part = match.group(1)
    tz_part = match.group(2) if match.group(2) else "+0000"
    
    # Parse the datetime part
    dt = datetime.strptime(dt_part, "%Y%m%d%H%M%S")
    
    # Parse the timezone offset
    tz_hours = int(tz_part[1:3])
    tz_minutes = int(tz_part[3:5])
    tz_offset = timedelta(hours=tz_hours, minutes=tz_minutes)
    
    # Apply the timezone offset to get UTC time
    if tz_part[0] == '+':
        dt = dt - tz_offset
    else:
        dt = dt + tz_offset
    
    # Convert to UTC first (as aware datetime)
    dt_utc = dt.replace(tzinfo=timezone.utc)
    
    # Then convert to CET
    dt_cet = dt_utc.astimezone(CET)
    
    return dt_cet

async def parse_programmes(xml_data: str, limit: Optional[int] = None) -> List[Dict[str, Optional[str]]]:
    """
    Parse XML data and extract programmes whose start time is closest to the current time in CET,
    but whose stop time hasn't passed yet.
    Returns a list of dictionaries with text and icon fields.
    """
    try:
        root = ET.fromstring(xml_data)
        programmes = root.findall(".//programme")
        
        # Dictionary to track the closest programme for each channel
        channel_programmes: Dict[str, Dict[str, Any]] = {}
        
        # Get current time in CET
        current_time_cet = datetime.now(CET)
        
        # Group programmes by channel
        for programme in programmes:
            # Get the channel ID from the programme element
            channel_id = programme.get("channel")
            
            if not channel_id:
                continue
                
            # Get start and stop times from the programme
            start_str = programme.get("start")
            stop_str = programme.get("stop")
            
            if not start_str or not stop_str:
                continue
                
            # Parse the start and stop times to CET
            try:
                start_time_cet = parse_xmltv_time(start_str)
                stop_time_cet = parse_xmltv_time(stop_str)
                
                # Only consider programmes whose stop time hasn't passed yet
                if stop_time_cet > current_time_cet:
                    # Calculate time difference between start time and current time (absolute value)
                    time_diff = abs((start_time_cet - current_time_cet).total_seconds())
                    
                    # If we haven't seen this channel yet, or if this programme's start time is closer to current time
                    if channel_id not in channel_programmes or time_diff < channel_programmes[channel_id]["time_diff"]:
                        title_element = programme.find(".//title")
                        title = title_element.text if title_element is not None else "No title available"
                        
                        channel_programmes[channel_id] = {
                            "text": title,
                            "icon": "7740",
                            "time_diff": time_diff,
                            "start_time": start_time_cet,  # Store for debugging
                            "stop_time": stop_time_cet     # Store for debugging
                        }
            except ValueError as e:
                # Skip programmes with unparseable times
                print(f"Error parsing time: {e}")
                continue
        
        # Convert the dictionary values to a list, removing the time_diff, start_time and stop_time fields
        results: List[Dict[str, Optional[str]]] = []
        for prog in channel_programmes.values():
            clean_prog: Dict[str, Optional[str]] = {
                "text": prog.get("text"),
                "icon": prog.get("icon")
            }
            results.append(clean_prog)
        
        # Apply limit if specified
        if limit is not None:
            results = results[:limit]
        
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
