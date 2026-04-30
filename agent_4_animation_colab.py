# Copy this entire cell into Google Colab (free GPU runtime)

"""
# Buster the Puppy - Animation Agent
# Run this on Colab with GPU enabled

!pip install diffusers transformers accelerate torch torchvision xformers imageio imageio-ffmpeg

import torch
from diffusers import MotionAdapter, DiffusionPipeline
from diffusers.utils import export_to_video
import json
import requests
from PIL import Image
import io
import os

# Load AnimateDiff
adapter = MotionAdapter.from_pretrained("guoyww/animatediff-motion-adapter-v1-5-2")
pipe = DiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    motion_adapter=adapter,
    torch_dtype=torch.float16
).to("cuda")

# Enable memory optimization
pipe.enable_vae_slicing()
pipe.enable_model_cpu_offload()

def download_image(url):
    response = requests.get(url)
    return Image.open(io.BytesIO(response.content)).convert("RGB")

def animate_scene(image, action_description, output_path):
    motion_prompt = f"{action_description}, subtle natural movement, cartoon animation"
    
    frames = pipe(
        prompt=motion_prompt,
        image=image,
        num_frames=16,
        guidance_scale=7.5,
        num_inference_steps=25,
    ).frames[0]
    
    export_to_video(frames, output_path, fps=6)
    return output_path

# Load image URLs
with open('images_output.json', 'r') as f:
    data = json.load(f)

os.makedirs("animated_clips", exist_ok=True)

for video in data['videos']:
    print(f"🎬 Animating: {video['scenario']}")
    
    scenes_text = video['scenes'].split('\n')
    for i, (scene_text, image_url) in enumerate(zip(scenes_text[:6], video.get('image_urls', []))):
        if image_url:
            print(f"  Scene {i+1}/6...")
            
            # Download and animate
            image = download_image(image_url)
            output_path = f"animated_clips/{video['video_id']}_scene_{i}.mp4"
            animate_scene(image, scene_text, output_path)
            print(f"    ✅ Animated scene {i+1}")

print("✅ All scenes animated!")
"""
