# Agent API

This repository contains a small serverless REST API built with AWS SAM. The
API now provides basic CRUD operations on agents stored in DynamoDB.
Authentication is handled by an Amazon Cognito user pool instead of the
previous dummy token authorizer.

After deployment the stack outputs the user pool and client IDs. Use these
in your front-end application to sign up users and obtain JWT tokens.

## Deployment

1. Install the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) and the AWS CLI.
2. Build and deploy in one step using the provided script:
   ```bash
   ./deploy.sh
   ```
   The script wraps `sam build` and `sam deploy` and prints the API endpoint once the stack is created.
   You can optionally pass the stack name, AWS profile and region as arguments. If no region is configured, `us-east-1` is used by default.

   Example:
   ```bash
   ./deploy.sh my-stack myprofile us-east-1
   ```

   If you prefer to deploy manually, run `sam build` followed by `sam deploy --guided` and note the `ApiUrl`, `UserPoolId` and `UserPoolClientId` outputs.

## Usage

Send HTTP requests to the API endpoint using a tool like Postman. Include the
`Authorization` header with a valid Cognito JWT access token.

Available endpoints:

- `GET /agents` – list all agents (optional `?category=` filter)
- `GET /agents/{id}` – retrieve a single agent
- `POST /agents` – create a new agent
- `PUT /agents/{id}` – update an existing agent
- `DELETE /agents/{id}` – delete an agent
- `POST /agents/{id}/run` – run an agent (placeholder)

Example using `curl`:

```bash
curl -H "Authorization: Bearer <jwt-token>" $API_URL/agents
```

## Local Testing

You can run the API locally with SAM:

```bash
sam local start-api
```

Then issue requests to `http://127.0.0.1:3000/agents` with a valid JWT token in
the `Authorization` header.

## Project Structure

- `src/app.py` – Lambda handler for the API
- `src/auth.py` – Dummy authorizer (unused)
- `template.yaml` – SAM template defining resources
