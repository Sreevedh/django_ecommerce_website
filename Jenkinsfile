pipeline {
  agent {
      label 'jenkins_slave'
  }
  stages {
    stage('checkout and clone') {
      steps {
        git(url: 'https://github.com/Sreevedh/django_ecommerce_website.git', branch: 'main')
      }
    }
    stage('build'){
      steps{
        docker.build('blog')
      }
    }

  }
}
