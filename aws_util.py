import boto3

class Ec2Util(object):
    def __init__(self, profile='default'):
        self.ec2_client = boto3.Session(profile_name=profile).client('ec2')
        self.ec2_resource = boto3.Session(profile_name=profile).resource('ec2')

    def _get_instance_by_id(self, instance_id):
        for i in self.ec2_resource.instances.all():
            if i.instance_id == instance_id:
                return i

    def _get_instance_by_tag_name(self, tag_name):
        for i in self.ec2_resource.instances.all():
            if i.tags is not None:
                for tag in i.tags:
                    if tag['Key'] == 'Name' and tag['Value'] == tag_name:
                        return i

    def get_instance(self, id_or_tag):
        instance = self._get_instance_by_tag_name(id_or_tag)
        if instance is None:
            instance = self._get_instance_by_id(id_or_tag)
        return instance

    def get_instance_type(self, id_or_tag):
        instance = self.get_instance(id_or_tag)
        return instance.instance_type

    def get_instance_status(self, id_or_tag):
        instance = self.get_instance(id_or_tag)
        if instance:
            return instance.state['Name']

    def start_instance(self, id_or_tag):
        instance = self.get_instance(id_or_tag)
        if instance.state['Name'] == 'stopped':
            instance.start()
            instance.wait_until_running()

    def stop_instance(self, id_or_tag):
        instance = self.get_instance(id_or_tag)
        if instance.state['Name'] == 'running':
            instance.stop()
            instance.wait_until_stopped()

    def change_instance_type(self, id_or_tag, instance_type):
        instance = self.get_instance(id_or_tag)
        current_instance_state = instance.state['Name']

        # If instance is running, we need to stop it before changing type
        if current_instance_state == 'running':
            instance.stop()
            instance.wait_until_stopped()

        self.ec2_client.modify_instance_attribute(InstanceId=instance.instance_id, InstanceType={'Value': instance_type})

        # If instance was running, we need to start it again
        if current_instance_state == 'running':
            instance.start()
            instance.wait_until_running()


class ElbUtil(object):
    def __init__(self, profile='default'):
        self.elb_client = boto3.Session(profile_name=profile).client('elb')

    def get_elb(self, elb_name):
        res = self.elb_client.describe_load_balancers(LoadBalancerNames=[elb_name])
        if len(res['LoadBalancerDescriptions']) > 0:
            return res['LoadBalancerDescriptions'][0]

    def register_instance(self, elb_name, instance_id):
        return self.elb_client.register_instances_with_load_balancer(LoadBalancerName=elb_name, Instances=[{'InstanceId': instance_id}])

    def deregister_instance(self, elb_name, instance_id):
        return self.elb_client.deregister_instances_from_load_balancer(LoadBalancerName=elb_name, Instances=[{'InstanceId': instance_id}])
