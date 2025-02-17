import json
from pathlib import Path

CONFIG_DIR = Path(__file__).parent.parent.parent.parent.joinpath('config').resolve()

# Prepare zone bounding boxes
ZONE_BOUNDING_BOXES = {}

# Read parser import list from config jsons
ZONES_CONFIG = json.load(open(CONFIG_DIR.joinpath('zones.json')))
EXCHANGES_CONFIG = json.load(open(CONFIG_DIR.joinpath('exchanges.json')))

# Read all zones
for zone_id, zone_config in ZONES_CONFIG.items():
    if 'bounding_box' in zone_config:
        ZONE_BOUNDING_BOXES[zone_id] = zone_config['bounding_box']

ZONE_NEIGHBOURS = {}
for k, v in EXCHANGES_CONFIG.items():
    zone_names = k.split('->')
    pairs = [
        (zone_names[0], zone_names[1]),
        (zone_names[1], zone_names[0])
    ]
    for zone_name_1, zone_name_2 in pairs:
        if zone_name_1 not in ZONE_NEIGHBOURS:
            ZONE_NEIGHBOURS[zone_name_1] = set()
        ZONE_NEIGHBOURS[zone_name_1].add(zone_name_2)
# we want neighbors to always be in the same order
for zone, neighbors in ZONE_NEIGHBOURS.items():
    ZONE_NEIGHBOURS[zone] = sorted(neighbors)

CO2EQ_PARAMETERS = json.load(open(CONFIG_DIR.joinpath('co2eq_parameters.json')))

def emission_factors(zone_key):
    override = CO2EQ_PARAMETERS['emissionFactors']['zoneOverrides'].get(zone_key, {})
    defaults = CO2EQ_PARAMETERS['emissionFactors']['defaults']
    merged = {**defaults, **override}
    return dict([(k, (v or {}).get('value')) for (k, v) in merged.items()])
