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
                stage('Update staging') {
                    sh 'docker tag ingestion-api gcr.io/cidc-dfci/ingestion-api:staging'
                }
                stage('Push to repo') {
                    withCredentials([string(credentialsId: 'cidc-dfci', variable: 'GCLOUD_SVC_JSON')]) {
                        sh 'docker login -u _json_key -p ${GCLOUD_SVC_JSON} https://gcr.io'
                    }
                    sh 'docker push gcr.io/cidc-dfci/ingestion-api:staging'
                }
            }
        }
}

