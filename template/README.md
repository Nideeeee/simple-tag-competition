# Student Submission Template

This directory contains the template for student submissions.

## Files

- `agent.py` - Template agent implementation that students should copy and modify

## Instructions for Students

1. Copy this `agent.py` to your submission directory: `submissions/<your_username>/agent.py`
2. Implement your agent logic in the `StudentAgent` class
3. Add any `.pth` model files to your submission directory
4. Test locally, then submit via Pull Request

## Template Structure

```python
class StudentAgent:
    def __init__(self, agent_type: str):
        # Initialize your agent (prey or predator)
        pass
    
    def get_action(self, observation, agent_id: str):
        # Return action based on observation
        pass
```

Your agent will be instantiated once per agent type and called repeatedly during evaluation episodes.
