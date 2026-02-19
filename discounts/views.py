from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Discount
import json

@require_POST
def apply_discount(request):
    data = json.loads(request.body)
    code = data.get('code', '').strip().upper()
    cart_total = float(data.get('cart_total', 0))

    try:
        discount = Discount.objects.get(code=code)
        if not discount.is_valid():
            return JsonResponse({'success': False, 'message': 'This discount code is expired or invalid.'})
        if cart_total < float(discount.minimum_order):
            return JsonResponse({'success': False, 'message': f'Minimum order of ₦{discount.minimum_order} required.'})
        new_total, saved = discount.apply(cart_total)
        return JsonResponse({
            'success': True,
            'discount_code': code,
            'discount_id': discount.id,
            'saved': float(saved),
            'new_total': float(new_total),
            'message': f'Discount applied! You saved ₦{saved:.2f}'
        })
    except Discount.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid discount code.'})
