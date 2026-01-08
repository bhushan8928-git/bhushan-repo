from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")


class Place(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    name: str
    description: str
    image: str
    price: str
    rating: float
    location: dict
    best_time: str
    duration: str

class Country(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    name: str
    description: str
    hero_image: str
    places: List[Place]


@api_router.get("/")
async def root():
    return {"message": "Travel Recommendation API"}

@api_router.get("/countries", response_model=List[Country])
async def get_countries():
    countries = await db.countries.find({}, {"_id": 0}).to_list(100)
    return countries

@api_router.get("/countries/{country_id}", response_model=Country)
async def get_country(country_id: str):
    country = await db.countries.find_one({"id": country_id}, {"_id": 0})
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

@api_router.get("/places", response_model=List[Place])
async def get_all_places():
    places = []
    countries = await db.countries.find({}, {"_id": 0}).to_list(100)
    for country in countries:
        places.extend(country.get('places', []))
    return places

@api_router.get("/places/{place_id}", response_model=Place)
async def get_place(place_id: str):
    countries = await db.countries.find({}, {"_id": 0}).to_list(100)
    for country in countries:
        for place in country.get('places', []):
            if place['id'] == place_id:
                return place
    raise HTTPException(status_code=404, detail="Place not found")

@api_router.post("/seed")
async def seed_data():
    await db.countries.delete_many({})
    
    countries_data = [
        {
            "id": "india",
            "name": "India",
            "description": "Experience the vibrant colors, rich heritage, and diverse landscapes of incredible India.",
            "hero_image": "https://images.unsplash.com/photo-1665849863716-b527b5e9ed62?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDN8MHwxfHNlYXJjaHwxfHxJbmRpYSUyMFRhaSUyME1haGFsJTIwc3Vuc2V0fGVufDB8fHx8MTc2Nzg4NDY5N3ww&ixlib=rb-4.1.0&q=85",
            "places": [
                {
                    "id": "taj-mahal",
                    "name": "Taj Mahal",
                    "description": "An ivory-white marble mausoleum, one of the Seven Wonders of the World. Built by Mughal emperor Shah Jahan in memory of his wife Mumtaz Mahal.",
                    "image": "https://images.unsplash.com/photo-1619947494583-29fc109e01d7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDN8MHwxfHNlYXJjaHwzfHxJbmRpYSUyMFRhaSUyME1haGFsJTIwc3Vuc2V0fGVufDB8fHx8MTc2Nzg4NDY5N3ww&ixlib=rb-4.1.0&q=85",
                    "price": "$1,200 - $2,000",
                    "rating": 4.9,
                    "location": {"lat": 27.1751, "lng": 78.0421},
                    "best_time": "October to March",
                    "duration": "3-4 days"
                },
                {
                    "id": "kerala-backwaters",
                    "name": "Kerala Backwaters",
                    "description": "A network of interconnected canals, rivers, and lakes. Experience serene houseboat cruises through lush green landscapes.",
                    "image": "https://images.unsplash.com/photo-1707893013488-51672ef83425?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwxfHxJbmRpYSUyMEtlcmFsYSUyMEJhY2t3YXRlcnMlMjBob3VzZWJvYXR8ZW58MHx8fHwxNzY3ODg0NzI2fDA&ixlib=rb-4.1.0&q=85",
                    "price": "$800 - $1,500",
                    "rating": 4.8,
                    "location": {"lat": 9.4981, "lng": 76.3388},
                    "best_time": "November to February",
                    "duration": "2-3 days"
                },
                {
                    "id": "jaipur",
                    "name": "Jaipur - Pink City",
                    "description": "Discover magnificent forts, palaces, and vibrant bazaars in Rajasthan's capital city known for its pink-colored architecture.",
                    "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800",
                    "price": "$900 - $1,600",
                    "rating": 4.7,
                    "location": {"lat": 26.9124, "lng": 75.7873},
                    "best_time": "November to February",
                    "duration": "2-3 days"
                },
                {
                    "id": "goa",
                    "name": "Goa Beaches",
                    "description": "Pristine beaches, Portuguese heritage, vibrant nightlife, and water sports on India's west coast.",
                    "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800",
                    "price": "$700 - $1,300",
                    "rating": 4.6,
                    "location": {"lat": 15.2993, "lng": 74.1240},
                    "best_time": "November to March",
                    "duration": "3-5 days"
                },
                {
                    "id": "varanasi",
                    "name": "Varanasi",
                    "description": "One of the oldest living cities in the world. Spiritual center on the banks of the Ganges River with ancient temples.",
                    "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=800",
                    "price": "$600 - $1,200",
                    "rating": 4.7,
                    "location": {"lat": 25.3176, "lng": 82.9739},
                    "best_time": "October to March",
                    "duration": "2-3 days"
                }
            ]
        },
        {
            "id": "japan",
            "name": "Japan",
            "description": "Discover the perfect blend of ancient traditions and cutting-edge technology in the Land of the Rising Sun.",
            "hero_image": "https://images.unsplash.com/photo-1723708489553-655d04168d39?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwxfHxKYXBhbiUyME1vdW50JTIwRnVqaSUyMGNoZXJyeSUyMGJsb3Nzb21zfGVufDB8fHx8MTc2Nzg4NDcwMXww&ixlib=rb-4.1.0&q=85",
            "places": [
                {
                    "id": "mount-fuji",
                    "name": "Mount Fuji",
                    "description": "Japan's iconic snow-capped volcano. Sacred mountain offering breathtaking views and hiking trails.",
                    "image": "https://images.unsplash.com/photo-1682768029347-0425b90fa196?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwyfHxKYXBhbiUyME1vdW50JTIwRnVqaSUyMGNoZXJyeSUyMGJsb3Nzb21zfGVufDB8fHx8MTc2Nzg4NDcwMXww&ixlib=rb-4.1.0&q=85",
                    "price": "$2,500 - $3,500",
                    "rating": 4.9,
                    "location": {"lat": 35.3606, "lng": 138.7274},
                    "best_time": "July to September",
                    "duration": "2-3 days"
                },
                {
                    "id": "kyoto-bamboo",
                    "name": "Kyoto Bamboo Forest",
                    "description": "Walk through towering bamboo groves in Arashiyama. Experience tranquility and ancient temples.",
                    "image": "https://images.unsplash.com/photo-1670735845005-09c877eb2853?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHxKYXBhbiUyMEt5b3RvJTIwQXJhc2hpeWFtYSUyMGJhbWJvbyUyMGZvcmVzdHxlbnwwfHx8fDE3Njc4ODQ3Mjh8MA&ixlib=rb-4.1.0&q=85",
                    "price": "$2,200 - $3,200",
                    "rating": 4.8,
                    "location": {"lat": 35.0170, "lng": 135.6719},
                    "best_time": "March to May, October to November",
                    "duration": "3-4 days"
                },
                {
                    "id": "tokyo",
                    "name": "Tokyo",
                    "description": "Bustling metropolis with neon-lit streets, ancient temples, world-class dining, and pop culture.",
                    "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800",
                    "price": "$2,800 - $4,000",
                    "rating": 4.9,
                    "location": {"lat": 35.6762, "lng": 139.6503},
                    "best_time": "March to May, September to November",
                    "duration": "4-5 days"
                },
                {
                    "id": "osaka",
                    "name": "Osaka",
                    "description": "Food capital of Japan with vibrant street food culture, historic castle, and lively entertainment districts.",
                    "image": "https://images.unsplash.com/photo-1589452271712-64b8a66c7b71?w=800",
                    "price": "$2,400 - $3,400",
                    "rating": 4.7,
                    "location": {"lat": 34.6937, "lng": 135.5023},
                    "best_time": "March to May, October to November",
                    "duration": "2-3 days"
                },
                {
                    "id": "hiroshima",
                    "name": "Hiroshima",
                    "description": "Peace Memorial Park, historic significance, and nearby Miyajima Island with floating torii gate.",
                    "image": "https://images.unsplash.com/photo-1590559604828-728952f7f3e0?w=800",
                    "price": "$2,000 - $3,000",
                    "rating": 4.6,
                    "location": {"lat": 34.3853, "lng": 132.4553},
                    "best_time": "March to May, October to November",
                    "duration": "2 days"
                }
            ]
        },
        {
            "id": "italy",
            "name": "Italy",
            "description": "Indulge in world-class cuisine, Renaissance art, and stunning Mediterranean coastlines.",
            "hero_image": "https://images.unsplash.com/photo-1715527532135-80764537c278?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHwxfHxJdGFseSUyMEFtYWxmaSUyMENvYXN0JTIwc3VtbWVyfGVufDB8fHx8MTc2Nzg4NDcwMnww&ixlib=rb-4.1.0&q=85",
            "places": [
                {
                    "id": "amalfi-coast",
                    "name": "Amalfi Coast",
                    "description": "Dramatic cliffs, colorful villages, azure waters, and Mediterranean charm along southern Italy's coastline.",
                    "image": "https://images.unsplash.com/photo-1723380831227-140af7f25d11?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHwyfHxJdGFseSUyMEFtYWxmaSUyMENvYXN0JTIwc3VtbWVyfGVufDB8fHx8MTc2Nzg4NDcwMnww&ixlib=rb-4.1.0&q=85",
                    "price": "$3,000 - $4,500",
                    "rating": 4.9,
                    "location": {"lat": 40.6340, "lng": 14.6027},
                    "best_time": "April to June, September to October",
                    "duration": "4-5 days"
                },
                {
                    "id": "venice",
                    "name": "Venice Canals",
                    "description": "Romantic gondola rides through historic waterways, St. Mark's Basilica, and Renaissance architecture.",
                    "image": "https://images.unsplash.com/photo-1514232290883-98c7b611c6da?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwxfHxJdGFseSUyMFZlbmljZSUyMENhbmFscyUyMGdvbmRvbGF8ZW58MHx8fHwxNzY3ODg0NzMyfDA&ixlib=rb-4.1.0&q=85",
                    "price": "$2,800 - $4,200",
                    "rating": 4.8,
                    "location": {"lat": 45.4408, "lng": 12.3155},
                    "best_time": "April to June, September to November",
                    "duration": "2-3 days"
                },
                {
                    "id": "rome",
                    "name": "Rome",
                    "description": "Ancient ruins, Vatican City, Colosseum, and centuries of art and history in the Eternal City.",
                    "image": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800",
                    "price": "$2,500 - $3,800",
                    "rating": 4.9,
                    "location": {"lat": 41.9028, "lng": 12.4964},
                    "best_time": "April to June, September to October",
                    "duration": "3-4 days"
                },
                {
                    "id": "florence",
                    "name": "Florence",
                    "description": "Renaissance capital with world-famous art, Duomo cathedral, and Tuscan cuisine.",
                    "image": "https://images.unsplash.com/photo-1541430507676-2c4b9e9c4c5b?w=800",
                    "price": "$2,400 - $3,600",
                    "rating": 4.8,
                    "location": {"lat": 43.7696, "lng": 11.2558},
                    "best_time": "April to June, September to October",
                    "duration": "2-3 days"
                },
                {
                    "id": "cinque-terre",
                    "name": "Cinque Terre",
                    "description": "Five colorful fishing villages perched on rugged cliffs overlooking the Italian Riviera.",
                    "image": "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?w=800",
                    "price": "$2,600 - $3,800",
                    "rating": 4.7,
                    "location": {"lat": 44.1271, "lng": 9.7215},
                    "best_time": "April to June, September to October",
                    "duration": "2-3 days"
                }
            ]
        },
        {
            "id": "switzerland",
            "name": "Switzerland",
            "description": "Majestic Alps, pristine lakes, charming villages, and world-class skiing destinations.",
            "hero_image": "https://images.unsplash.com/photo-1581010098149-a042c93c4b19?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDF8MHwxfHNlYXJjaHwxfHxTd2l0emVybGFuZCUyMFplcm1hdHQlMjBNYXR0ZXJob3JuJTIwd2ludGVyfGVufDB8fHx8MTc2Nzg4NDcwM3ww&ixlib=rb-4.1.0&q=85",
            "places": [
                {
                    "id": "zermatt",
                    "name": "Zermatt",
                    "description": "Car-free alpine village at the foot of the iconic Matterhorn mountain. World-class skiing and hiking.",
                    "image": "https://images.unsplash.com/photo-1601556169285-92cfcfcf0135?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDF8MHwxfHNlYXJjaHwyfHxTd2l0emVybGFuZCUyMFplcm1hdHQlMjBNYXR0ZXJob3JuJTIwd2ludGVyfGVufDB8fHx8MTc2Nzg4NDcwM3ww&ixlib=rb-4.1.0&q=85",
                    "price": "$4,000 - $6,000",
                    "rating": 4.9,
                    "location": {"lat": 46.0207, "lng": 7.7491},
                    "best_time": "December to March, June to September",
                    "duration": "3-4 days"
                },
                {
                    "id": "lucerne",
                    "name": "Lucerne Chapel Bridge",
                    "description": "Medieval covered bridge, pristine lake, and mountain panoramas in central Switzerland.",
                    "image": "https://images.unsplash.com/photo-1646273165630-b318ac083609?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2MzR8MHwxfHNlYXJjaHwxfHxTd2l0emVybGFuZCUyMEx1Y2VybmUlMjBDaGFwZWwlMjBCcmlkZ2V8ZW58MHx8fHwxNzY3ODg0NzMzfDA&ixlib=rb-4.1.0&q=85",
                    "price": "$3,500 - $5,200",
                    "rating": 4.8,
                    "location": {"lat": 47.0502, "lng": 8.3093},
                    "best_time": "May to September",
                    "duration": "2-3 days"
                },
                {
                    "id": "interlaken",
                    "name": "Interlaken",
                    "description": "Adventure capital between two lakes. Gateway to Jungfrau region with paragliding and skiing.",
                    "image": "https://images.unsplash.com/photo-1530841377377-3ff06c0ca713?w=800",
                    "price": "$3,800 - $5,500",
                    "rating": 4.8,
                    "location": {"lat": 46.6863, "lng": 7.8632},
                    "best_time": "May to September",
                    "duration": "3-4 days"
                },
                {
                    "id": "zurich",
                    "name": "Zürich",
                    "description": "Cosmopolitan city with lake views, historic old town, luxury shopping, and vibrant culture.",
                    "image": "https://images.unsplash.com/photo-1516550893923-42d28e5677af?w=800",
                    "price": "$3,200 - $4,800",
                    "rating": 4.7,
                    "location": {"lat": 47.3769, "lng": 8.5417},
                    "best_time": "May to September",
                    "duration": "2-3 days"
                },
                {
                    "id": "geneva",
                    "name": "Geneva",
                    "description": "International city on Lake Geneva with Jet d'Eau fountain, UN headquarters, and French border charm.",
                    "image": "https://images.unsplash.com/photo-1562832135-14a35d25edef?w=800",
                    "price": "$3,400 - $5,000",
                    "rating": 4.6,
                    "location": {"lat": 46.2044, "lng": 6.1432},
                    "best_time": "May to September",
                    "duration": "2 days"
                }
            ]
        },
        {
            "id": "thailand",
            "name": "Thailand",
            "description": "Tropical paradise with golden temples, pristine beaches, and world-renowned cuisine.",
            "hero_image": "https://images.unsplash.com/photo-1679220567464-8d6c659a2088?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzF8MHwxfHNlYXJjaHwxfHxUaGFpbGFuZCUyMFBodWtldCUyMGJlYWNoJTIwdHVycXVvaXNlJTIwd2F0ZXJ8ZW58MHx8fHwxNzY3ODg0NzA3fDA&ixlib=rb-4.1.0&q=85",
            "places": [
                {
                    "id": "phuket",
                    "name": "Phuket",
                    "description": "Thailand's largest island with turquoise waters, limestone cliffs, beach resorts, and nightlife.",
                    "image": "https://images.unsplash.com/photo-1687500161421-13c9c0d1d1b7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzF8MHwxfHNlYXJjaHwyfHxUaGFpbGFuZCUyMFBodWtldCUyMGJlYWNoJTIwdHVycXVvaXNlJTIwd2F0ZXJ8ZW58MHx8fHwxNzY3ODg0NzA3fDA&ixlib=rb-4.1.0&q=85",
                    "price": "$1,200 - $2,200",
                    "rating": 4.7,
                    "location": {"lat": 7.8804, "lng": 98.3923},
                    "best_time": "November to April",
                    "duration": "4-5 days"
                },
                {
                    "id": "bangkok-palace",
                    "name": "Bangkok Grand Palace",
                    "description": "Opulent royal complex with golden spires, intricate temples, and the sacred Emerald Buddha.",
                    "image": "https://images.unsplash.com/photo-1678915577720-86a211239d40?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHxUaGFpbGFuZCUyMEJhbmdrb2slMjBHcmFuZCUyMFBhbGFjZXxlbnwwfHx8fDE3Njc4ODQ3MzR8MA&ixlib=rb-4.1.0&q=85",
                    "price": "$1,400 - $2,400",
                    "rating": 4.8,
                    "location": {"lat": 13.7563, "lng": 100.5018},
                    "best_time": "November to February",
                    "duration": "2-3 days"
                },
                {
                    "id": "chiang-mai",
                    "name": "Chiang Mai",
                    "description": "Ancient city in northern mountains with temples, night markets, and elephant sanctuaries.",
                    "image": "https://images.unsplash.com/photo-1598935898639-81586f7d2129?w=800",
                    "price": "$1,000 - $1,800",
                    "rating": 4.7,
                    "location": {"lat": 18.7883, "lng": 98.9853},
                    "best_time": "November to February",
                    "duration": "3-4 days"
                },
                {
                    "id": "krabi",
                    "name": "Krabi",
                    "description": "Stunning limestone karsts, emerald lagoons, island hopping, and rock climbing adventures.",
                    "image": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800",
                    "price": "$1,100 - $2,000",
                    "rating": 4.8,
                    "location": {"lat": 8.0863, "lng": 98.9063},
                    "best_time": "November to April",
                    "duration": "3-4 days"
                },
                {
                    "id": "ayutthaya",
                    "name": "Ayutthaya",
                    "description": "Ancient capital with UNESCO World Heritage temples, Buddha statues, and rich Thai history.",
                    "image": "https://images.unsplash.com/photo-1601990893748-36a2a092ab1e?w=800",
                    "price": "$900 - $1,600",
                    "rating": 4.6,
                    "location": {"lat": 14.3692, "lng": 100.5877},
                    "best_time": "November to February",
                    "duration": "1-2 days"
                }
            ]
        }
    ]
    
    await db.countries.insert_many(countries_data)
    return {"message": "Data seeded successfully", "count": len(countries_data)}


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()