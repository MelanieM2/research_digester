# research_digester

A Python automation pipeline for retrieving research papers, generating AI-assisted summaries, and maintaining a structured research archive.

The project is designed to support automated retrieval, summarization, and archival of research papers while following security-first development practices, reproducible environments, and automated backup workflows.

The current implementation uses geometric deep learning papers from arXiv as a demonstration dataset, but the architecture is intentionally modular and can be adapted to other research domains.

---

## Project Goals

* Automate retrieval of research paper metadata from external repositories
* Generate AI-assisted summaries using large language models
* Maintain a versioned research archive (`research_log.md`)
* Automate Git-based tracking of newly collected research
* Preserve research outputs through redundant local and remote backup strategies
* Demonstrate secure credential management and defensive automation practices

---

## Architecture Overview

The project follows three core design principles:

### Security by Default

Credentials are supplied through operating-system environment variables rather than being stored in source code. Runtime validation ensures required configuration is present before any API requests are made.

### Reproducible Development

Dependencies are managed through `uv`, providing isolated environments, deterministic dependency resolution, and simplified execution.

### Automated Knowledge Archival

Research outputs are treated as first-class artifacts. New summaries are appended to a structured research log and can be automatically versioned, synchronized, and backed up through the automation layer.

---

## Technical Stack

| Component             | Technology              |
| --------------------- | ----------------------- |
| Language              | Python 3.x              |
| Dependency Management | uv                      |
| AI Summarization      | Google Gemini API       |
| Automation            | Bash (`automate.sh`)    |
| Version Control       | Git + GitHub            |
| Backup                | rsync + Git mirror      |
| Environment           | Linux / WSL2-compatible |

---

## Repository Structure

```text
research_digester/
├── fetcher.py          # paper retrieval and AI summarization pipeline
├── automate.sh         # orchestration and backup automation
├── test_security.py    # runtime environment validation
├── research_log.md     # generated research archive
├── pyproject.toml      # project configuration and dependencies
├── uv.lock             # reproducible dependency lockfile
└── .gitignore          # excludes sensitive files and build artifacts
```

---

## Core Components

### fetcher.py

The main application pipeline responsible for collecting and processing research content.

Responsibilities include:

* Querying academic repositories
* Retrieving paper metadata
* Parsing structured responses
* Filtering relevant papers
* Generating AI-assisted summaries
* Producing entries for the research archive

The current implementation targets arXiv and summarizes papers related to geometric deep learning, but the retrieval and summarization workflow can be extended to other topics and data sources.

To improve reliability, the summarization layer includes defensive exception handling and graceful fallback behavior when external AI services are unavailable or rate-limited.

---

### test_security.py

A lightweight validation utility executed before running the main pipeline.

Responsibilities include:

* Verifying required environment variables exist
* Detecting missing credentials early
* Preventing execution with incomplete configuration
* Providing clear diagnostic feedback

The script follows a fail-fast philosophy: configuration problems are detected immediately rather than producing confusing runtime failures later in the workflow.

---

### research_log.md

The primary output artifact of the project.

This file serves as a structured, human-readable archive of collected research and generated summaries.

Typical workflow:

1. Paper metadata is retrieved.
2. AI-generated summaries are produced.
3. Results are appended to `research_log.md`.
4. Changes are tracked through Git.
5. Updates are synchronized to configured backup targets.

By treating research notes as version-controlled artifacts, the project maintains a searchable historical record of collected knowledge.

---

### automate.sh

The automation layer responsible for orchestrating the entire workflow.

The script executes the research pipeline, detects newly generated content, and performs synchronization and backup operations when updates are present.

Key responsibilities:

* Execute `fetcher.py`
* Detect modifications to `research_log.md`
* Create timestamped Git commits
* Push updates to configured remotes
* Trigger backup operations
* Avoid unnecessary synchronization when no new content exists

To maximize portability, the script dynamically determines its own location at runtime rather than relying on machine-specific paths.

A deliberate design choice is that automation focuses on generated research artifacts rather than source code changes. This prevents accidental commits of unfinished development work while still preserving newly collected research.

---

## Infrastructure Setup

### SSH Authentication

The project uses SSH-based Git authentication for repository synchronization.

Benefits include:

* Secure key-based authentication
* Elimination of password-based workflows
* Independence from platform-specific credential managers
* Improved portability across Linux environments

---

### Environment Variable Security

Sensitive configuration values are externalized into environment variables and never stored directly in source code.

Examples include:

* API credentials
* Backup host addresses
* Infrastructure-specific configuration

This approach allows the repository to remain public while keeping deployment-specific information private.

---

### Multi-Layer Backup Strategy

The project supports a redundant backup architecture built around multiple independent storage layers.

```text
Local Repository
        ↓
    GitHub Remote

Local Repository
        ↓
   Local Git Mirror

Local Repository
        ↓
     File Backup
```

Typical deployment may include:

* Local Git repository for development and offline history
* GitHub repository for remote storage and collaboration
* Local Git mirror for independent infrastructure-controlled redundancy
* File-level backups using rsync

This layered approach reduces dependence on any single storage location and improves long-term resilience.

---

## Security Practices

The project demonstrates several security-focused engineering practices:

* Credentials loaded exclusively from environment variables
* No hardcoded API keys or infrastructure addresses
* Global and repository-level Git ignore policies
* SSH key authentication for repository synchronization
* Runtime credential validation before execution
* Separation of generated data from source code changes

---

## Workflow Overview

```text
Fetch Paper Metadata
          ↓
Generate AI Summaries
          ↓
Update research_log.md
          ↓
Detect Changes
          ↓
Create Git Commit
          ↓
Synchronize Repositories
          ↓
Execute Backup Tasks
```

Only meaningful updates trigger synchronization and backup operations, minimizing unnecessary network traffic and repository noise.

---

## Installation

### Prerequisites

* Python 3.x
* uv
* A valid Gemini API key
* Git
* Optional: SSH access to a backup server
* Optional: rsync for file-level backups

### Setup

```bash
git clone <repository-url>
cd research_digester
uv sync
```

### Environment Variables

Required variables should be supplied through your shell environment and never committed to source control.

Example:

```bash
export GEMINI_API_KEY="your_api_key"
export BACKUP_SERVER_HOST="your_backup_server"
```

---

## Usage

### Run the full pipeline

```bash
./automate.sh
```

### Run the fetch-and-summarize pipeline directly

```bash
uv run fetcher.py
```

### Verify environment configuration

```bash
uv run test_security.py
```

---

## Design Philosophy

The project was built around a simple idea: research outputs should be treated as durable, version-controlled artifacts rather than temporary notes.

By combining automated retrieval, AI-assisted summarization, secure credential management, version control, and redundant backups, the system creates a repeatable workflow for building and maintaining a personal research knowledge base.






## Development Notes & AI Usage

### AI-Assisted Pair-Programming

This repository is the result of an independent learning and development workflow, not agentic automation. While Claude Sonnet 4.6 was used to:

* generate structural snippets,
* clarify unfamiliar concepts,
* explore architectural design options,
* review and iterate on code structure,
* accelerate development of boilerplate and automation logic,

its output was above all used as a learning foundation. I evaluated, corrected, and manually typed the implementation to ensure a personal understanding of system design principles in Linux and Python.

---

### Runtime AI Integration

In addition to development support, the system integrates the Google Gemini API (`gemini-3.1-flash-lite`) at runtime to perform automated summarization and metadata processing of research papers within the pipeline.

This allows the project to combine:

* deterministic automation (Python + Bash + Git)
* with probabilistic AI-based summarization (LLM inference)

---

## Project Context

This project is part of a broader personal engineering track focused on:

* Python-based automation systems
* Linux system architecture and infrastructure design
* Bash scripting for workflow automation
* Applied machine learning and LLM-integrated pipelines

The goal is to bridge theoretical foundations in mathematics and machine learning with practical systems engineering and production-style automation workflows.