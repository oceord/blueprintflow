# BlueprintFlow

![Python](https://img.shields.io/badge/Python-3.12%2B-2a5a83?logo=python)
![LanceDB](https://img.shields.io/badge/LanceDB-VectorStore-e56e4b)
![LiteLLM](https://img.shields.io/badge/LiteLLM-LLM%20Interface-2e8555)

BlueprintFlow is a Python package designed to simplify code generation through local solutions.
It leverages LLMs to generate code from patterns and abstractions, adhering to predefined rules, guidelines, and preferences.
It emphasizes modularity and simplicity while maintaining a singular focus on code generation from upstream sources.

## Features

- **Pattern-Based Generation**: Generate code from existing patterns, abstractions, and good-quality code.
- **Offline-First**: Works entirely locally without requiring internet connectivity or external API calls.
- **Customizable**: Define rules, guidelines, and preferences.
- **Modular Architecture**: Use independent, reusable components that integrate seamlessly.
- **AI-Powered Intelligence**: Leverages LLMs to understand context and generate meaningful code.
- **Quality Assurance**: Built-in validation and traceability features ensure code quality.

## Philosophy

- **Singular Focus**: Generate high-quality code from existing patterns. Nothing more, nothing less.
- **AI-Powered Automation**: Leverage AI to generate contextually appropriate code that matches previously-defined rules.
- **Local-First Development**: Local processing is prioritized, ensuring security and eliminating network dependencies.
- **Community-Driven**: Built with transparency and collaboration in mind, empowering both contributors and users.

## Usage

BlueprintFlow provides a Python library with intuitive APIs for code generation:

- **Component Library**: Access pre-built, reusable modules for common tasks.
- **Flexible Configuration**: Customize rules, standards, output formats, and models.
- **Workflow Integration**: Seamlessly integrate with existing development tools and processes.
- **Project-Specific Settings**: Tailor every aspect of code generation to match project requirements.

## Quality Assurance

BlueprintFlow ensures code quality through multiple validation layers:

- **Human-in-the-Loop**: Generated code requires explicit human review, or it fails.
- **Custom Validation**: Define your own validation functions for project-specific requirements.
- **Full Traceability**: Track every piece of generated code back to its source patterns and rules.
- **Metadata Embedding**: Watermarks and identifiers provide context about code generation origins.

## Intelligent Search

BlueprintFlow uses advanced retrieval techniques to understand the context and improve generation quality:

- **Similarity Search**: Identifies similar information from its knowledge base.
- **Contextual Analysis**: Considers surrounding information context when generating new code.
- **Smart Search**: Automatically refines queries to find the most relevant code examples.

## Storage Architecture

BlueprintFlow uses a unified vector database (LanceDB) for all data storage, seamlessly integrating relational and similarity-based retrieval:

- **Data Storage**: All entities—including guidelines, rules, preferences, patterns, abstractions, and code snippets—are stored as records in LanceDB.
- **Vector Search**: Every entity supports vector search, enabling efficient and scalable similarity-based retrieval across the entire database.
