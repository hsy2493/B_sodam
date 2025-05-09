pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-signin', url: 'https://github.com/hsy2493/B_sodam.git'
            }
        }
        stage('Set up Python Environment') {
            steps {
                sh 'python -m venv .venv'
                sh 'source .venv/bin/activate'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t fastapi-app .'
            }
        }
        stage('Run Docker Container') {
            steps {
                sh 'docker run -d --name fastapi-container -p 8000:8000 fastapi-app'
            }
        }
    }
}