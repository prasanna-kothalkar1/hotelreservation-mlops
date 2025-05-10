pipeline{
    agent any
    environment{
        VENV_DIR = 'venv'
        GCP_PROJECT = 'mlopsproject1-458817'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin/'
    }
    stages{
        stage('Cloning github reopository to Jenkins'){
            steps{
                script{
                    echo 'Cloning github repository to Jenkins.............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/prasanna-kothalkar1/hotelreservation-mlops.git']])   
                }
            }
        }

        stage('Setting up virtual environment and installing dependencies'){
            steps{
                script{
                    echo 'Setting up virtual environment and installing dependencies.............'
                    sh '''
                    python -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -e .'''
                }
            }
        }
        
        stage('Building and pushing docker image to GCR'){
            steps{
                script{
                    withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                       script{
                        echo 'Building and pushing docker image to GCR.............'
                        sh '''
                        export PATH=$PATH:$GCLOUD_PATH
                        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                        gcloud config set project $GCP_PROJECT
                        gcloud auth configure-docker --quiet
                        docker build -t gcr.io/$GCP_PROJECT/hotelreservation-mlops:latest .
                        docker push gcr.io/$GCP_PROJECT/hotelreservation-mlops:latest
                        '''
                        echo 'Docker image pushed to GCR successfully'                   
                       }
                    }
                }
            }
            
        }
        stage('Deploying docker image to Google Cloud Run'){
            steps{
                script{
                    withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                       script{
                        echo 'Deploying docker image to Google Cloud Run.............'
                        sh '''
                        export PATH=$PATH:$GCLOUD_PATH
                        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                        gcloud config set project $GCP_PROJECT
                        gcloud run deploy hotelreservation-mlops \
                            --image=gcr.io/$GCP_PROJECT/hotelreservation-mlops:latest \
                            --platform=managed \
                            --region=us-central1 \
                            --allow-unauthenticated \
                        '''
                        echo 'Docker image deployed to Google Cloud Run successfully'                   
                       }
                    }
                }
            }            
        }
    }
}