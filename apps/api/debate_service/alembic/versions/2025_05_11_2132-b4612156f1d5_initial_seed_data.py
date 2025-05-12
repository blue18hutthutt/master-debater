"""initial seed_data

Revision ID: b4612156f1d5
Revises: c66b6ea45d9f
Create Date: 2025-05-11 21:32:57.081669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column, String, DateTime, Text, Integer, Float, Boolean
from datetime import datetime
import uuid
import json

# revision identifiers, used by Alembic.
revision: str = 'b4612156f1d5'
down_revision: Union[str, None] = 'c66b6ea45d9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Helper function for UUID generation
def generate_uuid():
    return str(uuid.uuid4())

def upgrade() -> None:
    # Current timestamp for created_at/updated_at fields
    now = datetime.utcnow()
    
    # Define table references for data insertion
    debate_formats = table('debate_formats',
        column('format_id', String),
        column('name', String),
        column('description', String),
        column('structure', String),
        column('created_at', DateTime),
        column('updated_at', DateTime)
    )
    
    debate_format_phases = table('debate_format_phases',
        column('phase_id', String),
        column('format_id', String),
        column('name', String),
        column('description', Text),
        column('sequence', Integer),
        column('prompt_template', Text),
        column('turn_limit', Integer),
        column('created_at', DateTime),
        column('updated_at', DateTime)
    )
    
    scoring_criteria = table('scoring_criteria',
        column('criteria_id', String),
        column('name', String),
        column('description', Text),
        column('max_score', Integer),
        column('weight', Float),
        column('created_at', DateTime),
        column('updated_at', DateTime)
    )
    
    llm_configs = table('llm_configs',
        column('config_id', String),
        column('name', String),
        column('role', String),
        column('model', String),
        column('base_prompt', Text),
        column('temperature', Float),
        column('max_tokens', Integer),
        column('other_params', String),
        column('created_at', DateTime),
        column('updated_at', DateTime)
    )
    
    users = table('users',
        column('user_id', String),
        column('username', String),
        column('email', String),
        column('is_llm', Boolean),
        column('llm_config_id', String),
        column('created_at', DateTime),
        column('updated_at', DateTime)
    )
    
    # Step 1: Insert debate formats
    format_ids = {
        'open_ended': generate_uuid(),
        'fixed_turn': generate_uuid(),
        'oxford': generate_uuid(),
        'lincoln_douglas': generate_uuid(),
        'popper': generate_uuid()
    }
    
    op.bulk_insert(debate_formats, [
        {
            'format_id': format_ids['open_ended'],
            'name': 'Open-Ended',
            'description': 'Flexible format with minimal structure',
            'structure': 'flexible',
            'created_at': now,
            'updated_at': now
        },
        {
            'format_id': format_ids['fixed_turn'],
            'name': 'Fixed-Turn (10)',
            'description': 'Simple debate with fixed number of turns alternating between sides',
            'structure': 'strict',
            'created_at': now,
            'updated_at': now
        },
        {
            'format_id': format_ids['oxford'],
            'name': 'Oxford Style',
            'description': 'Formal debate format with structured phases like opening statements, rebuttals, and closing arguments',
            'structure': 'strict',
            'created_at': now,
            'updated_at': now
        },
        {
            'format_id': format_ids['lincoln_douglas'],
            'name': 'Lincoln-Douglas',
            'description': 'One-on-one debate format with emphasis on substantive argumentation and cross-examination',
            'structure': 'strict',
            'created_at': now,
            'updated_at': now
        },
        {
            'format_id': format_ids['popper'],
            'name': 'Popper',
            'description': 'Format with initial positions followed by multiple rounds of free exchanges',
            'structure': 'strict',
            'created_at': now,
            'updated_at': now
        }
    ])
    
    # Step 2: Insert format phases
    # Create a dictionary of phase-specific prompts
    prompts = {
        # Open-Ended format
        'discussion': "Share your perspective on the topic, addressing previous points made in the discussion.",
        
        # Fixed-Turn format
        'debate': "Present your arguments {{position}} the proposition, responding to previous points made by your opponent.",
        
        # Oxford Style
        'opening_pro': "Present your initial arguments in favor of the proposition. Establish your key points and framework.",
        'opening_con': "Present your initial arguments against the proposition. Establish your key points and framework.",
        'rebuttal_pro': "Respond to the opposing side's arguments, defending your position and addressing their points.",
        'rebuttal_con': "Respond to the opposing side's arguments, defending your position and addressing their points.",
        'cross_examination': "Ask direct questions to probe weaknesses in your opponent's arguments. Be specific and focused.",
        'closing_pro': "Summarize your case in favor of the proposition, emphasizing your strongest points and addressing key counterarguments.",
        'closing_con': "Summarize your case against the proposition, emphasizing your strongest points and addressing key counterarguments.",
        
        # Lincoln-Douglas
        'affirmative_constructive': "Present a comprehensive case in favor of the proposition, outlining your value premise and criterion.",
        'cross_examination_1': "Ask questions to clarify and challenge aspects of your opponent's case.",
        'negative_constructive': "Present your case against the proposition, including both direct refutations and your own value framework.",
        'cross_examination_2': "Ask questions to clarify and challenge aspects of your opponent's case.",
        'affirmative_rebuttal': "Defend your case against criticisms and attack flaws in your opponent's arguments.",
        'negative_rebuttal': "Focus on the key points of clash in the debate, emphasizing the strongest arguments against the proposition.",
        'affirmative_conclusion': "Provide a final summary of why your framework and arguments should prevail in the debate.",
        
        # Popper
        'affirmative_position': "Present your initial case in favor of the proposition, establishing your main arguments.",
        'negative_position': "Present your initial case against the proposition, establishing your main arguments.",
        'exchange_1': "Engage directly with your opponent's arguments, highlighting strengths in your position and weaknesses in theirs.",
        'exchange_2': "Continue the debate, focusing on the key areas of disagreement that have emerged.",
        'exchange_3': "Address the most crucial points of clash in the debate, emphasizing your strongest arguments.",
        'affirmative_conclusion': "Summarize why the affirmative case remains stronger, addressing the main points of contention.",
        'negative_conclusion': "Summarize why the negative case remains stronger, addressing the main points of contention."
    }
    
    # Insert phases for each format
    # Open-Ended format phases
    op.bulk_insert(debate_format_phases, [
        {
            'phase_id': generate_uuid(),
            'format_id': format_ids['open_ended'],
            'name': 'discussion',
            'description': 'Free-form discussion of the topic',
            'sequence': 1,
            'prompt_template': prompts['discussion'],
            'turn_limit': None,
            'created_at': now,
            'updated_at': now
        }
    ])
    
    # Fixed-Turn format phases
    op.bulk_insert(debate_format_phases, [
        {
            'phase_id': generate_uuid(),
            'format_id': format_ids['fixed_turn'],
            'name': 'debate',
            'description': 'Alternating arguments between affirmative and negative positions',
            'sequence': 1,
            'prompt_template': prompts['debate'],
            'turn_limit': 10,
            'created_at': now,
            'updated_at': now
        }
    ])
    
    # Oxford Style format phases
    oxford_phases = [
        ('opening_pro', 'Initial presentation of arguments supporting the proposition', 1, 1),
        ('opening_con', 'Initial presentation of arguments opposing the proposition', 2, 1),
        ('rebuttal_pro', 'Response to opposing arguments from the affirmative side', 3, 1),
        ('rebuttal_con', 'Response to opposing arguments from the negative side', 4, 1),
        ('cross_examination', 'Direct questioning between debaters', 5, 3),
        ('closing_con', 'Final arguments and summary from the negative side', 6, 1),
        ('closing_pro', 'Final arguments and summary from the affirmative side', 7, 1)
    ]
    
    op.bulk_insert(debate_format_phases, [
        {
            'phase_id': generate_uuid(),
            'format_id': format_ids['oxford'],
            'name': phase_name,
            'description': description,
            'sequence': sequence,
            'prompt_template': prompts[phase_name],
            'turn_limit': turn_limit,
            'created_at': now,
            'updated_at': now
        }
        for phase_name, description, sequence, turn_limit in oxford_phases
    ])
    
    # Lincoln-Douglas format phases
    ld_phases = [
        ('affirmative_constructive', 'Initial affirmative case presentation', 1, 1),
        ('cross_examination_1', 'Negative questioning of affirmative', 2, 3),
        ('negative_constructive', 'Initial negative case presentation', 3, 1),
        ('cross_examination_2', 'Affirmative questioning of negative', 4, 3),
        ('affirmative_rebuttal', 'Affirmative defense and refutation', 5, 1),
        ('negative_rebuttal', 'Negative defense and refutation', 6, 1),
        ('affirmative_conclusion', 'Final affirmative summary', 7, 1)
    ]
    
    op.bulk_insert(debate_format_phases, [
        {
            'phase_id': generate_uuid(),
            'format_id': format_ids['lincoln_douglas'],
            'name': phase_name,
            'description': description,
            'sequence': sequence,
            'prompt_template': prompts[phase_name],
            'turn_limit': turn_limit,
            'created_at': now,
            'updated_at': now
        }
        for phase_name, description, sequence, turn_limit in ld_phases
    ])
    
    # Popper format phases
    popper_phases = [
        ('affirmative_position', 'Initial affirmative position statement', 1, 1),
        ('negative_position', 'Initial negative position statement', 2, 1),
        ('exchange_1', 'First exchange of arguments', 3, 2),
        ('exchange_2', 'Second exchange of arguments', 4, 2),
        ('exchange_3', 'Third exchange of arguments', 5, 2),
        ('affirmative_conclusion', 'Affirmative closing statement', 6, 1),
        ('negative_conclusion', 'Negative closing statement', 7, 1)
    ]
    
    op.bulk_insert(debate_format_phases, [
        {
            'phase_id': generate_uuid(),
            'format_id': format_ids['popper'],
            'name': phase_name,
            'description': description,
            'sequence': sequence,
            'prompt_template': prompts[phase_name],
            'turn_limit': turn_limit,
            'created_at': now,
            'updated_at': now
        }
        for phase_name, description, sequence, turn_limit in popper_phases
    ])
    
    # Step 3: Insert scoring criteria
    op.bulk_insert(scoring_criteria, [
        {
            'criteria_id': generate_uuid(),
            'name': 'Logical Reasoning',
            'description': 'Soundness of arguments, identification and avoidance of fallacies, strength of causal connections',
            'max_score': 10,
            'weight': 1.0,
            'created_at': now,
            'updated_at': now
        },
        {
            'criteria_id': generate_uuid(),
            'name': 'Evidence Quality',
            'description': 'Relevance of cited information, credibility of sources, appropriate use of data/statistics',
            'max_score': 10,
            'weight': 1.0,
            'created_at': now,
            'updated_at': now
        },
        {
            'criteria_id': generate_uuid(),
            'name': 'Responsiveness',
            'description': 'Direct engagement with opponent\'s arguments, quality of rebuttals, avoidance of straw man arguments',
            'max_score': 10,
            'weight': 1.0,
            'created_at': now,
            'updated_at': now
        },
        {
            'criteria_id': generate_uuid(),
            'name': 'Clarity & Organization',
            'description': 'Structured presentation of ideas, clear thesis and supporting points, effective use of examples',
            'max_score': 10,
            'weight': 1.0,
            'created_at': now,
            'updated_at': now
        },
        {
            'criteria_id': generate_uuid(),
            'name': 'Rhetorical Effectiveness',
            'description': 'Persuasiveness of language, strategic framing of arguments, appropriate tone for the context',
            'max_score': 10,
            'weight': 1.0,
            'created_at': now,
            'updated_at': now
        }
    ])
    
    # Step 4: Insert LLM configurations
    generic_base_prompt = """You are participating in a formal debate on the proposition: "{{proposition}}".

Your current role is: {{role}}

If you're a MODERATOR: Ensure civil discussion, enforce format rules, provide clarification, maintain balance, and offer meta-commentary while staying neutral.

If you're a JUDGE: Observe carefully and evaluate based on logical reasoning, evidence quality, responsiveness to opponent's arguments, clarity of ideas, and rhetorical effectiveness.

If you're a DEBATER: Make persuasive arguments {{position}} the proposition, using strong logic, compelling evidence, and effective rhetoric. Respond directly to your opponent's points and follow the format guidelines.

Current context: {{context}}"""
    
    config_ids = {
        'llama3_balanced': generate_uuid(),
        'llama3_precise': generate_uuid(),
        'llama3_creative': generate_uuid()
    }
    
    op.bulk_insert(llm_configs, [
        {
            'config_id': config_ids['llama3_balanced'],
            'name': 'Llama3 (Balanced)',
            'role': 'general',
            'model': 'llama3',
            'base_prompt': generic_base_prompt,
            'temperature': 0.7,
            'max_tokens': 1024,
            'other_params': json.dumps({"top_p": 0.95, "frequency_penalty": 0.0, "presence_penalty": 0.0}),
            'created_at': now,
            'updated_at': now
        },
        {
            'config_id': config_ids['llama3_precise'],
            'name': 'Llama3 (Precise)',
            'role': 'general',
            'model': 'llama3',
            'base_prompt': generic_base_prompt,
            'temperature': 0.3,
            'max_tokens': 1024,
            'other_params': json.dumps({"top_p": 0.85, "frequency_penalty": 0.1, "presence_penalty": 0.1}),
            'created_at': now,
            'updated_at': now
        },
        {
            'config_id': config_ids['llama3_creative'],
            'name': 'Llama3 (Creative)',
            'role': 'general',
            'model': 'llama3',
            'base_prompt': generic_base_prompt,
            'temperature': 0.9,
            'max_tokens': 1024,
            'other_params': json.dumps({"top_p": 0.98, "frequency_penalty": -0.2, "presence_penalty": 0.0}),
            'created_at': now,
            'updated_at': now
        }
    ])
    
    # Step 5: Insert admin user
    op.bulk_insert(users, [
        {
            'user_id': generate_uuid(),
            'username': 'Admin',
            'email': 'admin@example.com',
            'is_llm': False,
            'llm_config_id': None,
            'created_at': now,
            'updated_at': now
        }
    ])


def downgrade() -> None:
    # Delete seed data in reverse order
    op.execute("DELETE FROM users WHERE email = 'admin@example.com'")
    op.execute("DELETE FROM llm_configs WHERE role = 'general'")
    op.execute("DELETE FROM scoring_criteria")
    op.execute("DELETE FROM debate_format_phases")
    op.execute("DELETE FROM debate_formats")