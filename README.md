# Access Control Policy Negotiation Algorithm Experiment

This repository contains the implementation and experimental setup for evaluating the access control policy negotiation algorithm. The algorithm optimizes policy selection based on the collective preferences of multiple stakeholders through utility functions.

## Objective

The primary objective of this experiment is to validate the effectiveness of the policy negotiation algorithm in identifying the optimal policy $(P^*\)$ that maximizes aggregate utility, considering diverse stakeholder preferences and criteria such as security, usability, and compliance.

## Experiment Setup

### Data Preparation

- **Policies $(P\)$**: A predefined set of potential access control policies with varied attributes.
- **Stakeholders $(A\)$**: A group of stakeholders with distinct preferences, represented by weights $(w_{a_i,l}\)$ assigned to different criteria.
- **Criteria Evaluation Functions $(f_l(P_j)\))$**: Functions that assess policies based on specific criteria.

### Implementation Steps

![alt text](https://github.com/adityasissodiya/abacPolicyNegotiationAlgorithm/blob/main/figures/algorithmFlowchart.png)

1. **Utility Evaluation**: Calculate the utility for each policy from each stakeholder's perspective.
2. **Aggregate Utility Calculation**: Compute the aggregate utility for each policy.
3. **Optimization**: Identify the policy that maximizes aggregate utility.
4. **Consensus Check**: Determine if the optimal policy achieves consensus among stakeholders.
5. **Policy Selection**: Select the policy if it meets consensus; otherwise, adjust and iterate.

**Please find the real world scenario implementaion in the /realWorldScenario directory of the repository.**

# Policy Evaluation Tool

The Policy Evaluation Tool is designed to assist in the evaluation and optimization of various policies by considering the influence of stakeholders and their assigned weights to different policy attributes. This tool allows users to add policies and stakeholders, assign and update weights, and calculate the optimal policy based on the aggregate utility of each policy while considering the consensus among stakeholders.

![alt text](https://github.com/adityasissodiya/abacPolicyNegotiationAlgorithm/blob/main/figures/indexHtmlScreenshot.png)

## Features

- **Add Policies**: Users can add new policies with specific attributes such as security, utility, privacy, and accessibility scores.
- **Add Stakeholders**: Users can add stakeholders and define their influence levels.
- **Update Policies & Stakeholders**: Users can update policies and stakeholders.
- **Delete Policies & Stakeholders**: Users can delete policies and stakeholders.
- **Assign Weights**: Assign weights to different policy attributes from the perspective of each stakeholder.
- **Calculate Optimal Policy**: Calculate which policy has the highest aggregate utility based on the weights assigned by all stakeholders.
- **Check Consensus**: Check if the optimal policy reaches a consensus among stakeholders based on a defined utility threshold.

## Installation

This application is built using Flask and PostgreSQL for the backend and simple HTML/CSS/JavaScript for the frontend. Here are the steps to get it up and running:

### Prerequisites

- Python 3.8 or higher
- Docker

### Build and run the docker container image
- sudo docker-compose exec web flask init-db (to initialize the database)
- sudo docker-compose up --build (to start the web and db containers)
- The application should now be running on http://localhost:5000.

### Access the application
- Navigate to app/templates/index.html and open the file in a browser.
- You can now interact with the tool.
- To shut the server down press Ctrl+C to gracefully bring down the containers.
- Run "sudo docker-compose down" and "sudo systemctl restart docker" if the containers aren't up after a shutdown.

### Access the database
- https://medium.com/@bennokohrs/connect-to-postgresql-database-inside-docker-container-7dab32435b49
- Check the docker-compose.yml file for credentials and database name.

## Figures
![alt text](https://github.com/adityasissodiya/abacPolicyNegotiationAlgorithm/blob/main/figures/stakeholderUtilityHeatmap.png)
![alt text](https://github.com/adityasissodiya/abacPolicyNegotiationAlgorithm/blob/main/figures/utilitiesDistributionBoxGraph.png)
![alt text](https://github.com/adityasissodiya/abacPolicyNegotiationAlgorithm/blob/main/figures/utilityScoreBarGraph.png)
![alt text](https://github.com/adityasissodiya/abacPolicyNegotiationAlgorithm/blob/main/figures/utilityScoreDistribution.png)
![alt text](https://github.com/adityasissodiya/abacPolicyNegotiationAlgorithm/blob/main/figures/consensusAchievementUtilityThreshold.png)
