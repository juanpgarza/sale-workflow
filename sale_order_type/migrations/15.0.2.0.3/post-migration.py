# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade  # pylint: disable=W7936
import logging

_logger = logging.getLogger(__name__)

# 12.0.1.1.1
def _fill_sale_order_type(cr):
    _logger.info("Fill type_id in sale order if null as it is now required")

    cr.execute(
        """
    UPDATE sale_order
    SET
        type_id=(SELECT id FROM sale_order_type ORDER BY id LIMIT 1)
    WHERE
        type_id is null
        """
    )

@openupgrade.migrate()
def migrate(env, version):
    # 12.0.1.1.1
    _fill_sale_order_type(env.cr)

    # 13.0.1.0.0
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_move am
        SET sale_type_id = ai.sale_type_id
        FROM account_invoice ai
        WHERE ai.move_name = am.name""",
    )
    # 13.0.1.0.0 y 14.0.1.0.0
    openupgrade.load_data(
        env.cr, "sale_order_type", "migrations/15.0.2.0.3/noupdate_changes.xml"
    )
