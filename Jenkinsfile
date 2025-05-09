pipeline {
    agent {
        docker {
            image 'python:3.10-slim-buster'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-signin', branch: 'main', url: 'https://github.com/hsy2493/B_sodam.git'
            }
        }
        stage('Set up Python Environment') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t fastapi-app .'
            }
        }
    }
}