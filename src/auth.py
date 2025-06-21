import os

def lambda_handler(event, context):
    token = event.get("headers", {}).get("Authorization", "")
    method_arn = event.get("methodArn")
    if token == os.environ.get("DUMMY_TOKEN", "dummy-token"):
        effect = "Allow"
    else:
        effect = "Deny"
    return {
        "principalId": "user",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": method_arn,
                }
            ],
        },
    }
