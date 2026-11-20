# Configuración INSEGURA a propósito (R4.3 / control 5.23). No la despliegues: el pipeline la escanea.
# La versión corregida está en fixes/infra_main_seguro.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "datos_clientes" {
  bucket = "techsolutions-datos-clientes-demo"
}

# Bucket con acceso público permitido
resource "aws_s3_bucket_public_access_block" "datos_clientes" {
  bucket                  = aws_s3_bucket.datos_clientes.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# SSH abierto a todo internet
resource "aws_security_group" "servidor" {
  name        = "servidor-demo"
  description = "Servidor demo"
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Política IAM con todos los permisos sobre todos los recursos
resource "aws_iam_policy" "desarrolladores" {
  name = "desarrolladores-demo"
  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = "*", Resource = "*" }]
  })
}
