# Platform Contracts

This directory defines the platform-level contracts required to run and operate
the Lakehouse project on AWS.

These documents formalize the assumptions, responsibilities, and guarantees
between the Data Engineering team and the Platform / Security teams.

## Purpose

The goal of these contracts is to:
- Remove ambiguity about infrastructure expectations
- Enable fast security and architecture reviews
- Ensure production readiness despite a constrained budget

## Scope

This folder documents:
- Required AWS resources and configurations
- IAM and security constraints
- Runtime execution assumptions
- Storage layout and conventions

## Explicit Non-Goals

This repository does NOT:
- Provision AWS infrastructure
- Create or manage IAM roles
- Configure VPCs or networking
- Store credentials or secrets

## Change Policy

Any change impacting AWS resources, permissions, runtime behavior, or data
layout must be reflected in this directory and reviewed with the platform team.
