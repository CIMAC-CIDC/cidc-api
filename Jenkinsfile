def label = "worker-${UUID.randomUUID().toString()}"

podTemplate(label: label, namespace: "jenkins", ttyEnabled: true, command: 'cat', yaml: """
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    io.kompose.service: ingestion-api
  name: ingestion-api
  namespace: jenkins
spec:
  replicas: 1
  template:
    metadata:
      creationTimestamp: null
      labels:
        io.kompose.service: ingestion-api
    spec:
      containers:
      - env:
        - name: AUTH0_CLIENT_SECRET
          valueFrom:
            secretKeyRef:
              name: api-secret
              key: AUTH0_CLIENT_SECRET
        envFrom:
          - configMapRef:
              name: service-env
        command: ['python3']
        args: ['ingestion_api.py']
        image: undivideddocker/ingestion-api:latest
        name: cidc-ingestion-api
        ports:
        - containerPort: 5000
          name: eve-api
"""
) {
    node(label) {
        stage('Run Unit Tests') {
          container('cidc-ingestion-api') {
              checkout scm
              sh 'nose2'
          }
        }
    }
}
