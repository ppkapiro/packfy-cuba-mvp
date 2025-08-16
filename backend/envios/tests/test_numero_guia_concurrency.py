import threading

import pytest
from envios.models import Envio
from usuarios.models import Usuario


@pytest.mark.django_db
def test_numero_guia_concurrente_generacion():
    user = Usuario.objects.create_user(
        email="t@t.com", password="x", username="t"
    )
    generated = []
    errors = []

    def create_envio(idx):
        try:
            e = Envio.objects.create(
                descripcion=f"pkg {idx}",
                peso=1.0,
                remitente_nombre="R",
                remitente_direccion="D",
                remitente_telefono="123",
                destinatario_nombre="Dest",
                destinatario_direccion="Dir",
                destinatario_telefono="456",
                creado_por=user,
                actualizado_por=user,
            )
            generated.append(e.numero_guia)
        except Exception as ex:  # noqa
            errors.append(str(ex))

    threads = [
        threading.Thread(target=create_envio, args=(i,)) for i in range(10)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors, f"Errores durante concurrencia: {errors}"
    assert len(generated) == 10
    assert len(set(generated)) == 10, "numero_guia debe ser único"
