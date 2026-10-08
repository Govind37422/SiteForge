# Use multi-stage build for front & back end
# Stage 1: Build React Frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend .
RUN npm run build

# Stage 2: Build Python Backend
FROM python:3.11-slim
WORKDIR /app/backend

# Copy python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "uvicorn[standard]" gunicorn

# Copy backend source
COPY backend .

# Copy compiled frontend from Stage 1
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Expose port
EXPOSE 8000

# Set production environment variables
ENV NODE_ENV=production
ENV PYTHONUNBUFFERED=1

# Start Gunicorn server with Uvicorn workers
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
