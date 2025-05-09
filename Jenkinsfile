pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-signin', branch: 'main', url: 'https://github.com/hsy2493/B_sodam.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("fastapi-app", ".")
                }
            }
        }
    }
}