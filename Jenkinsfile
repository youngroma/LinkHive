pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "youngroma/referralhive"
        DOCKER_TAG = "latest"
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Skipping checkout, since it's managed in Jenkins UI."
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
                    echo "Creating Docker network..."
                    sh "docker network create mynetwork || true"

                    echo "Running tests..."
                    sh "docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm web python manage.py test"
                }
            }
        }

        stage('Push Docker Image to Registry') {
            steps {
                script {
                    echo "Logging in to Docker Hub..."
                    withCredentials([usernamePassword(credentialsId: REGISTRY_CREDENTIALS, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin"
                        sh "docker push ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up unused Docker images..."
            sh "docker image prune -f"
        }
    }
}
