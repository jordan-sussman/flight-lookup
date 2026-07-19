#!/usr/bin/env python3
"""Find current flights overhead by zip code. Usage: python3 flight-lookup.py 00000 [--radius km]"""

import argparse
import json
import time
import urllib.parse
import urllib.request

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; flight-lookup/1.0)"}


def get_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def get_json_or_none(url):
    try:
        return get_json(url)
    except Exception:
        return None


def geocode_zip(zip_code):
    place = get_json(f"https://api.zippopotam.us/us/{zip_code}")["places"][0]
    return float(place["latitude"]), float(place["longitude"])


def get_flights(lat, lon, radius_km=8, max_age_s=300):
    deg = radius_km / 111.0
    params = urllib.parse.urlencode(
        {
            "lamin": lat - deg,
            "lamax": lat + deg,
            "lomin": lon - deg,
            "lomax": lon + deg,
        }
    )
    data = get_json(f"https://opensky-network.org/api/states/all?{params}")
    now = data.get("time", time.time())

    flights = []
    for s in data.get("states") or []:
        icao24, callsign, _, _, last_contact = s[:5]
        on_ground = s[8]
        if not last_contact or now - last_contact > max_age_s or on_ground:
            continue
        flights.append({"icao24": icao24, "callsign": (callsign or "").strip()})
    return flights


def get_details(icao24, callsign):
    details = {}

    aircraft = get_json_or_none(f"https://hexdb.io/api/v1/aircraft/{icao24}")
    if aircraft:
        details["aircraft"] = aircraft.get("Type")
        details["airline"] = aircraft.get("RegisteredOwners")

    route = get_json_or_none(f"https://hexdb.io/api/v1/route/icao/{callsign}")
    if route and route.get("route"):
        origin, dest = route["route"].split("-")
        details["origin"] = (
            get_json_or_none(f"https://hexdb.io/api/v1/airport/icao/{origin}") or {}
        ).get("airport", origin)
        details["destination"] = (
            get_json_or_none(f"https://hexdb.io/api/v1/airport/icao/{dest}") or {}
        ).get("airport", dest)

    return details


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_code")
    parser.add_argument("--radius", type=float, default=8, help="km, default 8")
    args = parser.parse_args()

    lat, lon = geocode_zip(args.zip_code)
    flights = get_flights(lat, lon, args.radius)

    if not flights:
        print("No flights currently overhead. Try a larger --radius.")
        return

    for f in flights:
        print(f"\nCallsign:   {f['callsign'] or '(unknown)'}")
        if not f["callsign"]:
            continue
        d = get_details(f["icao24"], f["callsign"])
        print(f"Aircraft:   {d.get('aircraft', '-')}")
        print(f"Airline:    {d.get('airline', '-')}")
        print(f"Route:      {d.get('origin', '-')} -> {d.get('destination', '-')}")


if __name__ == "__main__":
    main()
