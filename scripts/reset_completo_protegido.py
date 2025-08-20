#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
🔄 RESET COMPLETO PROTEGIDO
Reinicia completamente la base de datos con protección
'''

import os
import django
from protector_bd import requiere_autorizacion

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

@requiere_autorizacion("RESET COMPLETO DE BASE DE DATOS")
def reset_completo():
    '''Reset completo: flush + migrate + restaurar'''
    print("🔄 INICIANDO RESET COMPLETO...")

    print("1️⃣ Limpiando base de datos...")
    call_command('flush', '--noinput')

    print("2️⃣ Ejecutando migraciones...")
    call_command('migrate')

    print("3️⃣ Restaurando estructura...")
    exec(open('restaurar_estructura_20250820_095645.py').read())

    print("✅ RESET COMPLETO FINALIZADO")

if __name__ == "__main__":
    reset_completo()
