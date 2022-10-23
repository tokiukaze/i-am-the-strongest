import os
from typing import Any

from aws_cdk import RemovalPolicy, Stack, aws_apigateway, aws_lambda, aws_logs
from constructs import Construct


class IAmTheStrongestStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # lambda layer
        powertools_layer = aws_lambda.LayerVersion.from_layer_version_arn(
            self,
            id="lambda-powertools",
            layer_version_arn=f"arn:aws:lambda:{os.getenv('CDK_DEFAULT_REGION', 'us-east-1')}:017000801446:layer:AWSLambdaPowertoolsPython:38",
        )

        # lambda
        stronges_function = aws_lambda.Function(
            self,
            "strongest-function",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            architecture=aws_lambda.Architecture.ARM_64,
            code=aws_lambda.Code.from_asset("strongest_function"),
            handler="index.handler",
            layers=[powertools_layer],
        )

        # api gateway
        strongest_api = aws_apigateway.RestApi(self, "strongest-apigateway")
        strongest_integration = aws_apigateway.LambdaIntegration(
            stronges_function,
        )
        api_integration = aws_apigateway.LambdaIntegration(stronges_function)

        # New Genesis Method
        new_genesis = strongest_api.root.add_resource("new-genesis")
        new_genesis.add_method(
            http_method="POST",
            integration=api_integration,
            operation_name="post_new_genesis",
            api_key_required=False,
        )
        # I'm invincible Method
        i_am_invincible = new_genesis.add_resource("i-am-invincible")
        i_am_invincible.add_method(
            http_method="PUT",
            integration=api_integration,
            operation_name="put_i_am_invincible",
            api_key_required=False,
        )
        # Status Method
        status = strongest_api.root.add_resource("status")
        status.add_method(
            http_method="GET",
            integration=api_integration,
            operation_name="get_new_genesis",
            api_key_required=False,
        )

        # cloud watch log group
        aws_logs.LogGroup(
            self,
            "stronges-log-group",
            log_group_name=f"/aws/lambda/{stronges_function.function_name}",
            removal_policy=RemovalPolicy.DESTROY,
            retention=aws_logs.RetentionDays.THREE_MONTHS,
        )
