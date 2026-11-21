# Configuración SEGURA según la línea base de TechSolutions (Anexo 4 del documento, CIS Benchmarks)
provider "aws" {
  region = "us-east-1"
}

resource "aws_kms_key" "datos" {
  description         = "Clave para cifrar datos de clientes"
  enable_key_rotation = true
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "AdministracionDeLaCuenta"
      Effect    = "Allow"
      Principal = { AWS = "arn:aws:iam::111122223333:root" }
      Action    = "kms:*"
      Resource  = "*"
    }]
  })
}

resource "aws_s3_bucket" "datos_clientes" {
  bucket = "techsolutions-datos-clientes-demo"
  #checkov:skip=CKV_AWS_144:Replicación entre regiones fuera del alcance de la demo
  #checkov:skip=CKV2_AWS_62:Notificaciones de eventos fuera del alcance de la demo
  #checkov:skip=CKV_AWS_18:Los registros de acceso se envían a CloudTrail (data events)
  #checkov:skip=CKV2_AWS_61:Ciclo de vida definido en la política de retención, fuera de la demo
}

resource "aws_s3_bucket_public_access_block" "datos_clientes" {
  bucket                  = aws_s3_bucket.datos_clientes.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "datos_clientes" {
  bucket = aws_s3_bucket.datos_clientes.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.datos.arn
    }
  }
}

resource "aws_s3_bucket_versioning" "datos_clientes" {
  bucket = aws_s3_bucket.datos_clientes.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Sin SSH desde internet: la administración se hace por SSM Session Manager
resource "aws_security_group" "servidor" {
  name        = "servidor-demo"
  description = "Servidor demo sin puertos de administracion abiertos"
  #checkov:skip=CKV2_AWS_5:En la demo no se crea la instancia EC2 que usa este grupo
  egress {
    description = "HTTPS saliente"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Mínimo privilegio: solo lectura del bucket del proyecto
resource "aws_iam_policy" "desarrolladores" {
  name = "desarrolladores-demo"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject", "s3:ListBucket"]
      Resource = [aws_s3_bucket.datos_clientes.arn, "${aws_s3_bucket.datos_clientes.arn}/*"]
    }]
  })
}
