#DB Secret example
To generate base-64 encoded string in linux ` echo 'somestring' | base64`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysql-secret
type: Opaque
data:
  app-db-username: app_db_username # Base-64 encoded string
  app-db-password: app_db_password # Base-64 encoded string
  mysql-root-password: mysql_root_password # Base-64 encoded string
```