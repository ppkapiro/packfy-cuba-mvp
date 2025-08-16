from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Refresca la materialized view envio_estado_stats (si existe)"

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cur:
                # Verificar existencia
                cur.execute(
                    """
                    SELECT to_regclass('public.envio_estado_stats') IS NOT NULL;
                    """
                )
                exists = cur.fetchone()[0]
                if not exists:
                    self.stdout.write(
                        self.style.WARNING(
                            "La materialized view 'envio_estado_stats' no existe."
                        )
                    )
                    return

                # Intentar concurrente (requiere índice único)
                try:
                    cur.execute(
                        "REFRESH MATERIALIZED VIEW CONCURRENTLY envio_estado_stats;"
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            "Materialized view refrescada (concurrently)"
                        )
                    )
                except (
                    Exception
                ) as concurrent_err:  # fallback a no concurrente
                    self.stdout.write(
                        self.style.WARNING(
                            f"Fallo CONCURRENTLY: {concurrent_err}. Intentando sin concurrently..."
                        )
                    )
                    cur.execute(
                        "REFRESH MATERIALIZED VIEW envio_estado_stats;"
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            "Materialized view refrescada (non-concurrent)"
                        )
                    )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f"No se pudo refrescar la vista: {e}")
            )
