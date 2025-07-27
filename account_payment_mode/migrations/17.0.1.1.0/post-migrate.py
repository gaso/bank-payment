# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

def migrate(cr, installed_version):
    """
    Migración adaptada del formato OpenUpgradeLib al formato nativo de Odoo.
    """
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Verificar si hay tags HTML en el campo note
    cr.execute(
        """
        SELECT
            id
        FROM account_payment_mode
        WHERE note::text ~* '<[^>]+>' LIMIT 1
        """
    )
    
    if cr.rowcount == 0:
        # Si no hay tags HTML en el campo note, convertirlo a HTML
        # Implementación manual de convert_field_to_html
        cr.execute("""
            UPDATE account_payment_mode
            SET note = '<p>' || COALESCE(note, '') || '</p>'
            WHERE note IS NOT NULL AND note != ''
        """)
