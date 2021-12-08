output "db_endpoint" {
  value = aws_db_instance.webdb.address
}

output "redis_endpoint" {
  value = aws_elasticache_cluster.flask-redis.cache_nodes.0.address
}