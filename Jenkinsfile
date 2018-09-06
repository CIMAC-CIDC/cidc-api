pipeline {
  agent {
    kubernetes {
      label 'helm-docker'
      defaultContainer 'jnlp'
      serviceAccount 'helm'
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
  - name: gcloud
    image: google/cloud-sdk:alpine
    command:
    - cat
    tty: true
  volumes:
  - name: docker-volume
    hostPath: 
      path: /var/run/docker.sock
"""
    }
  }
  environment {
      GOOGLE_APPLICATION_CREDENTIALS = credentials('google-service-account')
      deploy = "${UUID.randomUUID().toString()}"
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
            }
        }
    }
    stage('Docker push (master)') {
      when {
        branch 'master'
      }
      steps {
        container('docker') {
          sh 'docker tag ingestion-api gcr.io/cidc-dfci/ingestion-api:production'
          sh 'docker push gcr.io/cidc-dfci/ingestion-api:production'
        }
      }
    }
    stage('Docker build (staging)') {
      when {
        branch 'staging'
      }
      steps {
        container('docker') {
          sh 'docker tag ingestion-api gcr.io/cidc-dfci/ingestion-api:staging'
          sh 'docker push gcr.io/cidc-dfci/ingestion-api:staging'
        }
      }
    }
    stage('Docker deploy (staging)') {
      when {
          branch 'staging'
      }
      steps {
        container('gcloud') {
          sh 'apk add git --no-cache'
          sh 'apk add curl --no-cache'
          sh 'apk add bash --no-cache'
          sh 'apk add openssl --no-cache'
          sh 'gcloud container clusters get-credentials cidc-prod-cluster --zone us-east1-c --project cidc-dfci'
          sh 'curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get > get_helm.sh'
          sh 'chmod 700 get_helm.sh'
          sh './get_helm.sh --version v2.10.0'
          sh 'helm init --client-only'
          sh 'helm repo add cidc "http://${CIDC_CHARTMUSEUM_SERVICE_HOST}:${CIDC_CHARTMUSEUM_SERVICE_PORT}" '
          sh 'sleep 10'
          sh '''helm upgrade ingestion-api cidc/ingestion-api --set imageSHA=$(gcloud container images list-tags --format='get(digest)' --filter='tags:staging' gcr.io/cidc-dfci/ingestion-api) --set image.tag=staging'''
        }
      }
    }
  }
}
