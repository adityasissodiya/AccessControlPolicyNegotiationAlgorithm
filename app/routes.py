from flask import Flask, request, jsonify, abort
from app.logic import calculate_aggregate_utility, find_optimal_policy, check_for_consensus
from app.models import Policy, Stakeholder, Weight
from app import app, db

utility_threshold = 7  # Utility Threshold for Consensus

@app.route('/get/policies', methods=['GET'])
def get_policies():
    policies = Policy.query.all()
    return jsonify([{'policy_id': p.policy_id, 'name': p.name, 'details': p.details} for p in policies])

@app.route('/get/policy/<name>', methods=['GET'])
def get_policy_by_name(name):
    policy = Policy.query.filter_by(name=name).first()
    if policy:
        return jsonify({
            'policy_id': policy.policy_id,
            'name': policy.name,
            'details': policy.details
        })
    else:
        return 'Policy not found', 404

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

@app.route('/add/policies', methods=['POST'])
def add_policy():
    if not request.json or not 'name' in request.json or not 'details' in request.json:
        abort(400)  # bad request if missing JSON data
    new_policy = Policy(name=request.json['name'], details=request.json['details'])
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

if __name__ == '__main__':
    app.run(debug=True)