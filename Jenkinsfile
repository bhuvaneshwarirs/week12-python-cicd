pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Downloading source code from GitHub'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies'
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Build and Test') {
            steps {
                echo 'Running Python application tests'
                sh 'python3 -m pytest -v'
            }
        }

    }
}
