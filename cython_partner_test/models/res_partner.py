from odoo import fields, models
from odoo.exceptions import UserError
import importlib
from importlib.machinery import EXTENSION_SUFFIXES
from pathlib import Path


class ResPartner(models.Model):
    _inherit = "res.partner"

    demo_amount = fields.Float(string="Demo Amount", default=100.0)
    protected_result = fields.Float(string="Protected Result", readonly=True)

    def action_run_hidden_logic(self):
        pkg_dir = Path(__file__).resolve().parent
        present_files = sorted(p.name for p in pkg_dir.iterdir() if p.name.startswith("partner_secret"))

        try:
            partner_secret = importlib.import_module(".partner_secret", package=__package__)
        except Exception as exc:
            raise UserError(
                "Compiled hidden logic could not be loaded.\n"
                f"Supported suffixes on this server: {EXTENSION_SUFFIXES}\n"
                f"Files present in models/: {present_files}\n"
                f"Original error: {exc}"
            )

        for rec in self:
            rec.protected_result = partner_secret.compute_hidden_value(rec.demo_amount)

        return True