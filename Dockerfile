# Stage 1: Build frontend
FROM node:18-slim AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ ./
# API 走 nginx 反向代理，前端用相对路径
ENV VITE_API_URL=/api/v1
RUN npm run build

# Stage 2: Final image
FROM python:3.11-slim
WORKDIR /app

# Install nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy frontend build
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

# Nginx config
RUN cat > /etc/nginx/sites-available/default << 'EOF'
server {
    listen 7860;

    # Frontend static files
    location / {
        root /app/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check
    location /health {
        proxy_pass http://127.0.0.1:8000;
    }
}
EOF

# Start script
RUN cat > /app/start.sh << 'SCRIPT'
#!/bin/bash
cd /app/backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 &
nginx -g "daemon off;"
SCRIPT
RUN chmod +x /app/start.sh

EXPOSE 7860

CMD ["/app/start.sh"]
