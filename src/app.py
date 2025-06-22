import json
from decimal import Decimal
import os
import uuid
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["AGENTS_TABLE"])

def response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, cls=DecimalEncoder),
    }

def lambda_handler(event, context):
    http_method = event.get("httpMethod")
    resource = event.get("resource")
    if resource == "/agents" and http_method == "GET":
        return list_agents(event)
    if resource == "/agents/{id}" and http_method == "GET":
        return get_agent(event)
    if resource == "/agents" and http_method == "POST":
        return create_agent(event)
    if resource == "/agents/{id}" and http_method == "PUT":
        return update_agent(event)
    if resource == "/agents/{id}" and http_method == "DELETE":
        return delete_agent(event)
    if resource == "/agents/{id}/run" and http_method == "POST":
        return run_agent(event)
    return response(404, {"message": "Not found"})

def list_agents(event):
    params = event.get("queryStringParameters") or {}
    category = params.get("category") if params else None
    if category:
        result = table.query(
            IndexName="CategoryIndex",
            KeyConditionExpression=Key("category").eq(category),
        )
        items = result.get("Items", [])
    else:
        result = table.scan()
        items = result.get("Items", [])
    return response(200, items)

def get_agent(event):
    agent_id = event["pathParameters"]["id"]
    result = table.get_item(Key={"id": agent_id})
    item = result.get("Item")
    if not item:
        return response(404, {"message": "Agent not found"})
    return response(200, item)

def create_agent(event):
    data = json.loads(event.get("body") or "{}")
    agent_id = data.get("id", str(uuid.uuid4()))
    now = datetime.utcnow().isoformat()
    item = {**data, "id": agent_id, "createdAt": now, "updatedAt": now}
    table.put_item(Item=item)
    return response(201, item)

def update_agent(event):
    agent_id = event["pathParameters"]["id"]
    result = table.get_item(Key={"id": agent_id})
    existing = result.get("Item")
    if not existing:
        return response(404, {"message": "Agent not found"})
    data = json.loads(event.get("body") or "{}")
    now = datetime.utcnow().isoformat()
    item = {**existing, **data, "id": agent_id, "updatedAt": now}
    if "createdAt" not in item:
        item["createdAt"] = now
    table.put_item(Item=item)
    return response(200, item)

def delete_agent(event):
    agent_id = event["pathParameters"]["id"]
    table.delete_item(Key={"id": agent_id})
    return response(204, {})

def run_agent(event):
    agent_id = event["pathParameters"]["id"]
    # Placeholder for actual execution logic
    return response(202, {"message": f"Agent {agent_id} execution started"})
