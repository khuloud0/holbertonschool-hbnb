1. Introduction

This document provides a technical overview of the HBnB application design.
It consolidates the system architecture, business logic structure, and API interaction flows before implementation.

The goal of this documentation is to clearly define how different components of the system interact and to serve as a reference for future development stages.

2. High-Level Architecture

The HBnB application follows a three-layer architecture:
 • Presentation Layer (API)
Handles user requests and responses.
 • Business Logic Layer
Contains the core application rules and domain logic.
 • Persistence Layer (Database)
Manages data storage and retrieval.

Communication between layers is handled using the Facade Pattern, ensuring separation of concerns and maintainability

https://raw.githubusercontent.com/khuloud0/holbertonschool-hbnb/b8870fe87eaf765898f9db0560fb47bcacf97e55/part1/1.%20Detailed%20Class%20Diagram%20for%20Business%20Logic%20Layer.svg
