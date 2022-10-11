import boto3
import json

class RdsStop(object):
	client = boto3.client('rds')
	def getDbInstancesIds(self, client):
		# rds = boto3.client('rds')
		response = client.describe_db_instances()
		dbInstancesIds=[]
		for db in response['DBInstances']:
			dbInstancesIds.append(db['DBInstanceIdentifier'])
		return(dbInstancesIds)

	def getDbClustersIds(self, client):
		response_clusters = client.describe_db_clusters()
		dbClustersIds=[]
		for clusters in response_clusters['DBClusters']:
			dbClustersIds.append(clusters['DBClusterIdentifier'])
		return(dbClustersIds)

	def getInstancesOfCluster(self, client, clustersList):
		membersOfCluster=[]
		for cluster in clustersList:
			response = client.describe_db_clusters(DBClusterIdentifier=cluster,Marker='string')
			for db_member in response['DBClusters'][0]['DBClusterMembers']:
				membersOfCluster.append(db_member['DBInstanceIdentifier'])
		return(membersOfCluster)

# DbInstances
	def getDbInstanceStatus(self, client, DBInstanceIdentifier):
		response = client.describe_db_instances(DBInstanceIdentifier=DBInstanceIdentifier,Marker='string')
		DBInstanceStatus=response['DBInstances'][0]['DBInstanceStatus']
		ActivityStreamStatus=response['DBInstances'][0]['ActivityStreamStatus']
		# return("##### Instance Status: "+str(ActivityStreamStatus))
		return(DBInstanceStatus)
		
	def stopId(self, client, instanceId):
		DBInstanceStatus=self.getDbInstanceStatus(client, DBInstanceIdentifier=instanceId)
		if DBInstanceStatus =="available":
			response = client.stop_db_instance(DBInstanceIdentifier=instanceId)
			DBInstanceStatus=response['DBInstance']['DBInstanceStatus']
			return(f"newStopStatus: {DBInstanceStatus}")
		else :
			return(f"status : {DBInstanceStatus}")

	def startId(self, client, instanceId):
		DBInstanceStatus=self.getDbInstanceStatus(client, DBInstanceIdentifier=instanceId)
		if DBInstanceStatus =="stopped":
			response = client.start_db_instance(DBInstanceIdentifier=instanceId)
			DBInstanceStatus=response['DBInstance']['DBInstanceStatus']
			return(f"newStartStatus: {DBInstanceStatus}")
		else :
			return(f"status : {DBInstanceStatus}")
		# return("##### Start Id :" +str(response))

# DbClusters
	def getDbClusterStatus(self, client, DBClusterIdentifier):
		# client = self.client
		response = client.describe_db_clusters(DBClusterIdentifier=DBClusterIdentifier,Marker='string')
		DBClusterStatus=response['DBClusters'][0]['Status']
		ActivityStreamStatus=response['DBClusters'][0]['ActivityStreamStatus']
		return(DBClusterStatus)
	def stopCluster(self, client, DBClusterIdentifier):
		DBClusterStatus=self.getDbClusterStatus(client, DBClusterIdentifier=DBClusterIdentifier)
		if DBClusterStatus =="available":
			response = client.stop_db_cluster(DBClusterIdentifier=DBClusterIdentifier)
			DBClusterStatus=response['DBCluster']['Status']
			return(f"newStopStatus: {DBClusterStatus}")
		else :
			return(f"status : {DBClusterStatus}")
	def startCluster(self, client, DBClusterIdentifier):
		DBClusterStatus=self.getDbClusterStatus(client, DBClusterIdentifier=DBClusterIdentifier)
		if DBClusterStatus =="stopped":
			response = client.start_db_cluster(DBClusterIdentifier=DBClusterIdentifier)
			DBClusterStatus=response['DBCluster']['Status']
			return(f"newStartStatus: {DBClusterStatus}")
		else :
			return(f"status : {DBClusterStatus}")


	def getDbInstancesIdsNotInClusters(self, client):
		dbInstancesIds=self.getDbInstancesIds(client)
		# print(f"dbInstancesIds: {dbInstancesIds}")
		self.dbClustersIds=self.getDbClustersIds(client)
		# print(f"dbClustersIds: {self.dbClustersIds}")
		membersOfCluster=self.getInstancesOfCluster(client, self.dbClustersIds)
		# print(f"membersOfCluster: {membersOfCluster}")
		self.dbInstancesIdsNotInClusters = [x for x in dbInstancesIds if x not in membersOfCluster]
		# print(f"dbInstancesIdsNotInClusters: {self.dbInstancesIdsNotInClusters}")


# DbInstancesDbClusters Tags
	def tasksByDbTags(self, action):
		self.getDbInstancesIdsNotInClusters(self.client)
		dbInstancesIdsNotInClusters=self.dbInstancesIdsNotInClusters
		dbClustersIds=self.dbClustersIds

		# print(dbInstancesIdsNotInClusters)
		# print(dbClustersIds)
		print(f"\n {action}: ")

		file = open('tags.json')
		data_verify = json.load(file)
		verify_data = {(x["Key"], x["Value"]) for x in data_verify}
		# print(verify_data)
# instances
		print("\n InstancesDbs    : ")
		dataInstancesAws = {}
		for x in dbInstancesIdsNotInClusters:
		    responseInstances = self.client.describe_db_instances(
		        DBInstanceIdentifier=x,Marker='string'
		    )
		    for i in responseInstances['DBInstances']:
		        dataInstancesAws[x] = {(j["Key"], j["Value"]) for j in responseInstances['DBInstances'][0]['TagList']}
		print(dataInstancesAws)
		for instance in dataInstancesAws:
			if dataInstancesAws[instance].issuperset(verify_data):
			# if dataInstancesAws[instance] == verify_data:
				print(f"{instance} match keys")
				if action=='startId':
					self.startId(self.client, instance)
				elif action=='stopId':
					self.stopId(self.client, instance)
			else:
				print(f"{instance} no match")
		print(dataInstancesAws)
# cluster
		print("Clusters    : ")
		dataClustersAws = {}
		for x in dbClustersIds:
		    responseClusters = self.client.describe_db_clusters(
		        DBClusterIdentifier=x,Marker='string'
		    )
		    for i in responseClusters['DBClusters']:
		        dataClustersAws[x] = {(j["Key"], j["Value"]) for j in responseClusters['DBClusters'][0]['TagList']}
		for instance in dataClustersAws:
			if dataClustersAws[instance].issuperset(verify_data):
			# if dataClustersAws[instance] == verify_data:
				print(f"{instance} match keys")
				if action=='startCluster':
					self.startCluster(self.client, instance)
				elif action=='stopCluster':
					self.stopCluster(self.client, instance)
			else:
				print(f"{instance} no match")
		print(dataClustersAws)
