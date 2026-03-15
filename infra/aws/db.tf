resource "aws_db_instance" "seedling_db" {
  allocated_storage = 10
  engine            = "postgres"
  instance_class    = "db.t3.micro"
  db_name           = "seedling_db"
  username          = "postgres"
  password          = "password"
  skip_final_snapshot = true
}