pipeline {
	agent {
		label "Bond"

	}
	environment {
		 VERSION = "1.0.${env.BUILD_NUMBER}"
		 MY_USR = credentials('dockerlogin')
		 AWS_ACCESS_KEY = credentials('AWS_David_ACCESS_KEY')
		 AWS_SECRET_ACCESS_KEY = credentials('AWS_David_SECRET_ACCESS_KEY')
		 MONGO_ACCESS = credentials('David_MONGO_ACCESS')
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
					sudo apt-get update
					sudo apt-get install -y ca-certificates curl
					sudo apt-get install -y apt-transport-https
					sudo curl -fsSLo /etc/apt/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
					echo "deb [signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
					sudo apt-get update -y
					sudo apt-get install -y kubectl
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
					kubectl set image deployments/shopapp shopify=doovid1000/shopify:${VERSION} -o yaml --dry-run=client | kubectl apply -f -
					aws eks update-kubeconfig --region us-east-1 --name my-cluster
					kubectl delete -f kube.yaml
					kubectl get pods
					kubectl get deployments
					kubectl get svc
					echo gg
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

