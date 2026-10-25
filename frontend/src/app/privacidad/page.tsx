import type { Metadata } from "next";

import { LegalPage } from "@/components/legal-page";
import { contactLabel, ownerLabel } from "@/lib/legal";

export const metadata: Metadata = { title: "Política de privacidad" };

export default function PrivacyPage() {
  return (
    <LegalPage title="Política de privacidad">
      <p>
        Aprueba tu examen (apruebatuexamen.cl) es un servicio de {ownerLabel()} para preparar el
        examen de grado de Derecho. Esta política explica qué datos tratamos, para qué y qué
        derechos tienes sobre ellos.
      </p>

      <h2>1. Qué datos tratamos</h2>
      <ul>
        <li>
          <strong>Cuenta:</strong> tu correo y tu contraseña. La contraseña se guarda solo como
          un hash (Argon2id): nunca la almacenamos en texto legible.
        </li>
        <li>
          <strong>Ingreso con Google:</strong> si lo usas, recibimos de Google tu correo, si está
          verificado y un identificador de tu cuenta de Google. No accedemos a tus contactos,
          archivos ni otros datos de Google.
        </li>
        <li>
          <strong>Uso del servicio:</strong> tus respuestas, resultados, avance y plan de estudio.
          En la simulación oral guardamos la transcripción de tu respuesta, pero no el audio: el
          audio temporal se elimina al terminar la transcripción.
        </li>
        <li>
          <strong>Comentarios y reportes</strong> que nos envías desde la aplicación.
        </li>
        <li>
          <strong>Suscripción:</strong> el estado y las fechas de tu suscripción. El pago lo
          procesa Flow (flow.cl): nosotros no recibimos ni guardamos los datos de tu tarjeta.
        </li>
        <li>
          <strong>Datos técnicos mínimos</strong> para la seguridad del servicio, como la cookie
          de sesión y registros de intentos de acceso.
        </li>
      </ul>

      <h2>2. Para qué los usamos</h2>
      <ul>
        <li>Prestar el servicio: crear tu cuenta, guardar tu avance y mostrarte tus resultados.</li>
        <li>Verificar tu correo, proteger tu cuenta y enviarte los correos del servicio.</li>
        <li>Gestionar tu suscripción.</li>
        <li>Atender tus comentarios y reportes, y mejorar el contenido.</li>
      </ul>
      <p>No vendemos tus datos ni los usamos para publicidad.</p>

      <h2>3. Cookies</h2>
      <p>
        Usamos solo cookies necesarias para que el servicio funcione: la cookie de sesión, que te
        mantiene conectado, y una cookie temporal de diez minutos durante el ingreso con Google. No
        usamos cookies de publicidad ni de seguimiento de terceros.
      </p>

      <h2>4. Proveedores que tratan datos por nosotros</h2>
      <p>
        Para operar el servicio usamos proveedores que tratan datos solo para prestárnoslo: Vercel
        (sitio web), Render (servidor), Neon (base de datos), Resend (envío de correos), Google
        (ingreso con Google) y Flow (pagos). Cuando incorporemos proveedores de
        inteligencia artificial para transcribir y evaluar respuestas orales, actualizaremos esta
        política indicando cuáles son. Algunos de estos proveedores almacenan datos fuera de Chile,
        por ejemplo en Estados Unidos y Brasil.
      </p>

      <h2>5. Cuánto tiempo los conservamos</h2>
      <ul>
        <li>Transcripciones y resultados: hasta 12 meses.</li>
        <li>Datos de tu cuenta: mientras tu cuenta exista.</li>
        <li>
          Si pides eliminar tus transcripciones y resultados, lo hacemos en un plazo máximo de 30
          días, conservando solo un registro de que la eliminación se realizó, sin su contenido.
        </li>
      </ul>

      <h2>6. Tus derechos</h2>
      <p>
        Puedes pedir acceso, rectificación, eliminación de tus datos u oponerte a su tratamiento,
        conforme a la legislación chilena de protección de datos personales. Escríbenos a{" "}
        <strong>{contactLabel()}</strong>.
      </p>

      <h2>7. Seguridad</h2>
      <p>
        Toda la comunicación viaja cifrada (HTTPS), las contraseñas se guardan solo como hash y el
        acceso a los datos está restringido. Ningún sistema es infalible: si detectamos un
        incidente que afecte tus datos, te informaremos.
      </p>

      <h2>8. Cambios</h2>
      <p>
        Si cambiamos esta política, publicaremos la nueva versión aquí con su fecha y, si el cambio
        es relevante, te avisaremos por correo.
      </p>
    </LegalPage>
  );
}
