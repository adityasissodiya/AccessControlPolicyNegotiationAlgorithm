from flask import Flask, request, jsonify, abort
from app.logic import calculate_aggregate_utility, find_optimal_policy, check_for_consensus
from app.models import Policy, Stakeholder, Weight
from app import app, db

utility_threshold = 7  # Utility Threshold for Consensus

@app.route('/get/policies', methods=['GET'])
def get_policies():
    policies = Policy.query.all()
    return jsonify([{'policy_id': p.policy_id, 'name': p.name, 'details': p.details, 'description': p.description} for p in policies])

@app.route('/get/stakeholders', methods=['GET'])
def get_stakeholders():
    stakeholders = Stakeholder.query.all()
    return jsonify([{'stakeholder_id': s.stakeholder_id, 'name': s.name, 'influence': s.influence} for s in stakeholders])

@app.route('/get/stakeholder/<name>', methods=['GET'])
def get_stakeholder_by_name(name):
    stakeholder = Stakeholder.query.filter_by(name=name).first()
    if stakeholder:
        return jsonify({
            'stakeholder_id': stakeholder.stakeholder_id,
            'name': stakeholder.name,
            'influence': stakeholder.influence
        })
    else:
        return 'Stakeholder not found', 404

@app.route('/get/weights', methods=['GET'])
def get_weights():
    weights = Weight.query.all()
    return jsonify([{'weight_id': w.weight_id, 'stakeholder_id': w.stakeholder_id, 'policy_id': w.policy_id, 'weights': w.weights} for w in weights])

@app.route('/get/policy/<name>', methods=['GET'])
def get_policy_by_name(name):
    policy = Policy.query.filter_by(name=name).first()
    if policy:
        return jsonify({
            'policy_id': policy.policy_id,
            'name': policy.name,
            'details': policy.details,
            'description': policy.description
        })
    else:
        return 'Policy not found', 404

@app.route('/get/weight/<stakeholder_name>/<policy_name>', methods=['GET'])
def get_weight(stakeholder_name, policy_name):
    stakeholder = Stakeholder.query.filter_by(name=stakeholder_name).first()
    if not stakeholder:
        return jsonify({'error': 'Stakeholder not found'}), 404

    policy = Policy.query.filter_by(name=policy_name).first()
    if not policy:
        return jsonify({'error': 'Policy not found'}), 404

    weight_entry = Weight.query.filter_by(stakeholder_id=stakeholder.stakeholder_id, policy_id=policy.policy_id).first()
    if weight_entry:
        return jsonify({
            'stakeholder': stakeholder_name,
            'policy': policy_name,
            'weights': weight_entry.weights  # Returning the JSONB data directly
        })
    else:
        return jsonify({'error': 'No weights assigned by this stakeholder to this policy'}), 404

@app.route('/add/policies', methods=['POST'])
def add_policy():
    if not request.json or 'name' not in request.json or 'details' not in request.json:
        abort(400)
    new_policy = Policy(
        name=request.json['name'], 
        details=request.json['details'],
        description=request.json.get('description')  # Handle optional description
    )
    db.session.add(new_policy)
    db.session.commit()
    return jsonify({'message': 'Policy added successfully'}), 201

@app.route('/add/stakeholders', methods=['POST'])
def add_stakeholder():
    if not request.json or not 'name' in request.json or not 'influence' in request.json:
        abort(400)
    new_stakeholder = Stakeholder(name=request.json['name'], influence=request.json['influence'])
    db.session.add(new_stakeholder)
    db.session.commit()
    return jsonify({'message': 'Stakeholder added successfully'}), 201

@app.route('/add/weights', methods=['POST'])
def add_weight():
    if not request.json or not 'stakeholder_id' in request.json or not 'policy_id' in request.json or not 'weights' in request.json:
        abort(400)
    new_weight = Weight(stakeholder_id=request.json['stakeholder_id'], policy_id=request.json['policy_id'], weights=request.json['weights'])
    db.session.add(new_weight)
    db.session.commit()
    return jsonify({'message': 'Weight added successfully'}), 201

@app.route('/update/policy', methods=['POST'])
def update_policy():
    data = request.get_json()
    if not data or 'policy_name' not in data or 'details' not in data:
        return jsonify({'error': 'Missing policy name or details'}), 400

    policy_name = data['policy_name']
    policy = Policy.query.filter_by(name=policy_name).first()
    if not policy:
        return jsonify({'error': 'Policy not found'}), 404

    try:
        policy.details = data['details']
        policy.description = data.get('description', policy.description)  # Update description if provided
        db.session.commit()
        return jsonify({'message': 'Policy updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/update_stakeholder', methods=['POST'])
def update_stakeholder():
    data = request.json
    stakeholder_id = data.get('stakeholder_id')
    influence = data.get('influence')
    try:
        stakeholder = Stakeholder.query.get(stakeholder_id)
        if stakeholder:
            stakeholder.influence = float(influence)
            db.session.commit()
            return jsonify({'message': 'Stakeholder updated successfully'}), 200
        else:
            return jsonify({'message': 'Stakeholder not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
@app.route('/update_stakeholder_by_name', methods=['POST'])
def update_stakeholder_by_name():
    data = request.json
    name = data.get('name')  # Retrieve the name from the request data
    influence = data.get('influence')
    
    try:
        # Query the database to find the stakeholder by name
        stakeholder = Stakeholder.query.filter_by(name=name).first()
        if stakeholder:
            stakeholder.influence = float(influence)
            db.session.commit()
            return jsonify({'message': 'Stakeholder updated successfully'}), 200
        else:
            return jsonify({'message': 'Stakeholder not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/update/weights', methods=['POST'])
def update_weights():
    if not request.json or 'policy_name' not in request.json or 'stakeholder_name' not in request.json or 'weights' not in request.json:
        abort(400, description="Missing policy_name, stakeholder_name, or weights in request")

    policy_name = request.json['policy_name']
    stakeholder_name = request.json['stakeholder_name']
    weights = request.json['weights']

    # Fetch the policy and stakeholder by name
    policy = Policy.query.filter_by(name=policy_name).first()
    if not policy:
        return jsonify({'error': f"Policy named '{policy_name}' not found"}), 404

    stakeholder = Stakeholder.query.filter_by(name=stakeholder_name).first()
    if not stakeholder:
        return jsonify({'error': f"Stakeholder named '{stakeholder_name}' not found"}), 404

    # Check if there is already an entry in the Weight table
    weight_entry = Weight.query.filter_by(stakeholder_id=stakeholder.stakeholder_id, policy_id=policy.policy_id).first()
    if weight_entry:
        weight_entry.weights = weights
        action = 'Updated'
    else:
        weight_entry = Weight(stakeholder_id=stakeholder.stakeholder_id, policy_id=policy.policy_id, weights=weights)
        db.session.add(weight_entry)
        action = 'Created'

    db.session.commit()
    return jsonify({'message': f'Weights {action} successfully'}), 201 if action == 'Created' else 200

def fetch_all_policies_with_weights():
    # Fetch all policies
    policies = Policy.query.all()
    policy_list = []
    for policy in policies:
        # Fetch weights related to the current policy
        weights = Weight.query.filter_by(policy_id=policy.policy_id).all()
        # Convert weights to a list of dictionaries showing stakeholder and weight
        weights_list = [{'stakeholder_id': weight.stakeholder_id, 'weights': weight.weights} for weight in weights]
        # Append policy details and associated weights
        policy_list.append({
            'policy_id': policy.policy_id,
            'name': policy.name,
            'details': policy.details,
            'weights': weights_list
        })
    return policy_list


def fetch_all_stakeholders_with_weights():
    stakeholders = Stakeholder.query.all()
    stakeholder_list = []
    for stakeholder in stakeholders:
        # Fetch weights related to the current stakeholder
        weights_entries = Weight.query.filter_by(stakeholder_id=stakeholder.stakeholder_id).all()
        # Prepare a list of all weight dictionaries for the current stakeholder
        weights_list = [weight.weights for weight in weights_entries]  # Directly use the JSONB data
        stakeholder_list.append({
            'stakeholder_id': stakeholder.stakeholder_id,
            'name': stakeholder.name,
            'influence': stakeholder.influence,
            'weights': weights_list  # This is now a list of dictionaries
        })
    return stakeholder_list

@app.route('/calculate/optimal_policy', methods=['POST'])
def calculate_optimal_policy():
    data = request.get_json()
    utility_threshold = float(data.get('utilityThreshold', 0.75))  # Default to 0.75 if not provided
    alpha_enabled = data.get('alphaEnabled', True)  # Default to True if not provided

    policies = fetch_all_policies_with_weights()
    stakeholders = fetch_all_stakeholders_with_weights()

    if not policies or not stakeholders:
        return jsonify({'error': 'Missing policies or stakeholders'}), 400

    alpha = {stakeholder['name']: stakeholder['influence'] for stakeholder in stakeholders} if alpha_enabled else None

    # Calculate aggregate utilities
    aggregate_utilities = calculate_aggregate_utility(policies, stakeholders, alpha)

    # Find the optimal policy
    optimal_policy_name, optimal_policy_score = find_optimal_policy(aggregate_utilities)

    # Find the full policy details from the list using the optimal policy name
    optimal_policy = next((policy for policy in policies if policy['name'] == optimal_policy_name), None)
    if not optimal_policy:
        return jsonify({'error': 'Optimal policy not found'}), 404

    # Check for consensus
    consensus, stakeholders_utilities = check_for_consensus(optimal_policy, stakeholders, utility_threshold)

    return jsonify({
        'optimal_policy': optimal_policy_name,
        'optimal_policy_score': optimal_policy_score,
        'consensus': consensus,
        'stakeholders_utilities': stakeholders_utilities
    })

if __name__ == '__main__':
    app.run(debug=True)