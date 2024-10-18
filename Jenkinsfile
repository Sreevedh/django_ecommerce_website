pipeline {
    agent any

    environment {
        // Define environment variables
        DOCKER_CREDENTIALS_ID = 'jenkinsslave' // ID for Docker credentials in Jenkins
        DOCKER_IMAGE = '192.168.33.25:5000/blog' // Your Docker image name (with registry IP)
        GITHUB_REPO = 'https://github.com/Sreevedh/django_ecommerce_website.git' // Your GitHub repository URL
        DOCKER_COMPOSE_FILE = 'docker-compose.yaml' // Path to your Docker Compose file
        DOCKER_HOST = '192.168.33.10' // TCP URL for Docker host
    }

    stages {
        stage('Checkout Code') {
            when{
                branch 'main'
            }
            steps {
                // Pull code from GitHub
                git url: "${GITHUB_REPO}", branch: 'main' // Specify the branch to pull from
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image using the Dockerfile
                    // Set Docker environment variables
                    withEnv(["DOCKER_HOST=${DOCKER_HOST}"]) {
                        sh 'docker build -t ${DOCKER_IMAGE} .'
                    }
                }
            }
        }
        stage('Push to Docker Private Repo') {
            steps {
                script {
                    // Log in to Docker using Jenkins credentials
                    withEnv(["DOCKER_HOST=${DOCKER_HOST}"]) {
                        docker.withRegistry('192.168.33.25:5000', "${DOCKER_CREDENTIALS_ID}") {
                            // Push the built image to the Docker registry
                            sh 'docker push ${DOCKER_IMAGE}'
                        }
                    }
                }
            }
        }
        stage('Deploying Code in Docker') {
            steps {
                script {
                    // Deploy using Docker Compose
                    withEnv(["DOCKER_HOST=${DOCKER_HOST}"]) {
                        sh "docker pull ${DOCKER_IMAGE}"
                        sh "docker-compose -f ${DOCKER_COMPOSE_FILE} up -d" // -d for detached mode
                    }
                }
            }
        }
    }
    post {
        // Post actions to execute after the pipeline completes
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check the logs for details.'
        }
    }
}