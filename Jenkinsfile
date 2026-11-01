
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
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Build and Test') {
            steps {
                sh '.venv/bin/pytest -v'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=week12-python-cicd \
                            -Dsonar.sources=. \
                            -Dsonar.exclusions=.venv/**,.pytest_cache/**
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Docker Build and Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    sh '''
                        docker build -t "$DOCKERHUB_USER/week12-python-cicd:$BUILD_NUMBER" .
                        docker tag "$DOCKERHUB_USER/week12-python-cicd:$BUILD_NUMBER" "$DOCKERHUB_USER/week12-python-cicd:latest"

                        echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin

                        docker push "$DOCKERHUB_USER/week12-python-cicd:$BUILD_NUMBER"
                        docker push "$DOCKERHUB_USER/week12-python-cicd:latest"

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker pull devopsbhuvana/week12-python-cicd:$BUILD_NUMBER

                    docker rm -f week12-python-app || true

                    docker run --name week12-python-app \
                        devopsbhuvana/week12-python-cicd:$BUILD_NUMBER

                    docker logs week12-python-app

                    docker inspect week12-python-app \
                        --format='ExitCode={{.State.ExitCode}}'
                '''
            }
        }
    }
}
