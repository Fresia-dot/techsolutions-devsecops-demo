"""Demo 1b: leer un secreto desde AWS Secrets Manager en lugar de tenerlo en el código.

Requisitos: pip install boto3 y credenciales de un usuario o rol con permiso
secretsmanager:GetSecretValue sobre el secreto techsolutions/demo/api-key.
"""
import boto3

cliente = boto3.client("secretsmanager", region_name="us-east-1")
valor = cliente.get_secret_value(SecretId="techsolutions/demo/api-key")["SecretString"]
print("Secreto leído correctamente. Longitud:", len(valor))  # nunca imprimas el valor
