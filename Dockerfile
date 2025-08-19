# Multi-stage Dockerfile for HARSHALADOBE Application
FROM node:18-alpine AS frontend-builder

# Set working directory for frontend
WORKDIR /app/frontend

# Copy frontend package files
COPY HARSHALADOBE/package*.json ./

# Install frontend dependencies
RUN npm ci --only=production

# Copy frontend source code
COPY HARSHALADOBE/src ./src
COPY HARSHALADOBE/public ./public
COPY HARSHALADOBE/index.html ./
COPY HARSHALADOBE/vite.config.ts ./
COPY HARSHALADOBE/tsconfig*.json ./
COPY HARSHALADOBE/tailwind.config.ts ./
COPY HARSHALADOBE/postcss.config.js ./

# Build frontend
RUN npm run build

# Python backend stage
FROM python:3.11-slim AS backend-builder

# Set working directory for backend
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY HARSHALADOBE/backend/requirements.txt ./harshaladobe-requirements.txt
COPY adobev4/requirements.txt ./adobev4-requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r harshaladobe-requirements.txt
RUN pip install --no-cache-dir -r adobev4-requirements.txt

# Copy backend source code
COPY HARSHALADOBE/backend ./harshaladobe-backend
COPY adobev4 ./adobev4-backend

# Final stage
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend source code
COPY --from=backend-builder /app/harshaladobe-backend ./harshaladobe-backend
COPY --from=backend-builder /app/adobev4-backend ./adobev4-backend

# Copy frontend build
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Create necessary directories
RUN mkdir -p /app/harshaladobe-backend/audio_cache
RUN mkdir -p /app/harshaladobe-backend/uploads
RUN mkdir -p /app/harshaladobe-backend/documents
RUN mkdir -p /app/adobev4-backend/audio
RUN mkdir -p /app/adobev4-backend/documents
RUN mkdir -p /app/adobev4-backend/index

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting HARSHALADOBE Backend..."\n\
cd /app/harshaladobe-backend\n\
python main.py &\n\
HARSHALADOBE_PID=$!\n\
\n\
echo "Starting AdobeV4 Backend..."\n\
cd /app/adobev4-backend\n\
python run_server.py &\n\
ADOBEV4_PID=$!\n\
\n\
echo "Starting Frontend..."\n\
cd /app/frontend\n\
npx serve -s dist -l 3000 &\n\
FRONTEND_PID=$!\n\
\n\
echo "All services started!"\n\
echo "Frontend: http://localhost:3000"\n\
echo "HARSHALADOBE Backend: http://localhost:8000"\n\
echo "AdobeV4 Backend: http://localhost:8080"\n\
\n\
# Wait for all processes\n\
wait $HARSHALADOBE_PID $ADOBEV4_PID $FRONTEND_PID\n\
' > /app/start.sh && chmod +x /app/start.sh

# Install serve for frontend
RUN npm install -g serve

# Expose ports
EXPOSE 3000 8000 8080

# Set environment variables
ENV PYTHONPATH=/app/harshaladobe-backend:/app/adobev4-backend
ENV NODE_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Start all services
CMD ["/app/start.sh"]
