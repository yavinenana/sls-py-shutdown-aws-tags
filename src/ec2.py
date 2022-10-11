import boto3
import json

class Ec2Stop(object):
# InstancesEc2GetStatus
	def getInstanceStatus(self, InstanceId):
		ec2 = boto3.client('ec2', region_name='us-east-2')
		response = ec2.describe_instances(InstanceIds=InstanceId)
		instanceState=response['Reservations'][0]['Instances'][0]['State']['Name']
		# return("##### Instance Status: "+str(ActivityStreamStatus))
		return(instanceState)

	def getEc2InstancesIds(self):
		ec2 = boto3.client('ec2', region_name='us-east-2')
		response = ec2.describe_instances(InstanceIds=[])
		instancesIds=[]
		for i in response['Reservations']:
			# print(i['Instances'][0]['InstanceId'])
			instancesIds.append(i['Instances'][0]['InstanceId'])
		# print(instancesIds)
		return(instancesIds)

	def stopEc2(self, InstanceId):
		ec2 = boto3.client('ec2', region_name='us-east-2')
		instanceState=self.getInstanceStatus(InstanceId)
		if instanceState=="running":
			response=ec2.stop_instances(InstanceIds=InstanceId)
			instanceState=response['StoppingInstances'][0]['CurrentState']
			print(f"newStopStatus: {instanceState}")
		else:
			print(f"status : {instanceState}")

	def startEc2(self, InstanceId):
		ec2 = boto3.client('ec2', region_name='us-east-2')
		instanceState=self.getInstanceStatus(InstanceId)
		if instanceState=="stopped":
			response=ec2.start_instances(InstanceIds=InstanceId)
			instanceState=response['StartingInstances'][0]['CurrentState']
			print(f"newStopStatus: {instanceState}")
		else:
			print(f"status : {instanceState}")


# Tags
	def tasksByTags(self, action):
		ec2 = boto3.client('ec2', region_name='us-east-2')
		# getEc2InstancesIds=self.getEc2InstancesIds()
		instancesIds=self.getEc2InstancesIds()
		print(instancesIds)
		# instancesIds=self.instancesIds

		file = open('tags.json')
		data_verify = json.load(file)
		verify_data = {(x["Key"], x["Value"]) for x in data_verify}

		# instances
		print("\n Instances : ")
		tagsInstances = {}
		for x in instancesIds:
			# getInstanceStatus=self.getInstanceStatus(x)
		    responseInstances = ec2.describe_instances(
		        InstanceIds=[x])
		    # tags=response['Reservations'][0]['Instances'][0]['Tags']
		    for i in responseInstances['Reservations']:
		    	# print(i['Instances'][0]['Tags'])
		    	# print()
		        tagsInstances[x] = {(j["Key"], j["Value"]) for j in i['Instances'][0]['Tags']}
		print(tagsInstances)

		for instance in tagsInstances:
			if tagsInstances[instance].issuperset(verify_data):
			# if tagsInstances[instance] == verify_data:
				print(f"{instance} match keys")
				if action=='startEc2':
					# self.startEc2(instance)
					print('startEc2')
				elif action=='stopEc2':
					# self.stopEc2(instance)
					print('stopEc2')
			else:
				print(f"{instance} no match")
		print(tagsInstances)