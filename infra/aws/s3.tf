resource "aws_s3_bucket" "seedling_assets" {
  bucket = "seedling-assets"
}

resource "aws_s3_bucket_public_access_block" "assets_access" {
  bucket = aws_s3_bucket.seedling_assets.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "s3_bucket_name" {
  value = aws_s3_bucket.seedling_assets.id
}