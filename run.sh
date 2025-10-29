# run.sh
#!/bin/bash

# Start the backend server
echo "Starting FastAPI backend..."
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start the voice agent
echo "Starting Voice Agent..."
python -m agent.main_agent --voice

# When agent stops, also stop backend
kill $BACKEND_PID