# AI Education Agent - Cloud Deployment Guide

## 🌐 Cloud Platform Options

Choose the best cloud platform for your government school deployment:

### **Option 1: AWS (Amazon Web Services) - Recommended**

#### **Why AWS for Government Schools:**
- **AWS GovCloud**: Designed for government workloads
- **Cost-effective**: Free tier available, pay-as-you-scale
- **Reliable**: 99.99% uptime SLA
- **Secure**: SOC 2, ISO 27001 compliant
- **Indian presence**: Data centers in Mumbai and Hyderabad

#### **AWS Deployment Steps:**

1. **Create AWS Account**
   ```bash
   # Install AWS CLI
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install

   # Configure AWS credentials
   aws configure
   ```

2. **Deploy using AWS ECS (Elastic Container Service)**
   ```bash
   # Create ECS cluster
   aws ecs create-cluster --cluster-name ai-education-cluster

   # Deploy using Docker Compose
   docker context create ecs ai-education-context
   docker context use ai-education-context
   docker compose -f docker-compose.aws.yml up
   ```

3. **Set up RDS Database**
   ```bash
   # Create PostgreSQL RDS instance
   aws rds create-db-instance \
     --db-instance-identifier ai-education-db \
     --db-instance-class db.t3.micro \
     --engine postgres \
     --master-username ai_user \
     --master-user-password YOUR_STRONG_PASSWORD \
     --allocated-storage 20
   ```

#### **Estimated AWS Costs:**
- **Development**: $20-50/month
- **Small School (100 students)**: $100-200/month
- **Large Deployment (1000+ students)**: $500-1000/month

### **Option 2: DigitalOcean (Budget-Friendly) - Recommended for Start**

#### **Why DigitalOcean:**
- **Simple pricing**: Predictable costs starting at $40/month
- **Developer-friendly**: Easy to use interface
- **Good performance**: SSD-based droplets
- **Indian data centers**: Bangalore region available
- **Perfect for government schools**: Cost-effective scaling

#### **DigitalOcean Deployment:**

1. **Create Account and Droplet**
   - Go to https://www.digitalocean.com
   - Create account (get $200 free credit)
   - Create a droplet: 4GB RAM, 2 CPUs, 80GB SSD ($24/month)

2. **Quick Setup Commands**
   ```bash
   # SSH to your droplet
   ssh root@YOUR_DROPLET_IP

   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh

   # Install Docker Compose
   curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   chmod +x /usr/local/bin/docker-compose

   # Clone your project
   git clone https://github.com/YOUR_USERNAME/ai-education-agent.git
   cd ai-education-agent

   # Set up environment
   cp .env.example .env.production
   nano .env.production  # Edit with your settings

   # Deploy
   chmod +x scripts/deploy.sh
   ./scripts/deploy.sh
   ```

## 🚀 **Immediate Deployment Steps**

Let's deploy your AI Education Agent right now:

### **Step 1: Choose Your Deployment Method**

#### **A. Local Production (Test on your machine)**
```bash
# Set environment variables
export DB_PASSWORD="ai_education_strong_password_2024"
export GRAFANA_PASSWORD="grafana_admin_password_2024"

# Deploy locally
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

#### **B. DigitalOcean Cloud (Recommended)**
1. **Create DigitalOcean Account**: https://www.digitalocean.com
2. **Create Droplet**:
   - Ubuntu 20.04
   - 4GB RAM, 2 CPUs ($24/month)
   - Bangalore region
3. **Deploy using our script**

#### **C. AWS Free Tier**
1. **Create AWS Account**: https://aws.amazon.com
2. **Use EC2 Free Tier**: t2.micro instance
3. **Deploy with Docker**

### **Step 2: Domain Setup (Optional but Recommended)**

1. **Buy Domain**:
   - Namecheap: $10-15/year
   - GoDaddy: $12-20/year
   - Indian providers: BigRock, ResellerClub

2. **Point Domain to Server**:
   ```bash
   # Add A record in DNS settings
   Type: A
   Name: @
   Value: YOUR_SERVER_IP

   # Add CNAME for www
   Type: CNAME
   Name: www
   Value: your-domain.com
   ```

3. **Setup SSL (Free)**:
   ```bash
   # Install Certbot
   sudo apt install certbot python3-certbot-nginx

   # Get SSL certificate
   sudo certbot --nginx -d your-domain.com -d www.your-domain.com
   ```

## 💰 **Cost Breakdown for Government Schools**

### **Minimal Setup (100 students)**
- **DigitalOcean Droplet**: $24/month (4GB RAM, 2 CPU)
- **Domain**: $12/year
- **SSL Certificate**: Free (Let's Encrypt)
- **OpenAI API**: ~$20-50/month (depending on usage)
- **Total**: ~$50-75/month

### **Medium Setup (500 students)**
- **DigitalOcean Droplet**: $48/month (8GB RAM, 4 CPU)
- **Managed Database**: $15/month
- **CDN**: $5/month
- **OpenAI API**: ~$100-200/month
- **Total**: ~$170-270/month

### **Large Setup (2000+ students)**
- **Multiple Droplets**: $150/month
- **Load Balancer**: $12/month
- **Managed Database**: $50/month
- **OpenAI API**: ~$500-800/month
- **Total**: ~$700-1000/month

## 🎯 **Ready-to-Deploy Commands**

Choose one option and run these commands: