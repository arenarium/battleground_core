#!/bin/bash
./deploy_scripts/push_images.sh
ssh -o "StrictHostKeyChecking no" -i deploy_key $DEPLOY_HOST ./deploy.sh
