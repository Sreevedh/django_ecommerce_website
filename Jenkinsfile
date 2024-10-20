pipeline {
  agent {
    node {
      label 'slave'
    }

  }
  stages {
    stage('build') {
      steps {
        git(url: 'https://github.com/Sreevedh/django_ecommerce_website.git', branch: 'main')
      }
    }

  }
}