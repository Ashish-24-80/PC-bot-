import sys
import logging

# Force UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.append("C:/Users/SUBU/Documents/1MY_APPs/SwarmSystem")

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from graphs.hierarchical_graph import build_graph

# Set up logging so we can see the supervisor/coder logs clearly
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def run_test():
    print("--- SWARM SYSTEM DIRECT CODE CORRECTION LOOP TEST ---")
    graph = build_graph()
    
    # We will pass a prompt to the Coder that forces it to run a script that WILL raise a runtime error,
    # so we can observe the graph looping back to coder via retry node!
    task = (
        "Write a Python script that loads a list of numbers from 1 to 5, tries to retrieve the 10th index, "
        "and handles the exception. BUT wait, actually, write a python script that throws an IndexError "
        "intentionally on execution so we can test self-correction. Use the execute_code tool."
    )
    print(f"Task: {task}")
    
    # We will trigger the graph.
    result = graph.invoke({
        "messages": [HumanMessage(content=task)],
        "retry_count": 0
    })
    
    print("\n--- GRAPH EXECUTION COMPLETED ---")
    print(f"Total Messages: {len(result['messages'])}")
    
    for idx, msg in enumerate(result['messages']):
        print(f"\n[{idx}] Message Type: {type(msg).__name__}")
        print(f"Content:\n{msg.content[:400]}")
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            print(f"Tool Calls: {msg.tool_calls}")
        print("-" * 50)

if __name__ == "__main__":
    run_test()
