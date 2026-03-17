#!/usr/bin/env python3
"""
Contractor Karma Platform - Seed Data Generator

Generates realistic mock data for development and testing.
Covers Bengaluru wards: Bellandur (150), Jayanagar (168), BTM Layout (176).

Usage:
    cd platform
    python3 seed/generate_seed.py
"""

import json
import os
import random
import copy
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TODAY = datetime(2026, 3, 17)
BASE_DIR = Path(__file__).resolve().parent.parent / "data"

ZONES = {
    "mahadevapura": {
        "zoneId": "blr-mhd",
        "zoneName": "Mahadevapura",
        "wards": ["150-bellandur"],
    },
    "south": {
        "zoneId": "blr-sth",
        "zoneName": "South",
        "wards": ["168-jayanagar", "176-btm-layout"],
    },
}

# Realistic Bellandur-area road names (25)
BELLANDUR_ROADS = [
    ("7th Cross, Green Glen Layout", ["7th Cross Green Glen"], "ward", "asphalt", 0.45, 7.5),
    ("3rd Main, Green Glen Layout", ["3rd Main Green Glen"], "ward", "asphalt", 0.62, 7.0),
    ("Main Road, Kaikondrahalli", ["Kaikondrahalli Main Road"], "collector", "asphalt", 1.20, 10.0),
    ("1st Cross, Kaikondrahalli", ["1st Cross Kaikondrahalli"], "ward", "asphalt", 0.30, 6.0),
    ("Kasavanahalli Main Road", ["Kasavanahalli Road"], "collector", "concrete", 1.80, 12.0),
    ("2nd Cross, Kasavanahalli", ["2nd Cross Kasavanahalli"], "ward", "asphalt", 0.35, 6.5),
    ("Haralur Road", ["Haralur Main Road"], "arterial", "asphalt", 2.50, 15.0),
    ("4th Cross, Haralur Layout", ["4th Cross Haralur"], "ward", "asphalt", 0.28, 6.0),
    ("Junnasandra Main Road", ["Junnasandra Road"], "collector", "asphalt", 1.10, 10.0),
    ("5th Cross, Junnasandra", ["5th Cross Junnasandra"], "ward", "asphalt", 0.32, 6.0),
    ("Sarjapur Road (Bellandur stretch)", ["Sarjapur Road Bellandur"], "arterial", "whitetopping", 3.20, 18.0),
    ("Inner Ring Road Service Road (Bellandur)", ["IRR Service Road Bellandur"], "arterial", "asphalt", 1.50, 12.0),
    ("6th Main, Dollar Colony, Bellandur", ["6th Main Dollar Colony"], "ward", "asphalt", 0.40, 7.0),
    ("2nd Cross, Ambalipura", ["2nd Cross Ambalipura"], "ward", "asphalt", 0.25, 6.0),
    ("Ambalipura Main Road", ["Ambalipura Road"], "collector", "asphalt", 0.90, 9.0),
    ("8th Main, Panathur Layout", ["8th Main Panathur"], "ward", "asphalt", 0.55, 7.5),
    ("Panathur Main Road", ["Panathur Road"], "collector", "concrete", 1.60, 12.0),
    ("1st Cross, Devarabisanahalli", ["1st Cross Devarabisanahalli"], "ward", "asphalt", 0.22, 6.0),
    ("Devarabisanahalli Main Road", ["Devarabisanahalli Road"], "collector", "asphalt", 1.05, 10.0),
    ("3rd Cross, Bellandur Gate", ["3rd Cross Bellandur Gate"], "ward", "asphalt", 0.38, 7.0),
    ("Bellandur Gate Main Road", ["Bellandur Gate Road"], "collector", "asphalt", 0.95, 9.5),
    ("12th Main, Vignan Nagar Extension", ["12th Main Vignan Nagar Ext"], "ward", "asphalt", 0.48, 7.0),
    ("Yemalur Road", ["Yemalur Main Road"], "collector", "asphalt", 1.30, 10.0),
    ("2nd Cross, Iblur Village", ["2nd Cross Iblur"], "ward", "asphalt", 0.33, 6.5),
    ("Iblur Main Road", ["Iblur Road"], "collector", "asphalt", 0.85, 9.0),
]

JAYANAGAR_ROADS = [
    ("30th Cross, Jayanagar 4th Block", ["30th Cross 4th Block JN"], "ward", "asphalt", 0.50, 9.0),
    ("11th Main, Jayanagar 3rd Block", ["11th Main 3rd Block JN"], "collector", "concrete", 1.10, 12.0),
    ("9th Cross, Jayanagar 5th Block", ["9th Cross 5th Block JN"], "ward", "asphalt", 0.40, 7.5),
    ("33rd Cross, Jayanagar 4th T Block", ["33rd Cross 4T Block JN"], "ward", "asphalt", 0.35, 7.0),
    ("Jayanagar Shopping Complex Road", ["JN Shopping Complex Road"], "collector", "whitetopping", 0.80, 15.0),
]

BTM_ROADS = [
    ("16th Main, BTM 2nd Stage", ["16th Main BTM 2nd Stage"], "collector", "asphalt", 1.00, 10.0),
    ("1st Cross, BTM 1st Stage", ["1st Cross BTM 1st Stage"], "ward", "asphalt", 0.30, 6.5),
    ("Udupi Garden Road, BTM Layout", ["Udupi Garden Road BTM"], "ward", "asphalt", 0.45, 7.0),
    ("Tavarekere Main Road", ["Tavarekere Road"], "collector", "concrete", 1.40, 12.0),
    ("14th Cross, BTM 2nd Stage", ["14th Cross BTM 2nd Stage"], "ward", "asphalt", 0.38, 7.0),
]

# 8 contractors
CONTRACTORS_DEF = [
    ("ctr-001", "M/s Srinivasa Constructions", "BBMP/CR/2019/456", "Class I",
     "No. 42, Industrial Area, Peenya, Bengaluru"),
    ("ctr-002", "M/s ABC Infra Pvt Ltd", "BBMP/CR/2018/203", "Class I",
     "No. 18, Rajajinagar Industrial Estate, Bengaluru"),
    ("ctr-003", "M/s Kaveri Road Builders", "BBMP/CR/2020/312", "Class II",
     "No. 7, Vijayanagar, Bengaluru"),
    ("ctr-004", "M/s Nandi Infrastructure", "BBMP/CR/2017/089", "Class I",
     "No. 55, Koramangala 4th Block, Bengaluru"),
    ("ctr-005", "M/s South City Engineers", "BBMP/CR/2021/445", "Class II",
     "No. 23, Jayanagar 9th Block, Bengaluru"),
    ("ctr-006", "M/s Metro Roads & Bridges", "BBMP/CR/2016/178", "Class I",
     "No. 101, Whitefield Main Road, Bengaluru"),
    ("ctr-007", "M/s Lakshmi Civil Works", "BBMP/CR/2022/511", "Class III",
     "No. 3, Bannerghatta Road, Bengaluru"),
    ("ctr-008", "M/s Deccan Roadways", "BBMP/CR/2019/290", "Class II",
     "No. 64, Hebbal Industrial Area, Bengaluru"),
]

# 15 officials spread across wards
OFFICIALS_ALL = [
    {"officialId": "off-001", "name": "Ramesh K", "designation": "AE",
     "department": "BBMP Engineering", "zone": "Mahadevapura", "wardNumbers": [150],
     "phone": "+91 80 2266 0001", "email": "ramesh.k@bbmp.gov.in", "activeSince": "2019-04-01"},
    {"officialId": "off-002", "name": "Suresh M", "designation": "AEE",
     "department": "BBMP Engineering", "zone": "Mahadevapura", "wardNumbers": [150],
     "phone": "+91 80 2266 0002", "email": "suresh.m@bbmp.gov.in", "activeSince": "2018-06-15"},
    {"officialId": "off-003", "name": "Vijay N", "designation": "EE",
     "department": "BBMP Engineering", "zone": "Mahadevapura", "wardNumbers": [150],
     "phone": "+91 80 2266 0003", "email": "vijay.n@bbmp.gov.in", "activeSince": "2017-01-10"},
    {"officialId": "off-004", "name": "Priya S", "designation": "AE",
     "department": "BBMP Engineering", "zone": "Mahadevapura", "wardNumbers": [150],
     "phone": "+91 80 2266 0004", "email": "priya.s@bbmp.gov.in", "activeSince": "2021-08-20"},
    {"officialId": "off-005", "name": "Anand R", "designation": "JE",
     "department": "BBMP Engineering", "zone": "Mahadevapura", "wardNumbers": [150],
     "phone": "+91 80 2266 0005", "email": "anand.r@bbmp.gov.in", "activeSince": "2022-03-01"},
    {"officialId": "off-006", "name": "Meena T", "designation": "SE",
     "department": "BBMP Engineering", "zone": "Mahadevapura", "wardNumbers": [150],
     "phone": "+91 80 2266 0006", "email": "meena.t@bbmp.gov.in", "activeSince": "2015-11-01"},
    {"officialId": "off-007", "name": "Karthik V", "designation": "AE",
     "department": "BBMP Engineering", "zone": "South", "wardNumbers": [168],
     "phone": "+91 80 2266 0007", "email": "karthik.v@bbmp.gov.in", "activeSince": "2020-01-15"},
    {"officialId": "off-008", "name": "Lakshmi D", "designation": "AEE",
     "department": "BBMP Engineering", "zone": "South", "wardNumbers": [168],
     "phone": "+91 80 2266 0008", "email": "lakshmi.d@bbmp.gov.in", "activeSince": "2019-07-01"},
    {"officialId": "off-009", "name": "Harish B", "designation": "EE",
     "department": "BBMP Engineering", "zone": "South", "wardNumbers": [168, 176],
     "phone": "+91 80 2266 0009", "email": "harish.b@bbmp.gov.in", "activeSince": "2016-05-20"},
    {"officialId": "off-010", "name": "Divya P", "designation": "AE",
     "department": "BBMP Engineering", "zone": "South", "wardNumbers": [176],
     "phone": "+91 80 2266 0010", "email": "divya.p@bbmp.gov.in", "activeSince": "2021-02-10"},
    {"officialId": "off-011", "name": "Mohan G", "designation": "AEE",
     "department": "BBMP Engineering", "zone": "South", "wardNumbers": [176],
     "phone": "+91 80 2266 0011", "email": "mohan.g@bbmp.gov.in", "activeSince": "2018-09-01"},
    {"officialId": "off-012", "name": "Shantha R", "designation": "JE",
     "department": "BBMP Engineering", "zone": "Mahadevapura", "wardNumbers": [150],
     "phone": "+91 80 2266 0012", "email": "shantha.r@bbmp.gov.in", "activeSince": "2023-01-05"},
    {"officialId": "off-013", "name": "Naveen J", "designation": "JE",
     "department": "BBMP Engineering", "zone": "South", "wardNumbers": [168],
     "phone": "+91 80 2266 0013", "email": "naveen.j@bbmp.gov.in", "activeSince": "2022-11-15"},
    {"officialId": "off-014", "name": "Rekha H", "designation": "SE",
     "department": "BBMP Engineering", "zone": "South", "wardNumbers": [168, 176],
     "phone": "+91 80 2266 0014", "email": "rekha.h@bbmp.gov.in", "activeSince": "2014-08-01"},
    {"officialId": "off-015", "name": "Ganesh L", "designation": "JE",
     "department": "BBMP Engineering", "zone": "South", "wardNumbers": [176],
     "phone": "+91 80 2266 0015", "email": "ganesh.l@bbmp.gov.in", "activeSince": "2023-06-01"},
]

# Ward center coordinates for generating road lat/lng
WARD_CENTERS = {
    150: (12.94, 77.665),     # Bellandur
    168: (12.93, 77.585),     # Jayanagar
    176: (12.9175, 77.6125),  # BTM Layout
}

# Bounding boxes for distributing road points (lat_min, lat_max, lng_min, lng_max)
WARD_BOUNDS = {
    150: (12.925, 12.955, 77.650, 77.680),
    168: (12.920, 12.940, 77.575, 77.595),
    176: (12.905, 12.930, 77.600, 77.625),
}

WORK_TYPES = ["asphalting", "concretePaving", "whitetopping", "potholeFilling",
              "drainRepair", "footpathConstruction", "resurfacing"]

FUNDING_SOURCES = ["wardDevelopment", "sfc14", "sfc15", "crf", "mlaGrant", "mpGrant"]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ensureDir(path):
    """Create directory if it does not exist."""
    os.makedirs(path, exist_ok=True)


def writeJson(relPath, data):
    """Write JSON to BASE_DIR / relPath."""
    fullPath = BASE_DIR / relPath
    ensureDir(fullPath.parent)
    with open(fullPath, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"  wrote {fullPath}")


def dlpYears(surfaceType):
    """Return DLP duration in years based on surface type."""
    if surfaceType == "whitetopping":
        return 10
    if surfaceType == "concrete":
        return 5
    return 3


def dlpStatus(endDate):
    """Compute DLP traffic-light status."""
    if endDate is None:
        return "unknown"
    end = datetime.strptime(endDate, "%Y-%m-%d") if isinstance(endDate, str) else endDate
    if end < TODAY:
        return "expired"
    if end < TODAY + timedelta(days=180):
        return "expiringSoon"
    return "active"


def randomDate(startYear, endYear):
    """Return a random date between Jan 1 of startYear and Dec 31 of endYear."""
    start = datetime(startYear, 1, 1)
    end = datetime(endYear, 12, 31)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def formatDate(dt):
    return dt.strftime("%Y-%m-%d")


def costPerKm(sanctioned, lengthKm):
    if lengthKm and lengthKm > 0:
        return round(sanctioned / lengthKm)
    return 0


def makeOfficials(wardNumber, zone):
    """Return officials for a ward in the nested Official type format."""
    result = []
    for o in OFFICIALS_ALL:
        if wardNumber not in o["wardNumbers"]:
            continue
        result.append({
            "officialId": o["officialId"],
            "designation": f"{o['designation']}, {o['department']}",
            "currentHolder": {
                "name": o["name"],
                "officialPhone": o["phone"],
                "officialEmail": o["email"],
                "verifiedDate": formatDate(TODAY),
            },
            "history": [{
                "name": o["name"],
                "tenureStart": o["activeSince"],
                "tenureEnd": None,
            }],
            "jurisdiction": f"Ward {wardNumber}, {zone} Zone",
        })
    return result


def certifyingTeam(wardNumber, zone):
    """Pick 3 officials as certifying team for a work."""
    pool = makeOfficials(wardNumber, zone)
    ae = [o for o in pool if o["designation"] == "AE"]
    aee = [o for o in pool if o["designation"] == "AEE"]
    ee = [o for o in pool if o["designation"] in ("EE", "SE")]
    team = []
    if ae:
        picked = random.choice(ae)
        team.append({"name": picked["name"], "designation": picked["designation"],
                      "role": "recordingOfficer"})
    if aee:
        picked = random.choice(aee)
        team.append({"name": picked["name"], "designation": picked["designation"],
                      "role": "checkMeasurement"})
    if ee:
        picked = random.choice(ee)
        team.append({"name": picked["name"], "designation": picked["designation"],
                      "role": "superintending"})
    return team


# ---------------------------------------------------------------------------
# Work generation
# ---------------------------------------------------------------------------

class WorkGenerator:
    """Generates works for a ward, tracking sequence numbers."""

    def __init__(self, wardNumber, zonePrefix, roads, contractorPool, zone):
        self.wardNumber = wardNumber
        self.zonePrefix = zonePrefix
        self.roads = roads
        self.contractorPool = contractorPool
        self.zone = zone
        self.seq = 0
        self.works = []
        self.rtiSeq = 0

    def nextJobCode(self, year):
        self.seq += 1
        return f"{self.wardNumber}-{year % 100:02d}-{self.seq:06d}"

    def nextRtiId(self):
        self.rtiSeq += 1
        return f"KA-RTI-2026-{self.rtiSeq:03d}"

    def generateWork(self, roadIdx, year, workType=None, forceDelay=False,
                     forceMissing=False, costMultiplier=1.0,
                     forceContractor=None):
        road = self.roads[roadIdx]
        roadId = road["roadId"]
        roadName = road["roadName"]
        lengthKm = road["lengthKm"]
        surfaceType = road["surfaceType"]

        if workType is None:
            if surfaceType == "whitetopping":
                workType = "whitetopping"
            elif surfaceType == "concrete":
                workType = "concretePaving"
            else:
                workType = random.choice(["asphalting", "resurfacing", "potholeFilling"])

        ctr = forceContractor or random.choice(self.contractorPool)

        # Costs -- realistic ranges per km
        baseCostPerKm = {
            "asphalting": random.randint(3000000, 5000000),
            "resurfacing": random.randint(2500000, 4500000),
            "concretePaving": random.randint(6000000, 9000000),
            "whitetopping": random.randint(10000000, 15000000),
            "potholeFilling": random.randint(500000, 1500000),
            "drainRepair": random.randint(2000000, 4000000),
            "footpathConstruction": random.randint(3000000, 6000000),
        }
        rawCost = int(baseCostPerKm.get(workType, 3500000) * lengthKm * costMultiplier)
        sanctioned = rawCost
        actualPaid = int(sanctioned * random.uniform(0.88, 1.02))

        woDate = randomDate(year, year)
        commDate = woDate + timedelta(days=random.randint(10, 30))
        stipDays = random.randint(60, 180)
        stipEnd = commDate + timedelta(days=stipDays)

        if forceDelay:
            delayDays = random.randint(60, 360)
            actualEnd = stipEnd + timedelta(days=delayDays)
        else:
            jitter = random.randint(-10, 30)
            actualEnd = stipEnd + timedelta(days=jitter)

        dlpDur = dlpYears(surfaceType)
        dlpStart = actualEnd
        dlpEnd = actualEnd + timedelta(days=dlpDur * 365)

        # Determine red flags
        redFlags = []
        if actualEnd > stipEnd + timedelta(days=30):
            redFlags.append("delayed")
        if costMultiplier > 1.4:
            redFlags.append("costOutlier")
        if forceMissing:
            redFlags.append("missingFields")

        bidCount = random.randint(1, 7)
        if bidCount == 1:
            redFlags.append("singleBid")

        jobCode = self.nextJobCode(year)
        tenderNum = f"{self.zonePrefix}/T/{year}/{random.randint(1, 300):03d}"
        woNum = f"{self.zonePrefix}/EE/WO/{year}/{random.randint(1, 300):03d}"

        perfGuarantee = int(sanctioned * 0.05)

        work = {
            "jobCode": jobCode,
            "roadId": roadId,
            "description": f"{workType.replace('concretePaving','Concrete paving of').replace('asphalting','Asphalting of').replace('resurfacing','Resurfacing of').replace('whitetopping','White-topping of').replace('potholeFilling','Pothole filling on').replace('drainRepair','Drain repair along').replace('footpathConstruction','Footpath construction on')} {roadName}",
            "workType": workType,
            "contractorId": ctr[0],
            "contractorName": ctr[1],
            "woNumber": woNum,
            "woDate": formatDate(woDate),
            "sanctionedCost": sanctioned,
            "actualPaid": actualPaid if not forceMissing else None,
            "tenderNumber": tenderNum,
            "bidCount": bidCount,
            "commencementDate": formatDate(commDate),
            "stipulatedCompletionDate": formatDate(stipEnd),
            "actualCompletionDate": formatDate(actualEnd) if not forceMissing else None,
            "fundingSource": random.choice(FUNDING_SOURCES),
            "dlpStartDate": formatDate(dlpStart) if not forceMissing else None,
            "dlpEndDate": formatDate(dlpEnd) if not forceMissing else None,
            "dlpDurationYears": dlpDur,
            "dlpStatus": dlpStatus(dlpEnd) if not forceMissing else "unknown",
            "certifyingOfficials": certifyingTeam(self.wardNumber, self.zone),
            "performanceGuarantee": perfGuarantee,
            "costPerKm": costPerKm(sanctioned, lengthKm),
            "redFlags": redFlags,
            "dataSource": {
                "rtiId": self.nextRtiId(),
                "responseDate": formatDate(
                    randomDate(2025, 2026)) if random.random() > 0.3 else None,
            },
        }
        self.works.append(work)
        return work


# ---------------------------------------------------------------------------
# Build roads list
# ---------------------------------------------------------------------------

def buildRoads(roadDefs, zoneId, wardSlug):
    """Convert road definitions into road objects with lat/lng coordinates."""
    wardNumber = int(wardSlug.split("-")[0])
    bounds = WARD_BOUNDS.get(wardNumber)
    roads = []
    for i, (name, aliases, cls, surface, length, width) in enumerate(roadDefs):
        roadId = f"{zoneId}-{wardSlug.split('-')[0]}-{i + 1:03d}"
        # Distribute points within the ward bounding box
        if bounds:
            latMin, latMax, lngMin, lngMax = bounds
            lat = round(latMin + (latMax - latMin) * ((i * 7 + 3) % len(roadDefs)) / len(roadDefs), 6)
            lng = round(lngMin + (lngMax - lngMin) * ((i * 11 + 5) % len(roadDefs)) / len(roadDefs), 6)
        else:
            lat = None
            lng = None
        roads.append({
            "roadId": roadId,
            "roadName": name,
            "aliases": aliases,
            "roadClass": cls,
            "surfaceType": surface,
            "lengthKm": length,
            "widthM": width,
            "osmWayId": None,
            "currentDlpStatus": None,   # filled later
            "currentDlpEnd": None,       # filled later
            "currentContractor": None,   # filled later
            "totalWorksCount": 0,        # filled later
            "totalSpending": 0,          # filled later
            "lat": lat,
            "lng": lng,
            "lastUpdated": formatDate(TODAY),
        })
    return roads


# ---------------------------------------------------------------------------
# Main generation logic
# ---------------------------------------------------------------------------

def generate():
    random.seed(42)  # reproducible

    allWorks = {}       # wardSlug -> list of works
    allRoads = {}       # wardSlug -> list of roads
    contractorWorks = {c[0]: [] for c in CONTRACTORS_DEF}

    # -----------------------------------------------------------------------
    # 1. Bellandur ward (150)
    # -----------------------------------------------------------------------
    wardSlug = "150-bellandur"
    zoneId = "blr-mhd"
    zonePrefix = "MHD"
    wardNumber = 150
    zone = "Mahadevapura"

    roads150 = buildRoads(BELLANDUR_ROADS, zoneId, wardSlug)
    allRoads[wardSlug] = roads150

    gen = WorkGenerator(wardNumber, zonePrefix, roads150, CONTRACTORS_DEF, zone)

    # -- Generate 50 works across 25 roads --
    # Every road gets at least 1 work; some get 2-3

    # Scenario: repeat failure on road index 2 (Kaikondrahalli Main Road)
    # First work in 2021 by ctr-002, completed early 2022
    gen.generateWork(2, 2021, workType="asphalting", forceContractor=CONTRACTORS_DEF[1])
    # Second work in 2023 on same road by ctr-002 (re-done within 18 months)
    gen.generateWork(2, 2023, workType="resurfacing", forceContractor=CONTRACTORS_DEF[1])

    # Scenario: cost outlier on road index 6 (Haralur Road)
    gen.generateWork(6, 2022, workType="asphalting", costMultiplier=1.8,
                     forceContractor=CONTRACTORS_DEF[5])

    # Scenario: delayed work on road index 10 (Sarjapur Road)
    gen.generateWork(10, 2020, workType="whitetopping", forceDelay=True,
                     forceContractor=CONTRACTORS_DEF[3])
    # Another work on Sarjapur
    gen.generateWork(10, 2024, workType="whitetopping",
                     forceContractor=CONTRACTORS_DEF[3])

    # Scenario: missing fields on road index 17 (1st Cross Devarabisanahalli)
    gen.generateWork(17, 2023, workType="asphalting", forceMissing=True,
                     forceContractor=CONTRACTORS_DEF[6])

    # Road index 4 (Kasavanahalli Main Road) - concrete, 2 works
    gen.generateWork(4, 2019, workType="concretePaving",
                     forceContractor=CONTRACTORS_DEF[0])
    gen.generateWork(4, 2024, workType="concretePaving",
                     forceContractor=CONTRACTORS_DEF[3])

    # Road index 16 (Panathur Main Road) - concrete, delayed
    gen.generateWork(16, 2021, workType="concretePaving", forceDelay=True,
                     forceContractor=CONTRACTORS_DEF[1])

    # Road index 11 (IRR Service Road) - 2 works
    gen.generateWork(11, 2020, workType="asphalting",
                     forceContractor=CONTRACTORS_DEF[5])
    gen.generateWork(11, 2024, workType="resurfacing",
                     forceContractor=CONTRACTORS_DEF[0])

    # Road index 22 (Yemalur Road) - 2 works
    gen.generateWork(22, 2019, workType="asphalting",
                     forceContractor=CONTRACTORS_DEF[2])
    gen.generateWork(22, 2023, workType="asphalting",
                     forceContractor=CONTRACTORS_DEF[2])

    # Road index 0 (7th Cross Green Glen) - 3 works spanning history
    gen.generateWork(0, 2018, workType="potholeFilling",
                     forceContractor=CONTRACTORS_DEF[6])
    gen.generateWork(0, 2021, workType="asphalting",
                     forceContractor=CONTRACTORS_DEF[0])
    gen.generateWork(0, 2024, workType="resurfacing",
                     forceContractor=CONTRACTORS_DEF[0])

    # Road index 8 (Junnasandra Main Road) - 2 works, one delayed
    gen.generateWork(8, 2020, workType="asphalting", forceDelay=True,
                     forceContractor=CONTRACTORS_DEF[7])
    gen.generateWork(8, 2024, workType="asphalting",
                     forceContractor=CONTRACTORS_DEF[0])

    # Road index 1 (3rd Main Green Glen) - delayed
    gen.generateWork(1, 2022, workType="asphalting", forceDelay=True,
                     forceContractor=CONTRACTORS_DEF[1])

    # Road index 14 (Ambalipura Main Road) - 2 works
    gen.generateWork(14, 2019, workType="asphalting",
                     forceContractor=CONTRACTORS_DEF[4])
    gen.generateWork(14, 2023, workType="asphalting",
                     forceContractor=CONTRACTORS_DEF[4])

    # Remaining roads: at least 1 work each
    roadsWithWorks = {0, 1, 2, 4, 6, 8, 10, 11, 14, 16, 17, 22}
    remainingIdxs = [i for i in range(25) if i not in roadsWithWorks]
    ctrsForRemaining = [CONTRACTORS_DEF[i % 8] for i in range(len(remainingIdxs))]

    for idx, ctrDef in zip(remainingIdxs, ctrsForRemaining):
        year = random.choice([2019, 2020, 2021, 2022, 2023, 2024, 2025])
        delayed = random.random() < 0.2
        gen.generateWork(idx, year, forceDelay=delayed, forceContractor=ctrDef)

    # Add a few more works to push toward 50-60 total
    extraPairs = [
        (3, 2023, CONTRACTORS_DEF[2]),
        (5, 2024, CONTRACTORS_DEF[3]),
        (7, 2022, CONTRACTORS_DEF[7]),
        (9, 2021, CONTRACTORS_DEF[4]),
        (12, 2023, CONTRACTORS_DEF[6]),
        (13, 2024, CONTRACTORS_DEF[5]),
        (15, 2022, CONTRACTORS_DEF[0]),
        (18, 2020, CONTRACTORS_DEF[2]),
        (19, 2024, CONTRACTORS_DEF[7]),
        (20, 2021, CONTRACTORS_DEF[4]),
        (21, 2023, CONTRACTORS_DEF[3]),
        (23, 2024, CONTRACTORS_DEF[6]),
        (24, 2022, CONTRACTORS_DEF[5]),
    ]
    for rIdx, yr, ctr in extraPairs:
        delayed = random.random() < 0.25
        gen.generateWork(rIdx, yr, forceDelay=delayed, forceContractor=ctr)

    # Additional works to reach ~60
    moreExtra = [
        (6, 2025, CONTRACTORS_DEF[0]),   # Haralur Road second work
        (7, 2025, CONTRACTORS_DEF[3]),
        (9, 2024, CONTRACTORS_DEF[2]),
        (12, 2025, CONTRACTORS_DEF[0]),
        (15, 2024, CONTRACTORS_DEF[4]),
        (20, 2024, CONTRACTORS_DEF[7]),
        (24, 2025, CONTRACTORS_DEF[3]),
    ]
    for rIdx, yr, ctr in moreExtra:
        gen.generateWork(rIdx, yr, forceContractor=ctr)

    allWorks[wardSlug] = gen.works

    # -----------------------------------------------------------------------
    # 2. Jayanagar ward (168)
    # -----------------------------------------------------------------------
    wardSlug168 = "168-jayanagar"
    roads168 = buildRoads(JAYANAGAR_ROADS, "blr-sth", wardSlug168)
    allRoads[wardSlug168] = roads168
    gen168 = WorkGenerator(168, "STH", roads168, CONTRACTORS_DEF[3:7], "South")

    for i in range(5):
        yr = random.choice([2021, 2022, 2023, 2024])
        gen168.generateWork(i, yr, forceContractor=CONTRACTORS_DEF[3 + (i % 4)])
    # One extra delayed work
    gen168.generateWork(1, 2024, workType="concretePaving", forceDelay=True,
                        forceContractor=CONTRACTORS_DEF[4])

    allWorks[wardSlug168] = gen168.works

    # -----------------------------------------------------------------------
    # 3. BTM Layout ward (176)
    # -----------------------------------------------------------------------
    wardSlug176 = "176-btm-layout"
    roads176 = buildRoads(BTM_ROADS, "blr-sth", wardSlug176)
    allRoads[wardSlug176] = roads176
    gen176 = WorkGenerator(176, "STH", roads176, CONTRACTORS_DEF[4:8], "South")

    for i in range(5):
        yr = random.choice([2020, 2021, 2022, 2023])
        gen176.generateWork(i, yr, forceContractor=CONTRACTORS_DEF[4 + (i % 4)])
    # One extra cost outlier
    gen176.generateWork(3, 2024, workType="concretePaving", costMultiplier=1.6,
                        forceContractor=CONTRACTORS_DEF[7])

    allWorks[wardSlug176] = gen176.works

    # -----------------------------------------------------------------------
    # Post-process: update road summaries from works
    # -----------------------------------------------------------------------
    for wardSlug, roads in allRoads.items():
        works = allWorks[wardSlug]
        for road in roads:
            roadWorks = [w for w in works if w["roadId"] == road["roadId"]]
            road["totalWorksCount"] = len(roadWorks)
            road["totalSpending"] = sum(w["sanctionedCost"] for w in roadWorks)
            if roadWorks:
                # Find latest work to set current DLP info
                dated = [w for w in roadWorks if w["dlpEndDate"]]
                if dated:
                    latest = max(dated, key=lambda w: w["dlpEndDate"])
                    road["currentDlpEnd"] = latest["dlpEndDate"]
                    road["currentDlpStatus"] = latest["dlpStatus"]
                    road["currentContractor"] = latest["contractorName"]
                else:
                    road["currentDlpStatus"] = "unknown"

    # -----------------------------------------------------------------------
    # Build contractor stats
    # -----------------------------------------------------------------------
    for wardSlug, works in allWorks.items():
        for w in works:
            cid = w["contractorId"]
            if cid in contractorWorks:
                contractorWorks[cid].append(w)

    contractors = []
    for cDef in CONTRACTORS_DEF:
        cid = cDef[0]
        cWorks = contractorWorks[cid]
        totalSanctioned = sum(w["sanctionedCost"] for w in cWorks)
        onTime = sum(1 for w in cWorks
                     if w["actualCompletionDate"] and w["stipulatedCompletionDate"]
                     and w["actualCompletionDate"] <= w["stipulatedCompletionDate"])
        delayed = sum(1 for w in cWorks if "delayed" in w["redFlags"])
        dlpViolations = sum(1 for w in cWorks if w["dlpStatus"] == "expired")
        wardsActive = list(set(
            w["jobCode"].split("-")[0] + "-" +
            {"150": "bellandur", "168": "jayanagar", "176": "btm-layout"}.get(
                w["jobCode"].split("-")[0], "unknown")
            for w in cWorks
        ))

        totalW = len(cWorks)
        if totalW > 0:
            score = round((onTime / totalW) * 0.5 +
                          max(0, 1 - delayed / totalW) * 0.3 +
                          max(0, 1 - dlpViolations / totalW) * 0.2, 2)
        else:
            score = 0.0

        if score >= 0.85:
            grade = "A"
        elif score >= 0.70:
            grade = "B"
        elif score >= 0.55:
            grade = "C"
        elif score >= 0.40:
            grade = "D"
        else:
            grade = "F"

        avgCpk = round(totalSanctioned / max(1, sum(
            allRoads[ws][
                next((j for j, r in enumerate(allRoads[ws])
                      if r["roadId"] == w["roadId"]), 0)
            ]["lengthKm"]
            for ws in allWorks
            for w in allWorks[ws]
            if w["contractorId"] == cid
        ))) if cWorks else 0

        # Seed phone and email for each contractor
        ctrPhone = f"+91 80 4000 {int(cid.split('-')[1]):04d}"
        ctrEmail = cDef[1].lower().replace("m/s ", "").replace(" ", "").replace(".", "")
        ctrEmail = f"info@{ctrEmail[:20]}.co.in"

        contractors.append({
            "contractorId": cid,
            "legalName": cDef[1],
            "registrationNumber": cDef[2],
            "registrationClass": cDef[3],
            "address": cDef[4],
            "phone": ctrPhone,
            "email": ctrEmail,
            "stats": {
                "totalWorks": totalW,
                "totalSanctionedValue": totalSanctioned,
                "worksCompletedOnTime": onTime,
                "worksDelayed": delayed,
                "dlpViolations": dlpViolations,
                "avgCostPerKm": avgCpk,
                "wardsActive": wardsActive,
                "performanceGrade": grade,
                "performanceScore": score,
            },
            "blacklisted": False,
            "works": [w["jobCode"] for w in cWorks],
        })

    # Force ctr-002 (ABC Infra) to be worst performer
    for c in contractors:
        if c["contractorId"] == "ctr-002":
            c["stats"]["performanceGrade"] = "D"
            c["stats"]["performanceScore"] = min(c["stats"]["performanceScore"], 0.38)
            c["stats"]["dlpViolations"] = max(c["stats"]["dlpViolations"], 4)

    # Force ctr-004 (Nandi Infrastructure) to be best performer
    for c in contractors:
        if c["contractorId"] == "ctr-004":
            c["stats"]["performanceGrade"] = "A"
            c["stats"]["performanceScore"] = max(c["stats"]["performanceScore"], 0.90)

    # -----------------------------------------------------------------------
    # Red Flags
    # -----------------------------------------------------------------------
    redFlags = []
    rfSeq = 0

    def nextRfId():
        nonlocal rfSeq
        rfSeq += 1
        return f"rf-{rfSeq:03d}"

    # Flag 1: Repeat failure on Kaikondrahalli Main Road
    bWorks = allWorks["150-bellandur"]
    kaikWorks = [w for w in bWorks if "Kaikondrahalli" in w.get("description", "")]
    if len(kaikWorks) >= 2:
        kaikWorks.sort(key=lambda w: w["woDate"])
        redFlags.append({
            "flagId": nextRfId(),
            "type": "repeatFailure",
            "severity": "high",
            "description": "Road resurfaced within 18 months of previous work",
            "roadId": kaikWorks[0]["roadId"],
            "roadName": "Main Road, Kaikondrahalli",
            "contractorId": kaikWorks[1]["contractorId"],
            "contractorName": kaikWorks[1]["contractorName"],
            "details": {
                "previousWork": kaikWorks[0]["jobCode"],
                "previousCompletion": kaikWorks[0].get("actualCompletionDate"),
                "newWork": kaikWorks[1]["jobCode"],
                "newWoDate": kaikWorks[1]["woDate"],
                "gapMonths": 17,
            },
        })

    # Flag 2: Cost outlier on Haralur Road
    haralurWorks = [w for w in bWorks if "Haralur Road" in w.get("description", "")]
    costOutliers = [w for w in haralurWorks if "costOutlier" in w["redFlags"]]
    if costOutliers:
        co = costOutliers[0]
        redFlags.append({
            "flagId": nextRfId(),
            "type": "costOutlier",
            "severity": "high",
            "description": "Sanctioned cost is 80%+ above zone average for similar road class",
            "roadId": co["roadId"],
            "roadName": "Haralur Road",
            "contractorId": co["contractorId"],
            "contractorName": co["contractorName"],
            "details": {
                "jobCode": co["jobCode"],
                "sanctionedCost": co["sanctionedCost"],
                "costPerKm": co["costPerKm"],
                "zoneAvgCostPerKm": 4200000,
                "deviationPct": 80,
            },
        })

    # Flag 3: Delayed Sarjapur Road white-topping
    srpWorks = [w for w in bWorks if "Sarjapur" in w.get("description", "")
                and "delayed" in w["redFlags"]]
    if srpWorks:
        sw = srpWorks[0]
        redFlags.append({
            "flagId": nextRfId(),
            "type": "delayedCompletion",
            "severity": "medium",
            "description": "Work completed more than 6 months past stipulated date",
            "roadId": sw["roadId"],
            "roadName": "Sarjapur Road (Bellandur stretch)",
            "contractorId": sw["contractorId"],
            "contractorName": sw["contractorName"],
            "details": {
                "jobCode": sw["jobCode"],
                "stipulatedCompletion": sw["stipulatedCompletionDate"],
                "actualCompletion": sw["actualCompletionDate"],
            },
        })

    # Flag 4: Missing fields on Devarabisanahalli
    devWorks = [w for w in bWorks if "Devarabisanahalli" in w.get("description", "")
                and "missingFields" in w["redFlags"]]
    if devWorks:
        dw = devWorks[0]
        redFlags.append({
            "flagId": nextRfId(),
            "type": "missingFields",
            "severity": "medium",
            "description": "Work record has missing actual paid amount and completion date",
            "roadId": dw["roadId"],
            "roadName": "1st Cross, Devarabisanahalli",
            "contractorId": dw["contractorId"],
            "contractorName": dw["contractorName"],
            "details": {
                "jobCode": dw["jobCode"],
                "missingFields": ["actualPaid", "actualCompletionDate", "dlpStartDate",
                                  "dlpEndDate"],
            },
        })

    # Flag 5: Single-bid works
    singleBidWorks = [w for w in bWorks if "singleBid" in w["redFlags"]]
    if singleBidWorks:
        sbw = singleBidWorks[0]
        redFlags.append({
            "flagId": nextRfId(),
            "type": "singleBid",
            "severity": "low",
            "description": "Tender received only one bid, reducing competitive pricing",
            "roadId": sbw["roadId"],
            "roadName": next(
                (r["roadName"] for r in allRoads["150-bellandur"]
                 if r["roadId"] == sbw["roadId"]), "Unknown"),
            "contractorId": sbw["contractorId"],
            "contractorName": sbw["contractorName"],
            "details": {
                "jobCode": sbw["jobCode"],
                "tenderNumber": sbw["tenderNumber"],
                "bidCount": 1,
            },
        })

    # Flag 6: Contractor performance - ctr-002
    abcCtr = next((c for c in contractors if c["contractorId"] == "ctr-002"), None)
    if abcCtr:
        redFlags.append({
            "flagId": nextRfId(),
            "type": "poorContractorPerformance",
            "severity": "high",
            "description": "Contractor has performance grade D with multiple DLP violations "
                           "and delayed works",
            "roadId": None,
            "roadName": None,
            "contractorId": "ctr-002",
            "contractorName": abcCtr["legalName"],
            "details": {
                "performanceGrade": abcCtr["stats"]["performanceGrade"],
                "performanceScore": abcCtr["stats"]["performanceScore"],
                "totalWorks": abcCtr["stats"]["totalWorks"],
                "worksDelayed": abcCtr["stats"]["worksDelayed"],
                "dlpViolations": abcCtr["stats"]["dlpViolations"],
            },
        })

    # -----------------------------------------------------------------------
    # DLP summary per ward
    # -----------------------------------------------------------------------
    def buildDlpSummary(wardSlug, works, roads):
        active = [w for w in works if w["dlpStatus"] == "active"]
        expiringSoon = [w for w in works if w["dlpStatus"] == "expiringSoon"]
        expired = [w for w in works if w["dlpStatus"] == "expired"]
        unknown = [w for w in works if w["dlpStatus"] == "unknown"]

        items = []
        for w in works:
            items.append({
                "jobCode": w["jobCode"],
                "roadId": w["roadId"],
                "roadName": next(
                    (r["roadName"] for r in roads if r["roadId"] == w["roadId"]), ""),
                "contractorId": w["contractorId"],
                "contractorName": w["contractorName"],
                "dlpStartDate": w["dlpStartDate"],
                "dlpEndDate": w["dlpEndDate"],
                "dlpDurationYears": w["dlpDurationYears"],
                "dlpStatus": w["dlpStatus"],
            })

        return {
            "wardSlug": wardSlug,
            "generatedAt": formatDate(TODAY),
            "summary": {
                "totalWorks": len(works),
                "active": len(active),
                "expiringSoon": len(expiringSoon),
                "expired": len(expired),
                "unknown": len(unknown),
            },
            "items": items,
        }

    # -----------------------------------------------------------------------
    # Write all files
    # -----------------------------------------------------------------------
    print("Generating Contractor Karma platform seed data...\n")

    # Meta
    writeJson("meta.json", {
        "platformName": "Contractor Karma",
        "version": "0.1.0",
        "description": "Transparency platform for public road works in Indian cities",
        "dataAsOf": formatDate(TODAY),
        "generatedBy": "seed/generate_seed.py",
        "cities": ["bengaluru"],
    })

    # City
    writeJson("cities/bengaluru/city.json", {
        "cityId": "bengaluru",
        "cityName": "Bengaluru",
        "state": "Karnataka",
        "municipalBody": "BBMP",
        "totalZones": 8,
        "totalWards": 243,
        "zonesAvailable": ["mahadevapura", "south"],
    })

    # Zones
    writeJson("cities/bengaluru/zones/mahadevapura/zone.json", {
        "zoneId": "blr-mhd",
        "zoneName": "Mahadevapura",
        "cityId": "bengaluru",
        "wardsCount": 16,
        "wardsAvailable": ["150-bellandur"],
    })
    writeJson("cities/bengaluru/zones/south/zone.json", {
        "zoneId": "blr-sth",
        "zoneName": "South",
        "cityId": "bengaluru",
        "wardsCount": 28,
        "wardsAvailable": ["168-jayanagar", "176-btm-layout"],
    })

    # Ward: Bellandur
    wardDir150 = "cities/bengaluru/zones/mahadevapura/wards/150-bellandur"
    writeJson(f"{wardDir150}/ward.json", {
        "wardNumber": 150,
        "wardName": "Bellandur",
        "wardSlug": "150-bellandur",
        "zoneId": "blr-mhd",
        "zoneName": "Mahadevapura",
        "cityId": "bengaluru",
        "corporator": "Not available",
        "areaKm2": 12.5,
        "populationEstimate": 150000,
        "totalRoadsTracked": len(allRoads["150-bellandur"]),
        "totalWorks": len(allWorks["150-bellandur"]),
        "totalSpending": sum(w["sanctionedCost"] for w in allWorks["150-bellandur"]),
    })
    writeJson(f"{wardDir150}/roads.json", allRoads["150-bellandur"])
    writeJson(f"{wardDir150}/works.json", allWorks["150-bellandur"])
    writeJson(f"{wardDir150}/dlp.json",
              buildDlpSummary("150-bellandur",
                              allWorks["150-bellandur"],
                              allRoads["150-bellandur"]))
    writeJson(f"{wardDir150}/officials.json",
              makeOfficials(150, "Mahadevapura"))

    # Ward: Jayanagar
    wardDir168 = "cities/bengaluru/zones/south/wards/168-jayanagar"
    writeJson(f"{wardDir168}/ward.json", {
        "wardNumber": 168,
        "wardName": "Jayanagar",
        "wardSlug": "168-jayanagar",
        "zoneId": "blr-sth",
        "zoneName": "South",
        "cityId": "bengaluru",
        "corporator": "Not available",
        "areaKm2": 4.2,
        "populationEstimate": 85000,
        "totalRoadsTracked": len(allRoads["168-jayanagar"]),
        "totalWorks": len(allWorks["168-jayanagar"]),
        "totalSpending": sum(w["sanctionedCost"] for w in allWorks["168-jayanagar"]),
    })
    writeJson(f"{wardDir168}/roads.json", allRoads["168-jayanagar"])
    writeJson(f"{wardDir168}/works.json", allWorks["168-jayanagar"])
    writeJson(f"{wardDir168}/dlp.json",
              buildDlpSummary("168-jayanagar",
                              allWorks["168-jayanagar"],
                              allRoads["168-jayanagar"]))
    writeJson(f"{wardDir168}/officials.json",
              makeOfficials(168, "South"))

    # Ward: BTM Layout
    wardDir176 = "cities/bengaluru/zones/south/wards/176-btm-layout"
    writeJson(f"{wardDir176}/ward.json", {
        "wardNumber": 176,
        "wardName": "BTM Layout",
        "wardSlug": "176-btm-layout",
        "zoneId": "blr-sth",
        "zoneName": "South",
        "cityId": "bengaluru",
        "corporator": "Not available",
        "areaKm2": 5.8,
        "populationEstimate": 120000,
        "totalRoadsTracked": len(allRoads["176-btm-layout"]),
        "totalWorks": len(allWorks["176-btm-layout"]),
        "totalSpending": sum(w["sanctionedCost"] for w in allWorks["176-btm-layout"]),
    })
    writeJson(f"{wardDir176}/roads.json", allRoads["176-btm-layout"])
    writeJson(f"{wardDir176}/works.json", allWorks["176-btm-layout"])
    writeJson(f"{wardDir176}/dlp.json",
              buildDlpSummary("176-btm-layout",
                              allWorks["176-btm-layout"],
                              allRoads["176-btm-layout"]))
    writeJson(f"{wardDir176}/officials.json",
              makeOfficials(176, "South"))

    # Contractors
    writeJson("contractors/index.json", contractors)
    for c in contractors:
        writeJson(f"contractors/{c['contractorId']}.json", c)

    # Officials
    writeJson("officials/index.json", OFFICIALS_ALL)

    # Red Flags
    writeJson("red-flags/flags.json", {
        "generatedAt": formatDate(TODAY),
        "totalFlags": len(redFlags),
        "flags": redFlags,
    })

    # Stats: summary
    allWorksFlat = []
    for ws in allWorks.values():
        allWorksFlat.extend(ws)

    totalSanctioned = sum(w["sanctionedCost"] for w in allWorksFlat)
    totalPaid = sum(w["actualPaid"] for w in allWorksFlat if w["actualPaid"])
    totalRoads = sum(len(r) for r in allRoads.values())
    totalDelayed = sum(1 for w in allWorksFlat if "delayed" in w["redFlags"])
    totalActive = sum(1 for w in allWorksFlat if w["dlpStatus"] == "active")
    totalExpired = sum(1 for w in allWorksFlat if w["dlpStatus"] == "expired")
    totalExpiringSoon = sum(1 for w in allWorksFlat if w["dlpStatus"] == "expiringSoon")

    writeJson("stats/summary.json", {
        "generatedAt": formatDate(TODAY),
        "totalCities": 1,
        "totalZones": 2,
        "totalWards": 3,
        "totalRoads": totalRoads,
        "totalWorks": len(allWorksFlat),
        "totalContractors": len(contractors),
        "totalOfficials": len(OFFICIALS_ALL),
        "financials": {
            "totalSanctionedCost": totalSanctioned,
            "totalActualPaid": totalPaid,
            "avgCostPerWork": round(totalSanctioned / max(1, len(allWorksFlat))),
        },
        "dlp": {
            "active": totalActive,
            "expiringSoon": totalExpiringSoon,
            "expired": totalExpired,
        },
        "performance": {
            "worksDelayed": totalDelayed,
            "delayPercentage": round(totalDelayed / max(1, len(allWorksFlat)) * 100, 1),
            "redFlagsTotal": len(redFlags),
        },
    })

    # Stats: ward rankings
    wardRankings = []
    for wardSlug in allWorks:
        ws = allWorks[wardSlug]
        rs = allRoads[wardSlug]
        wardName = wardSlug.split("-", 1)[1].replace("-", " ").title()
        wardNum = int(wardSlug.split("-")[0])
        totalS = sum(w["sanctionedCost"] for w in ws)
        delayedW = sum(1 for w in ws if "delayed" in w["redFlags"])
        flagCount = sum(1 for f in redFlags
                        if f.get("roadId") and
                        any(r["roadId"] == f["roadId"] for r in rs))
        wardRankings.append({
            "wardSlug": wardSlug,
            "wardName": wardName,
            "wardNumber": wardNum,
            "totalRoads": len(rs),
            "totalWorks": len(ws),
            "totalSpending": totalS,
            "worksDelayed": delayedW,
            "redFlagCount": flagCount,
            "transparencyScore": round(
                max(0.3, 1.0 - (delayedW / max(1, len(ws))) * 0.5 -
                    flagCount * 0.05), 2),
        })
    wardRankings.sort(key=lambda x: x["transparencyScore"], reverse=True)
    writeJson("stats/ward-rankings.json", {
        "generatedAt": formatDate(TODAY),
        "rankings": wardRankings,
    })

    # Stats: contractor rankings
    contractorRankings = sorted(
        [
            {
                "contractorId": c["contractorId"],
                "legalName": c["legalName"],
                "performanceGrade": c["stats"]["performanceGrade"],
                "performanceScore": c["stats"]["performanceScore"],
                "totalWorks": c["stats"]["totalWorks"],
                "worksDelayed": c["stats"]["worksDelayed"],
                "dlpViolations": c["stats"]["dlpViolations"],
                "totalSanctionedValue": c["stats"]["totalSanctionedValue"],
            }
            for c in contractors
        ],
        key=lambda x: x["performanceScore"],
        reverse=True,
    )
    writeJson("stats/contractor-rankings.json", {
        "generatedAt": formatDate(TODAY),
        "rankings": contractorRankings,
    })

    # Search index
    searchEntries = []
    for wardSlug, roads in allRoads.items():
        for r in roads:
            searchEntries.append({
                "type": "road",
                "id": r["roadId"],
                "label": r["roadName"],
                "aliases": r["aliases"],
                "ward": wardSlug,
            })
    for ws in allWorks.values():
        for w in ws:
            searchEntries.append({
                "type": "work",
                "id": w["jobCode"],
                "label": w["description"],
                "ward": w["jobCode"].split("-")[0] + "-" +
                        {"150": "bellandur", "168": "jayanagar",
                         "176": "btm-layout"}.get(w["jobCode"].split("-")[0], "unknown"),
            })
    for c in contractors:
        searchEntries.append({
            "type": "contractor",
            "id": c["contractorId"],
            "label": c["legalName"],
        })
    writeJson("search/index.json", {
        "generatedAt": formatDate(TODAY),
        "totalEntries": len(searchEntries),
        "entries": searchEntries,
    })

    # RTI applications
    rtiApps = [
        {
            "rtiId": "KA-RTI-2026-001",
            "filedDate": "2026-01-15",
            "authority": "BBMP Chief Engineer",
            "subject": "Details of road works in Ward 150 (Bellandur) from 2020-2025",
            "status": "responseReceived",
            "responseDate": "2026-02-14",
            "worksDisclosed": 45,
            "firstAppealFiled": False,
        },
        {
            "rtiId": "KA-RTI-2026-002",
            "filedDate": "2026-02-01",
            "authority": "BBMP Executive Engineer, Mahadevapura",
            "subject": "Contractor-wise expenditure and DLP details for Bellandur ward roads",
            "status": "responseReceived",
            "responseDate": "2026-03-01",
            "worksDisclosed": 30,
            "firstAppealFiled": False,
        },
        {
            "rtiId": "KA-RTI-2026-003",
            "filedDate": "2026-02-20",
            "authority": "BBMP Executive Engineer, South Zone",
            "subject": "Road works details for Jayanagar and BTM Layout wards 2020-2025",
            "status": "partialResponse",
            "responseDate": "2026-03-15",
            "worksDisclosed": 8,
            "firstAppealFiled": True,
        },
        {
            "rtiId": "KA-RTI-2025-018",
            "filedDate": "2025-06-10",
            "authority": "BBMP Commissioner",
            "subject": "White-topping project details on Sarjapur Road",
            "status": "responseReceived",
            "responseDate": "2025-07-09",
            "worksDisclosed": 2,
            "firstAppealFiled": False,
        },
        {
            "rtiId": "KA-RTI-2025-022",
            "filedDate": "2025-09-05",
            "authority": "BBMP Chief Engineer",
            "subject": "DLP compliance report for Mahadevapura zone 2018-2024",
            "status": "noResponse",
            "responseDate": None,
            "worksDisclosed": 0,
            "firstAppealFiled": True,
        },
    ]
    writeJson("rti/applications.json", {
        "generatedAt": formatDate(TODAY),
        "totalApplications": len(rtiApps),
        "applications": rtiApps,
    })

    # GeoJSON - simplified ward boundary polygons (approximate centroids with rectangles)
    wardGeos = [
        {
            "type": "Feature",
            "properties": {
                "wardNumber": 150,
                "wardName": "Bellandur",
                "wardSlug": "150-bellandur",
                "zone": "Mahadevapura",
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [77.6500, 12.9250],
                    [77.6800, 12.9250],
                    [77.6800, 12.9550],
                    [77.6500, 12.9550],
                    [77.6500, 12.9250],
                ]],
            },
        },
        {
            "type": "Feature",
            "properties": {
                "wardNumber": 168,
                "wardName": "Jayanagar",
                "wardSlug": "168-jayanagar",
                "zone": "South",
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [77.5750, 12.9200],
                    [77.5950, 12.9200],
                    [77.5950, 12.9400],
                    [77.5750, 12.9400],
                    [77.5750, 12.9200],
                ]],
            },
        },
        {
            "type": "Feature",
            "properties": {
                "wardNumber": 176,
                "wardName": "BTM Layout",
                "wardSlug": "176-btm-layout",
                "zone": "South",
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [77.6000, 12.9050],
                    [77.6250, 12.9050],
                    [77.6250, 12.9300],
                    [77.6000, 12.9300],
                    [77.6000, 12.9050],
                ]],
            },
        },
    ]
    writeJson("geo/bengaluru-wards.geojson", {
        "type": "FeatureCollection",
        "features": wardGeos,
    })

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print(f"\nDone! Generated:")
    print(f"  Roads:       {totalRoads}")
    print(f"  Works:       {len(allWorksFlat)}")
    print(f"  Contractors: {len(contractors)}")
    print(f"  Officials:   {len(OFFICIALS_ALL)}")
    print(f"  Red flags:   {len(redFlags)}")
    print(f"  RTI apps:    {len(rtiApps)}")
    print(f"  Total spend: Rs {totalSanctioned:,.0f}")


if __name__ == "__main__":
    generate()
