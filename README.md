# Multi-Agent AI Research

A Python-based multi-agent research system designed to gather information, summarize findings, persist memory, and operate in a secure AWS deployment environment. It combines research agents, safety controls, queue processing, semantic caching, and vector-based long-term memory into a single architecture for AI-powered research workflows.

## Overview

The repository is built around a research agent pattern where specialized agents can:

- explore a topic using LLM-based research workflows
- summarize key findings into structured outputs
- remember recent context for session continuity
- reuse previous reports through semantic and vector-based memory
- enforce safety checks on input and output content
- process research jobs asynchronously in the background

This project is best described as an architecture-first platform for AI research automation with cloud-native deployment support.

## What is built in this project

### Multi-agent research flow
The project includes a research workflow with agent logic for:

- searching for key facts about a topic
- summarizing findings into readable output
- tracking state across iterations
- preserving session context for follow-up questions

The core agent logic is designed to work with a configurable inference gateway and supports retry handling for transient model failures.

### Safety and policy enforcement
The project includes AWS Bedrock Guardrails integration to validate content before and after generation. This helps protect the research workflow by blocking unsafe or disallowed content and enforcing policy boundaries.

### Session memory
Short-term conversation memory is stored so the system can retain recent interactions and use them as context during follow-up research tasks. This keeps the agent aware of what the user has already asked in the active session.

### Long-term memory
The project also stores research reports with embeddings and uses similarity-based retrieval to find relevant prior work. This enables:

- searching for related previous reports
- reusing past results with topic-aware similarity matching
- comparing new reports against older ones
- improving continuity across repeated research tasks

### Semantic caching
The application uses embedding-based caching for repeated or similar queries. When a new query is close to a previous one, the system can reuse cached results instead of sending the same work back to the model.

### Async job processing
The project includes Redis-based job queueing so research work can be processed asynchronously. It supports:

- creating jobs
- reading message streams
- storing result payloads
- acknowledging jobs after processing

This makes the system suitable for background work and worker-based execution patterns.

### Cloud deployment foundation
The infrastructure code provisions an AWS environment for the research service, including:

- VPC and networking
- private/public subnets
- application load balancer
- ECS-based application deployment
- Redis for queueing and memory
- PostgreSQL for long-term storage
- Secrets Manager for configuration
- CloudWatch logging
- ECR repositories
- AWS service integration for Bedrock and other components

## Project structure

The repository is organized into the following main areas:

- Main entry point for the app
- Core configuration and secrets management
- Authentication helpers
- Safety guardrail validation
- Retry logic
- Queue and background job management
- Research agent implementation
- Database pooling and memory storage
- Semantic cache logic
- Terraform infrastructure definitions

## Core components

### Configuration layer
The application centralizes runtime settings into a configuration object. It loads sensitive values from AWS Secrets Manager and exposes settings for:

- AWS region
- guardrail identifiers
- Redis connection
- database connection
- LLM gateway endpoint
- API keys
- tracing configuration
- cache thresholds and TTL
- session limits
- long-term memory tuning
- queue and worker settings

### Agent layer
The agent layer contains the actual research workflow logic. It is designed to:

- accept a research topic
- gather relevant facts
- summarize information into structured output
- use prior context when available
- store results for later retrieval

### Memory layer
The memory system combines:

- short-term Redis-based memory
- semantic cache with embedding similarity
- long-term vector memory in PostgreSQL

Together, these systems provide both conversational continuity and reusable knowledge.

### Queue layer
The queue layer manages research jobs through Redis Streams. This supports asynchronous execution patterns and allows jobs to be processed independently from the main request flow.

### Safety layer
The project includes input/output validation for research content using Bedrock Guardrails. This reduces the risk of unsafe or policy-violating output reaching users.

## Technology stack

The project uses:

- Python
- FastAPI
- LangGraph
- LangSmith
- TensorZero-compatible inference calls
- Redis
- PostgreSQL
- vector similarity search
- AWS Bedrock
- AWS Secrets Manager
- Boto3
- SentenceTransformers
- NumPy
- asyncpg
- Terraform

## Deployment

The infrastructure is built with Terraform and is intended for AWS deployment. It provisions the main cloud resources to run the app, queue, memory services, and supporting infrastructure in a production-style environment.

## Current status

This repository is a functional foundation for a multi-agent AI research platform. It contains the core architecture, memory systems, safety controls, queueing, and AWS deployment scaffolding needed for a real research assistant system.

It is not yet a fully polished end-user application, but it is a strong starting point for a secure, cloud-hosted AI research platform.

## Summary

This project is built to provide a cloud-native research agent system that can:

- search and summarize information
- retain short-term and long-term memory
- reuse similar results through semantic caching
- run background jobs asynchronously
- protect content with AWS guardrails
- deploy on AWS using Terraform

It represents a production-oriented foundation for an AI research assistant and future agentic workflows.
