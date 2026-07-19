# flight-lookup

Find current flights overhead by zip code.

## Usage

```bash
python3 flight-lookup.py 54321
python3 flight-lookup.py 54321 --radius 15
```

Output:

```
Callsign:   ASA1234
Aircraft:   B737 800
Airline:    Alaska Airlines
Route:      Seattle-Tacoma International Airport -> Portland International Airport
```

## How it works

1. Geocodes the ZIP code ([Zippopotam.us](https://www.zippopotam.us/))
2. Queries [OpenSky Network](https://opensky-network.org/) for aircraft within the radius, seen airborne in the last 5 minutes
3. Looks up aircraft type, airline, and route by callsign via [hexdb.io](https://hexdb.io/)

## Notes

- Requires Python 3.6+
- No API key or external dependencies
- Data may not be fully available for all aircraft, as hexdb.io's database is built from primarily commercial traffic
