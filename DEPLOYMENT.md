# AI Education Agent - Deployment Guide

## 🚀 Production Deployment

This guide covers deploying the AI Education Agent system for government schools in a production environment.

## 🏗️ Infrastructure Requirements

### Minimum Production Setup
- **Application Server**: 8GB RAM, 4 CPU cores, 100GB SSD
- **Database Server**: 16GB RAM, 4 CPU cores, 200GB SSD
- **Load Balancer**: 4GB RAM, 2 CPU cores
- **Backup Storage**: 500GB for data backups

### Recommended Production Setup
- **Application Servers**: 2x (16GB RAM, 8 CPU cores, 200GB SSD)
- **Database Server**: 32GB RAM, 8 CPU cores, 500GB SSD with replication
- **Redis Cluster**: 3x (8GB RAM, 2 CPU cores)
- **Load Balancer**: HA setup with failover

## 🔧 Deployment Options

### Option 1: Docker Swarm (Recommended for Government Infrastructure)

#### 1. Initialize Swarm
```bash
# On manager node
docker swarm init --advertise-addr <MANAGER-IP>

# On worker nodes
docker swarm join --token <TOKEN> <MANAGER-IP>:2377
```

#### 2. Deploy Stack
```bash
# Create production environment file
cp .env.example .env.production

# Deploy the stack
docker stack deploy -c docker-compose.prod.yml ai-education
```

#### 3. Scale Services
```bash
# Scale backend services
docker service scale ai-education_backend=3

# Scale frontend services
docker service scale ai-education_frontend=2
```

### Option 2: Kubernetes Deployment

#### 1. Create Namespace
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ai-education
```

#### 2. Deploy Database
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: ai-education
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        env:
        - name: POSTGRES_DB
          value: ai_education
        - name: POSTGRES_USER
          value: ai_user
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi
```

#### 3. Deploy Application
```bash
kubectl apply -f k8s/
```

### Option 3: Traditional Server Deployment

#### 1. Server Setup (Ubuntu 20.04)
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Nginx
sudo apt install nginx -y

# Install SSL certificates (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx -y
```

#### 2. SSL Configuration
```bash
# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

#### 3. Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API Documentation
    location /docs {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 Security Configuration

### 1. Environment Variables
```bash
# Production environment file (.env.production)
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=<generate-strong-secret-key>
DATABASE_URL=postgresql://ai_user:<strong-password>@db-server:5432/ai_education
OPENAI_API_KEY=<your-openai-key>

# Security headers
SECURE_SSL_REDIRECT=true
SECURE_HSTS_SECONDS=31536000
SECURE_CONTENT_TYPE_NOSNIFF=true
SECURE_BROWSER_XSS_FILTER=true
```

### 2. Database Security
```sql
-- Create dedicated database user
CREATE USER ai_app_user WITH PASSWORD '<strong-password>';
GRANT CONNECT ON DATABASE ai_education TO ai_app_user;
GRANT USAGE ON SCHEMA public TO ai_app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO ai_app_user;

-- Enable SSL
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/etc/ssl/certs/server.crt';
ALTER SYSTEM SET ssl_key_file = '/etc/ssl/private/server.key';
```

### 3. Firewall Configuration
```bash
# UFW firewall setup
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 📊 Monitoring and Logging

### 1. Application Monitoring
```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana

  node-exporter:
    image: prom/node-exporter
    ports:
      - "9100:9100"

volumes:
  grafana-storage:
```

### 2. Log Management
```bash
# Configure log rotation
sudo nano /etc/logrotate.d/ai-education

# Content:
/var/log/ai-education/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        docker-compose restart backend
    endscript
}
```

### 3. Health Checks
```bash
# Health check script
#!/bin/bash
# /usr/local/bin/health-check.sh

# Check backend health
if ! curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "Backend health check failed"
    # Send alert or restart service
    docker-compose restart backend
fi

# Check frontend health
if ! curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "Frontend health check failed"
    docker-compose restart frontend
fi

# Add to crontab
# */5 * * * * /usr/local/bin/health-check.sh
```