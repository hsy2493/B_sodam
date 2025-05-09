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
                sh '/usr/local/bin/python3 -m venv venv'
                sh '. venv/bin/activate && /usr/local/bin/pip3 install --upgrade pip'
                sh '. venv/bin/activate && /usr/local/bin/pip3 install -r requirements.txt'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t fastapi-app .'
            }
        }
    }
}
