import google.generativeai as genai
import json
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def break_into_scenes(scenario, comedy_beat):
    prompt = f"""
Break this comedy scenario into 6 short scenes (each 8-10 seconds) for a silent puppy video.

Scenario: {scenario}
Comedy beat: {comedy_beat}

The character is "Buster" - a clumsy golden retriever puppy who causes chaos accidentally.

For each scene, provide:
1. What happens (simple action)
2. The comedy moment

Format as:
SCENE 1: [action] → [comedy moment]
SCENE 2: [action] → [comedy moment]
...
SCENE 6: [action] → [comedy moment]
"""
    response = model.generate_content(prompt)
    return response.text

def process_all_scenarios():
    with open('daily_scenarios.json', 'r') as f:
        daily = json.load(f)
    
    for video in daily['videos']:
        print(f"Processing: {video['scenario']}")
        scenes = break_into_scenes(video['scenario'], video['comedy_beat'])
        video['scenes'] = scenes
        print(f"  ✅ Generated 6 scenes")
    
    with open('scenes_output.json', 'w') as f:
        json.dump(daily, f, indent=2)
    
    print("✅ All scenarios broken into scenes")

if __name__ == "__main__":
    process_all_scenarios()
