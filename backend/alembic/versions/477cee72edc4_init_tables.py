"""init tables

Revision ID: 477cee72edc4
Revises: 
Create Date: 2023-06-15 20:55:49.318398

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "477cee72edc4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.create_table(
        "conversation",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_conversation_id"), "conversation", ["id"], unique=False)
    op.create_table(
        "message",
        sa.Column("conversation_id", sa.UUID(), nullable=True),
        sa.Column("content", sa.String(), nullable=True),
        sa.Column(
            "role",
            postgresql.ENUM("user", "assistant", name="MessageRoleEnum"),
            nullable=True,
        ),
        sa.Column(
            "status",
            postgresql.ENUM("PENDING", "SUCCESS", "ERROR", name="MessageStatusEnum"),
            nullable=True,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["conversation_id"],
            ["conversation.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_message_id"), "message", ["id"], unique=False)
    op.create_table(
        "messagesubprocess",
        sa.Column("message_id", sa.UUID(), nullable=True),
        sa.Column("content", sa.String(), nullable=True),
        sa.Column(
            "source",
            postgresql.ENUM(
                "CHUNKING",
                "NODE_PARSING",
                "EMBEDDING",
                "LLM",
                "QUERY",
                "RETRIEVE",
                "SYNTHESIZE",
                "TREE",
                "CONSTRUCTED_QUERY_ENGINE",
                name="MessageSubProcessSourceEnum",
            ),
            nullable=True,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["message_id"],
            ["message.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_messagesubprocess_id"), "messagesubprocess", ["id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_messagesubprocess_id"), table_name="messagesubprocess")
    op.drop_table("messagesubprocess")
    op.drop_index(op.f("ix_message_id"), table_name="message")
    op.drop_table("message")
    op.drop_index(op.f("ix_conversation_id"), table_name="conversation")
    op.drop_table("conversation")
    # ### end Alembic commands ###
