# Deployment Guide

**Author**: Cavin Otieno  
**Contact**: [cavin.otieno012@gmail.com](mailto:cavin.otieno012@gmail.com) | **WhatsApp**: [+254708101604](https://wa.me/254708101604)

## Overview

This guide provides step-by-step instructions for deploying the Enterprise Multi-Agent System (EMAS) across multiple environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Local Development](#local-development)
4. [Docker Compose Deployment](#docker-compose-deployment)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [Production Deployment](#production-deployment)
7. [Monitoring Setup](#monitoring-setup)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

**Minimum Requirements:**
- **CPU**: 4 cores
- **Memory**: 8GB RAM
- **Storage**: 50GB SSD
- **OS**: Ubuntu 20.04+ / CentOS 8+ / Docker Desktop

**Recommended for Production:**
- **CPU**: 8+ cores
- **Memory**: 16GB+ RAM
- **Storage**: 100GB+ SSD
- **Network**: 1Gbps+

### Required Software

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install kubectl (for Kubernetes)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Helm (optional)
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install other tools
sudo apt-get update
sudo apt-get install -y git curl wget unzip htop
```

### Cloud Provider Setup (Optional)

**AWS:**
- Install AWS CLI
- Configure EKS cluster
- Set up RDS PostgreSQL
- Configure ELB/ALB

**Google Cloud:**
- Install Google Cloud SDK
- Create GKE cluster
- Set up Cloud SQL
- Configure Load Balancer

**Azure:**
- Install Azure CLI
- Create AKS cluster
- Set up Azure Database
- Configure Load Balancer

---

## Environment Setup

### 1. Clone Repository

```bash
# Clone the repository
git clone https://github.com/OumaCavin/jac-smart-learning.git
cd jac-smart-learning

# Verify repository structure
ls -la
```

### 2. Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env
cp .env.example .env.local

# Edit configuration
nano .env
```

**Required Environment Variables:**

```bash
# Database Configuration
DATABASE_URL=postgresql://emas_user:secure_password_123@localhost:5432/emas_db
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=emas_db
DATABASE_USER=emas_user
DATABASE_PASSWORD=secure_password_123

# Redis Configuration
REDIS_URL=redis://:redis_password_123@localhost:6379/0
REDIS_PASSWORD=redis_password_123

# NATS Configuration
NATS_URL=nats://localhost:4222

# Security
JWT_SECRET=your-super-secret-jwt-key-change-in-production-at-least-64-chars

# AI/LLM Integration
OPENAI_API_KEY=<OPENAI_API_KEY_PLACEHOLDER>
SUPABASE_URL=https://rjgrobamzmbcvakwltxt.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJqZ3JvYmFtem1iY3Zha3dsdHh0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM1ODc2ODQsImV4cCI6MjA3OTE2MzY4NH0.NH6i7UUor07PevpK7AMzMw7LvLP8j9wtuypfa_azip0
SUPABASE_SERVICE_ROLE=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJqZ3JvYmFtem1iY3Zha3dsdHh0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzU4NzY4NCwiZXhwIjoyMDc5MTYzNjg0fQ.5m60ck3umars1l2_Yz-BOI5URajEZoDqELkcVglv2lA

# Email Configuration
GMAIL_USER=cavin.otieno012@gmail.com
GMAIL_APP_PASSWORD=<GMAIL_APP_PASSWORD_PLACEHOLDER>

# Contact Information
EMAIL_FROM_NAME="EMAS System"
EMAIL_FROM_ADDRESS=cavin.otieno012@gmail.com
EMAIL_REPLY_TO=noreply@cavnotieno.com
```

### 3. Generate Secure Secrets

```bash
# Generate secure JWT secret
openssl rand -base64 64

# Generate database password
openssl rand -base64 32

# Generate Redis password
openssl rand -base64 32

# Generate NATS password
openssl rand -base64 32
```

---

## Local Development

### 1. Start Development Environment

```bash
# Install dependencies
npm run setup:dev

# Start development services
npm run dev

# Or use Docker Compose for development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### 2. Access Services

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432
- **Redis**: localhost:6379

### 3. Development Commands

```bash
# Run tests
npm run test

# Build for production
npm run build

# Run linting
npm run lint

# Format code
npm run format
```

---

## Docker Compose Deployment

### 1. Production Configuration

```bash
# Copy production environment
cp .env.example .env.production

# Edit production settings
nano .env.production
```

**Production Environment Settings:**
```bash
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Secure passwords for production
DATABASE_PASSWORD=<secure_production_password>
REDIS_PASSWORD=<secure_redis_password>
JWT_SECRET=<secure_jwt_secret>

# Disable development features
DEBUG_SQL=false
AUTO_RELOAD=false

# Enable monitoring
PROMETHEUS_ENABLED=true
JAEGER_ENABLED=true
LOKI_ENABLED=true
```

### 2. Deploy with Docker Compose

```bash
# Build and start all services
docker-compose -f docker-compose.yml --env-file .env.production up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f emas-backend
docker-compose logs -f emas-frontend

# Scale backend services
docker-compose up -d --scale emas-backend=3
```

### 3. Docker Compose Services

| Service | Port | Description |
|---------|------|-------------|
| postgres | 5432 | PostgreSQL database |
| redis | 6379 | Redis cache |
| nats | 4222 | NATS message bus |
| backend | 8000 | FastAPI backend |
| frontend | 3000 | React frontend |
| prometheus | 9090 | Metrics collection |
| grafana | 3001 | Visualization |
| jaeger | 16686 | Tracing |
| loki | 3100 | Log aggregation |
| vault | 8200 | Secret management |

### 4. Backup and Restore

```bash
# Create backup
docker-compose exec postgres pg_dump -U emas_user emas_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
docker-compose exec -T postgres psql -U emas_user emas_db < backup_20240115_120000.sql

# Backup Redis
docker-compose exec redis redis-cli --rdb /data/dump.rdb
docker cp emas-redis:/data/dump.rdb ./redis_backup_$(date +%Y%m%d_%H%M%S).rdb
```

---

## Kubernetes Deployment

### 1. Prerequisites for Kubernetes

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify cluster access
kubectl cluster-info
kubectl get nodes
```

### 2. Create Namespace

```bash
# Create EMAS namespace
kubectl apply -f k8s/manifests/namespace.yaml

# Set context
kubectl config set-context --current --namespace=emas
```

### 3. Deploy Database Services

```bash
# Create persistent volumes (if needed)
kubectl apply -f k8s/manifests/storage.yaml

# Deploy database services
kubectl apply -f k8s/manifests/database.yaml

# Wait for services to be ready
kubectl get pods -w
kubectl get services
```

### 4. Deploy Backend

```bash
# Build and push Docker images
docker build -t ghcr.io/oumacavin/emas-backend:latest backend/
docker push ghcr.io/oumacavin/emas-backend:latest

# Deploy backend
kubectl apply -f k8s/manifests/backend.yaml

# Check deployment
kubectl get deployments
kubectl get pods
kubectl logs -l app=emas-backend
```

### 5. Deploy Frontend

```bash
# Build and push frontend image
docker build -t ghcr.io/oumacavin/emas-frontend:latest frontend/
docker push ghcr.io/oumacavin/emas-frontend:latest

# Deploy frontend
kubectl apply -f k8s/manifests/frontend.yaml

# Check deployment
kubectl get ingress
kubectl get services
```

### 6. Configure Ingress

```bash
# Install NGINX Ingress Controller (if not already installed)
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# Apply ingress configuration
kubectl apply -f k8s/manifests/ingress.yaml

# Check ingress status
kubectl get ingress
kubectl describe ingress emas-ingress
```

### 7. Monitoring Stack

```bash
# Deploy monitoring services
kubectl apply -f k8s/manifests/monitoring/

# Check monitoring services
kubectl get pods -n monitoring
kubectl get svc -n monitoring

# Access Grafana (admin/admin)
kubectl port-forward svc/grafana 3000:3000 -n monitoring
```

### 8. Verify Deployment

```bash
# Check all services
kubectl get all

# Check ingress
kubectl get ingress

# Test API endpoint
kubectl get svc emas-backend
curl http://$(kubectl get svc emas-backend -o jsonpath='{.status.loadBalancer.ingress[0].ip}')/health

# Check application logs
kubectl logs -l app=emas-backend --tail=100
kubectl logs -l app=emas-frontend --tail=100
```

---

## Production Deployment

### 1. Cloud Provider Setup

#### AWS EKS

```bash
# Create EKS cluster
eksctl create cluster \
  --name emas-production \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type m5.large \
  --nodes 3 \
  --nodes-min 2 \
  --nodes-max 10 \
  --managed

# Configure kubectl
aws eks update-kubeconfig --region us-east-1 --name emas-production
```

#### Google GKE

```bash
# Create GKE cluster
gcloud container clusters create emas-production \
  --zone=us-central1-a \
  --num-nodes=3 \
  --machine-type=n1-standard-2 \
  --enable-autoscaling \
  --min-nodes=2 \
  --max-nodes=10 \
  --enable-autorepair

# Configure kubectl
gcloud container clusters get-credentials emas-production --zone=us-central1-a
```

#### Azure AKS

```bash
# Create resource group
az group create --name emas-rg --location eastus

# Create AKS cluster
az aks create \
  --resource-group emas-rg \
  --name emas-production \
  --node-count 3 \
  --node-vm-size Standard_D2s_v3 \
  --enable-addons monitoring \
  --generate-ssh-keys
```

### 2. SSL/TLS Configuration

#### Using cert-manager

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer
kubectl apply -f k8s/manifests/cert-manager.yaml

# Update ingress with domain
kubectl apply -f k8s/manifests/ingress.yaml
```

#### Manual SSL Setup

```bash
# Generate SSL certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=emas.cavinotieno.com"

# Create TLS secret
kubectl create secret tls emas-tls-secret \
  --key=tls.key \
  --cert=tls.crt \
  --namespace=emas
```

### 3. Database Setup

#### AWS RDS

```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier emas-production-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15.3 \
  --master-username emas_user \
  --master-user-password <secure_password> \
  --allocated-storage 20 \
  --storage-type gp2 \
  --vpc-security-group-ids sg-12345678

# Wait for instance to be available
aws rds wait db-instance-available --db-instance-identifier emas-production-db
```

#### Google Cloud SQL

```bash
# Create Cloud SQL instance
gcloud sql instances create emas-production-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --storage-type=SSD \
  --storage-size=10GB

# Create database and user
gcloud sql databases create emas_db --instance=emas-production-db
gcloud sql users create emas_user --instance=emas-production-db --password=<secure_password>
```

### 4. Load Balancer Configuration

```bash
# Configure application load balancer
aws elbv2 create-load-balancer \
  --name emas-alb \
  --subnets subnet-12345678 subnet-87654321 \
  --security-groups sg-12345678 \
  --scheme internet-facing \
  --type application

# Create target group
aws elbv2 create-target-group \
  --name emas-backend-tg \
  --protocol HTTP \
  --port 80 \
  --vpc-id vpc-12345678 \
  --health-check-path /health \
  --health-check-interval-seconds 30 \
  --health-check-timeout-seconds 5 \
  --healthy-threshold-count 2 \
  --unhealthy-threshold-count 3

# Create listener
aws elbv2 create-listener \
  --load-balancer-arn <alb_arn> \
  --protocol HTTPS \
  --port 443 \
  --certificates CertificateArn=arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012 \
  --default-actions Type=forward,TargetGroupArn=<target_group_arn>
```

---

## Monitoring Setup

### 1. Prometheus Configuration

```yaml
# prometheus-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    scrape_configs:
    - job_name: 'emas-backend'
      static_configs:
      - targets: ['emas-backend.emas.svc.cluster.local:80']
      metrics_path: /metrics
    
    - job_name: 'emas-frontend'
      static_configs:
      - targets: ['emas-frontend.emas.svc.cluster.local:80']
```

### 2. Grafana Dashboard

```bash
# Deploy Grafana
kubectl apply -f k8s/manifests/grafana.yaml

# Access Grafana
kubectl port-forward svc/grafana 3000:3000 -n monitoring

# Login with admin/admin
```

### 3. Alerting Setup

```yaml
# alerting-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: emas-alerts
  namespace: monitoring
spec:
  groups:
  - name: emas.rules
    rules:
    - alert: EMASBackendDown
      expr: up{job="emas-backend"} == 0
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: "EMAS Backend is down"
        description: "EMAS backend has been down for more than 1 minute."
```

---

## Troubleshooting

### Common Issues

#### 1. Pod Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name> --previous

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp
```

#### 2. Database Connection Issues

```bash
# Test database connectivity
kubectl exec -it <postgres-pod> -- psql -U emas_user -d emas_db -c "SELECT 1;"

# Check database logs
kubectl logs <postgres-pod>

# Verify service endpoints
kubectl get endpoints postgres
```

#### 3. Frontend Not Loading

```bash
# Check ingress configuration
kubectl describe ingress emas-ingress

# Check frontend service
kubectl get svc emas-frontend

# Test backend connectivity
kubectl exec <frontend-pod> -- curl -f http://emas-backend/health
```

#### 4. High Memory Usage

```bash
# Check resource usage
kubectl top pods

# Check for memory leaks
kubectl describe pod <pod-name> | grep -A 10 "Conditions:"

# Adjust resource limits
kubectl patch deployment emas-backend -p '{"spec":{"template":{"spec":{"containers":[{"name":"emas-backend","resources":{"limits":{"memory":"2Gi"}}}]}}}}'
```

### Performance Tuning

#### 1. Database Optimization

```sql
-- Enable query statistics
ALTER SYSTEM SET track_activities = on;
ALTER SYSTEM SET track_counts = on;
ALTER SYSTEM SET track_io_timing = on;

-- Adjust connection pooling
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';

-- Restart PostgreSQL
SELECT pg_reload_conf();
```

#### 2. Application Optimization

```bash
# Enable connection pooling
# Update environment variable
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40

# Enable caching
REDIS_MAX_CONNECTIONS=50

# Optimize NATS
NATS_MAX_PENDING=1000000
```

### Backup and Recovery

#### 1. Automated Backup

```bash
#!/bin/bash
# backup-script.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/emas"

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
kubectl exec deploy/postgres -- pg_dump -U emas_user emas_db > $BACKUP_DIR/database_$DATE.sql

# Redis backup
kubectl exec deploy/redis -- redis-cli --rdb /data/dump.rdb
kubectl cpemas-redis:/data/dump.rdb $BACKUP_DIR/redis_$DATE.rdb

# Application data backup
kubectl exec deploy/emas-backend -- tar -czf /tmp/app_backup.tar.gz /app/uploads
kubectl cpemas-backend:/tmp/app_backup.tar.gz $BACKUP_DIR/app_$DATE.tar.gz

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -type f -mtime +7 -delete
```

#### 2. Disaster Recovery

```bash
# Restore database
kubectl exec -i <postgres-pod> -- psql -U emas_user emas_db < database_backup.sql

# Restore Redis
kubectl cp redis_backup.rdb <redis-pod>:/data/dump.rdb
kubectl exec <redis-pod> -- redis-server --daemonize no

# Restart services
kubectl rollout restart deployment/emas-backend
kubectl rollout restart deployment/emas-frontend
```

### Monitoring and Alerting

#### Key Metrics to Monitor

1. **Application Metrics:**
   - Request rate and latency
   - Error rates
   - Active connections
   - Memory and CPU usage

2. **Database Metrics:**
   - Connection pool usage
   - Query performance
   - Disk usage
   - Replication lag

3. **Infrastructure Metrics:**
   - Pod status and readiness
   - Service availability
   - Network latency
   - Storage capacity

#### Alert Thresholds

```yaml
# Critical Alerts
- Alert: HighErrorRate
  Condition: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
  Duration: 2m
  
- Alert: DatabaseConnectionsHigh
  Condition: pg_stat_database_numbackends / pg_settings_max_connections > 0.8
  Duration: 5m

- Alert: HighMemoryUsage
  Condition: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
  Duration: 5m
```

---

## Security Checklist

### Pre-Deployment Security

- [ ] All secrets are stored securely
- [ ] SSL/TLS certificates are valid
- [ ] Network policies are configured
- [ ] RBAC is properly configured
- [ ] Images are scanned for vulnerabilities
- [ ] Security contexts are enforced
- [ ] Audit logging is enabled

### Post-Deployment Security

- [ ] Regular security scans
- [ ] Monitor for suspicious activity
- [ ] Keep dependencies updated
- [ ] Review access logs regularly
- [ ] Test disaster recovery procedures
- [ ] Update security patches promptly

---

## Support and Maintenance

### Regular Maintenance Tasks

1. **Weekly:**
   - Review system metrics
   - Check for security updates
   - Verify backup integrity

2. **Monthly:**
   - Review and update documentation
   - Performance optimization
   - Capacity planning review

3. **Quarterly:**
   - Security audit
   - Disaster recovery testing
   - Technology stack updates

### Support Contact

**Primary Contact**: Cavin Otieno  
**Email**: [cavin.otieno012@gmail.com](mailto:cavin.otieno012@gmail.com)  
**WhatsApp**: [+254708101604](https://wa.me/254708101604)  
**LinkedIn**: [Cavin Otieno](https://www.linkedin.com/in/cavin-otieno-9a841260/)  

### Office Hours

- **Schedule**: Every Tuesday 2:00 PM EAT
- **Format**: Google Meet (link shared in GitHub discussions)
- **Duration**: 1 hour
- **Purpose**: Technical support and mentorship

---

## Conclusion

This deployment guide provides comprehensive instructions for deploying EMAS across different environments. Follow the appropriate section based on your deployment requirements and ensure all prerequisites are met before proceeding.

For additional support or questions, please contact Cavin Otieno through the channels provided above.

**Remember**: Always test deployments in a staging environment before applying to production!