# Flask Kubernetes CI/CD Assignment

A complete end-to-end CI/CD pipeline implementation for a Flask application using GitHub Actions, Jenkins, Docker, and Kubernetes (minikube). This project demonstrates modern DevOps practices including continuous integration, continuous delivery, automated testing, containerization, and orchestration.

## Project Overview

This project implements a simple Flask web application with a comprehensive CI/CD pipeline that automates testing, building, and deployment processes. The application is containerized using Docker and orchestrated using Kubernetes, providing features such as automated rollouts, horizontal scaling, and load balancing.

### Key Features

- **Continuous Integration (CI)**: Automated testing and building using GitHub Actions
- **Continuous Delivery (CD)**: Automated deployment to Kubernetes using Jenkins
- **Containerization**: Multi-stage Docker builds for optimized image size
- **Orchestration**: Kubernetes deployment with rolling updates, scaling, and load balancing
- **Code Quality**: Automated linting (flake8) and unit testing (pytest)
- **Resource Management**: CPU and memory limits/requests for containers
- **Health Checks**: Liveness and readiness probes for container health monitoring

## Kubernetes Features Used

### 1. **Deployment with Rolling Updates**
- **Rolling Update Strategy**: Configured with `maxSurge: 1` and `maxUnavailable: 1` to ensure zero-downtime deployments
- **Replicas**: Multiple pod replicas (3) for high availability
- **Rollout Management**: Supports `kubectl rollout undo` for quick rollbacks

### 2. **Service Load Balancing**
- **NodePort Service**: Exposes the application on port 30008 for external access
- **Load Distribution**: Automatically distributes traffic across all healthy pod replicas
- **Service Discovery**: Internal DNS-based service discovery within the cluster

### 3. **Resource Management**
- **Resource Requests**: CPU (100m) and Memory (128Mi) requests for scheduling
- **Resource Limits**: CPU (200m) and Memory (256Mi) limits to prevent resource exhaustion
- **Namespace Isolation**: Application deployed in dedicated `flask-app` namespace

### 4. **Health Monitoring**
- **Liveness Probe**: HTTP GET on `/health` endpoint to detect and restart unhealthy containers
- **Readiness Probe**: HTTP GET on `/` endpoint to ensure pods are ready before receiving traffic

### 5. **Scaling Capabilities**
- **Horizontal Scaling**: Supports manual and automatic scaling using `kubectl scale`
- **Replica Management**: Kubernetes automatically maintains desired replica count

## Project Structure

```
flask-k8s-ci-cd-assignment/
├── app.py                      # Flask application entry point
├── utils.py                    # Utility functions for testing
├── requirements.txt            # Python dependencies
├── dockerfile                  # Multi-stage Docker build configuration
├── jenkinsfile                 # Jenkins declarative pipeline
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI workflow
├── kubernetes/
│   ├── namespace.yml          # Kubernetes namespace definition
│   ├── deployment.yaml        # Kubernetes deployment manifest
│   └── service.yaml           # Kubernetes service manifest
└── tests/
    └── test_utils.py          # Unit tests for utility functions
```

## Prerequisites

Before building and running the application, ensure you have the following installed:

- **Docker**: Version 20.10 or higher
- **Python**: Version 3.9 or higher
- **Kubernetes**: minikube (for local Kubernetes cluster)
- **kubectl**: Kubernetes command-line tool
- **Jenkins**: For CI/CD pipeline execution (optional for local Docker runs)

## Building and Running Locally with Docker

### Step 1: Build the Docker Image

Navigate to the project root directory and build the Docker image:

```bash
docker build -t flask-app:latest .
```

This command:
- Uses a multi-stage build process
- Installs Python dependencies in the builder stage
- Creates an optimized runtime image
- Tags the image as `flask-app:latest`

### Step 2: Run the Container

Run the Flask application in a Docker container:

```bash
docker run -d -p 5000:5000 --name flask-app flask-app:latest
```

This command:
- Runs the container in detached mode (`-d`)
- Maps container port 5000 to host port 5000 (`-p 5000:5000`)
- Names the container `flask-app`

### Step 3: Verify the Application

Test the application by accessing it in your browser or using curl:

```bash
# Using curl
curl http://localhost:5000

# Expected output: Hello, World!
```

### Step 4: Stop and Remove the Container

When done testing, stop and remove the container:

```bash
docker stop flask-app
docker rm flask-app
```

## Deploying to Kubernetes Using Jenkins Pipeline

This section describes how to deploy the application to Kubernetes using the Jenkins CI/CD pipeline.

### Prerequisites for Jenkins Deployment

1. **Minikube Setup** (Admin):
   ```bash
   # Start minikube cluster
   minikube start
   
   # Verify cluster status
   minikube status
   
   # Configure kubectl to use minikube context
   kubectl config use-context minikube
   ```

2. **Jenkins Configuration** (Admin):
   - Install Jenkins with required plugins:
     - Pipeline plugin
     - Docker Pipeline plugin
     - Kubernetes CLI plugin
   - Configure Jenkins to access minikube:
     ```bash
     # Copy minikube kubeconfig to Jenkins
     # Or configure Jenkins to use minikube context
     ```

3. **Create Kubernetes Namespace**:
   ```bash
   kubectl apply -f kubernetes/namespace.yml
   ```

### Jenkins Pipeline Setup

1. **Create Jenkins Pipeline Job**:
   - Go to Jenkins Dashboard → New Item
   - Select "Pipeline" job type
   - Name: `flask-k8s-deployment`

2. **Configure Pipeline**:
   - **Pipeline Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: Your GitHub repository URL
   - **Branch**: `main` (or `*/main`)
   - **Script Path**: `jenkinsfile`

3. **Configure Build Triggers** (Optional):
   - **GitHub hook trigger for GITScm polling**: Enable for automatic builds on push
   - Or manually trigger builds from Jenkins dashboard

### Pipeline Execution

The Jenkins pipeline consists of the following stages:

#### Stage 1: Checkout Code
- Clones the repository from GitHub
- Ensures latest code is available

#### Stage 2: Build Docker Image
- Builds the Docker image using the Dockerfile
- Tags the image as `flask-app:latest`
- Verifies image creation

#### Stage 3: Deploy to Kubernetes
- Applies Kubernetes manifests from `kubernetes/` directory
- Creates/updates Deployment and Service resources
- Waits for deployment rollout to complete (timeout: 300s)

#### Stage 4: Verify Deployment
- Checks pod status and health
- Verifies service configuration
- Displays deployment status
- Shows rollout history

#### Stage 5: Smoke Test
- Validates that pods are running
- Ensures at least one pod is in Running state
- Fails pipeline if no healthy pods found

### Running the Pipeline

1. **Manual Trigger**:
   - Go to Jenkins Dashboard
   - Click on `flask-k8s-deployment` job
   - Click "Build Now"

2. **Automatic Trigger** (if webhook configured):
   - Push changes to `main` branch
   - Jenkins automatically detects changes and triggers build

3. **Monitor Pipeline**:
   - View console output in real-time
   - Check each stage execution
   - Verify deployment success

### Verifying Deployment

After successful pipeline execution, verify the deployment:

```bash
# Check pods
kubectl get pods -n flask-app

# Check services
kubectl get services -n flask-app

# Check deployments
kubectl get deployments -n flask-app

# Get service URL (if using minikube)
minikube service flask-service -n flask-app --url
```

### Accessing the Application

Once deployed, access the application:

```bash
# Get NodePort service URL
kubectl get service flask-service -n flask-app

# Access via minikube
minikube service flask-service -n flask-app

# Or directly via NodePort (default: 30008)
curl http://$(minikube ip):30008
```

## Automated Rollouts, Scaling, and Load Balancing

### Automated Rollouts

The Kubernetes deployment is configured with a **Rolling Update** strategy that ensures zero-downtime deployments:

- **maxSurge: 1**: Allows one extra pod to be created during updates
- **maxUnavailable: 1**: Allows one pod to be unavailable during updates

**How it works**:
1. When a new version is deployed, Kubernetes creates a new pod with the updated image
2. Once the new pod is ready (readiness probe passes), traffic is gradually shifted to it
3. Old pods are terminated only after new pods are healthy
4. This process continues until all pods are running the new version

**Rollback Process**:
```bash
# View rollout history
kubectl rollout history deployment/flask-app -n flask-app

# Rollback to previous version
kubectl rollout undo deployment/flask-app -n flask-app

# Rollback to specific revision
kubectl rollout undo deployment/flask-app --to-revision=2 -n flask-app
```

### Scaling

The deployment supports both manual and automatic scaling:

**Manual Scaling**:
```bash
# Scale to 5 replicas
kubectl scale deployment/flask-app --replicas=5 -n flask-app

# Verify scaling
kubectl get pods -n flask-app
```

**Automatic Scaling** (requires HorizontalPodAutoscaler):
```yaml
# Example HPA configuration (not included in current manifests)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: flask-app-hpa
  namespace: flask-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flask-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**Scaling Benefits**:
- **High Availability**: Multiple replicas ensure service continuity if pods fail
- **Load Distribution**: Traffic is distributed across all healthy pods
- **Resource Optimization**: Scale down during low traffic, scale up during high traffic

### Load Balancing

The **NodePort Service** provides load balancing across all pod replicas:

**How Load Balancing Works**:
1. **Service Discovery**: Kubernetes Service acts as a stable endpoint
2. **Endpoint Selection**: Service automatically selects healthy pods (readiness probe passed)
3. **Traffic Distribution**: Incoming requests are distributed using round-robin algorithm
4. **Health Monitoring**: Unhealthy pods are automatically removed from the load balancer pool

**Service Configuration**:
- **Type**: NodePort (exposes service on cluster node IP)
- **Port**: 80 (internal service port)
- **Target Port**: 5000 (container port)
- **NodePort**: 30008 (external access port)

**Load Balancing Features**:
- **Automatic Failover**: If a pod becomes unhealthy, traffic is automatically routed to healthy pods
- **Session Affinity**: Can be configured for sticky sessions (not enabled by default)
- **Health-based Routing**: Only routes traffic to pods that pass readiness probes

## CI/CD Pipeline Flow

### Complete Workflow

1. **Developer** pushes code to feature branch
2. **GitHub Actions** automatically triggers:
   - Runs flake8 linting (max line length: 90 characters)
   - Executes pytest unit tests
   - Builds Docker image
3. **Developer** creates Pull Request to `develop` branch
4. **Admin** reviews and merges PR after CI passes
5. **Admin** merges `develop` to `main` branch
6. **Jenkins** automatically triggers (or manually triggered):
   - Builds Docker image
   - Deploys to Kubernetes
   - Verifies deployment
   - Runs smoke tests

### GitHub Actions CI Workflow

The CI workflow (`.github/workflows/ci.yml`) performs:
- **Code Quality**: Flake8 linting with 90-character line limit
- **Unit Testing**: Pytest tests for utility functions
- **Docker Build**: Validates Dockerfile and builds image

### Jenkins CD Pipeline

The CD pipeline (`jenkinsfile`) performs:
- **Docker Build**: Creates production-ready image
- **Kubernetes Deployment**: Applies manifests and manages rollouts
- **Verification**: Validates deployment health and status
- **Smoke Testing**: Ensures application is accessible

## Testing

### Running Tests Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run linting
flake8 --max-line-length=90 app.py utils.py

# Run unit tests
pytest tests/ -v
```

### Test Coverage

- **Unit Tests**: Tests for `add_numbers()` and `multiply_numbers()` functions
- **Linting**: Code style validation with flake8
- **Integration**: End-to-end testing via Jenkins pipeline

## Troubleshooting

### Common Issues

1. **Pods not starting**:
   ```bash
   kubectl describe pod <pod-name> -n flask-app
   kubectl logs <pod-name> -n flask-app
   ```

2. **Service not accessible**:
   ```bash
   kubectl get endpoints flask-service -n flask-app
   minikube service list
   ```

3. **Deployment stuck**:
   ```bash
   kubectl rollout status deployment/flask-app -n flask-app
   kubectl get events -n flask-app --sort-by='.lastTimestamp'
   ```

4. **Jenkins pipeline failures**:
   - Check Jenkins console output
   - Verify kubectl access to minikube
   - Ensure Docker is accessible from Jenkins

## Technologies Used

- **Flask**: Python web framework
- **Docker**: Containerization platform
- **Kubernetes**: Container orchestration
- **minikube**: Local Kubernetes cluster
- **GitHub Actions**: CI/CD automation
- **Jenkins**: CD pipeline automation
- **pytest**: Python testing framework
- **flake8**: Python linting tool

## License

This project is created for educational purposes as part of the Cloud MLOps course assignment.

## Contributors

- **Admin**: Repository administration, branch protection, minikube setup, PR reviews
- **Developer**: Application development, Docker assets, Kubernetes manifests, PR creation

---

**Note**: This project demonstrates a complete CI/CD pipeline implementation.