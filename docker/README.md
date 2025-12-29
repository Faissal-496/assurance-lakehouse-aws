# Docker Environment

## Purpose

Docker provides a reproducible execution environment for Spark jobs across
local development and EC2 execution.

## Principles

- No credentials baked into images
- Minimal and explicit dependencies
- Same image for dev and validation

## Usage

Docker is used for:
- Local development
- Integration testing
- Controlled execution on EC2
