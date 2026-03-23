#!/bin/bash
# Test script for jasmine task with Zhipu AI glm-5 model

# Remove previous results to avoid auto-resume
rm -rf results/jasminum_nudiflorum_info_glm5

# Run the jasmine task with glm-5 model
pixi run python pipeline.py \
    --model glm-5 \
    --mcp-service playwright \
    --task-id jasminum_nudiflorum_info \
    --output-dir results/jasminum_nudiflorum_info_glm5 \
    --timeout 600
