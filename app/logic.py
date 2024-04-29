def calculate_utility(policy, stakeholder):
    """
    Calculate the utility of a policy for a given stakeholder.
    
    Parameters:
    - policy: A dictionary representing a policy with attributes and scores.
    - stakeholder: A dictionary representing a stakeholder with weights for each criterion.
    
    Returns:
    - Utility score as a float.
    """
    utility_score = 0
    for criterion, weight in stakeholder['weights'].items():
        policy_score = policy.get(criterion, 0)  # Default to 0 if criterion not in policy
        utility_score += weight * policy_score
    return utility_score

def calculate_aggregate_utility(policies, stakeholders, alpha):
    """
    Calculate the aggregate utility of each policy, considering all stakeholders.

    Parameters:
    - policies: A list of dictionaries, each representing a policy.
    - stakeholders: A list of dictionaries, each representing a stakeholder with weights for each criterion.
    - alpha: An optional list or dictionary of relative influences of stakeholders. If None, equal influence is assumed.
    
    Returns:
    - A dictionary with policy names as keys and their aggregate utility scores as values.
    """
    aggregate_utilities = {}
    for policy in policies:
        aggregate_utility = 0
        for i, stakeholder in enumerate(stakeholders):
            # Calculate the utility of the policy for the stakeholder
            utility = calculate_utility(policy, stakeholder)
            # Determine the influence factor for the stakeholder
            if alpha is None:
                stakeholder_influence = 1  # Equal influence if alpha is not provided
            else:
                stakeholder_influence = alpha.get(stakeholder['name'], 1)  # Default to 1 if not specified
            # Add to the aggregate utility
            aggregate_utility += stakeholder_influence * utility
        # Assign the calculated aggregate utility to the policy
        aggregate_utilities[policy['name']] = aggregate_utility
    return aggregate_utilities

def find_optimal_policy(aggregate_utilities):
    """
    Identify the policy with the highest aggregate utility.

    Parameters:
    - aggregate_utilities: A dictionary with policy names as keys and their aggregate utility scores as values.
    
    Returns:
    - A tuple containing the name of the optimal policy and its aggregate utility score.
    """
    # Find the policy with the maximum aggregate utility
    optimal_policy = max(aggregate_utilities.items(), key=lambda x: x[1])
    return optimal_policy

def check_for_consensus(optimal_policy, stakeholders, utility_threshold):
    """
    Check if the optimal policy achieves consensus among all stakeholders by meeting a minimum utility threshold.
    
    Parameters:
    - optimal_policy: The policy identified as optimal, represented as a dictionary.
    - stakeholders: A list of dictionaries, each representing a stakeholder with weights for each criterion.
    - utility_threshold: The minimum utility threshold (θ) that must be met for each stakeholder.
    
    Returns:
    - A boolean value indicating whether the policy achieves consensus.
    - A dictionary mapping each stakeholder's name to their utility score for the optimal policy.
    """
    consensus = True
    stakeholders_utilities = {}
    
    for stakeholder in stakeholders:
        # Calculate the utility of the optimal policy for the current stakeholder
        utility = calculate_utility(optimal_policy, stakeholder)
        stakeholders_utilities[stakeholder['name']] = utility
        # Check if the utility meets the threshold
        if utility < utility_threshold:
            consensus = False
    
    return consensus, stakeholders_utilities