"""
Configuration for media monitoring keywords and people of interest.
"""

# People to track with Thai and English name variants
PEOPLE = {
    "poonpong": {
        "name_en": "Poonpong Naiyanapakorn",
        "name_th": "พูนพงษ์ นัยนาภากรณ์",
        "role": "Director General, Department of Business Development",
        "priority": "high",
        "search_terms": ["พูนพงษ์", "Poonpong", "อธิบดีกรมพัฒนาธุรกิจการค้า"],
    },
    "narongsak": {
        "name_en": "Narongsak (CEO/Founder NC Coconut Co. Ltd.)",
        "name_th": "ณรงค์ศักดิ์",
        "role": "CEO/Founder, NC Coconut Co. Ltd.",
        "priority": "high",
        "search_terms": ["ณรงค์ศักดิ์", "Narongsak", "NC Coconut", "เอ็นซี โคโคนัท"],
    },
    "mathieu": {
        "name_en": "Mathieu Chaumont",
        "name_th": "มาติเยอ โชมงต์",
        "role": "Press Conference Participant",
        "priority": "high",
        "search_terms": ["Mathieu Chaumont", "มาติเยอ", "Chaumont"],
    },
    "chawarn": {
        "name_en": "Chawarn Khongsub",
        "name_th": "ชวาล คงทรัพย์",
        "role": "Director of Agriculture, HHT",
        "priority": "medium",
        "search_terms": ["ชวาล", "Chawarn", "Khongsub"],
    },
    "paphoppol": {
        "name_en": "Paphoppol Punnathanathai",
        "name_th": "ปภพล ปัณณธนาไท",
        "role": "Associate Director of Sourcing and Procurement, HHT",
        "priority": "medium",
        "search_terms": ["ปภพล", "Paphoppol", "Punnathanathai"],
    },
    "raveepat": {
        "name_en": "Raveepat Vattanarom",
        "name_th": "รวีพัชร์ วัฒนารมย์",
        "role": "Senior Manager of Compliance, HHT",
        "priority": "medium",
        "search_terms": ["รวีพัชร์", "Raveepat", "Vattanarom"],
    },
}

# Company/brand search terms
COMPANIES = {
    "harmless_harvest": {
        "name": "Harmless Harvest",
        "priority": "high",
        "search_terms": [
            "Harmless Harvest",
            "ฮาร์มเลส ฮาร์เวสท์",
            "Harmless Harvest Thailand",
            "HHT",
        ],
    },
    "nc_coconut": {
        "name": "NC Coconut Co. Ltd.",
        "priority": "high",
        "search_terms": ["NC Coconut", "เอ็นซี โคโคนัท"],
    },
}

# Topic-level search queries for Google News
SEARCH_QUERIES = [
    "กรมพัฒนาธุรกิจการค้า มะพร้าวน้ำหอม",
    "กรมพัฒนาธุรกิจการค้า นอมินี มะพร้าว",
    "มะพร้าวน้ำหอม ราชบุรี นอมินี",
    "Harmless Harvest Thailand",
    "Harmless Harvest มะพร้าว",
    "พูนพงษ์ มะพร้าวน้ำหอม",
    "NC Coconut มะพร้าว",
    # YouTube-specific queries
    "site:youtube.com มะพร้าวน้ำหอม",
    "site:youtube.com กรมพัฒนาธุรกิจการค้า มะพร้าว",
    "site:youtube.com นอมินี มะพร้าว",
]

# Outlets of particular interest
PRIORITY_OUTLETS = [
    "mcot.net", "pptvhd36.com", "thaipbs.or.th",
    "matichon.co.th", "prachachat.net", "thansettakij.com",
    "nextnews", "strategic-online", "youtube.com",
]
