pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                // Get the code from GitHub
                checkout scm
            }
        }
        
        stage('Test Environment') {
            steps {
                // Check if we have the tools installed
                sh 'python3 --version'
                sh 'docker --version'
                sh 'kubectl version --client'
            }
        }
    }
}