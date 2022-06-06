#!/bin/bash
REGION="ap-southeast-2"
`aws ecr get-login --no-include-email --region ${REGION}`
