# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

def migrate(cr, installed_version):
    """
    Migración adaptada del formato OpenUpgradeLib al formato nativo de Odoo.
    """
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Verificar si hay tags HTML en el campo note (ahora es JSON)
    cr.execute(
        """
        SELECT
            id
        FROM account_payment_mode
        WHERE note IS NOT NULL 
        AND jsonb_typeof(note::jsonb) IS NOT NULL
        AND EXISTS (
            SELECT 1 
            FROM jsonb_each_text(note::jsonb) AS t(key, value)
            WHERE value ~* '<[^>]+>'
        )
        LIMIT 1
        """
    )
    
    if cr.rowcount == 0:
        # Si no hay tags HTML en ninguna traducción, convertir a HTML
        cr.execute("""
            UPDATE account_payment_mode
            SET note = (
                SELECT jsonb_object_agg(
                    key,
                    CASE 
                        WHEN value IS NULL OR value = '' THEN value
                        ELSE '<p>' || REPLACE(REPLACE(value, E'\n', '</p><p>'), E'\r', '') || '</p>'
                    END
                )
                FROM jsonb_each_text(note::jsonb)
            )
            WHERE note IS NOT NULL 
            AND jsonb_typeof(note::jsonb) IS NOT NULL
        """)
