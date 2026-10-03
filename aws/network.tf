resource "aws_vpc" "hq_vpc" {
  cidr_block = "10.0.0.0/16"
  tags       = { Name = "hq-vpc" }
}

resource "aws_subnet" "hq_public" {
  vpc_id                  = aws_vpc.hq_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
  tags                    = { Name = "hq-public-subnet" }
}

resource "aws_subnet" "hq_private" {
  vpc_id            = aws_vpc.hq_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1a"
  tags              = { Name = "hq-private-subnet" }
}

resource "aws_internet_gateway" "hq_igw" {
  vpc_id = aws_vpc.hq_vpc.id
  tags   = { Name = "hq-igw" }
}

resource "aws_eip" "hq_nat_eip" {
  domain = "vpc"
}

resource "aws_nat_gateway" "hq_nat_gw" {
  allocation_id = aws_eip.hq_nat_eip.id
  subnet_id     = aws_subnet.hq_public.id
  tags          = { Name = "hq-nat-gw" }
  depends_on    = [aws_internet_gateway.hq_igw]
}

resource "aws_route_table" "hq_public_rt" {
  vpc_id = aws_vpc.hq_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.hq_igw.id
  }
  tags = { Name = "hq-public-rt" }
}

resource "aws_route_table_association" "hq_public_assoc" {
  subnet_id      = aws_subnet.hq_public.id
  route_table_id = aws_route_table.hq_public_rt.id
}

resource "aws_route_table" "hq_private_rt" {
  vpc_id = aws_vpc.hq_vpc.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.hq_nat_gw.id
  }
  tags = { Name = "hq-private-rt" }
}

resource "aws_route_table_association" "hq_private_assoc" {
  subnet_id      = aws_subnet.hq_private.id
  route_table_id = aws_route_table.hq_private_rt.id
}
