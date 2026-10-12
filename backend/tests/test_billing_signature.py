"""Firma de webhooks de Mercado Pago, con los casos de prueba del SDK oficial de Python."""

import hashlib
import hmac

import pytest

from app.billing.signature import InvalidSignature, verify

# Valores de tests/test_webhook_signature_validator.py del SDK oficial (MIT).
SECRET = "your_secret_key_here"
REQUEST_ID = "2066ca19-c6f1-498a-be75-1923005edd06"
DATA_ID_RAW = "ORD01JQ4S4KY8HWQ6NA5PXB65B3D3"
DATA_ID_LOWER = "ord01jq4s4ky8hwq6na5pxb65b3d3"
TS = "1742505638683"


def sdk_hash(data_id, request_id, ts, secret):
    # Copia literal de compute_hash() del SDK: referencia independiente de nuestra implementación.
    parts = []
    if data_id:
        parts.append(f"id:{data_id}")
    if request_id:
        parts.append(f"request-id:{request_id}")
    parts.append(f"ts:{ts}")
    manifest = ";".join(parts) + ";"
    return hmac.new(secret.encode("utf-8"), manifest.encode("utf-8"), hashlib.sha256).hexdigest()


def header(h, ts=TS, version="v1"):
    return f"ts={ts},{version}={h}"


def test_firma_valida():
    verify(
        header(sdk_hash(DATA_ID_LOWER, REQUEST_ID, TS, SECRET)), REQUEST_ID, DATA_ID_LOWER, SECRET
    )


def test_data_id_en_mayusculas_se_conserva_tal_cual():
    signed = header(sdk_hash(DATA_ID_RAW, REQUEST_ID, TS, SECRET))
    verify(signed, REQUEST_ID, DATA_ID_RAW, SECRET)
    with pytest.raises(InvalidSignature):
        verify(signed, REQUEST_ID, DATA_ID_LOWER, SECRET)


def test_sin_request_id_se_omite_del_manifiesto():
    verify(header(sdk_hash(DATA_ID_LOWER, None, TS, SECRET)), None, DATA_ID_LOWER, SECRET)


def test_espacios_alrededor_se_ignoran():
    signed = header(sdk_hash(DATA_ID_LOWER, REQUEST_ID, TS, SECRET))
    verify(f"  {signed.replace(',', ' , ')}  ", f" {REQUEST_ID} ", DATA_ID_LOWER, SECRET)


@pytest.mark.parametrize(
    "bad_header",
    [None, "", "   ", "basura", f"v1={'0' * 64}", "ts=abc,v1=00", f"ts={TS}", f"ts={TS},v2=00"],
)
def test_encabezados_ausentes_o_malformados(bad_header):
    with pytest.raises(InvalidSignature):
        verify(bad_header, REQUEST_ID, DATA_ID_LOWER, SECRET)


def test_otra_clave_no_valida():
    signed = header(sdk_hash(DATA_ID_LOWER, REQUEST_ID, TS, "otra-clave"))
    with pytest.raises(InvalidSignature):
        verify(signed, REQUEST_ID, DATA_ID_LOWER, SECRET)


def test_otro_data_id_no_valida():
    signed = header(sdk_hash(DATA_ID_LOWER, REQUEST_ID, TS, SECRET))
    with pytest.raises(InvalidSignature):
        verify(signed, REQUEST_ID, "otro-id", SECRET)
