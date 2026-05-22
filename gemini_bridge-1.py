from google import genai
from google.genai import types
import os


def print_stage(stage: int, description: str):
    """
    Utility function to print stage headers in a consistent format.
    """
    print(f"--- STAGE {stage}: {description} ---")


class GeminiMythosBridge:
    """
    A bridge that applies the OpenMythos Recurrent-Depth Transformer (RDT)
    architecture logic to the Gemini API.

    Stages:
    1. Prelude: Initial codebase ingestion and "encoding".
    2. Recurrent Block: Iterative deepening of the analysis (Looped Reasoning).
    3. Coda: Final synthesis into a structured output.
    """

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        # API key is expected to be set in the environment variable GEMINI_API_KEY)
        self.client = genai.Client()
        self._model_name = model_name

    def generate_content(self, prompt: str) -> types.GenerateContentResponse:
        """
        Generates content using the Gemini API based on the provided prompt.
        """
        return self.client.models.generate_content(
            contents=prompt, model=self._model_name
        )

    def scan_project(self, project_path: str, n_loops: int = 3) -> str:
        """
        Scans a project directory using the OpenMythos looped reasoning approach.
        """
        # 1. PRELUDE: Load files and get initial understanding
        print_stage(1, "PRELUDE (Ingesting {project_path})")
        code_context = self._load_project_files(project_path)

        prelude_prompt = f"""
        System: You are the 'Prelude' stage of an OpenMythos RDT.
        Initial Encoding.

        Codebase:
        {code_context}

        Task: Provide a high-level architectural overview and identify the core components of this project.
        """

        response = self.generate_content(prelude_prompt)
        latent_thought = response.text
        print("Prelude complete.")

        # 2. RECURRENT BLOCK: Looped reasoning
        print_stage(2, f"RECURRENT BLOCK ({n_loops} Loops)")
        for i in range(n_loops):
            print(f"Loop {i + 1}/{n_loops}...")
            loop_prompt = f"""
            System: You are the 'Recurrent Block' stage of an OpenMythos RDT. 
            Reasoning Loop {i + 1}.

            Current Latent Thought: {latent_thought}

            Original Codebase: (Injected Signal)
            {code_context[:2000]}... [truncated]

            Task: Deepen your analysis. Identify potential bugs, security flaws,
            or architectural bottlenecks that weren't obvious in the previous
            iteration. Focus on the interaction between components.
            """

            response = self.generate_content(loop_prompt)
            latent_thought = response.text

        # 3. CODA: Final Synthesis
        print_stage(3, "CODA (Final Synthesis)")
        coda_prompt = f"""
        System: You are the 'Coda' stage of an OpenMythos RDT. Final Synthesis.

        Accumulated Reasoning: {latent_thought}

        Task: Format this entire analysis into a comprehensive, professional HTML report.
        Use CSS for styling. Include sections for Overview, Security, Architecture, and Recommendations.
        """

        response = self.generate_content(coda_prompt)
        print("Coda complete.")
        return str(response.text)

    def _load_project_files(self, project_path: str) -> str:
        """
        Reads files from the project path and concatenates them into a context string.
        """
        context = ""
        # Note: In a real scenario, we would filter for relevant files (e.g., .py, .js)
        # For now, we'll try to read the directory structure if possible.
        try:
            for root, _dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith((".py", ".md", ".txt", ".json")):
                        file_path = os.path.join(root, file)
                        print(f"Loading file: {file_path}")
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                context += f"\n--- File: {file} ---\n{f.read()}\n"
                        except Exception as e:
                            context += f"\n--- File: {file} (Error reading: {e}) ---\n"
        except Exception as e:
            return f"Error accessing directory: {e}"
        return context


def main():
    API_KEY = os.environ.get("GEMINI_API_KEY")
    if API_KEY is None:
        print("!!! Please set the GEMINI_API_KEY environment variable !!!")
        exit(1)

    # Example usage (Note: User must ensure path is accessible or files are moved)
    bridge = GeminiMythosBridge()
    print("GeminiMythosBridge initialized. Reading project files...")

    # We will need to adjust the path once the user provides access to the files
    report = bridge.scan_project(".", n_loops=3)
    print("Writing results to file")
    with open("mythos_report.html", "w", encoding="utf-8") as f:
        f.write(report)
    print("Done")


if __name__ == "__main__":
    main()
