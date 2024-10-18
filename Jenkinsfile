pipeline {
  agent {
    node {
      label 'slave'
    }

  }
  stages {
    stage('Checkout Code') {
      steps {
        git(url: "${GITHUB_REPO}", branch: 'main')
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          withEnv(["DOCKER_HOST=${DOCKER_HOST}"]) {
            sh 'docker build -t ${DOCKER_IMAGE} .'
          }
        }

      }
    }

    stage('Push to Docker Private Repo') {
      steps {
        script {
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
          withEnv(["DOCKER_HOST=${DOCKER_HOST}"]) {
            sh "docker pull ${DOCKER_IMAGE}"
            sh "docker-compose -f ${DOCKER_COMPOSE_FILE} up -d" // -d for detached mode
          }
        }

      }
    }

  }
  environment {
    DOCKER_CREDENTIALS_ID = 'jenkinsslave'
    DOCKER_IMAGE = '192.168.33.25:5000/blog'
    GITHUB_REPO = 'https://github.com/Sreevedh/django_ecommerce_website.git'
    DOCKER_COMPOSE_FILE = 'docker-compose.yaml'
    DOCKER_HOST = '192.168.33.10'
  }
  post {
    success {
      echo 'Pipeline completed successfully.'
    }

    failure {
      echo 'Pipeline failed. Check the logs for details.'
    }

  }
}