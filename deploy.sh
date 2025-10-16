#!/bin/bash

# Set project variables
PROJECT_ID="hackathon-project-$(date +%s)"
REGION="us-central1"

echo "Setting up Google Cloud project: $PROJECT_ID"

# Create and set project
gcloud projects create $PROJECT_ID --name="Hackathon Multi-Agent System"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable pubsub.googleapis.com
gcloud services enable aiplatform.googleapis.com

# Create Pub/Sub topic and subscription
echo "Creating Pub/Sub resources..."
gcloud pubsub topics create plan-events
gcloud pubsub subscriptions create plan-events-logistics-sub --topic=plan-events

# Build and deploy PlannerAgent
echo "Building and deploying PlannerAgent..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/planner-agent agents/planner/

gcloud run deploy planner-agent \
  --image gcr.io/$PROJECT_ID/planner-agent \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID \
  --port 8080

# Build and deploy LogisticsAgent
echo "Building and deploying LogisticsAgent..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/logistics-agent agents/logistics/

gcloud run deploy logistics-agent \
  --image gcr.io/$PROJECT_ID/logistics-agent \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID \
  --port 8081

# Get service URLs
echo "Getting service URLs..."
PLANNER_URL=$(gcloud run services describe planner-agent --region=$REGION --format="value(status.url)")
LOGISTICS_URL=$(gcloud run services describe logistics-agent --region=$REGION --format="value(status.url)")

echo "Deployment complete!"
echo "PlannerAgent URL: $PLANNER_URL"
echo "LogisticsAgent URL: $LOGISTICS_URL"

# Test the services
echo "Testing PlannerAgent..."
curl -X POST "$PLANNER_URL/create-plan" \
  -H "Content-Type: application/json" \
  -d '{"destination": "Paris"}'

echo ""
echo "Waiting 10 seconds for message processing..."
sleep 10

echo "Checking LogisticsAgent messages..."
curl "$LOGISTICS_URL/messages"