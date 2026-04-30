import json
import random
from datetime import datetime

def load_scenarios():
    with open('comedy_scenarios.json', 'r') as f:
        return json.load(f)['scenarios']

def select_daily_scenarios():
    scenarios = load_scenarios()
    # Select 15 random scenarios for daily videos
    selected = random.sample(scenarios, min(15, len(scenarios)))
    
    output = {
        "date": datetime.now().isoformat(),
        "videos": []
    }
    
    for i, scenario in enumerate(selected):
        output["videos"].append({
            "video_id": f"buster_{datetime.now().strftime('%Y%m%d')}_{i+1:03d}",
            "category": scenario['category'],
            "scenario": scenario['scenario'],
            "comedy_beat": scenario['comedy_beat']
        })
    
    with open('daily_scenarios.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ Selected {len(selected)} scenarios for today")
    return output

if __name__ == "__main__":
    select_daily_scenarios()
