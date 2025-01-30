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

def send_inference_image(
    file_path: str,
    filename: str,
    content_type: str,
    trainerId: int,
    modelKey: str,
    prediction: str,
    clientKey: str,
    imageKey: str
):
    nest_url = f"{settings.trainer_node_service_url}/inference"

    data = {
        "trainerId": trainerId,
        "modelKey": modelKey,
        "predictedCategoryName": prediction,
        "clientKey": clientKey,
        "imageKey": imageKey
    }
    headers = {
        "Authorization": f"Bearer {settings.jwt_token}"
    }
    try:
        with httpx.Client(timeout=10.0) as client:
            with open(file_path, "rb") as f:
                files = {
                    "image": (filename, f, content_type)
                }
                response = client.post(nest_url, data=data, files=files, headers=headers)
                response.raise_for_status()
    except Exception as e:
        print(f"Failed to send image to Nest API: {e}")