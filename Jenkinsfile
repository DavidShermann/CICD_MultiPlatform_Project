pipeline {
	agent {
		label "Bond"

	}
	environment {
		 VERSION = "1.0.${env.BUILD_NUMBER}"
		 MY_USR = credentials('dockerlogin')
		 AWS_ACCESS_KEY = credentials('AWS_David_ACCESS_KEY')
		 AWS_SECRET_ACCESS_KEY = credentials('AWS_David_SECRET_ACCESS_KEY')
	}

	stages {
		stage("Build"){
			steps{
				dir('/home/ubuntu/jenkins/workspace/MixProjectDavid'){
				sh '''
					docker build . -t shopify --rm
					docker run -d --name shop -p 5000:5000 shopify
				'''
				
				}
			}
		}
		stage("Test"){
			steps{	
				dir('/home/ubuntu/jenkins/workspace/MixProjectDavid'){
			sh '''
			    docker exec shop python3 appTest.py
				echo 'testing' 
			'''
				}
			}
		}
		stage("Push"){
			steps{
				sh ''' 
					echo "$MY_USR_PSW" | docker login --username $MY_USR_USR --password-stdin
					docker tag shopify doovid1000/shopify:$VERSION
					docker push doovid1000/shopify:$VERSION
					docker logout 
				'''
			}
		}
		stage("Clean"){
		 	steps{
		 		sh'''
					docker rm -f shop
					docker rmi -f doovid1000/shopify:$VERSION
					docker rmi -f shopify
		 		'''
		 	}
		 }
	    stage("Deploy"){
			steps{
				dir('/home/ubuntu/jenkins/workspace/MixProjectDavid'){
                    withKubeConfig(
					[serverUrl: 'https://55911BA85A2B111147EA93B63BF45ACE.gr7.us-east-1.eks.amazonaws.com',
					contextName: 'arn:aws:eks:us-east-1:402440999262:cluster/my-cluster',
                    clusterName: 'my-cluster',
                    ]) {
      				sh 'kubectl get nodes'
				// sh '''
				// 	kubectl delete -f kube.yaml
				// 	kubectl apply -f kube.yaml
				// '''
					}
			}
		} 
	}
	}
	post{
		failure{
				sh'''
					docker rm -f shop
					docker rmi -f doovid1000/shopify:$VERSION
					docker rmi -f shopify
		 		'''
		}
	}
}

