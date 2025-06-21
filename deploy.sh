#!/bin/bash
# Build and deploy the SAM application and print the API endpoint.
# Usage: ./deploy.sh [stack-name] [aws-profile] [region]
# stack-name defaults to 'agent-api'. The AWS profile and region are read from the AWS CLI config if not provided.
set -euo pipefail

STACK_NAME=${1:-agent-api}
AWS_PROFILE=${2:-default}


REGION=${3:-$(aws configure get region --profile "$AWS_PROFILE")}


sam build
sam deploy \
  --stack-name "$STACK_NAME" \
  --capabilities CAPABILITY_IAM \
  --region "$REGION" \
  --profile "$AWS_PROFILE" \
  --resolve-image-repos

API_URL=$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='ApiUrl'].OutputValue" \
  --output text \
  --region "$REGION" \
  --profile "$AWS_PROFILE")

printf '\nDeployed API URL: %s\n' "$API_URL"
printf 'Example request:\n  curl -H "Authorization: Bearer <jwt-token>" %s/agents\n' "$API_URL"
