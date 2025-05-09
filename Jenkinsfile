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
                script {
                    docker.image('python:3.10-slim-buster').inside {
                        sh 'python -m venv venv'
                        sh '. venv/bin/activate && pip install --upgrade pip'
                        sh '. venv/bin/activate && pip install -r requirements.txt'
                    }
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("fastapi-app", ".")
                }
            }
        }
        // stage('Run Docker Container') {
        //     steps {
        //         script {
        //             docker.image('fastapi-app').withRun('-d -p 8000:8000') { c ->
        //                 sh "docker logs -f ${c.id}"
        //             }
        //         }
        //     }
        // }
    }
}