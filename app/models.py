from app import db
from sqlalchemy.dialects.postgresql import JSONB 

class Policy(db.Model):
    __tablename__ = 'policies'
    policy_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    details = db.Column(JSONB, nullable=False)
    description = db.Column(db.String(1024), nullable=True)

class Stakeholder(db.Model):
    __tablename__ = 'stakeholders'
    stakeholder_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    influence = db.Column(db.Float, nullable=False)

class Weight(db.Model):
    __tablename__ = 'weights'
    weight_id = db.Column(db.Integer, primary_key=True)
    stakeholder_id = db.Column(db.Integer, db.ForeignKey('stakeholders.stakeholder_id'), nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey('policies.policy_id'), nullable=False)
    weights = db.Column(JSONB, nullable=False)