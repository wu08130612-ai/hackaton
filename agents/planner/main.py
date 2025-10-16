import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from google.cloud import pubsub_v1
import uvicorn

app = FastAPI(title="PlannerAgent", version="1.0.0")

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Pub/Sub configuration
publisher = pubsub_v1.PublisherClient()
project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "hackathon-project")
topic_name = "plan-events"
topic_path = publisher.topic_path(project_id, topic_name)

class PlanRequest(BaseModel):
    destination: str = "Paris"

class PlanResponse(BaseModel):
    plan_id: str
    destination: str
    description: str
    status: str

@app.get("/")
async def health_check():
    return {"status": "PlannerAgent is running", "service": "planner"}

@app.post("/create-plan", response_model=PlanResponse)
async def create_plan(request: PlanRequest = PlanRequest()):
    try:
        # Generate hardcoded plan
        plan_id = "123"
        destination = request.destination
        
        # Get Gemini description for the destination
        prompt = f"Write a brief, exciting description for {destination} as a travel destination in one sentence."
        try:
            response = model.generate_content(prompt)
            description = response.text.strip()
        except Exception as e:
            description = f"Beautiful destination: {destination}"
            print(f"Gemini API error: {e}")
        
        # Create plan data
        plan_data = {
            "plan_id": plan_id,
            "destination": destination,
            "description": description,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        # Publish to Pub/Sub instead of returning directly
        message_data = json.dumps(plan_data).encode('utf-8')
        future = publisher.publish(topic_path, message_data)
        message_id = future.result()
        
        print(f"Published plan to Pub/Sub: {message_id}")
        
        return PlanResponse(
            plan_id=plan_id,
            destination=destination,
            description=description,
            status=f"Plan published to Pub/Sub with message ID: {message_id}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating plan: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)