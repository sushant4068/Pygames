pipeline {
  agent any
  stages {
    stage('Initialize') {
      steps {
        echo 'Welcome to Pygames'
      }
    }
    stage('Build') {
      steps {
        git(url: 'git@github.com:sushant4068/Pygames.git', branch: 'master', credentialsId: 'sushant4068/adi@2017')
      }
    }
  }
}