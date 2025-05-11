# apps/api/debate-service/app/models/models.py
from sqlalchemy import Column, String, Boolean, Integer, Float, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, nullable=False)
    email = Column(String, unique=True)
    is_llm = Column(Boolean, nullable=False, default=False)
    llm_config_id = Column(String, ForeignKey("llm_configs.config_id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    llm_config = relationship("LLMConfig", back_populates="users")
    
class LLMConfig(Base):
    __tablename__ = "llm_configs"
    
    config_id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'debater', 'judge', 'moderator'
    model = Column(String, nullable=False)
    base_prompt = Column(Text, nullable=False)
    temperature = Column(Float, nullable=False, default=0.7)
    max_tokens = Column(Integer)
    other_params = Column(String)  # JSON string
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="llm_config")

class Debate(Base):
    __tablename__ = "debates"
    
    debate_id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    description = Column(String)
    proposition = Column(Text, nullable=False)
    format = Column(String, nullable=False)
    status = Column(String, nullable=False)
    moderator_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    time_limit_minutes = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    participants = relationship("DebateParticipant", back_populates="debate")
    turns = relationship("DebateTurn", back_populates="debate")
    moderator_comments = relationship("ModeratorComment", back_populates="debate")
    checkpoints = relationship("DebateCheckpoint", back_populates="debate")
    scores = relationship("DebateScore", back_populates="debate")

class DebateFormat(Base):
    __tablename__ = "debate_formats"
    
    format_id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    phases = Column(String, nullable=False)  # JSON array of phase names
    turn_limits = Column(String)  # JSON object mapping phases to turn limits
    structure = Column(String, nullable=False)  # 'strict', 'flexible'
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class DebateParticipant(Base):
    __tablename__ = "debate_participants"
    
    participant_id = Column(String, primary_key=True, default=generate_uuid)
    debate_id = Column(String, ForeignKey("debates.debate_id"), nullable=False)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    side = Column(String, nullable=False)  # 'affirmative', 'negative', 'moderator', 'judge'
    
    # Relationships
    debate = relationship("Debate", back_populates="participants")
    user = relationship("User")
    turns = relationship("DebateTurn", back_populates="participant")
    memories = relationship("LLMMemory", back_populates="participant")
    judge_scores = relationship("DebateScore", back_populates="judge", foreign_keys="DebateScore.judge_id")
    __table_args__ = (UniqueConstraint("debate_id", "user_id", name="unique_participant"),)


class DebateTurn(Base):
    __tablename__ = "debate_turns"
    
    turn_id = Column(String, primary_key=True, default=generate_uuid)
    debate_id = Column(String, ForeignKey("debates.debate_id"), nullable=False)
    participant_id = Column(String, ForeignKey("debate_participants.participant_id"), nullable=False)
    content = Column(Text, nullable=False)
    turn_number = Column(Integer, nullable=False)
    phase = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    tokens_used = Column(Integer)
    
    # Relationships
    debate = relationship("Debate", back_populates="turns")
    participant = relationship("DebateParticipant", back_populates="turns")
    moderator_comments = relationship("ModeratorComment", back_populates="turn")
    checkpoints = relationship("DebateCheckpoint", back_populates="last_turn")
    __table_args__ = (UniqueConstraint("debate_id", "turn_number", name="unique_turn_number"),)


class ModeratorComment(Base):
    __tablename__ = "moderator_comments"
    
    comment_id = Column(String, primary_key=True, default=generate_uuid)
    debate_id = Column(String, ForeignKey("debates.debate_id"), nullable=False)
    turn_id = Column(String, ForeignKey("debate_turns.turn_id"))
    content = Column(Text, nullable=False)
    comment_type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    debate = relationship("Debate", back_populates="moderator_comments")
    turn = relationship("DebateTurn", back_populates="moderator_comments")

class ScoringCriteria(Base):
    __tablename__ = "scoring_criteria"
    
    criteria_id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    max_score = Column(Integer, nullable=False, default=10)
    weight = Column(Float, nullable=False, default=1.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    criteria_scores = relationship("CriteriaScore", back_populates="criteria")

class DebateScore(Base):
    __tablename__ = "debate_scores"
    
    score_id = Column(String, primary_key=True, default=generate_uuid)
    debate_id = Column(String, ForeignKey("debates.debate_id"), nullable=False)
    judge_id = Column(String, ForeignKey("debate_participants.participant_id"), nullable=False)
    verdict_summary = Column(Text)
    winner_side = Column(String)  # 'affirmative', 'negative', 'tie'
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    debate = relationship("Debate", back_populates="scores")
    judge = relationship("DebateParticipant", back_populates="judge_scores", foreign_keys=[judge_id])
    criteria_scores = relationship("CriteriaScore", back_populates="debate_score")
    __table_args__ = (UniqueConstraint("debate_id", "judge_id", name="unique_judge_score"),)


class CriteriaScore(Base):
    __tablename__ = "criteria_scores"
    
    criteria_score_id = Column(String, primary_key=True, default=generate_uuid)
    score_id = Column(String, ForeignKey("debate_scores.score_id"), nullable=False)
    criteria_id = Column(String, ForeignKey("scoring_criteria.criteria_id"), nullable=False)
    score_value = Column(Integer, nullable=False)
    comment = Column(Text)
    
    # Relationships
    debate_score = relationship("DebateScore", back_populates="criteria_scores")
    criteria = relationship("ScoringCriteria", back_populates="criteria_scores")
    __table_args__ = (UniqueConstraint("score_id", "criteria_id", name="unique_criteria_score"),)

class DebateCheckpoint(Base):
    __tablename__ = "debate_checkpoints"
    
    checkpoint_id = Column(String, primary_key=True, default=generate_uuid)
    debate_id = Column(String, ForeignKey("debates.debate_id"), nullable=False)
    last_turn_id = Column(String, ForeignKey("debate_turns.turn_id"), nullable=False)
    checkpoint_data = Column(Text, nullable=False)  # JSON blob
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    debate = relationship("Debate", back_populates="checkpoints")
    last_turn = relationship("DebateTurn", back_populates="checkpoints")

class LLMMemory(Base):
    __tablename__ = "llm_memory"
    
    memory_id = Column(String, primary_key=True, default=generate_uuid)
    participant_id = Column(String, ForeignKey("debate_participants.participant_id"), nullable=False)
    debate_id = Column(String, ForeignKey("debates.debate_id"), nullable=False)
    memory_key = Column(String, nullable=False)
    memory_value = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    participant = relationship("DebateParticipant", back_populates="memories")
    __table_args__ = (UniqueConstraint("participant_id", "debate_id", "memory_key", name="unique_memory_key"),)
