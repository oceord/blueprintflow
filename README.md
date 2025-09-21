# BlueprintFlow

![Python](https://img.shields.io/badge/Python-3.12%2B-2a5a83?logo=python)
![LanceDB](https://img.shields.io/badge/LanceDB-VectorStore-e56e4b)
![LiteLLM](https://img.shields.io/badge/LiteLLM-LLM%20Interface-2e8555)

BlueprintFlow is a Python library for offline-first, pattern-based code generation, powered by LLMs and modular workflows.
It enables developers to generate high-quality code from patterns, abstractions, and existing snippets while ensuring validation, traceability, and metadata embedding.

> [!WARNING]
> BlueprintFlow is in active development and not yet ready for production use.
> Expect breaking changes, missing features, and potential bugs as the project evolves.

📌 For a detailed development plan, see the [Roadmap](./docs/roadmap.md).

## Features

### Core Features

- **Pattern-Based Generation**: Generate code from existing patterns, abstractions, and high-quality code snippets.
- **Offline-First**: Operates entirely locally without internet dependencies by default.
- **Modular Architecture**: Independent, reusable components that integrate seamlessly with Python code.
- **Customizable**: Define rules, guidelines, and project-specific preferences.

### Advanced Features

- **AI-Powered Intelligence**: Leverages LLMs to understand context and generate meaningful code.
- **Quality Assurance**: Built-in human-in-the-loop validation ensures safe code generation.
- **Traceability and Metadata**: Track the origin of generated code and embed identifiers/watermarks.
- **Intelligent Search**: Similarity search, lexical analysis, reranking, and contextual retrieval for improved generation.

## Philosophy

- **Singular Focus**: Generate high-quality code from existing patterns, nothing more, nothing less.
- **AI-Powered Automation**: Generate contextually appropriate code that follows predefined rules and patterns.
- **Local-First Development**: Prioritize local processing to maximize security and minimize external dependencies.
- **Community-Driven**: Open-source, transparent, and collaborative.

## Tech Stack

- **Python 3.12+**
- **LiteLLM**: Local LLM interface for code generation.
- **LanceDB**: Unified vector store for patterns, abstractions, and code snippets.
- **Pydantic**: Data validation and structured models for safe operations.

## Usage

BlueprintFlow provides a flexible Python library for code generation:

- **Component Library**: Access pre-built, reusable modules for common development tasks.
- **Workflow Integration**: Integrate seamlessly with your existing dev tools.
- **Flexible Configuration**: Customize rules, standards, output formats, and LLM models.
- **Project-Specific Settings**: Tailor every aspect of generation to your project requirements.

## Quality Assurance

- **Human-in-the-Loop**: Generated code requires explicit human review or fails.
- **Custom Validation**: Define your own validation functions for project-specific rules.
- **Full Traceability**: Track every piece of code back to its source patterns and rules.
- **Metadata Embedding**: Embed identifiers and watermarks for context on code origins.

## Intelligent Search

- **Similarity Search**: Identify similar information from the knowledge base.
- **Contextual Analysis**: Consider surrounding context during code generation.
- **Smart Search**: Automatically refine queries to find the most relevant code examples.
- **Lexical Similarity & Reranking**: Improve search relevance and retrieval accuracy.

## Storage Architecture

- **Unified Vector Database (LanceDB)**: Store all entities including guidelines, rules, patterns, abstractions, and code snippets.
- **Vector Search**: Efficient, scalable similarity-based retrieval across all entities in the database.

## License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.
