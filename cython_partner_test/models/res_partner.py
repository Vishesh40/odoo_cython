from odoo import fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    demo_amount = fields.Float(string="Demo Amount", default=100.0)
    protected_result = fields.Float(string="Protected Result", readonly=True)

    def action_run_hidden_logic(self):
        try:
            from . import partner_secret
        except Exception as exc:
            raise UserError(
                f"Compiled hidden logic could not be loaded: {exc}"
            )

        for rec in self:
            rec.protected_result = partner_secret.compute_hidden_value(rec.demo_amount)

        return True