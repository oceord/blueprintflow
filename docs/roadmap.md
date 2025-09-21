# BlueprintFlow Roadmap

This roadmap outlines the development trajectory of BlueprintFlow.
The milestones are ordered by development sequence.

## Phase 1: Core Functionality and Vector Store

**Objective**: Establish the foundational architecture for data storage and retrieval.

### Phase 1: Milestones

- [x] **Vector Store Functionality**
  - [x] Implement core vector store functionality using LanceDB
  - [x] Support CRUD operations for all entities
- [x] **Data Bootstrapping**
  - [x] Allow bootstrapping data into the datastore
  - [x] Provide utilities for initial data ingestion
- [x] **Similarity Search**
  - Implement similarity search using vector embeddings
- [ ] **Python Library Module**
  - [x] Create a Python module to connect with the datastore
  - [x] Provide methods for data ingestion
  - [ ] Provide methods for data retrieval

## Phase 2: Code Generation Workflow and Library Interface

**Objective**: Develop a base workflow for code generation and provide a Python interface for it.

### Phase 2 Milestones

- [ ] **Base Workflow**
  - [ ] Develop a base code generation workflow with hardcoded steps
  - [ ] Generate code from bootstrapped data and user requests
  - [ ] Apply similarity search only to patterns, abstractions, and code snippets
- [ ] **Library Interface**
  - Provide a Python library interface to call and orchestrate the workflow

## Phase 3: Accountability, Transparency, and Human Oversight

**Objective**: Ensure generated code is safe, reviewable, and transparent by requiring human validation, embedding metadata, and tracking its origin and context.

### Phase 3 Milestones

- [ ] **Human-in-the-Loop**
  - Ensure generated code requires explicit human review or fails by default
- [ ] **Traceability**
  - Track the origin and context of generated content
- [ ] **Metadata Embedding**
  - Embed watermarks and identifiers in generated code

## Phase 4: Dynamic Workflow

**Objective**: Dynamically determine workflow steps based on context and requirements.

### Phase 4 Milestones

- [ ] **Dynamic Workflow**
  - Use LLMs to dynamically determine workflow steps

## Phase 5: Smart Search and Contextual Retrieval

**Objective**: Enhance search capabilities with contextual and query expansion retrieval.

### Phase 5 Milestones

- [ ] **Similarity Search for All Entities**
  - Extend similarity search to support all entities in the datastore, beyond patterns and code
- [ ] **Smart Search**
  - Automatically refine queries for relevant code examples
- [ ] **Contextual Retrieval**
  - Consider surrounding context for code generation
- [ ] **Query Expansion Retrieval**
  - Expand queries to improve retrieval accuracy
- [ ] **Lexical Similarity**
  - Add lexical similarity search for keyword-based matches
- [ ] **Reranker**
  - Implement reranking of retrieved results for higher relevance

## Phase 6: Custom Validation and Abstraction Generation

**Objective**: Support custom validation and generate abstractions.

### Phase 6 Milestones

- [ ] **Custom Validation**
  - Allow users to define project-specific validation functions
- [ ] **Abstraction Generation**
  - Generate abstractions from existing patterns and code

## Phase 7: Non-Code Generation and User Interaction

**Objective**: Expand user interaction beyond the software library.

### Phase 7 Milestones

- [ ] **Non-Code Generation**
  - Support generating non-code artifacts (e.g, documentation, technical documents, usage guides, specifications)
- [ ] **User Interaction**
  - Add Q&A and chat interfaces for user interaction
- [ ] **Interactive Refinement**
  - Enable back-and-forth interaction between the LLM and the user to iteratively refine requirements and outputs
