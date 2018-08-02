pipeline {
  agent {
    kubernetes {
      label 'docker'
      defaultContainer 'jnlp'
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: docker:latest
    command:
    - cat
    tty: true
    volumeMounts:
    - mountPath: /var/run/docker.sock
      name: docker-volume
  volumes:
  - name: docker-volume
    hostPath: 
      path: /var/run/docker.sock
"""
    }
  }
  environment {
      GOOGLE_APPLICATION_CREDENTIALS = credentials('google-service-account')
  }
  stages {
    stage('Checkout SCM') {
      steps {
        container('docker') {
          checkout scm
        }
      }
    }
    stage('Docker login') {
      steps {
        container('docker') {
          sh 'cat ${GOOGLE_APPLICATION_CREDENTIALS} | docker login -u _json_key --password-stdin https://gcr.io'
        }
      }
    }
    stage('Docker build') {
      steps {
        container('docker') {
          sh 'docker build -t ingestion-api .'
          sh 'docker tag ingestion-api gcr.io/cidc-dfci/ingestion-api:staging'
          sh 'docker push gcr.io/cidc-dfci/ingestion-api:staging'
        }
      }
    }
  }
}
