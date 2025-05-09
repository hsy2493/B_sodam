pipeline {
    agent {
        docker { 
            image 'python:3.10' 
            dockerHost 'unix:///Users/hwangseoyeong/Library/Containers/com.docker.docker/socket'
            
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
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install --upgrade pip'
                sh '. .venv/bin/activate && pip install -r requirements.txt'
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