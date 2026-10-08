pipeline {

    agent any

    stages {

    
        stage('Install Dependencies') {
    steps {
        bat 'python --version'
        bat 'python -m pip install -r requirements.txt'
    }
}

stage('Build') {
    steps {
        echo 'Building Flask application...'

        bat '''
            if exist build rmdir /S /Q build
            mkdir build
            xcopy /E /I /Y app.py build\\
            xcopy /E /I /Y requirements.txt build\\
            xcopy /E /I /Y templates build\\templates\\
            xcopy /E /I /Y tests build\\tests\\
        '''
    }
}

stage('Test') {
    steps {
        bat 'python -m pytest'
    }
}

        stage('Package') {
            steps {
                echo 'Creating deployment package...'

                bat '''
                    if exist app.zip del app.zip
                    powershell -Command "Compress-Archive -Path app.py,requirements.txt,templates -DestinationPath app.zip"
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'

                bat '''
                    if not exist C:\\JenkinsDeploy mkdir C:\\JenkinsDeploy
                    copy /Y app.zip C:\\JenkinsDeploy\\app.zip
                '''
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