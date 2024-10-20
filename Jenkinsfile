pipeline {
    agent {
      label 'jenkins_slave'
    }

    environment {
        DOCKER_VM_IP = '192.168.33.25' // IP address of your Docker VM
        DOCKER_VM_PORT = '5000'
        BUILD_NUMBER = 'v1.0'
        DOCKER_REPO = 'blog' // Docker repository name
        GIT_REPO_URL = 'https://github.com/Sreevedh/django_ecommerce_website.git' // Your Git repository URL
        DOCKER_IMAGE_TAG = 'latest' // Tag for your Docker image
        SSH_CREDENTIALS_ID = 'docker_repo' // ID of your SSH credentials in Jenkins
    }

    stages {
        stage('Clone Git Repository') {
            steps {
                git branch: 'main', url: "${GIT_REPO_URL}"
                // sh """
                // docker login -u vagrant -p vagrant 192.168.33.25:5000
                // docker build -t ${DOCKER_REPO} .
                // docker image tag ${DOCKER_REPO} ${DOCKER_VM_IP}:${DOCKER_VM_PORT}/${DOCKER_REPO}:${BUILD_NUMBER}
                // docker push ${DOCKER_VM_IP}:${DOCKER_VM_PORT}/${DOCKER_REPO}:${BUILD_NUMBER}
                // """
            }
        }

        // ssh -o StrictHostKeyChecking=no vagrant@${DOCKER_VM_IP} \
        //             'cd /home/vagrant && docker build -t ${DOCKER_REPO} .'
        //             docker image tag ${DOCKER_REPO} ${DOCKER_VM_IP}:${DOCKER_VM_PORT}/${DOCKER_REPO}:${BUILD_NUMBER}
        //             docker push ${DOCKER_VM_IP}:${DOCKER_VM_PORT}/${DOCKER_REPO}:${BUILD_NUMBER}
        stage('Build Docker Image on Docker VM and pushing to registry') {
            steps {
                sshagent (credentials: ["${SSH_CREDENTIALS_ID}"]) {
                    sh """
                    ls
                    echo "hello"
                    """
                }
            }
        }

    }
}

