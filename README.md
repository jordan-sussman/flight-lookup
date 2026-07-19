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
```

## How it works

1. Geocodes the ZIP code ([Zippopotam.us](https://www.zippopotam.us/))
2. Queries [OpenSky Network](https://opensky-network.org/) for aircraft within the radius, seen airborne in the last 5 minutes
3. Looks up aircraft type and airline by callsign via [hexdb.io](https://hexdb.io/)

## Defaults

- Radius: 8 km (can be overriden via `--radius`)
- Last seen within last: 5 minutes

## Notes

- Requires Python 3.6+
- No API key or external dependencies
- Some data can be unavailable for aircraft as hexdb.io's database is primarily built for commercial traffic
