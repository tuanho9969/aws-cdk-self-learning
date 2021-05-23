from aws_cdk import (
    aws_ec2 as ec2,
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
        
        instance = ec2.Instance(
            self, "MyFirstCDKInstance",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            instance_type=ec2.InstanceType(instance_type_identifier="t2.large"),
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
            ),
            instance_name="MyFirstCDKEC2Instance",
            #user_data=ec2.UserData.add_execute_file_command(self, file_path="./user_data.sh")
            user_data=httpd,
            )
            
        instance.connections.allow_from_any_ipv4(
            ec2.Port.tcp(22), "Internet access SSH"
            )
        instance.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access HTTP"
            )