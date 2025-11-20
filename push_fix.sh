#!/bin/bash
cd /workspace
echo "Current directory: $(pwd)"
echo "Files modified:"
git add docker-compose.yml start_backend.sh start_databases.sh
git commit -m "fix: resolve Neo4j startup issue with password validation"
git push origin main
echo "Push completed!"