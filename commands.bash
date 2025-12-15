curl -X 'POST' \
  'http://127.0.0.1:8000/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "sachin@example.com",
  "password": "sachin",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}'


