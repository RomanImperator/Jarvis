from interpreter import interpreter

class JarvisAgent:
    """
    Agent class that wraps Open Interpreter to perform tasks on the user's computer.
    """
    def __init__(self):
        # 1. Configure Open Interpreter to use a local LLM (Ollama running on Docker)
        interpreter.offline = True # Disable sending data to OpenAI for privacy
        interpreter.llm.model = "ollama/qwen2.5-coder:14b"
        interpreter.llm.api_base = "http://localhost:11434/v1"
        
        # 2. Security Configuration:
        # False = Autonomous mode (Powerful but risky, executes code without asking)
        # True = Safe mode (Asks for [y/n] confirmation before executing code)
        interpreter.auto_run = False 
        
        # 3. System Message (Agent Personality and Instructions)
        interpreter.system_message += """
        You are Jarvis. You execute tasks on the user's computer.
        Be concise, explain your steps briefly, but focus on action.
        """

    def perform_task(self, command):
        """
        Passes a natural language command to the agent for execution.
        
        Args:
            command (str): The task description.
            
        Returns:
            str: The result or status of the task.
        """
        print(f"[AGENT]: Received order -> {command}")
        
        # interpreter.chat returns a list of messages/actions
        # stream=True allows seeing the output in real-time in the terminal
        try:
            # Note: Open Interpreter handles the loop: Code -> Error -> Correction -> Code
            interpreter.chat(command)
            return "Task completed."
        except Exception as e:
            return f"I encountered a problem during execution: {e}"

# Quick test if running this file directly
if __name__ == "__main__":
    agent = JarvisAgent()
    agent.perform_task("Check how much free RAM is available on this system")