# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuración de CORS
CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS", "https://localhost:3000,https://localhost:5173"
).split(",")
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]

# URL del frontend para las notificaciones
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://localhost:5173")
