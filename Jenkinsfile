pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "youngroma/referralhive"
        DOCKER_TAG = "latest"
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'

        SECRET_KEY = credentials('SECRET_KEY_ID')
        DB_USER = credentials('DB_USER_ID')
        DB_PASSWORD = credentials('DB_PASSWORD_ID')
        
        DB_HOST = "db"
        DB_PORT = "5432"
        DB_NAME = "refhive"
        REDIS_HOST = "redis"
        REDIS_PORT = "6379"
    }

    stages {      
        stage('Create .env file') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'SECRET_KEY_ID', variable: 'SECRET_KEY'),
                                      string(credentialsId: 'DB_USER_ID', variable: 'DB_USER'),
                                      string(credentialsId: 'DB_PASSWORD_ID', variable: 'DB_PASSWORD')]) {
                        echo "Creating .env file..."
                        writeFile file: '.env', text: """
                            SECRET_KEY=${SECRET_KEY}
                            DB_USER=${DB_USER}
                            DB_PASSWORD=${DB_PASSWORD}
                            DB_HOST=${DB_HOST}
                            DB_PORT=${DB_PORT}
                            DB_NAME=${DB_NAME}
                            REDIS_HOST=${REDIS_HOST}
                            REDIS_PORT=${REDIS_PORT}
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    docker.build("${DOCKER_IMAGE_NAME}:${DOCKER_TAG}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo "Running tests..."
                    bat "docker-compose --env-file .env -f ${DOCKER_COMPOSE_FILE} run --rm web python manage.py test"
                }
            }
        }

        stage('Push Docker Image to Registry') {
            steps {
                script {
                    echo "Logging in to Docker Hub..."
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        docker.image("${DOCKER_IMAGE_NAME}:${DOCKER_TAG}").push()
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up unused Docker images..."
            bat "docker image prune -f"

            echo "Deleting .env file..."
            bat "del .env"
        }
    }
}
