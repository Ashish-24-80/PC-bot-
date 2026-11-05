import sys
from pathlib import Path

# Force UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add SwarmSystem directory to system path
sys.path.append("C:/Users/SUBU/Documents/1MY_APPs/SwarmSystem")

from langchain_core.messages import HumanMessage
from graphs.hierarchical_graph import build_graph

def run_test():
    print("--- SWARM SYSTEM DIRECT GRAPH EXECUTION TEST ---")
    graph = build_graph()
    
    # Prompt the supervisor and coder with a task that requires the tool
    task = "Optimize a 3-dimensional sphere function using 64 particles and tell me the results."
    print(f"Task: {task}")
    
    result = graph.invoke({
        "messages": [HumanMessage(content=task)],
        "retry_count": 0
    })
    
    print("\n--- GRAPH EXECUTION COMPLETED ---")
    print(f"Total Messages: {len(result['messages'])}")
    
    for idx, msg in enumerate(result['messages']):
        print(f"\n[{idx}] Message Type: {type(msg).__name__}")
        print(f"Role/Sender: {getattr(msg, 'name', 'N/A') or 'N/A'}")
        print(f"Content:\n{msg.content}")
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            print(f"Tool Calls: {msg.tool_calls}")
        print("-" * 50)

if __name__ == "__main__":
    run_test()
