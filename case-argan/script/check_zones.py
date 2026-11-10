#!/usr/bin/env python3
"""check_zones.py — controle de cloisonnement des zones d'Argan Retail.
Verifie l'accessibilite declaree entre zones, pas seulement les identifiants.
Codes : 0 conforme, 1 ecart reel, 2 controle impossible.
"""
import sys, ipaddress, yaml

try:
    zones = yaml.safe_load(open("data/zones.yml", encoding="utf-8"))["zones"]
except Exception as e:
    print(f"check impossible: {e}")
    sys.exit(2)

declared = [z for z in zones if "allowed_to_reach" in z]
if not declared:
    print("check impossible: no reachability rules declared")
    sys.exit(2)

names = {z["name"] for z in zones}
errors = []

# 1. identite : VLAN et VRF uniques, prefixes disjoints
vlans = [z["vlan"] for z in zones]
if len(set(vlans)) != len(vlans):
    errors.append("duplicate VLAN id")
vrfs = [z["vrf"] for z in zones]
if len(set(vrfs)) != len(vrfs):
    errors.append("two zones share a VRF")
nets = [(z["name"], ipaddress.ip_network(z["prefix"])) for z in zones]
for i, (a, na) in enumerate(nets):
    for b, nb in nets[i + 1:]:
        if na.overlaps(nb):
            errors.append(f"prefix overlap: {a} / {b}")

# 2. accessibilite : la vraie propriete
if len(declared) != len(zones):
    errors.append("some zones declare no reachability rule")
reach = {z["name"]: set(z.get("allowed_to_reach", [])) for z in zones}
for src, dsts in reach.items():
    for d in dsts:
        if d in ("*", "any"):
            errors.append(f"{src} may reach everything")
        elif d != "internet" and d not in names:
            errors.append(f"{src} references unknown zone {d}")

# 3. politique attendue
FORBIDDEN = [("guest", z) for z in names if z != "guest"]
FORBIDDEN += [("warehouse-wifi", z) for z in names if z not in ("warehouse-wifi", "datacentre")]
FORBIDDEN += [("warehouse-control", z) for z in names if z not in ("warehouse-control", "datacentre")]
for s, d in FORBIDDEN:
    if d in reach.get(s, set()):
        errors.append(f"forbidden path: {s} -> {d}")

n = len(zones)
if sum(len(r & names) for r in reach.values()) >= n * (n - 1):
    errors.append("every zone can reach every other zone")

if errors:
    for e in errors:
        print("FAIL:", e)
    sys.exit(1)
print(f"{n} zones: declared reachability matches the policy")
sys.exit(0)