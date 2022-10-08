import decimal
from decimal import Decimal
from datetime import datetime, time, timedelta


def conv_flot_totime(t):
    hour, minute = divmod(t, 1)
    minute *= 60
    return int(hour), int(minute)


def conv_time_float(value):
    vals = value.split(':')
    t, hours = divmod(float(vals[0]), 24)
    t, minutes = divmod(float(vals[1]), 60)
    minutes = minutes / 60.0
    return hours + minutes


if __name__ == '__main__':
    costo = 20
    slot = 60
    start_time = float(11)
    end_time = float(19.666666666666668)

    sh, ss = conv_flot_totime(start_time)
    eh, es = conv_flot_totime(end_time)
    start = time(sh, ss)
    end = time(eh, es)
    print(" Start time %s" % start)
    print(" End time %s" % end)
    decimal.getcontext().rounding = decimal.ROUND_HALF_EVEN
    ds = timedelta(hours=start.hour, minutes=start.minute)
    de = timedelta(hours=end.hour, minutes=end.minute)
    delta = de - ds
    print(conv_time_float(str(delta)))
    print(" time diff %s" % delta)
    minuti = delta.total_seconds() / 60
    ore = minuti / 60
    costo_al_minuto = (costo / slot)
    print("Costo al minuto %s" % costo_al_minuto)
    print("Ore totali di prenotazione: %s" % ore)
    print("Costo totale di prenotazione: %s" % decimal.Decimal(costo_al_minuto * minuti))
    print("Costo totale di prenotazione: %s" % decimal.Decimal(costo_al_minuto * minuti).quantize(Decimal("2.0")))
