\# Decision note - architecture of the Atlas Industrie campus



\## 1. Context and requirements



Atlas Industrie operates two buildings: building A (head office and IT) and building B (production). The campus network must serve IT, voice, guests, OT (automates and supervision) and a DMZ, with 14 devices to manage: 2 cores, 2 firewalls and 10 access switches (6 in A, 4 in B).



Stated requirements:



\- Production in building B must continue if building A is isolated.

\- Zones are separated by firewalls. The OT zone is protected from IT by a default-deny policy: nothing crosses from IT to OT unless explicitly allowed.

\- The addressing plan (`data/vlans.yml`) is hierarchical so that a rule such as "OT to IT" can be written on a single prefix (10.42.64.0/20).

\- Horizon: 5 years.



\## 2. Technical targets retained



\- Dual-stack addressing (IPv4 plus a ULA IPv6 prefix), one VLAN per function, VLAN 99 as a non-routed parking VLAN.

\- Firewall placement: one firewall per site (FW-A, FW-B), between the cores and the outside, and between the trust zones (IT, OT, guests, DMZ). The DMZ (VLAN 60) hangs off the firewalls and is reachable from the other zones only through explicit rules.

\- Default deny between IT and OT. Only flows that are named and justified (for example supervision to controllers) are opened.

\- Two cores, one in each building, linked by two fibres on distinct routes.

\- Availability target: 99.99 %. See section 6 for why it is not demonstrated.



\## 3. The two architectures compared



Three scenarios were priced. S3 is not an equivalent alternative (see section 5), it prices the requirement.



| | S1: three tiers | S2: collapsed core, distributed A and B | S3: collapsed core, single site |

|---|---|---|---|

| Core | 2 modular L3 cores | 2 fixed 10/25G L3 cores | 2 fixed 10/25G L3 cores, both in A |

| Distribution | 4 L3 distribution switches | none | none |

| Access | 10 | 10 | 10 |

| Firewalls | 2 | 2 | 2 |

| Devices counted | 18 | 14 | 14 |

| Survives isolation of building A | yes | yes | no |

| Fibre between cores | three tiers, 129,600 MAD | second fibre on a distinct route, 108,000 MAD | single site, 86,400 MAD |

| Operational complexity | highest (more layers) | medium | lowest |



\## 4. Five-year costing



All amounts in MAD, excluding tax, at the teaching rate 1 EUR = 10.8 MAD. Support is 10 % of CAPEX per year. Operations is 1.5 days per device per year at 5,400 MAD a day, i.e. 8,100 MAD per device per year. Firewalls are counted as devices.



TCO(5 years) = CAPEX + 5 x (annual support + annual operations)



\*\*CAPEX\*\*



| Item | S1 | S2 | S3 |

|---|---|---|---|

| Cores | 2 x 162,000 = 324,000 | 2 x 86,400 = 172,800 | 2 x 86,400 = 172,800 |

| Distribution | 4 x 54,000 = 216,000 | 0 | 0 |

| Access | 10 x 27,000 = 270,000 | 270,000 | 270,000 |

| Firewall pair | 216,000 | 216,000 | 216,000 |

| Optics and fibre | 129,600 | 108,000 | 86,400 |

| \*\*CAPEX\*\* | \*\*1,155,600\*\* | \*\*766,800\*\* | \*\*745,200\*\* |



\*\*Running costs and TCO\*\*



| | S1 | S2 | S3 |

|---|---|---|---|

| Devices | 18 | 14 | 14 |

| Annual support (10 % of CAPEX) | 115,560 | 76,680 | 74,520 |

| Annual operations (devices x 8,100) | 145,800 | 113,400 | 113,400 |

| Annual running cost | 261,360 | 190,080 | 187,920 |

| 5-year support | 577,800 | 383,400 | 372,600 |

| 5-year operations | 729,000 | 567,000 | 567,000 |

| \*\*TCO (5 years)\*\* | \*\*2,462,400\*\* | \*\*1,717,200\*\* | \*\*1,684,800\*\* |



\*\*The two gaps that carry the decision\*\*



\- S2 against S1: S2 is cheaper by 745,200 MAD over 5 years (about 30 % of S1's TCO). The saving comes from removing 4 distribution switches and replacing two modular cores with two fixed cores.

\- S2 against S3: S2 costs 32,400 MAD more over 5 years (about 1.9 % of S3's TCO): 21,600 MAD of extra CAPEX (the distributed-core fibre) plus 10,800 MAD of extra support.



\## 5. Decision and justification



\*\*Decision: retain S2, the collapsed core distributed between buildings A and B.\*\*



Against S1: both tolerate the loss of a building, but S1 adds a distribution layer that the campus size does not need. It costs 745,200 MAD more over 5 years, adds 4 devices to operate and adds one more layer of failure and configuration.



Against S3, the cheapest: S3 is not rejected because it is "worse". It does not satisfy a stated requirement, namely that production continues if building A is isolated, since both of its cores are in A. S3 is therefore a different solution, not a cheaper equivalent one. It serves to price the requirement: meeting it costs 32,400 MAD over 5 years.



Is that extra cost worth it? At 108,000 MAD per hour of production outage, 32,400 MAD corresponds to 0.3 hour, i.e. \*\*18 minutes\*\* of production downtime. If, over 5 years, isolating building A would stop production for more than 18 minutes in total, S2 pays for itself. Given that a single cable cut, a power failure or a firewall mistake in building A would be enough to exceed that, the extra cost is justified.



\## 6. Risks and points of failure



\- \*\*The 99.99 % target is not demonstrated.\*\* Three devices in series at 99.9 % each give 0.999^3 = 0.997, about 99.7 %. Doubling the core and the firewall makes each pair about 0.999999 (1 - 0.001^2), but the access switch is not redundant and stays at 0.999. The chain is then about 0.999 x 0.999999 x 0.999999 = 0.999, about 99.9 %: below the target, and set by the non-redundant access switch. To go further, we would have to analyse power supplies, fibre routes and failover mechanisms.

\- \*\*Common causes make the theoretical figure overstate reality.\*\* The parallel model assumes independent failures. Same software version on both cores, same cable chamber, same type of room: these are not independent failures. In the physical view (`docs/schemas/campus-physique.md`), the two fibres between CC-A and CC-B are on distinct routes (north technical gallery, south outer facade) but meet again in the cable chamber under the courtyard, so one digger cuts both. This route is an assumption.

\- \*\*Single point of failure at the access layer.\*\* Each access switch uplinks to one core. Its loss isolates the ports it serves.

\- \*\*Firewall policy errors.\*\* A mistake in the IT-OT rules is a larger risk than hardware failure. The default-deny principle and a versioned rule set limit it.

\- \*\*Addressing errors.\*\* The IP plan is checked automatically (`scripts/check\_vlans.py`), but the script does not validate IPv6 or the consistency between VLAN, zone and subnet.



\## 7. Assumptions and limits



\- Prices are the orders of magnitude provided by the course, in MAD excluding tax at 1 EUR = 10.8 MAD. They are to be replaced by quotations in a real project.

\- Horizon is 5 years. Support is 10 % of CAPEX per year. Operations is 1.5 days per device per year at 5,400 MAD a day.

\- Outage cost is assumed at 108,000 MAD per hour of lost production.

\- The device count includes the two firewalls (18 in S1, 14 in S2 and S3).

\- The firewall pair costs 216,000 MAD in all three scenarios.

\- \*\*Excluded from the costing:\*\* power and cooling, UPS, civil works and cabling infrastructure, network cards, software licences beyond vendor support, training, and decommissioning.

\- The fibre routes, technical rooms and the junction point in the cable chamber are assumptions, not a surveyed cabling plan.

\- Component availability of 99.9 % per device is the chapter's working figure, not a vendor commitment.

