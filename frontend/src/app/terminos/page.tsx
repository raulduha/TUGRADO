import type { Metadata } from "next";
import Link from "next/link";

import { LegalPage } from "@/components/legal-page";
import { contactLabel, ownerLabel } from "@/lib/legal";

export const metadata: Metadata = { title: "Términos y condiciones" };

export default function TermsPage() {
  return (
    <LegalPage title="Términos y condiciones">
      <p>
        Estos términos regulan el uso de Aprueba tu examen (apruebatuexamen.cl), un servicio de{" "}
        {ownerLabel()}. Al crear una cuenta o usar el servicio, los aceptas.
      </p>

      <h2>1. El servicio</h2>
      <p>
        Aprueba tu examen es una herramienta para preparar el examen de grado de Derecho: práctica
        con preguntas, simulación del examen oral con evaluación asistida por inteligencia
        artificial y un plan de estudio.
      </p>

      <h2>2. Sin garantía de resultado</h2>
      <ul>
        <li>
          Las evaluaciones son orientativas: no son una calificación oficial ni reemplazan la
          evaluación de una comisión examinadora.
        </li>
        <li>El uso del servicio no garantiza la aprobación del examen.</li>
        <li>
          Revisamos el contenido, pero puede contener errores o quedar desactualizado. No
          constituye asesoría legal. Si encuentras un error, puedes reportarlo desde la aplicación.
        </li>
      </ul>

      <h2>3. Tu cuenta</h2>
      <ul>
        <li>Debes entregar un correo válido y mantener tu contraseña en reserva.</li>
        <li>La cuenta es personal: no la compartas con otras personas.</li>
        <li>Eres responsable de la actividad realizada con tu cuenta.</li>
      </ul>

      <h2>4. Suscripción</h2>
      <ul>
        <li>
          El acceso a las funciones de estudio requiere una suscripción mensual de $9.990 (CLP),
          con 7 días de prueba gratis.
        </li>
        <li>
          El pago se procesa mediante Mercado Pago y se renueva automáticamente cada mes hasta que
          la canceles. Puedes cancelarla en cualquier momento desde la aplicación.
        </li>
        <li>
          Antes de habilitar los cobros informaremos aquí las condiciones de acceso posteriores a
          la cancelación y de reembolso.
        </li>
      </ul>

      <h2>5. Uso aceptable</h2>
      <ul>
        <li>No copies, vendas ni redistribuyas el contenido del servicio.</li>
        <li>No intentes acceder a cuentas o datos ajenos ni vulnerar la seguridad del servicio.</li>
        <li>No uses el servicio para fines ilícitos.</li>
      </ul>
      <p>Podemos suspender cuentas que incumplan estas reglas.</p>

      <h2>6. Propiedad intelectual</h2>
      <p>
        El contenido, el diseño y el software del servicio pertenecen a {ownerLabel()} o a sus
        licenciantes. Tus respuestas siguen siendo tuyas; nos autorizas a tratarlas para prestarte
        el servicio, según la <Link href="/privacidad" className="text-brand underline-offset-4 hover:underline">
          Política de privacidad
        </Link>.
      </p>

      <h2>7. Responsabilidad</h2>
      <p>
        Hacemos lo posible para que el servicio esté disponible y funcione correctamente, sin
        perjuicio de los derechos que te reconoce la legislación chilena de protección al
        consumidor.
      </p>

      <h2>8. Cambios y ley aplicable</h2>
      <p>
        Podemos actualizar estos términos; publicaremos la nueva versión aquí y, si el cambio es
        relevante, te avisaremos por correo. Estos términos se rigen por las leyes de Chile.
      </p>

      <h2>9. Contacto</h2>
      <p>
        Escríbenos a <strong>{contactLabel()}</strong>.
      </p>
    </LegalPage>
  );
}
