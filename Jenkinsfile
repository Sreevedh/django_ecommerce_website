pipeline {
    agent {
      label 'jenkins_slave'
    }

    environment {
        DOCKER_VM_IP = '192.168.33.25' // IP address of your Docker VM
        DOCKER_VM_PORT = '5000'
        DOCKER_DEPLOY_VM = '192.168.33.15'
        DOCKER_REPO = 'blog' // Docker repository name
        GIT_REPO_URL = 'https://github.com/Sreevedh/django_ecommerce_website.git' // Your Git repository URL
        DOCKER_IMAGE_TAG = 'latest' // Tag for your Docker image
        SSH_CREDENTIALS_ID = 'docker_repo' // ID of your SSH credentials in Jenkins
    }

    stages {
        stage('Clone Git Repository') {
            steps {
                git branch: 'main', url: "${GIT_REPO_URL}"
            }
        }
        
        
        stage('Build Docker Image on Docker VM and pushing to registry') {
            steps {
                       script{
                            sh """
                               docker build -t ${DOCKER_VM_IP}:${DOCKER_VM_PORT}/${DOCKER_REPO}:${BUILD_NUMBER} .
                               echo "build SUCCESSFUL"
                               docker push ${DOCKER_VM_IP}:${DOCKER_VM_PORT}/${DOCKER_REPO}:${BUILD_NUMBER}
                               echo "PUSH TO REGISTRY SUCCESSFUL"
                               docker rmi ${DOCKER_VM_IP}:${DOCKER_VM_PORT}/${DOCKER_REPO}:${BUILD_NUMBER}
                             """
                        }
                       
            }
            
        }
        stage('Pulling from docker repo and deploying'){
            steps{
                sshagent (credentials: ["${SSH_CREDENTIALS_ID}"]) {
                    sh '''
                    ssh -t -o StrictHostKeyChecking=no vagrant@${DOCKER_DEPLOY_VM} << EOF
                    docker container stop blog >> /dev/null
                    docker container remove blog >> /dev/null
                    docker rmi $(docker images -q) >> /dev/null
                    docker pull ${DOCKER_VM_IP}:${DOCKER_VM_PORT}/${DOCKER_REPO}:${BUILD_NUMBER}
                    docker run -d -p 8000:8000 --name blog ${DOCKER_VM_IP}:${DOCKER_VM_PORT}/${DOCKER_REPO}:${BUILD_NUMBER}
                    '''
                }
            }
        }

    }
}

