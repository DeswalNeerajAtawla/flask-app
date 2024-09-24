pipeline {
    agent any
    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/DeshwalNeerajAtawla/flask-app.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("flask-app")
                }
            }
        }
        stage('Test') {
            steps {
                // You can add testing steps here later (e.g., unit tests)
                echo 'Running tests...'
            }
        }
        stage('Deploy') {
            steps {
                script {
                    dockerImage.run("-p 5000:5000")
                }
            }
        }
    }
}
