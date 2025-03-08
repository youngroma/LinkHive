pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "youngroma/referralhive"
        DOCKER_TAG = "latest"
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'  // ID Jenkins Credentials для Docker Hub
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo "Running tests..."
                    sh "docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm web python manage.py test"
                }
            }
        }

        stage('Push Docker Image to Registry') {
            steps {
                script {
                    echo "Logging in to Docker Hub..."
                    withDockerRegistry([credentialsId: REGISTRY_CREDENTIALS]) {
                        sh "docker push ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up Docker cache..."
            sh "docker system prune -f"
        }
    }
}
