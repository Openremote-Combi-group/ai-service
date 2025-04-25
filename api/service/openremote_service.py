import json


class OpenRemoteService:
    def fetch_assets(self):
        return json.loads("""
    [{
  "id": "71F157uBwTR2WI9xMB7PwX",
  "version": 4,
  "createdOn": 1744878843597,
  "name": "Fontys R10",
  "accessPublicRead": false,
  "parentId": "56SzD7ckLvgQe8WAXDe5uE",
  "realm": "master",
  "type": "BuildingAsset",
  "path": [
    "56SzD7ckLvgQe8WAXDe5uE",
    "71F157uBwTR2WI9xMB7PwX"
  ],
  "attributes": {
    "area": {
      "name": "area",
      "type": "positiveInteger",
      "meta": {
        "ruleState": true
      },
      "value": 20,
      "timestamp": 1744879288866
    },
    "country": {
      "name": "country",
      "type": "text",
      "meta": {},
      "value": "Netherlands",
      "timestamp": 1744879240113
    },
    "notes": {
      "name": "notes",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878843595
    },
    "city": {
      "name": "city",
      "type": "text",
      "meta": {},
      "value": "Eindhoven",
      "timestamp": 1744879235088
    },
    "street": {
      "name": "street",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878843595
    },
    "postalCode": {
      "name": "postalCode",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878843595
    },
    "model": {
      "name": "model",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744879257359
    },
    "location": {
      "name": "location",
      "type": "GEO_JSONPoint",
      "meta": {},
      "value": null,
      "timestamp": 1744878843595
    }
  }
},
{
  "id": "6lDPL8mEyissE1cLzxz5Zr",
  "version": 3,
  "createdOn": 1744878834634,
  "name": "Fontys TQ",
  "accessPublicRead": false,
  "parentId": "56SzD7ckLvgQe8WAXDe5uE",
  "realm": "master",
  "type": "BuildingAsset",
  "path": [
    "56SzD7ckLvgQe8WAXDe5uE",
    "6lDPL8mEyissE1cLzxz5Zr"
  ],
  "attributes": {
    "area": {
      "name": "area",
      "type": "positiveInteger",
      "meta": {
        "ruleState": true
      },
      "value": 10,
      "timestamp": 1744879341122
    },
    "country": {
      "name": "country",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878834623
    },
    "notes": {
      "name": "notes",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878834623
    },
    "city": {
      "name": "city",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878834623
    },
    "street": {
      "name": "street",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878834623
    },
    "postalCode": {
      "name": "postalCode",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878834623
    },
    "location": {
      "name": "location",
      "type": "GEO_JSONPoint",
      "meta": {},
      "value": null,
      "timestamp": 1744878834623
    }
  }
},
{
  "id": "56SzD7ckLvgQe8WAXDe5uE",
  "version": 2,
  "createdOn": 1744878993725,
  "name": "Eindhoven",
  "accessPublicRead": false,
  "realm": "master",
  "type": "CityAsset",
  "path": [
    "56SzD7ckLvgQe8WAXDe5uE"
  ],
  "attributes": {
    "country": {
      "name": "country",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878993716
    },
    "notes": {
      "name": "notes",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878993716
    },
    "total_area": {
      "name": "total_area",
      "type": "integer",
      "meta": {
        "ruleState": true
      },
      "value": 30,
      "timestamp": 1744879415190
    },
    "location": {
      "name": "location",
      "type": "GEO_JSONPoint",
      "meta": {},
      "value": null,
      "timestamp": 1744878993716
    }
  }
}]
    """)