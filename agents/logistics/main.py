import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import pubsub_v1
from concurrent.futures import ThreadPoolExecutor
import uvicorn
import threading
import time

app = FastAPI(title="LogisticsAgent", version="1.0.0")

# Pub/Sub configuration
subscriber = pubsub_v1.SubscriberClient()
project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "hackathon-project")
subscription_name = "plan-events-logistics-sub"
subscription_path = subscriber.subscription_path(project_id, subscription_name)

class LogisticsResponse(BaseModel):
    status: str
    message: str

# Global variable to track received messages
received_messages = []

def callback(message):
    """Callback function to handle received messages"""
    try:
        # Decode message
        message_data = json.loads(message.data.decode('utf-8'))
        plan_id = message_data.get('plan_id')
        destination = message_data.get('destination')
        
        # This is the key log message we need to see
        log_message = f"LogisticsAgent received plan_id: {plan_id} for destination: {destination}"
        print(log_message)
        
        # Store the message
        received_messages.append({
            "plan_id": plan_id,
            "destination": destination,
            "timestamp": time.time(),
            "log_message": log_message
        })
        
        # Acknowledge the message
        message.ack()
        
    except Exception as e:
        print(f"Error processing message: {e}")
        message.nack()

def start_subscriber():
    """Start the Pub/Sub subscriber in a separate thread"""
    try:
        print(f"Starting subscriber for: {subscription_path}")
        flow_control = pubsub_v1.types.FlowControl(max_messages=100)
        streaming_pull_future = subscriber.subscribe(
            subscription_path, 
            callback=callback,
            flow_control=flow_control
        )
        print(f"Listening for messages on {subscription_path}...")
        
        # Keep the subscriber running
        try:
            streaming_pull_future.result()
        except KeyboardInterrupt:
            streaming_pull_future.cancel()
            
    except Exception as e:
        print(f"Subscriber error: {e}")

@app.get("/")
async def health_check():
    return {
        "status": "LogisticsAgent is running", 
        "service": "logistics",
        "messages_received": len(received_messages)
    }

@app.get("/messages")
async def get_received_messages():
    return {
        "total_messages": len(received_messages),
        "messages": received_messages[-10:]  # Return last 10 messages
    }

@app.on_event("startup")
async def startup_event():
    """Start the Pub/Sub subscriber when the app starts"""
    # Start subscriber in a separate thread
    subscriber_thread = threading.Thread(target=start_subscriber, daemon=True)
    subscriber_thread.start()
    print("LogisticsAgent started with Pub/Sub subscriber")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8081))
    uvicorn.run(app, host="0.0.0.0", port=port)