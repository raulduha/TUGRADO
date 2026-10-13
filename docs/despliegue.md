# Despliegue: desarrollo y producción

## Arquitectura

| Pieza | Desarrollo | Producción |
|---|---|---|
| Frontend (Next.js) | `pnpm dev` en `http://localhost:3000` | Vercel, proyecto `tugrado`, dominio `apruebatuexamen.cl` (`www` redirige con 308) |
| Backend (FastAPI) | Docker Compose, `http://127.0.0.1:8000`, recarga en caliente | Render, servicio `apruebatuexamen-api` (Docker, Ohio), dominio `api.apruebatuexamen.cl` |
| Base de datos | Docker, `pgvector/pgvector:pg18` | Neon, proyecto `grado` (Ohio, PostgreSQL 18, `pgvector`) |
| Correo | `EMAIL_PROVIDER=console` (en el log del backend) | Resend, remitente `no-reply@apruebatuexamen.cl` |
| Pagos | `BILLING_PROVIDER=fake` (simulador) | Mercado Pago (pendiente de credenciales) |
| DNS | — | Vercel DNS (NIC Chile delega a `ns1/ns2.vercel-dns.com`) |

El navegador solo habla con el frontend: Vercel reenvía `/api/*` a `BACKEND_URL`. Por eso la cookie de sesión es de primera parte y el backend acepta únicamente el `Origin` de `FRONTEND_BASE_URL`.

## Cómo se despliega

- **Backend:** cada merge a `main` despliega en Render. `backend/start.sh` aplica `alembic upgrade head` y arranca la API, porque el plan gratuito no tiene comando previo al despliegue.
- **Frontend:** cada merge a `main` despliega en Vercel (producción); cada PR genera una vista previa. `BACKEND_URL` debe existir en Production y Preview, o la compilación falla a propósito.
- **CI** (`.github/workflows/ci.yml`): en cada PR corre ruff, migraciones, `alembic check` y pytest contra PostgreSQL 18, y lint, tipos y compilación del frontend.

Para volver atrás: en Render y en Vercel se puede volver a publicar un despliegue anterior desde su panel. Las migraciones no se revierten solas; si una migración falla, el contenedor no arranca y queda activo el despliegue anterior.

## Variables de entorno de producción

Los valores de negocio son los mismos de `.env.example`. Cambian estos:

| Variable | Producción | Nota |
|---|---|---|
| `APP_ENV` | `production` | Hoy está en `development` (entorno de pruebas) hasta tener Mercado Pago. Con `production` el backend no arranca si hay simulador de pagos, correo por consola o cookies sin `Secure`. |
| `DATABASE_URL` | Conexión **directa** de Neon (sin `-pooler`), con `postgresql+psycopg://` y `sslmode=require` | El pooler en modo transacción interfiere con Alembic y las sentencias preparadas de psycopg. |
| `FRONTEND_BASE_URL` | `https://apruebatuexamen.cl` | Base de los enlaces de correo y único `Origin` aceptado. |
| `AUTH_COOKIE_SECURE` | `true` | |
| `EMAIL_PROVIDER` / `RESEND_API_KEY` | `resend` / clave "render-produccion" | Clave solo de envío, limitada al dominio. |
| `BILLING_PROVIDER` | `mercadopago` | Requiere `MERCADOPAGO_ACCESS_TOKEN` y `MERCADOPAGO_WEBHOOK_SECRET`. |

Vercel solo necesita `BACKEND_URL=https://api.apruebatuexamen.cl` (Production y Preview).

Los secretos viven únicamente en los paneles de Render y Vercel; nunca en el repositorio.

## Antes de abrir a usuarios reales

1. Credenciales de Mercado Pago y webhook a `https://api.apruebatuexamen.cl/billing/webhooks/mercadopago`.
2. `APP_ENV=production` y `BILLING_PROVIDER=mercadopago` en Render.
3. Plan Starter en Render: el gratuito se suspende sin uso y los webhooks deben responderse en menos de 22 s.
4. Revisión tributaria y de consumidor (README, pendiente 7).
