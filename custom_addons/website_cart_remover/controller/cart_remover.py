# -*- coding: utf-8 -*-

from odoo.http import request, Controller, route


class CartRemover(Controller):
    @route(['/shop/clear_cart'], type='json', auth="public", website=True)
    def clear_cart(self):
        order = request.website.sale_get_order()
        if order:
            for line in order.website_order_line:
                line.unlink()