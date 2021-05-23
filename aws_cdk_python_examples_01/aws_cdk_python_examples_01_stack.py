from aws_cdk import (
    aws_ec2 as ec2,
    aws_autoscaling as asg,
    aws_elasticloadbalancingv2 as elb,
    core
    )

class CDKExample01Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        
        vpc = ec2.Vpc(self, "MyVPC")
        
        data = open("./user_data.sh", "rb").read()
        httpd = ec2.UserData.for_linux()
        httpd.add_commands(str(data,'utf-8'))
        
        _asg = asg.AutoScalingGroup(
            self,
            "ASG",
            vpc=vpc,
            instance_type=ec2.InstanceType(instance_type_identifier="t2.large"),
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
                ),
            user_data=httpd,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            desired_capacity=2,
            auto_scaling_group_name="FirstASG"
        )
        
        _asg.scale_on_cpu_utilization("ScaleOnCPU_Utilization",target_utilization_percent=50)
        
        alb = elb.ApplicationLoadBalancer(
            self,
            "ALB",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            load_balancer_name="FirstALB",
            internet_facing=True
            )
        
        listener = alb.add_listener("Listener", port=80)
        listener.add_targets("Target", port=80, targets=[_asg])
        listener.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Allows HTTP from the World to call"
            )
            
        core.CfnOutput(self,"LoadBalancer",export_name="LoadBalancer", value=alb.load_balancer_dns_name)
        
        
        #_asg.connections.allow_from_any_ipv4(
        #    ec2.Port.tcp(22), "Internet access SSH"
        #   )
        #_asg.connections.allow_from_any_ipv4(
        #    ec2.Port.tcp(80), "Internet access HTTP"
        #    )
            
        #instance.connections.allow_from_any_ipv4(
        #    ec2.Port.tcp(22), "Internet access SSH"
        #    )
        #instance.connections.allow_from_any_ipv4(
        #    ec2.Port.tcp(80), "Internet access HTTP"
        #    )