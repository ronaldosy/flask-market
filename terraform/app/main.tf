terraform {
  backend "remote" {
    organization = "cloudlabid"

    workspaces {
      name = "flask-market"
    }
  }
}

provider "aws" {
  region = var.region
}

provider "vault" {
  address = "https://vault.westconcloud-id.net:8200"
  token   = var.VAULT_TOKEN
  
}

data "vault_genereic_secret" "flask-market" {
  path = "kv/flask-market/app"
}

resource "aws_security_group" "web_server" {
  name        = "tf_sg_web_server"
  description = "Allow web traffic to web server"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

resource "aws_security_group" "web_db" {
  depends_on = [
    aws_security_group.web_server
  ]
  name        = "tf_sg_web_db"
  description = "Allow mysql traffice from web servers to db"
  vpc_id      = var.vpc_id

  ingress {
    from_port = 3306
    to_port   = 3306
    protocol  = "tcp"
    security_groups = [
      aws_security_group.web_server.id
    ]
  }
}

resource "aws_instance" "web-server" {
  ami                    = "ami-059a389e9cc27b315"
  instance_type          = "t2.micro"
  subnet_id              = "subnet-0f60f247f26a854a2"
  vpc_security_group_ids = [aws_security_group.web_server.id]
  key_name               = var.ec2_key

  root_block_device {
    delete_on_termination = "true"
    volume_size           = "10"
    volume_type           = "gp2"
  }

  tags = {
    Name   = "Web Server"
    Status = "Dev"
  }
}

resource "aws_db_subnet_group" "private_db_subnet" {
  name       = "private_db_subnet_group"
  subnet_ids = var.priv_subnet

  tags = {
    Name        = "Subnet Group DB"
    Description = "Subnet group for DB inside private VPC Subnet"
  }
}

resource "aws_db_instance" "webdb" {
  depends_on = [
    aws_db_subnet_group.private_db_subnet
  ]
  allocated_storage      = 10
  engine                 = "mysql"
  engine_version         = "5.7"
  instance_class         = "db.t3.micro"
  name                   = "webdb"
  username               = "${data.vault_generic_secret.flask-market.data["app_db_user "]}"
  password               = "${data.vault_generic_secret.flask-market.data["app_db_pwd"]}"
  parameter_group_name   = "default.mysql5.7"
  skip_final_snapshot    = true
  db_subnet_group_name   = aws_db_subnet_group.private_db_subnet.name
  vpc_security_group_ids = [aws_security_group.web_db.id]

  tags = {
    Name   = "Flask Market DB"
    Status = "Dev"
  }
}
