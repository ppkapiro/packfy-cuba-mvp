from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from envios.models import Envio

def enviar_notificacion_estado(envio, estado_anterior=None):
    """
    Envía notificaciones por email cuando cambia el estado de un envío
    """
    # Verificar si se debe enviar notificación al remitente, destinatario o ambos
    enviar_a_remitente = envio.remitente_email and '@' in envio.remitente_email
    enviar_a_destinatario = envio.destinatario_email and '@' in envio.destinatario_email
    
    if not (enviar_a_remitente or enviar_a_destinatario):
        return False  # No hay direcciones válidas para enviar
    
    # Preparar los datos para la plantilla
    context = {
        'envio': envio,
        'numero_guia': envio.numero_guia,
        'estado_actual': envio.get_estado_actual_display(),
        'estado_anterior': dict(Envio.EstadoChoices.choices).get(estado_anterior, None) if estado_anterior else None,
        'fecha_actualizacion': envio.ultima_actualizacion,
        'url_seguimiento': f"{getattr(settings, 'FRONTEND_URL', '')}/rastrear?guia={envio.numero_guia}"
    }
    
    # Determinar el asunto según el estado
    asunto = f"Envío #{envio.numero_guia} - "
    if envio.estado_actual == Envio.EstadoChoices.RECIBIDO:
        asunto += "Paquete recibido"
    elif envio.estado_actual == Envio.EstadoChoices.EN_TRANSITO:
        asunto += "En tránsito"
    elif envio.estado_actual == Envio.EstadoChoices.EN_REPARTO:
        asunto += "En proceso de entrega"
    elif envio.estado_actual == Envio.EstadoChoices.ENTREGADO:
        asunto += "Entregado satisfactoriamente"
    elif envio.estado_actual == Envio.EstadoChoices.DEVUELTO:
        asunto += "Paquete devuelto"
    elif envio.estado_actual == Envio.EstadoChoices.CANCELADO:
        asunto += "Envío cancelado"
    else:
        asunto += "Actualización de estado"
    
    # Renderizar la plantilla HTML
    html_message = render_to_string('emails/notificacion_estado.html', context)
    plain_message = strip_tags(html_message)
    
    # Preparar destinatarios
    destinatarios = []
    if enviar_a_remitente:
        destinatarios.append(envio.remitente_email)
    if enviar_a_destinatario:
        destinatarios.append(envio.destinatario_email)
    
    # Enviar el email a cada destinatario por separado
    try:
        for destinatario in destinatarios:
            send_mail(
                subject=asunto,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[destinatario],
                html_message=html_message,
                fail_silently=False,
            )
        return True
    except Exception as e:
        print(f"Error enviando notificación: {e}")
        return False
