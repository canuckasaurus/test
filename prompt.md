Prompt 1: Architectural Context & File Tree

Role: You are a Principal SDET and QA Architect.
Task: Analyze the provided directory structure and high-level architectural summary of this Elixir/Phoenix application.
Context: The system handles high-concurrency workflows, real-time state updates via LiveView, and complex domain logic (e.g., exception management, distributed state).
Input: [Insert tree command output or file structure] and [Insert a brief summary of the core domains/modules].
Action: Identify the core business domains and categorize the files into 1) Core Domain Logic, 2) Web/LiveView Interfaces, 3) External Integrations/APIs, and 4) Existing Test Modules. Do not generate code yet. Simply acknowledge the structure and list the top 5 most critical areas that require high test coverage.

Phase 2: Test Evaluation and Gap Analysis
Feed the actual code and existing tests into the model in logical chunks (e.g., domain by domain) to assess the current state.

Prompt 2: Integration and Functional Test Evaluation

Task: Evaluate the existing functional and integration tests for the [Insert Domain/Module Name] domain.
Input: > - Source code: [Insert source files for the domain]

Test code: [Insert existing _test.exs files for the domain]
Action: > 1. Analyze the existing tests. Are they effectively mocking external dependencies? Are they covering LiveView lifecycle events (mount, handle_event, handle_info) and complex state transitions?

Identify the gaps. List specific user journeys, edge cases, and integration points that currently lack functional or integration test coverage.

Categorize these gaps by severity (Critical, High, Medium) based on their impact on system stability and data integrity.

(Repeat Prompt 2 for each major domain or microservice in your repository).

Phase 3: The HTML Scorecard
Once the model has evaluated the domains, generate the visual report.

Prompt 3: Scorecard Generation

Task: Based on the test evaluation and gap analyses performed in the previous steps, generate a comprehensive Test Coverage Scorecard in a single, well-structured HTML file.
Requirements:

Styling: Use embedded CSS for a clean, modern, and professional dashboard look (e.g., using a minimalist corporate styling suitable for engineering leadership).

Summary Metrics: Include a top-level summary displaying estimated functional/integration coverage percentages, total existing tests, and total missing tests identified.

Detailed Breakdown: Create a table with the following columns: Domain/Module, Current Coverage Status (Good/Fair/Poor), Critical Missing Tests (bulleted list), and Risk Level.

Action Plan: A concluding section prioritizing which missing tests should be written first based on systemic risk.
Output: Output ONLY valid HTML/CSS code. Do not use markdown wrappers if possible, or ensure it is ready to be saved directly as an .html file.

Phase 4: Generating the Missing Tests
Now, instruct the model to write the tests it identified as missing, maintaining strict testing standards.

Prompt 4: Test Generation Strategy & Execution

Task: Write the missing functional and integration tests for [Insert Domain/Module Name] identified in the scorecard.
Guidelines:

Framework: Use ExUnit.

Style: Write idiomatic, robust code. Avoid brittle tests. Use setup blocks efficiently.

LiveView: For UI functional tests, use Phoenix.LiveViewTest. Ensure you are testing the actual rendered DOM and simulating real user interactions (e.g., render_click, render_change) rather than just testing pure functions.

Integrations: For external integrations, provide examples using standard mocking libraries (like Mox) to ensure the integration tests are deterministic and do not hit live external endpoints.

Data: Use factories (e.g., ExMachina) or robust fixtures for setting up test state.
Input: Provide the missing test scenarios you identified for this domain: [Copy/paste the specific missing tests from the scorecard for this domain].
Output: Generate the complete _test.exs file(s) required to close these gaps. Include comments explaining the intent behind complex assertions.
