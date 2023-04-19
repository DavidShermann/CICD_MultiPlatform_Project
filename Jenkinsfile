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
			parallel {
				stage("Build on amd64")
				{
					agent {
						label "or_agent"
					}
					steps{
						dir('/home/ubuntu/workspace/MixProjectDavid'){
							sh '''
							docker buildx build -f Dockerfile_amd . --platform linux/amd64 -t shopify_amd64 --load
							'''	
						}
					}
				}
				stage("Build on arm64")
				{
					agent{
						label "Bond"
					}
					steps{
						dir('/home/ubuntu/jenkins/workspace/MixProjectDavid'){
						sh '''
							docker buildx build -f Dockerfile_arm . --platform linux/arm64 -t shopify_arm64 --load
							docker run --rm -d --name shop -p 5000:5000 shopify_arm64
							'''	
						}
					}
				}
			}
		}
		stage("Test"){
			
			steps{	
				dir('/home/ubuntu/jenkins/workspace/MixProjectDavid'){
			sh '''
			    docker run --rm -e MONGO_PASSWORD=${MONGO_ACCESS} shopify_arm64 python3 -m unittest appTest.py
				echo 'testing' 
			'''
				}
			}
		}
		stage("Push"){
			parallel {
				stage("Push amd64 image")
				{
					agent {
						label "or_agent"
					}
					steps{
							sh ''' 
					echo "$MY_USR_PSW" | docker login --username $MY_USR_USR --password-stdin
					docker tag shopify_amd64 doovid1000/shopify_amd64:$VERSION
					docker push doovid1000/shopify_amd64:$VERSION
					docker logout 
				'''
			}
					}
				}
				stage("Push arm64 image")
				{
					agent{
						label "Bond"
					}
					steps{
						sh ''' 
					echo "$MY_USR_PSW" | docker login --username $MY_USR_USR --password-stdin
					docker tag shopify_arm64 doovid1000/shopify_arm64:$VERSION
					docker push doovid1000/shopify_arm64:$VERSION
					docker logout 
				'''
						}
				}
		}
		stage("Clean"){
			parallel{
				stage("Clean amd64")
				{
					agent{
						label "or_agent"
					}
					post{
						always{
					sh'''
					docker rmi -f doovid1000/shopify_amd64:$VERSION
					docker rmi -f shopify_amd64
		 		'''
						}
					}
				}
				stage("clean arm64")
				{
					agent{
						label "Bond"
					}
					post{
						always{
						sh'''
					docker rm -f shop
					
					docker rmi -f doovid1000/shopify_arm64:$VERSION
					docker rmi -f shopify_arm64
		 		'''
						}
					}
				}
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
					aws eks update-kubeconfig --region us-east-1 --name my-cluster
					kubectl set image deployments/shopapp shopify=doovid1000/shopify_arm64:${VERSION} -o yaml --dry-run=client | kubectl apply -f -
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
	// post{
	// 	always{
	// 			sh'''
	// 				docker rm -f shop
	// 				docker rmi -f doovid1000/shopify_amd64:$VERSION
	// 				docker rmi -f doovid1000/shopify_arm64:$VERSION
	// 				docker rmi -f shopify
	// 	 		'''
	// 	}
	// }
}

