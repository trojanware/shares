from django.http import HttpResponse
from django.db.models import Sum, Avg
from models import *
import json

def get_summary(request):
    ''' Returns data for summary screen '''

    summary = Transaction.objects.values('scrip__scrip_id', 'scrip__scrip_name', 'scrip__mkt_value', 'transaction_type').annotate(avg_rate=Avg('rate'), total_qty=Sum('qty')).order_by('scrip', 'transaction_type')
    computed_fields = _compute_fields(summary)
    serialized_data = json.dumps(computed_fields)
    return HttpResponse(serialized_data)


def _get_or_add_key(key, d, value=None):
    try:
	val = d[key]
	return val

    except KeyError:
	d[key] = value
	return False


def _add_common_fields(dest, src):
    dest['name'] = src['scrip__scrip_name']
    dest['current'] = src['scrip__mkt_value']


def _prepare_fields(summary):
    result = {}
    for info in summary:
	scrip_id = info['scrip__scrip_id']
	transaction_type = info['transaction_type']
	qty = info['total_qty']
	avg_rate = info['avg_rate']
	val = _get_or_add_key(scrip_id, result, {})
	if isinstance(val, bool) and not val:
	    _add_common_fields(result[scrip_id], info)

	result[scrip_id][transaction_type] = {
	    'qty': qty,
	    'avg_rate': avg_rate
	}
    return result


def _compute_fields(summary):
    prepared_fields = _prepare_fields(summary)
    computed_fields = []
    for scrip_id, info in prepared_fields.iteritems():
#Get total buy rate
	buy_info = info.get('BUY', {})
	buy_avg_rate = buy_info.get('avg_rate', 0)
	buy_qty = buy_info.get('qty', 0)
	info['BUY'] = {
	    'avg_rate': buy_avg_rate,
	    'qty': buy_qty
	}

	sell_info = info.get('SELL', {})
	sell_avg_rate = sell_info.get('avg_rate', 0)
	sell_qty = sell_info.get('qty', 0)
	info['SELL'] = {
	    'avg_rate': sell_avg_rate,
	    'qty': sell_qty
	}

	if sell_qty:
	    pl_booked = buy_avg_rate * sell_qty - sell_avg_rate * sell_qty
	else:
	    pl_booked = 0
	outstanding_shares = buy_qty - sell_qty

	info['id'] = scrip_id
	info['pl_booked'] = pl_booked
	info['outstanding_shares'] = outstanding_shares
	computed_fields.append(info)

    return computed_fields

