pipeline {
	agent {
		label "Bond"

	}
	environment {
		 VERSION = "1.0.${env.BUILD_NUMBER}"
		 MY_USR = credentials('dockerlogin')
	}

	stages {
		stage("Build"){
			steps{
//				dir('/home/ubuntu/jenkins/workspace/MixProject'){
//				sh '''
//					docker build . -t shopify --rm
//					docker run -d --name shop -p 5000:5000 shopify
//				'''
					sh 'echo build'
				}
			}
		}
		stage("Test"){
			steps{	
			sh '''
				echo 'test'
			'''
			}
		}
//		stage("Push"){
//			steps{
//				sh ''' 
//					echo "$MY_USR_PSW" | docker login --username $MY_USR_USR --password-stdin
//					docker tag weather-app doovid1000/weather-app:$VERSION
//					docker push doovid1000/weather-app:$VERSION
//					docker logout
//				'''
//			}
//		}
//		stage("Clean"){
//		 	steps{
//		 		sh'''
//					docker rm -f weather
//					docker rmi -f doovid1000/weather-app:$VERSION
//					docker rmi -f weather-app
//		 		'''
//		 	}
//		 }
//	}
//	post{
//		success{
	//		        build job: 'KubernetesFile', parameters: [
  //                  string(name: 'version', value: '$VERSION'),
      //          ]
	//	}
	//}
}
}
