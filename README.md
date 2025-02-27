# BlueprintFlow

BlueprintFlow aims to simplify code generation through abstractions and structured data retrieval, allowing developers to create high-quality, modularized code with reduced overhead and adherence to established standards.

## Overview

### Goals

- **Systematic Code Generation**: enable structured and consistent code generation
- **Architecture Replication**: replicate existing architectural structures
- **Modularity**: facilitate the creation of reusable, independent components
- **Reduced Overhead**: minimize initial development efforts

### Philosophy

- **Offline-First**: prioritize solutions that operate completely locally, without the need for internet connection
- **Embedded-First**: prioritize in-process solutions
- **Open-Source**: promote transparency, collaboration, and community-driven development

### Generative AI

- **Code Generation**: automate the production of efficient, modular code
- **Abstraction Generation**: create high-level, reusable code structures using AI

### User Interaction

- **Q&A**: provide question and answer mechanisms to support development needs
- **Chat**: allow user to communicate with AI through a chat interface
- **Configuration**: allow tool customization for tailored usage
- **Software Library**: provide reusable components and modules
- **Validation Checks**: ensure the code generated meets quality standards

### Content Validation

- **Code Failure by Default**: fail code generated without human validation
- **Function Calling**: allow custom validations through function calling
- **Traceability**: track content generation up to its origins
- **Watermarks**: embed identifiers for metadata purposes

### Information Retrieval

- **RAG**: use Retrieval-Augmented Generation
- **GraphRAG**: use graph-based approaches for structured data access
- **Contextual Retrieval**: enhance efficiency by considering retrieval context
- **Query Expansion Retrieval**: refine search queries for more relevant results

### Storage

- **VectorStore**: store abstractions and high-quality code along with their vectors
- **GraphDB**: store guidelines and rules in graph structures

### Tech Stack

- Python
- [LiteLLM](https://github.com/BerriAI/litellm)
- [Pydantic](https://github.com/pydantic/pydantic)
- [LanceDB](https://github.com/lancedb/lancedb)
- [Kùzu](https://github.com/kuzudb/kuzu)
