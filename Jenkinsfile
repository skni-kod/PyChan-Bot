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
                label 'host'
            }
            environment {
                SCANNER_HOME = tool 'Scanner'
                ORGANIZATION = "SKNI-KOD"
                PROJECT_NAME = "PyChan-Bot"
            }
            steps{
                withCredentials([file(credentialsId: 'pychan-config', variable: 'PC_CONFIG')]) {
                    sh """
                    rm -rf .env
                    cp $PC_CONFIG config.py"""
                }
                withSonarQubeEnv('Sonarqube') {
                sh """$SCANNER_HOME/bin/sonar-scanner -Dsonar.organization=$ORGANIZATION \
                -Dsonar.projectKey=$PROJECT_NAME \
                -Dsonar.sources=. \
                -Dsonar.sourceEncoding=UTF-8 \
                -Dsonar.language=python """
                }
            }
        }
/*        stage("Quality Gate") {
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    // Parameter indicates whether to set pipeline to UNSTABLE if Quality Gate fails
                    // true = set pipeline to UNSTABLE, false = don't
                    waitForQualityGate abortPipeline: true
                }
            }
        }*/
        stage('Scan source') {
            agent{
                label 'host'
            }
            steps {
                // Scan all vuln levels
                sh 'mkdir -p reports'
                sh 'trivy filesystem --ignore-unfixed --vuln-type os,library --format json -o reports/php.json .'
                // Scan again and fail on CRITICAL vulns
                sh 'trivy filesystem --ignore-unfixed --vuln-type os,library --exit-code 1 --severity CRITICAL .'
		        archiveArtifacts 'reports/php.json'
            }
        }
        stage('Build'){
            agent{
                label 'host'
            }
            steps{
                    sh """
                    docker build -t $IMAGE:$BUILD_ID .
                    """
            }
        }
        stage('Scan image') {
            agent{
                label 'host'
            }
            steps {
                sh 'mkdir -p reports'
                sh 'trivy image --format json -o reports/image.json $IMAGE:$BUILD_ID '
                // Scan again and fail on CRITICAL vulns
                sh 'trivy image --exit-code 1 --severity CRITICAL  $IMAGE:$BUILD_ID '
		        archiveArtifacts 'reports/image.json'
            }
        }
        stage('Push to registry - back'){
            agent{
                label 'host'
            }
            steps{
                withCredentials([usernamePassword(credentialsId: 'harbor', passwordVariable: 'passwd', usernameVariable: 'username')]) {
                    sh """
                    docker login -u $username -p $passwd  ${env.REGISTRY}
                       docker push $IMAGE:$BUILD_ID
                       docker tag $IMAGE:$BUILD_ID $IMAGE:latest
                       docker push $IMAGE:latest
                       docker image rm $IMAGE:latest
                       docker image rm $IMAGE:$BUILD_ID
                    """
                }
            }
        }
        stage('Update k8s config') {
            agent{
                label 'host'
            }
            steps {
		        sh 'sed -i "s|harbor.skni.edu.pl/library/pychan:latest|harbor.skni.edu.pl/library/pychan:${BUILD_ID}|g" k8s/pychan-deployment.yaml'
                stash name: 'kubernetes', includes: 'k8s/**'
            }
        }
        stage('Deploy'){
	    agent {
	        docker {
	            image 'bitnami/kubectl:latest'
	            args "--entrypoint=''"
	        }
	    }
            steps{
		        unstash 'kubernetes'
                withCredentials([file(credentialsId: 'k8s-kubeconfig', variable: 'CONFIG')]) {
                        sh """
        	    		    mv k8s/* .
        	    		    kubectl --kubeconfig=$CONFIG apply -f pychan-deployment.yaml
        	    		    kubectl --kubeconfig=$CONFIG apply -f pychan-service.yaml	
                  		"""
                }
            }
        }
    }
    post {
        always {
            node('host') {
                deleteDir()
            }
        }
    }
}

