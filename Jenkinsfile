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
    - mountPath: '/var/run/docker.sock'
      name: 'docker-volume'
  volumes:
  - hostPath:
      path: '/var/run/docker.sock'
      name: 'docker-volume'
"""
        }
    }
    environment {
      GOOGLE_APPLICATION_CREDENTIALS = credentials('google-service-accounts')
    }
    stages {
      stage('Checkout SCM') {
        steps {
          container('docker') {
            checkout scm
          }
        }
      }
      stage('Docker Login') {
        steps {
          container('docker') {
            sh 'cat ${GOOGLE_APPLICATION_CREDENTIALS} | docker login -u _json_key --password-stdin https://gcr.io'
          }
        }
      }
      stage('Docker Build') {
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