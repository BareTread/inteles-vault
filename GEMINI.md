# GEMINI.md

## Directory Overview

This directory, "inteles-vault," is a comprehensive, highly-structured knowledge base and operational hub for the Romanian dream-interpretation website, [inteles.ro](https://inteles.ro). It is designed to be used by an AI Writer Agent to create, update, and monetize SEO-optimized content in a systematic and quality-controlled manner.

The vault contains everything from high-level content strategy and monetization plans to granular standard operating procedures (SOPs), content templates, and automation scripts. The core of the project is a set of Markdown files that guide the AI agent through the entire content lifecycle.

## Key Files

*   **`START-HERE.md`**: The primary entry point and guide for the AI Writer Agent. It outlines the core principles, a 3-step quick start guide, article structure templates, and common mistakes to avoid. **Always start here.**
*   **`00-INDEX.md`**: The central navigation hub for the entire vault, providing quick links to all major sections, including workflows, templates, and tracking documents.
*   **`SOP.md`**: Details the guiding philosophy and overarching Standard Operating Procedures for content creation, emphasizing user-first principles, evidence-based content, and strict monetization rules.
*   **`00-AGENT-CONTEXT/04-SEO-RUBRIC.md`**: A 100-point scoring rubric used to evaluate and score articles before publication. The target score is 80/100 to ensure high-quality, competitive content.
*   **`04-Monetization/MASTER-PRODUCTS-LIST.md`**: The master list of approved affiliate products from the 2Performant network. This is the single source of truth for monetization links.
*   **`07-Templates/`**: A directory containing various HTML snippets and content templates (e.g., for dream interpretation articles, info boxes, FAQ blocks) to ensure consistency and speed up creation.
*   **`03-MCP-Operations/`**: Contains guides for interacting with the WordPress site and the Pexels API, including command-line instructions.
*   **`scripts/`**: Contains Python scripts for automating repetitive tasks.
    *   `scripts/images/pexels_pipeline.py`: A key script that fetches images from Pexels, processes them into WebP format, and generates a manifest for WordPress integration.

## Usage and Workflows

This vault is not a static documentation site; it is an active, operational system. The primary workflow is as follows:

1.  **Initialization**: The AI agent starts by loading the context from critical files, primarily `START-HERE.md`, `SOP.md`, and the `04-SEO-RUBRIC.md`.
2.  **Task Definition**: The agent receives a task, which is typically to create a new article or update an existing one.
3.  **Content Creation**:
    *   The agent uses the templates from `07-Templates/` and follows the structure defined in `START-HERE.md`.
    *   It consults the `04-Monetization/MASTER-PRODUCTS-LIST.md` to select 1-2 relevant affiliate products.
    *   It writes comprehensive, user-focused content, often including psychological perspectives (Jung/Freud) and Romanian cultural context.
4.  **Image Processing**: The agent uses the `pexels_pipeline.py` script to find, download, and process relevant images for the article.
5.  **SEO & Quality Assurance**: Before publishing, the agent self-evaluates the article against the `04-SEO-RUBRIC.md` to ensure it meets the ≥80/100 quality threshold.
6.  **Publishing**: The agent uses the commands and workflows outlined in `03-MCP-Operations/` to publish the final content to the inteles.ro WordPress site.
7.  **Tracking**: Finally, the agent updates the `09-Tracking/Article-Pipeline.md` to log the work and maintain a clear overview of the content status.

This structured process ensures that every piece of content is high-quality, well-monetized, and aligned with the overall project strategy.
