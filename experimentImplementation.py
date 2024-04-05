# Policies
policies = [
    {"name": "policyA", "security": 8, "utility": 9, "privacy": 5, "accessibility": 4},
    {"name": "policyB", "security": 4, "utility": 5, "privacy": 9, "accessibility": 8},
    {"name": "policyC", "security": 1, "utility": 2, "privacy": 3, "accessibility": 6}
]

# Stakeholders
stakeholders = [
    {"name": "car_workshop", "weights": {"security": 0.1, "utility": 0.7, "privacy": 0.2, "accessibility": 0.2}},
    {"name": "car_owner", "weights": {"security": 0.3, "utility": 0.3, "privacy": 0.4, "accessibility": 0.4}},
    {"name": "car_manufacturer", "weights": {"security": 0.6, "utility": 0.2, "privacy": 0.2, "accessibility": 0.6}},
    {"name": "insurance_company", "weights": {"security": 0.1, "utility": 0.7, "privacy": 0.2, "accessibility": 0.8}}
]

#Influence of Stakeholders
alpha = {
    "car_workshop": 1.5,  # Higher influence
    "car_owner": 1.0,     # Standard influence
    "car_manufacturer": 0.5,    # Lower influence
    "insurance_company": 0.2    #Lowest influence
}

# Utility Threshold for Consensus
utility_threshold = 7

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

# Calculate aggregate utilities
aggregate_utilities = calculate_aggregate_utility(policies, stakeholders, alpha)
print("Aggregate Utilities:", aggregate_utilities)

# Find the optimal policy
optimal_policy_name, optimal_policy_utility = find_optimal_policy(aggregate_utilities)
print(f"Optimal Policy: {optimal_policy_name} with Aggregate Utility: {optimal_policy_utility}")


# Get the optimal policy's details
optimal_policy = next(policy for policy in policies if policy['name'] == optimal_policy_name)

# Check for consensus
consensus, stakeholders_utilities = check_for_consensus(optimal_policy, stakeholders, utility_threshold)

# Display the results
print(f"Consensus Achieved: {consensus}")
for stakeholder, utility in stakeholders_utilities.items():
    print(f"{stakeholder}: Utility = {utility}")