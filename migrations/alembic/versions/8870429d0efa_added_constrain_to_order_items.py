"""added constrain to order_items

Revision ID: 8870429d0efa
Revises: 5e762d1ed7da
Create Date: 2025-11-04 22:48:20.200429

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8870429d0efa"
down_revision: Union[str, Sequence[str], None] = "5e762d1ed7da"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "sqlite":
        # Use batch operations for SQLite
        with op.batch_alter_table("order_items") as batch_op:
            batch_op.create_unique_constraint(
                "uix_order_item_unique", ["order_id", "item_id"]
            )
    else:
        op.create_unique_constraint(
            "uix_order_item_unique", "order_items", ["order_id", "item_id"]
        )


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "sqlite":
        with op.batch_alter_table("order_items") as batch_op:
            batch_op.drop_constraint("uix_order_item_unique", type_="unique")
    else:
        op.drop_constraint(
            "uix_order_item_unique", "order_items", type_="unique"
        )
