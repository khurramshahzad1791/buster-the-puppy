import requests
import json
import time
import os
from PIL import Image

LEONARDO_API_KEY = os.environ["LEONARDO_API_KEY"]
LEONARDO_URL = "https://cloud.leonardo.ai/api/rest/v1/generations"

with open('character_prompts.json', 'r') as f:
    CHARACTER = json.load(f)

def generate_scene_image(video_id, scene_num, action_description):
    prompt = f"""{CHARACTER['visual_prompt_base']}, {action_description}, {CHARACTER['comedy_style']}, cinematic, bright, funny, high quality, 4K"""
    
    payload = {
        "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",
        "prompt": prompt,
        "negative_prompt": "text, watermark, signature, blurry, dark, scary, sad, violent",
        "width": 1024,
        "height": 576,
        "num_images": 1,
        "contrastRatio": 1.0,
        "public": False
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {LEONARDO_API_KEY}"
    }
    
    response = requests.post(LEONARDO_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        generation_id = response.json()["sdGenerationJob"]["generationId"]
        return generation_id
    return None

def check_generation(generation_id):
    url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
    headers = {"authorization": f"Bearer {LEONARDO_API_KEY}"}
    
    for _ in range(30):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data["generations_by_pk"]["status"] == "COMPLETE":
                return data["generations_by_pk"]["generated_images"][0]["url"]
        time.sleep(2)
    return None

def main():
    with open('scenes_output.json', 'r') as f:
        data = json.load(f)
    
    os.makedirs("images", exist_ok=True)
    
    for video in data['videos'][:5]:  # Start with 5 videos/day
        print(f"🎨 Generating images for: {video['scenario']}")
        video['image_urls'] = []
        
        scenes_text = video['scenes'].split('\n')
        for i, scene_text in enumerate(scenes_text[:6]):
            if scene_text.strip():
                print(f"  Scene {i+1}/6...")
                gen_id = generate_scene_image(video['video_id'], i+1, scene_text)
                if gen_id:
                    url = check_generation(gen_id)
                    if url:
                        video['image_urls'].append(url)
                        print(f"    ✅ Image {i+1} generated")
    
    with open('images_output.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("✅ All images generated")

if __name__ == "__main__":
    main()
