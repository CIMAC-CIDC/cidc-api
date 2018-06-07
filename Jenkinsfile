def label = "worker-${UUID.randomUUID().toString()}"

podTemplate(label: label, namespace: "jenkins", ttyEnabled: true, command: 'cat', containers: [
    containerTemplate(
        name: 'api',
        image: 'undivideddocker/ingestion-api', ttyEnabled: true, command: 'cat', alwaysPullImage: true)
]) {
    node(label) {
        stage('Run Unit Tests') {
          container('api') {
              checkout scm
              sh 'nose2'
          }
        }
    }
}
