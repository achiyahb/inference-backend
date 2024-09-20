import httpx
from app.config import settings

model_data_cache = {}

async def fetch_model_data(hmacHex: str):
    try:
        if hmacHex in model_data_cache:
            return model_data_cache[hmacHex]
        
        trainer_service_url = f"{settings.trainer_node_service_url}/cars/model"
        print("Fetching trainer data", trainer_service_url)
        headers = {
            "Authorization": f"Bearer {settings.jwt_token}"
        }
        response = httpx.get(trainer_service_url, headers=headers, params={"hmacHex": hmacHex})
        response.raise_for_status()
        json = response.json()
        model_data_cache[hmacHex] = json
        return json
    except httpx.HTTPStatusError as e:
        print(f"HTTP error while fetching trainer data: {e}")
    except Exception as e:
        print(f"Error fetching trainer data: {e}")