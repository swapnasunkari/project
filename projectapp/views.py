from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import Rule
from .serializers import RuleSerializer
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
import json

def home_view(request):
    return HttpResponse("Welcome to the Rule Engine API! Use /api/create_rule/ to create rules and /api/evaluate_rule/ to evaluate them.")

def rule_engine_view(request):
    return render(request, 'rule_engine.html')

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type
        self.left = left
        self.right = right
        self.value = value

    def to_dict(self):
        return {
            "type": self.node_type,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
        }

def create_rule(rule_string):
    # Placeholder for parsing logic to create the AST
    return Node("operator", 
                Node("operand", value="age"), 
                Node("operand", value="30"))

def evaluate_rule(ast, data):
    if ast.node_type == 'operator':
        left_value = evaluate_rule(ast.left, data)
        right_value = evaluate_rule(ast.right, data)
        
        if ast.value == '>':
            return left_value > right_value
        # Add more operators as needed

    elif ast.node_type == 'variable':
        # Return the value from data using the variable's name
        return data.get(ast.value, 0)  # Default to 0 if not found

    elif ast.node_type == 'constant':
        # Convert the constant value to an integer
        return int(ast.value)

    return None

@api_view(['POST'])  # type: ignore
def create_rule_view(request):
    serializer = RuleSerializer(data=request.data)
    if serializer.is_valid():
        rule_string = serializer.validated_data['rule_string']
        ast = create_rule(rule_string)
        rule_data = {
            'rule_string': rule_string,
            'ast': json.dumps(ast.to_dict())  # Serialize AST
        }
        rule = Rule.objects.create(**rule_data)
        return JsonResponse({"message": "Rule created", "rule_id": rule.id})
    return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
def evaluate_rule_view(request):
    # Access the AST and data directly from request.data
    ast_data = request.data.get("ast")
    data = request.data.get("data")

    # Make sure to validate the input data
    if ast_data is None or data is None:
        return Response({"error": "AST and data are required."}, status=status.HTTP_400_BAD_REQUEST)

    def build_ast(node_data):
        if node_data is None:
            return None
        left = build_ast(node_data.get('left'))
        right = build_ast(node_data.get('right'))
        return Node(node_data['type'], left, right, node_data.get('value'))

    ast_root = build_ast(ast_data)

    # Evaluate the AST here based on your logic
    result = evaluate_rule(ast_root, data)

    return Response({"result": result}, status=status.HTTP_200_OK)
