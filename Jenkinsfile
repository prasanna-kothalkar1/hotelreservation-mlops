pipeline{
    agent any
    environment{
        VENV_DIR = 'venv'
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
    }
}