podTemplate(label: 'docker', namespace: 'jenkins',
    containers: [containerTemplate(image: 'docker', name: 'docker', command: 'cat', ttyEnabled: true)],
    volumes: [hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock')]) {
        node('docker') {
            container('docker') {
                sh 'docker --version'
                stage('Check out SCM') {
                    checkout scm
                }
                stage('Docker image build') {
                    sh 'docker build -t ingestion-api .'
                }
                
                withCredentials([file(credentialsId: 'google-service-account', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    stage('docker login') {
                        sh '''
                            curl -L "https://github.com/GoogleCloudPlatform/docker-credential-gcr/releases/download/v1.5.0/docker-credential-gcr_linux_amd64-1.5.0.tar.gz" \
                            | tar xz --to-stdout docker-credential-gcr \
                            > /usr/bin/docker-credential-gcr && chmod +x /usr/bin/docker-credential-gcr
                        '''
                        sh 'docker-credential-gcr configure-docker'
                    }
                    stage('Update staging') {
                        sh 'docker tag ingestion-api gcr.io/cidc-dfci/ingestion-api:staging'
                    }
                    stage('Push to repo') {
                        sh 'docker push gcr.io/cidc-dfci/ingestion-api:staging'
                    }
                    
                }
            }
        }
}

