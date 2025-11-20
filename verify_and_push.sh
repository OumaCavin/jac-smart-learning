#!/bin/bash

echo "=== Checking git status ==="
git status

echo -e "\n=== Adding changed files ==="
git add docker-compose.yml start_backend.sh start_databases.sh

echo -e "\n=== Committing changes ==="
git commit -m "fix: resolve Neo4j startup issue with password validation

- Update Neo4j container password from 'neo4j' to 'password123' to comply with Neo4j 5.x security requirements
- Update backend configuration and database scripts to use the new password  
- Fix restart loop caused by invalid default password validation"

echo -e "\n=== Pushing to remote ==="
git push origin main

echo -e "\n=== Verification - checking logs ==="
git log --oneline -2