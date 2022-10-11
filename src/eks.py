import boto3
import json

class EksAsg(object):
	client = boto3.client('eks')
	scalingConfigGrow={'minSize': 0, 'maxSize': 2, 'desiredSize': 1}
	scalingConfigDowngrade={'minSize': 0, 'maxSize': 2, 'desiredSize': 0}
	# scalingGrow=[0,2,1]
	# scalingDowngrade=[0,2,0]
	list_clusters = client.list_clusters()
	list_clusters=list_clusters['clusters']

	def listNodeGroups(self, client, clusterName):
		# client = boto3.client('eks')
		response = client.list_nodegroups(clusterName=clusterName,maxResults=10,nextToken='')
		listNodeGroups=response['nodegroups']
		return(listNodeGroups)

	def downgradeNodeGroup(self,client, clusterName, nodegroupName):
		# client = boto3.client('eks')
		# response = client.update_nodegroup_config(clusterName='saleor-backendv2',nodegroupName='saleor-backendv2-services-better-woodcock',scalingConfig={'minSize': 0,'maxSize': 2,'desiredSize': 0})
		# downgradeNodeGroup = client.update_nodegroup_config(clusterName='saleor-backendv2',nodegroupName='saleor-backendv2-services-better-woodcock',scalingConfig=self.scalingConfigDowngrade)
		# downgradeNodeGroup = client.update_nodegroup_config(clusterName='saleor-backendv2',nodegroupName=nodegroupName,scalingConfig=self.scalingConfigDowngrade)
		downgradeNodeGroup = client.update_nodegroup_config(clusterName=clusterName,nodegroupName=nodegroupName,scalingConfig=self.scalingConfigDowngrade)
		# print(downgradeNodeGroup['update']['status'])
		# status1=self.describeNodeGroups(clusterName='saleor-backendv2',nodegroupName='saleor-backendv2-services-better-woodcock')
		return(downgradeNodeGroup['update']['status'])

	def growNodeGroup(self,client, clusterName, nodegroupName):	
		growNodeGroup = client.update_nodegroup_config(clusterName=clusterName,nodegroupName=nodegroupName,scalingConfig=self.scalingConfigGrow)
		return(growNodeGroup['update']['status'])


	def tasksByTags(self, action):
		# client = boto3.client('eks')
		# # list_clusters = client.list_clusters()
		# # list_clusters=list_clusters['clusters']
		file = open('tags.json')
		data_verify = json.load(file)
		verify_data = {(x["Key"], x["Value"]) for x in data_verify}

		# instances
		print("\n getTagsClusters : ")
		try:
			pass
			getTagsClusters={}
			for i in self.list_clusters:
				responseCluster=self.client.describe_cluster(name=i)
				tagsClusters=responseCluster['cluster']['tags']
				getTagsClusters[i]={(y) for y in tagsClusters.items()}
			# print(getTagsClusters)

			for tagOf in getTagsClusters:
				if getTagsClusters[tagOf].issuperset(verify_data):
					print(f"{tagOf} match keys")
					if action=='growNodeGroup':
						# print("\ngrowNodeGroup")
						listNodeGroups = self.listNodeGroups(self.client, tagOf)
						print(listNodeGroups)
						for node in listNodeGroups:
							print('growNodeGroup')
							growNodeGroup = self.growNodeGroup(self.client, tagOf,node)
						print(growNodeGroup)
					elif action=='downgradeNodeGroup':
						# print("\ndowngradeNodeGroup")
						listNodeGroups = self.listNodeGroups(self.client, tagOf)
						# print(listNodeGroups)
						for node in listNodeGroups:
							print('downgradeNodeGroup')
							downgradeNodeGroup = self.downgradeNodeGroup(self.client, tagOf,node)
						# print(downgradeNodeGroup)
				else:
					print(f"{tagOf} no match")
			# print(getTagsClusters)			
		except Exception as e:
			raise
		# else:
		# 	pass
		# finally:
		# 	pass

