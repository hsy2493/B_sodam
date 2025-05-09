pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-signin', branch: 'main', url: 'https://github.com/hsy2493/B_sodam.git'
            }
        }
        stage('Set up Python Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t fastapi-app .'
            }
        }
        // Optional: Docker 실행 단계 (활성화 시 주의)
        // stage('Run Docker Container') {
        //     steps {
        //         sh 'docker run -d -p 8000:8000 --name fastapi-container fastapi-app'
        //     }
        // }
    }
}
