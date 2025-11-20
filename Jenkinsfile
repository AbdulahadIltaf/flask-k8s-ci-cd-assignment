pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-k8s-app"
        IMAGE_TAG = "latest"
        KUBE_CONFIG = "$HOME/.kube/config"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                echo "Building Docker Image..."
                sh '''
                    docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying to Kubernetes..."
                sh '''
                    kubectl apply -f kubernetes/deployment.yaml
                    kubectl apply -f kubernetes/service.yaml
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                echo "Checking rollout status..."
                sh '''
                    kubectl rollout status deployment/flask-deployment
                    echo "------ PODS -------"
                    kubectl get pods
                    echo "------ SERVICES -------"
                    kubectl get services
                '''
            }
        }

    }

    post {
        success {
            echo "Pipeline completed successfully! Application deployed."
        }
        failure {
            echo "Pipeline failed. Please check logs."
        }
    }
}
