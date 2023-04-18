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
				sh '''
					curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.23.17/2023-03-17/bin/linux/amd64/kubectl
					chmod +x ./kubectl
					mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin
					'''
				sh '''	
					curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
					unzip -u awscliv2.zip
					sudo ./aws/install
					aws --version
					'''
				sh '''	
					aws eks --region us-east-1 update-kubeconfig --name my-cluster
					kubectl delete -f kube.yaml
					kubectl apply -f kube.yaml
				'''
					}
			}
		} 
	}
	post{
		always{
				sh'''
					docker rm -f shop
					docker rmi -f doovid1000/shopify:$VERSION
					docker rmi -f shopify
		 		'''
		}
	}
}

