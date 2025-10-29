from box_correct_score import compute_score
import re

# Boxed format reward - checks if answer is within \boxed{} format
def boxed_format_reward(prompts, responses, answers):
    """
    Reward function for \boxed{} format.
    Awards points based on:
    - Contains \boxed{...} format: 0.5 points
    - \boxed{} has non-empty content: additional 0.3 points
    - \boxed{} contains a number: additional 0.2 points
    Total maximum: 1.0 points
    """
    rewards = []
    boxed_pattern = r'\\boxed\{([^}]*)\}'
    
    for response in responses:
        reward = 0.0
        match = re.search(boxed_pattern, response)
        
        if match:
            reward += 0.5  # Has boxed format
            content = match.group(1).strip()
            if content:  # Boxed content is non-empty
                reward += 0.3
                # Check if content is a number (integer or decimal, with optional negative sign)
                if content.replace('.', '', 1).replace('-', '', 1).isdigit():
                    reward += 0.2
        
        rewards.append(reward)
    
    return rewards


def boxed_correctness_reward(prompts, responses, answers, step=None):
    ret_rewards = []
    for response, answer in zip(responses, answers):
        reward = compute_score(solution_str=response, ground_truth=str(answer), is_longcot=False, is_use_math_verify=True)
        ret_rewards.append(reward)
        
    if step is not None and step % 5 == 0:
        print("=" * 50)
        print("question:\n", prompts[0], "\n")
        print("response:\n", responses[0], "\n")
        print("answer:\n", answers[0], "\n")
    print("reward:\n", ret_rewards[0], "\n")
        
    return ret_rewards
