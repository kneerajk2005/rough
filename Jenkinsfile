pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Build') {
            steps {
                echo 'Building Flask application...'
            }
        }

        stage('Test') {
            steps {
                bat 'pytest'
            }
        }

        stage('Package') {
            steps {
                bat '''
                    if exist app.zip del app.zip
                    powershell -Command "Compress-Archive -Path app.py,requirements.txt,templates,static -DestinationPath app.zip"
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'CI/CD pipeline failed!'
        }
    }
}