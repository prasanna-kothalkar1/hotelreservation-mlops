pipeline{
    agent any
    stages{
        stage('Cloning github reopository to Jenkins'){
            steps{
                script{
                    echo 'Cloning github repository to Jenkins.............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/prasanna-kothalkar1/hotelreservation-mlops.git']])    }
}