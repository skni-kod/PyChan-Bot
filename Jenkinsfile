pipeline{
    agent none
    environment {
        REGISTRY = 'harbor.skni.edu.pl/'
        DOCKER_REGISTRY_CREDENTIALS_ID = 'harbor'
        IMAGE = 'harbor.skni.edu.pl/library/pychan'
    }
    stages{
        stage('Sonar'){
            agent{
                label 'sonar'
            }
            environment {
                ORGANIZATION = "SKNI-KOD"
                PROJECT_NAME = "PyChan-Bot"
                SONAR_SERVER = "https://sonar.skni.edu.pl"
            }
            steps{
                container('sonarqube') {
                    withCredentials([string(credentialsId: 'sonar', variable: 'TOKEN')]) {
                        sh """sonar-scanner -Dsonar.organization=$ORGANIZATION \
                            -Dsonar.projectKey=$PROJECT_NAME \
                            -Dsonar.host.url=$SONAR_SERVER \
                            -Dsonar.login=$TOKEN \
                            -Dsonar.sources=. \
                            -Dsonar.exclusions=./helm/**/* \
                            -Dsonar.sourceEncoding=UTF-8 \
                            -Dsonar.language=python \
                            -Dsonar.python.version=3.10
                        """
                    }
                }
            }
        }
        stage('Scan source') {
            agent{
                label 'trivy'
            }
            steps {
                container('trivy'){
                    // Scan all vuln levels
                    sh 'mkdir -p reports'
                    sh 'trivy filesystem --ignore-unfixed --vuln-type os,library --format json -o reports/python.json .'
                    // Scan again and fail on CRITICAL vulns
                    sh 'trivy filesystem --ignore-unfixed --vuln-type os,library --exit-code 1 --severity CRITICAL .'
		            archiveArtifacts 'reports/python.json'
                }
            }
        }
        stage('Build'){
            agent{
                label 'kaniko'
            }
            steps{
                sh "/kaniko/executor --context=\$(pwd) --dockerfile=\$(pwd)/Dockerfile --destination=$IMAGE:$BUILD_ID"
            }
        }

        stage('Deploy'){
	        agent {
	            label 'helm'
	        }
            steps{
        		container(name: 'helm', shell: '/bin/sh') {
                    withCredentials([file(credentialsId: 'k8s-ca', variable: 'MY_CA'), string(credentialsId: 'k8s-token', variable: 'MY_TOKEN')]) { 
                    sh """
                        kubectl config set-cluster mycluster --server=https://kubernetes.default --certificate-authority=${MY_CA}
                        kubectl config set-credentials jenkins-robot --token=${MY_TOKEN}
                        kubectl config set-context mycontext --cluster=mycluster --user=jenkins-robot
                        kubectl config use-context mycontext
                        helm upgrade --install --namespace pychan --set image.tag=${BUILD_ID} pychan ./helm
                    """
                    }
                }
            }
        }
    }
}

