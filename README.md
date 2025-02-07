# Kafka-Spark Stream Processing

Real-time stream processing application demonstrating stream-to-stream joins between orders and payments using Apache Kafka and Apache Spark Structured Streaming.

## Project Overview

This project implements:
1. Order and payment event generation
2. Real-time stream processing with windowed joins
3. Dockerized Kafka and Zookeeper setup

## Architecture

- **Apache Kafka**: Message broker for handling real-time data streams
- **Apache Spark**: Stream processing engine with structured streaming
- **Docker**: Containerization for Kafka and Zookeeper
- **Python**: Implementation language with PySpark

## Components

### 1. Orders & Payments Generator (`orders_payments.py`)
- Generates synthetic order and payment events
- Publishes to Kafka topics:
  - `orders`: Contains order_id, amount, timestamp
  - `payments`: Contains order_id, payment_amount, timestamp
- Configurable generation rate and data patterns

### 2. Stream Join Processor (`stream_join.py`)
- Implements stream-to-stream joins using Spark Structured Streaming
- Features:
  - Watermarking (30 seconds)
  - Event-time processing
  - Inner and Left Outer joins
  - 1-minute join windows

## Prerequisites

- Docker & Docker Compose
- Python 3.9+
- pip
