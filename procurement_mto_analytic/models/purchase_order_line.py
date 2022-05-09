# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _find_candidate(self, product_id, product_qty, product_uom,
            location_id, name, origin, company_id, values):
        so_account_analytic = (
            values["move_dest_ids"][0].sale_line_id.order_id.analytic_account_id
            if values["move_dest_ids"] else None
        )
        lines = self.filtered(
            lambda po_line: po_line.account_analytic_id == so_account_analytic
        ) if so_account_analytic else self
        return super(PurchaseOrderLine, lines)._find_candidate(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
        )

    @api.model
    def _prepare_purchase_order_line_from_procurement(
        self, product_id, product_qty, product_uom, company_id, values, po
    ):
        so_account_analytic = (
            values["move_dest_ids"][0].sale_line_id.order_id.analytic_account_id
            if values["move_dest_ids"]
            else None
        )
        res = super()._prepare_purchase_order_line_from_procurement(
            product_id, product_qty, product_uom, company_id, values, po
        )
        if so_account_analytic:
            res["account_analytic_id"] = so_account_analytic.id
        return res
