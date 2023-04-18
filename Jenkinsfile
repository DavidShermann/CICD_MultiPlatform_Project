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
					curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
					curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
					sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
					kubectl version --client
					'''
				sh '''
					sudo apt-get install unzip -y	
					curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
					unzip -u awscliv2.zip
					sudo ./aws/install --update
					aws --version
					aws configure set aws_access_key_id $AWS_ACCESS_KEY
					aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
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

