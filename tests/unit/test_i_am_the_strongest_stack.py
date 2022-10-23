import aws_cdk as core
import aws_cdk.assertions as assertions

from i_am_the_strongest.i_am_the_strongest_stack import IAmTheStrongestStack

# example tests. To run these tests, uncomment this file along with the example
# resource in i_am_the_strongest/i_am_the_strongest_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = IAmTheStrongestStack(app, "i-am-the-strongest")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
