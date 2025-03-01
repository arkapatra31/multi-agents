from langchain_experimental.tools import PythonREPLTool
from langchain_core.tools import tool

@tool
def python_tool(code: str) -> str:
    """
    Name: Python REPL
    Description: A tool that can be used to generate and execute Python code.
    Usage: Run the code in a Python REPL and return the output.
    """
    python_repl = PythonREPLTool()
    return python_repl.run(tool_input=code)