pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    parameters {
        string(name: 'DOCKERHUB_REPOSITORY', defaultValue: 'your-dockerhub-user/sentiment-app', description: 'Docker Hub namespace/repository')
        booleanParam(name: 'DEPLOY_TO_KUBERNETES', defaultValue: false, description: 'Deploy to the Kubernetes context configured on this Jenkins agent')
    }

    environment {
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Test') {
            steps {
                sh 'python -m pip install --disable-pip-version-check pytest'
                sh 'python -m pytest -q'
            }
        }

        stage('Build and push image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_TOKEN')]) {
                    sh '''
                        set +x
                        echo "$DOCKERHUB_TOKEN" | docker login --username "$DOCKERHUB_USERNAME" --password-stdin
                        docker build --pull -t "$DOCKERHUB_REPOSITORY:$IMAGE_TAG" .
                        docker push "$DOCKERHUB_REPOSITORY:$IMAGE_TAG"
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                expression { params.DEPLOY_TO_KUBERNETES }
            }
            steps {
                sh '''
                    kubectl apply -f k8s/
                    kubectl set image deployment/sentiment-test sentiment-test="$DOCKERHUB_REPOSITORY:$IMAGE_TAG"
                    kubectl rollout status deployment/sentiment-test --timeout=5m
                '''
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }
    }
}
