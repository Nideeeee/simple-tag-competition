# Simple Tag Competition - RL Class Project

Welcome to the Simple Tag Competition! This project uses the [Simple Tag environment from PettingZoo's MPE](https://pettingzoo.farama.org/environments/mpe/simple_tag/).

## Overview

In this competition, you will train both **prey** and **predator** agents. Your agents will be evaluated against private reference implementations to measure their performance.

## Environment

- **Simple Tag**: A cooperative/competitive multi-agent environment where predators try to catch prey
- Multiple predators chase multiple prey in a continuous 2D space
- Predators are rewarded for catching prey; prey are rewarded for avoiding capture

## Submission Guidelines

### What to Submit

You must submit **via Pull Request** from your fork:

1. **One Python file**: `agent.py` - Contains your agent implementation
2. **Model weights** (optional): Any `.pth` files for your neural networks

### File Structure

Your submission should follow this structure:
```
submissions/<your_username>/
├── agent.py          # Required: Your agent implementation
├── prey_model.pth    # Optional: Your prey neural network weights
└── predator_model.pth # Optional: Your predator neural network weights
```

### Agent Implementation Requirements

Your `agent.py` must implement the following class:

```python
class StudentAgent:
    def __init__(self, agent_type: str):
        """
        Initialize your agent.
        
        Args:
            agent_type: Either "prey" or "predator"
        """
        pass
    
    def get_action(self, observation, agent_id: str):
        """
        Get action for the given observation.
        
        Args:
            observation: Agent's observation from the environment
            agent_id: Unique identifier for this agent instance
            
        Returns:
            action: Action to take in the environment
        """
        pass
```

See `template/agent.py` for a complete template.

### How to Submit

1. **Fork** this repository
2. **Create** your submission folder: `submissions/<your_username>/`
3. **Add** your `agent.py` (and optional `.pth` files)
4. **Create a Pull Request** to the main repository
5. **Wait** for automatic evaluation - results will appear on the [leaderboard](https://nathanael-fijalkow.github.io/simple-tag-competition/)

### Evaluation

- Your agents are evaluated against **private reference implementations**
- Seeds are set on the server side for reproducibility
- Each PR triggers automatic evaluation via GitHub Actions
- Results are published to the leaderboard immediately
- **Note**: PRs are not merged - they are only used for evaluation

### Rules

- You may use any RL algorithm (DQN, PPO, SAC, etc.)
- You may train your agents however you like
- You may use pre-trained models
- You can submit multiple times (new PRs will update your score)
- Do not modify files outside your submission folder
- Do not submit more than one Python file

## Local Development

### Installation

```bash
# Clone the repository
git clone https://github.com/nathanael-fijalkow/simple-tag-competition.git
cd simple-tag-competition

# Install dependencies
pip install -r requirements.txt
```

### Testing Your Agent Locally

```bash
python test_agent.py submissions/<your_username>/agent.py
```

## Leaderboard

Check the live leaderboard at: [https://nathanael-fijalkow.github.io/simple-tag-competition/](https://nathanael-fijalkow.github.io/simple-tag-competition/)

The leaderboard shows:
- Student username
- Prey score (average reward)
- Predator score (average reward)
- Submission timestamp
- Ranking