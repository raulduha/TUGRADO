"""Cédula UC de Derecho del Trabajo (electiva)."""

JURISDICCION = "Chile"
PROGRAMA = "Cédulas UC (licenciatura, vigentes desde 2021)"
CEDULA = "Cédula 16: Derecho del Trabajo (02-12-2025)"
MATERIA = "Derecho del Trabajo"

CT = "Código del Trabajo"
UC = "Cédula UC Derecho del Trabajo"

PREGUNTAS = [
    # --------------------------------------------------------- bases y principios
    (
        "Bases y principios del Derecho del Trabajo",
        1,
        "¿Qué establece el art. 5 del Código del Trabajo sobre los derechos laborales?",
        [
            "Son irrenunciables mientras subsista el contrato de trabajo.",
            "Pueden renunciarse libremente en el contrato individual.",
            "Son renunciables si el trabajador gana más de cierto monto.",
            "Solo son irrenunciables los derechos de los trabajadores sindicalizados.",
        ],
        "A",
        "Es la A porque el art. 5 inciso 2.º declara irrenunciables los derechos que "
        "establecen las leyes laborales mientras subsista el contrato; es una expresión del "
        "principio protector. La B no, porque la renuncia anticipada está prohibida. La C "
        "no, porque la ley no hace esa distinción. La D no, porque la regla protege a todos "
        "los trabajadores.",
        f"{CT}, art. 5; {UC}, cap. I",
    ),
    (
        "Bases y principios del Derecho del Trabajo",
        2,
        "Una persona presta servicios personales, bajo subordinación y dependencia y por una "
        "remuneración, pero firmó un contrato de honorarios. ¿Qué dispone el art. 8 del "
        "Código del Trabajo?",
        [
            "Que esa prestación hace presumir la existencia de un contrato de trabajo.",
            "Que prima lo que las partes escribieron en el contrato de honorarios.",
            "Que el contrato es nulo y el trabajador no tiene derechos.",
            "Que solo la Inspección del Trabajo puede calificar la relación, sin recurso.",
        ],
        "A",
        "Es la A porque el art. 8 dispone que toda prestación de servicios en los términos "
        "del art. 7 hace presumir la existencia de un contrato de trabajo; es una aplicación "
        "del principio de primacía de la realidad. La B no, porque prima la realidad de la "
        "relación sobre su denominación. La C no, porque el trabajador conserva sus derechos "
        "laborales. La D no, porque la calificación corresponde, en definitiva, a los "
        "tribunales.",
        f"{CT}, arts. 7 y 8; {UC}, cap. I",
    ),
    (
        "Bases y principios del Derecho del Trabajo",
        2,
        "Tras la Ley 21.643 (Ley Karin), ¿qué exige el Código del Trabajo para que haya acoso "
        "laboral?",
        [
            "Una conducta de agresión u hostigamiento que puede manifestarse una sola vez o de "
            "manera reiterada.",
            "Una conducta reiterada en el tiempo, por al menos seis meses.",
            "Que la agresión provenga exclusivamente del empleador.",
            "Que exista una condena penal previa del agresor.",
        ],
        "A",
        "Es la A porque la Ley 21.643 modificó el art. 2 para definir el acoso laboral como "
        "toda conducta de agresión u hostigamiento, ejercida por el empleador o por uno o más "
        "trabajadores, sea que se manifieste una sola vez o de manera reiterada, que cause "
        "menoscabo, maltrato o humillación, o amenace o perjudique la situación laboral. La B "
        "no, porque la reiteración dejó de ser un requisito. La C no, porque también pueden "
        "cometerlo otros trabajadores. La D no, porque no se exige una condena penal.",
        f"{CT}, art. 2; Ley 21.643; {UC}, cap. I",
    ),
    # --------------------------------------------------------- contrato de trabajo
    (
        "Elementos y tiempo de trabajo",
        1,
        "Según el art. 7 del Código del Trabajo, ¿qué elemento distingue al contrato de "
        "trabajo de otras prestaciones de servicios?",
        [
            "Que los servicios se presten bajo dependencia y subordinación.",
            "Que el trabajador sea profesional.",
            "Que el contrato conste por escrito.",
            "Que se pague en dinero efectivo cada semana.",
        ],
        "A",
        "Es la A porque el art. 7 define el contrato de trabajo como la convención por la que "
        "el trabajador presta servicios personales bajo dependencia y subordinación del "
        "empleador, y este paga una remuneración determinada. La B no, porque cualquier "
        "persona puede ser trabajador. La C no, porque el contrato es consensual; la "
        "escrituración es una exigencia de prueba (art. 9). La D no, porque la ley no exige "
        "pago semanal.",
        f"{CT}, arts. 7 y 9; {UC}, cap. II",
    ),
    (
        "Elementos y tiempo de trabajo",
        2,
        "¿En qué plazo debe el empleador escriturar el contrato de trabajo por regla general?",
        [
            "Dentro de 15 días desde la incorporación del trabajador.",
            "Dentro de 90 días desde la incorporación.",
            "Antes del primer pago de remuneraciones, cualquiera sea su fecha.",
            "No hay plazo: basta el acuerdo verbal.",
        ],
        "A",
        "Es la A porque el art. 9 exige escriturarlo dentro de 15 días, o de 5 si es por "
        "obra, trabajo o servicio determinado o de duración inferior a 30 días; si no lo "
        "hace, se presume legalmente que son estipulaciones del contrato las que declare el "
        "trabajador. La B no, porque el plazo es mucho menor. La C no, porque la ley fija un "
        "plazo desde la incorporación. La D no, porque la ley exige escriturarlo.",
        f"{CT}, art. 9; {UC}, cap. II",
    ),
    (
        "Elementos y tiempo de trabajo",
        2,
        "¿Qué duración máxima tiene, por regla general, el contrato de trabajo a plazo fijo?",
        [
            "Un año, o dos años para gerentes o personas con título profesional o técnico.",
            "Seis meses, sin excepción.",
            "Tres años.",
            "No tiene duración máxima.",
        ],
        "A",
        "Es la A porque así lo dispone el art. 159 n.º 4, que además convierte en indefinido "
        "el contrato cuando el trabajador sigue prestando servicios con conocimiento del "
        "empleador después de vencido el plazo, o cuando se renueva por segunda vez. La B "
        "no, porque el límite es mayor. La C no, porque no es el límite legal. La D no, "
        "porque la ley fija una duración máxima.",
        f"{CT}, art. 159 n.º 4; {UC}, cap. II",
    ),
    (
        "Elementos y tiempo de trabajo",
        2,
        "Desde el 26 de abril de 2026, ¿cuál es la jornada ordinaria máxima semanal según la "
        "Ley 21.561?",
        [
            "42 horas.",
            "45 horas.",
            "44 horas.",
            "40 horas.",
        ],
        "A",
        "Es la A porque la Ley 21.561 redujo gradualmente la jornada del art. 22: 44 horas "
        "desde el 26 de abril de 2024, 42 horas desde el 26 de abril de 2026 y 40 horas desde "
        "el 26 de abril de 2028. La B no, porque 45 horas era la jornada anterior a la ley. "
        "La C no, porque las 44 horas rigieron entre 2024 y 2026. La D no, porque las 40 "
        "horas recién rigen desde 2028.",
        f"{CT}, art. 22; Ley 21.561, disposiciones transitorias; {UC}, cap. II",
    ),
    (
        "Elementos y tiempo de trabajo",
        2,
        "¿Qué límites tienen las horas extraordinarias en el Código del Trabajo?",
        [
            "Máximo dos por día, pactadas por escrito con vigencia transitoria de hasta tres "
            "meses renovables, y pagadas con un recargo de 50 % sobre el sueldo convenido.",
            "Máximo cuatro por día, sin necesidad de pacto escrito.",
            "Las que el empleador ordene, pagadas como horas ordinarias.",
            "Solo se permiten los días domingo.",
        ],
        "A",
        "Es la A porque así lo disponen los arts. 31 y 32, siempre que la naturaleza de las "
        "labores no perjudique la salud del trabajador. La B no, porque el máximo es de dos "
        "horas diarias y se exige pacto escrito. La C no, porque deben pactarse y llevan "
        "recargo. La D no, porque la ley no las limita a los domingos.",
        f"{CT}, arts. 31 y 32; {UC}, cap. II",
    ),
    (
        "Elementos y tiempo de trabajo",
        1,
        "¿A cuántos días de feriado anual tiene derecho el trabajador con más de un año de "
        "servicio?",
        [
            "A 15 días hábiles, con remuneración íntegra.",
            "A 30 días corridos.",
            "A 10 días hábiles.",
            "A los que acuerde con el empleador, sin mínimo legal.",
        ],
        "A",
        "Es la A porque el art. 67 concede un feriado anual de 15 días hábiles con "
        "remuneración íntegra, y para estos efectos el sábado se considera inhábil. La B no, "
        "porque el feriado se cuenta en días hábiles. La C no, porque el mínimo legal es "
        "mayor. La D no, porque la ley fija un mínimo irrenunciable.",
        f"{CT}, arts. 67 y 69; {UC}, cap. II",
    ),
    (
        "Remuneraciones y cotizaciones",
        2,
        "¿Cuál de estas prestaciones NO constituye remuneración según el art. 41 del Código "
        "del Trabajo?",
        [
            "La asignación de colación.",
            "El sueldo.",
            "Las comisiones.",
            "El sobresueldo por horas extraordinarias.",
        ],
        "A",
        "Es la A porque el art. 41 inciso 2.º excluye de la remuneración las asignaciones de "
        "movilización, pérdida de caja, desgaste de herramientas y colación, los viáticos, "
        "las prestaciones familiares y las indemnizaciones, entre otras. La B no, porque el "
        "sueldo es la remuneración básica (art. 42 letra a). La C no, porque la comisión es "
        "remuneración (art. 42 letra c). La D no, porque el sobresueldo también lo es (art. "
        "42 letra b).",
        f"{CT}, arts. 41 y 42; {UC}, cap. II",
    ),
    (
        "Remuneraciones y cotizaciones",
        3,
        "Si el empleador opta por la gratificación del art. 50 del Código del Trabajo, ¿cuánto "
        "debe pagar?",
        [
            "El 25 % de lo devengado en el ejercicio por remuneraciones mensuales, con un "
            "tope de 4,75 ingresos mínimos mensuales.",
            "El 30 % de las utilidades líquidas, sin tope.",
            "Un sueldo mensual completo en diciembre.",
            "El 10 % de las ventas de la empresa.",
        ],
        "A",
        "Es la A porque así lo establece el art. 50, alternativa que libera al empleador de "
        "la obligación del art. 47 de distribuir el 30 % de las utilidades líquidas. La B no, "
        "porque esa es la modalidad del art. 47, que además se reparte en proporción a las "
        "remuneraciones. La C no, porque la ley no fija esa forma. La D no, porque la "
        "gratificación no se calcula sobre las ventas.",
        f"{CT}, arts. 47 y 50; {UC}, cap. II",
    ),
    (
        "Subcontratación y servicios transitorios",
        2,
        "¿Cómo responde la empresa principal por las obligaciones laborales y previsionales "
        "del contratista respecto de sus trabajadores?",
        [
            "Solidariamente, pero solo subsidiariamente si ejerce sus derechos de información "
            "y retención.",
            "No responde en ningún caso.",
            "Solo moralmente, sin responsabilidad jurídica.",
            "Responde siempre en forma exclusiva, y el contratista queda liberado.",
        ],
        "A",
        "Es la A porque el art. 183-B establece la responsabilidad solidaria de la empresa "
        "principal, que el art. 183-D convierte en subsidiaria cuando hace efectivo su "
        "derecho a ser informada y su derecho de retención. La B no, porque la ley la hace "
        "responder. La C no, porque la responsabilidad es jurídica. La D no, porque el "
        "contratista sigue siendo el empleador y principal obligado.",
        f"{CT}, arts. 183-A, 183-B y 183-D; {UC}, cap. II",
    ),
    (
        "Subcontratación y servicios transitorios",
        3,
        "¿Qué caracteriza al trabajo en régimen de servicios transitorios?",
        [
            "Una empresa de servicios transitorios pone trabajadores a disposición de una "
            "usuaria, solo en las circunstancias que la ley autoriza.",
            "La usuaria contrata directamente al trabajador por un plazo indefinido.",
            "Puede usarse para reemplazar a trabajadores en huelga.",
            "No requiere contrato escrito entre la empresa de servicios y la usuaria.",
        ],
        "A",
        "Es la A porque los arts. 183-F y siguientes regulan ese régimen y el art. 183-Ñ "
        "limita las circunstancias que lo justifican, como suspensiones del contrato, "
        "eventos extraordinarios o aumentos ocasionales de actividad. La B no, porque el "
        "empleador es la empresa de servicios transitorios. La C no, porque la ley lo "
        "prohíbe expresamente. La D no, porque se exige contrato escrito de puesta a "
        "disposición.",
        f"{CT}, arts. 183-F, 183-N, 183-Ñ y 183-P; {UC}, cap. II",
    ),
    (
        "Suspensión y terminación",
        2,
        "¿Qué causal de terminación del contrato puede invocar el empleador por "
        "racionalización o modernización de la empresa?",
        [
            "Las necesidades de la empresa, establecimiento o servicio (art. 161).",
            "La falta de probidad del trabajador (art. 160).",
            "El vencimiento del plazo convenido (art. 159).",
            "El caso fortuito o fuerza mayor (art. 159).",
        ],
        "A",
        "Es la A porque el art. 161 incluye entre las necesidades de la empresa las derivadas "
        "de la racionalización o modernización, las bajas en la productividad y los cambios "
        "en las condiciones del mercado o de la economía. La B no, porque esa es una causal "
        "disciplinaria imputable al trabajador. La C no, porque se refiere al término del "
        "plazo. La D no, porque exige un hecho imprevisto e irresistible.",
        f"{CT}, arts. 159, 160 y 161; {UC}, cap. II",
    ),
    (
        "Suspensión y terminación",
        2,
        "¿Cómo se calcula la indemnización por años de servicio del art. 163, a falta de "
        "pacto?",
        [
            "Treinta días de la última remuneración mensual por cada año de servicio y "
            "fracción superior a seis meses, con un límite de 330 días.",
            "Un mes de remuneración por año, sin límite alguno.",
            "Quince días por año, con un límite de 180 días.",
            "Un monto fijo igual a tres ingresos mínimos.",
        ],
        "A",
        "Es la A porque así lo dispone el art. 163 cuando el contrato ha estado vigente un "
        "año o más y termina por la causal del art. 161; además, la remuneración que sirve "
        "de base tiene un tope de 90 unidades de fomento (art. 172). La B no, porque hay "
        "límite de 330 días. La C no, porque la base legal es de 30 días por año. La D no, "
        "porque la indemnización depende de la antigüedad.",
        f"{CT}, arts. 163 y 172; {UC}, cap. II",
    ),
    (
        "Suspensión y terminación",
        2,
        "Si el juez declara injustificada la aplicación de la causal del art. 161, ¿qué "
        "recargo se aplica a la indemnización por años de servicio?",
        [
            "Un 30 %.",
            "Un 80 %.",
            "Un 100 %.",
            "Un 10 %.",
        ],
        "A",
        "Es la A porque el art. 168 letra a) fija un recargo de 30 % cuando la causal del "
        "art. 161 se aplica improcedentemente. La B no, porque el 80 % corresponde a la "
        "aplicación injustificada de las causales del art. 160. La C no, porque el 100 % "
        "rige cuando ciertas causales del art. 160 se invocan sin motivo plausible. La D no, "
        "porque no es un recargo previsto por la ley.",
        f"{CT}, art. 168; {UC}, cap. II",
    ),
    (
        "Suspensión y terminación",
        2,
        "¿En qué plazo debe el trabajador demandar por despido injustificado?",
        [
            "Dentro de 60 días hábiles desde la separación, plazo que se suspende si reclama "
            "ante la Inspección del Trabajo, sin exceder de 90 días hábiles.",
            "Dentro de dos años desde la separación.",
            "Dentro de cinco días corridos.",
            "En cualquier momento, porque la acción es imprescriptible.",
        ],
        "A",
        "Es la A porque así lo dispone el art. 168. La B no, porque dos años es la "
        "prescripción de los derechos del art. 510, no el plazo de caducidad para reclamar "
        "del despido. La C no, porque el plazo es mayor. La D no, porque es un plazo de "
        "caducidad.",
        f"{CT}, arts. 168 y 510; {UC}, cap. II",
    ),
    (
        "Suspensión y terminación",
        3,
        "¿Qué efecto tiene despedir a un trabajador sin haber pagado sus cotizaciones "
        "previsionales, según el art. 162 del Código del Trabajo?",
        [
            "El despido no produce el efecto de poner término al contrato, y el empleador "
            "debe pagar las remuneraciones hasta que convalide el despido pagando las "
            "cotizaciones.",
            "El despido es válido, pero el empleador paga una multa administrativa.",
            "El trabajador pierde su derecho a las cotizaciones adeudadas.",
            "El contrato se transforma en uno a plazo fijo.",
        ],
        "A",
        "Es la A porque el art. 162 incisos 5.º y siguientes establecen la llamada nulidad "
        "del despido: mientras no se paguen las cotizaciones y se comunique ese pago al "
        "trabajador, el empleador debe pagarle las remuneraciones y demás prestaciones. La B "
        "no, porque el despido no produce su efecto propio. La C no, porque las cotizaciones "
        "siguen siendo exigibles. La D no, porque la ley no transforma el contrato.",
        f"{CT}, art. 162; {UC}, cap. II",
    ),
    (
        "Suspensión y terminación",
        2,
        "¿Durante qué período goza de fuero la trabajadora por maternidad?",
        [
            "Durante el embarazo y hasta un año después de expirado el descanso de "
            "maternidad.",
            "Solo durante el descanso prenatal y postnatal.",
            "Durante los seis meses siguientes al parto.",
            "Durante todo el tiempo que amamante a su hijo, sin límite.",
        ],
        "A",
        "Es la A porque así lo dispone el art. 201; durante ese período el empleador no "
        "puede poner término al contrato sin autorización previa del juez, conforme al art. "
        "174. La B no, porque el fuero es más extenso. La C no, porque no es el período "
        "legal. La D no, porque la ley fija un límite.",
        f"{CT}, arts. 174 y 201; {UC}, cap. II",
    ),
    (
        "Prescripción y caducidad",
        2,
        "Según el art. 510 del Código del Trabajo, ¿en qué plazo prescriben los derechos "
        "regidos por el Código?",
        [
            "En dos años desde que se hicieron exigibles; las acciones provenientes de los "
            "actos y contratos prescriben en seis meses desde la terminación de los "
            "servicios.",
            "En cinco años desde la terminación del contrato.",
            "En un año desde la firma del contrato.",
            "En diez años, como las acciones ordinarias civiles.",
        ],
        "A",
        "Es la A porque así lo establece el art. 510. La B no, porque cinco años es el plazo "
        "de prescripción de la acción ordinaria civil. La C no, porque el plazo no se cuenta "
        "desde la firma. La D no, porque el Código del Trabajo tiene plazos especiales más "
        "breves.",
        f"{CT}, art. 510; {UC}, cap. II",
    ),
    # ---------------------------------------- sindicatos, negociación y huelga
    (
        "Sindicatos, negociación colectiva y huelga",
        2,
        "¿Cómo adquiere personalidad jurídica un sindicato?",
        [
            "Por el solo depósito del acta de constitución y sus estatutos en la Inspección "
            "del Trabajo.",
            "Por decreto del Ministerio del Trabajo.",
            "Por sentencia judicial.",
            "Por inscripción en el Registro de Comercio.",
        ],
        "A",
        "Es la A porque el art. 222 dispone que el sindicato adquiere personalidad jurídica "
        "desde el depósito del acta original de constitución y de los estatutos en la "
        "Inspección del Trabajo, que debe hacerse dentro de 15 días desde la asamblea. La B "
        "no, porque no se requiere decreto. La C no, porque no se requiere sentencia. La D "
        "no, porque el sindicato no se inscribe en el Registro de Comercio.",
        f"{CT}, art. 222; {UC}, cap. III",
    ),
    (
        "Sindicatos, negociación colectiva y huelga",
        2,
        "Tras la Ley 20.940, ¿puede el empleador reemplazar a los trabajadores que ejercen "
        "legalmente su derecho a huelga?",
        [
            "No: la ley prohíbe el reemplazo, y hacerlo es una práctica desleal grave.",
            "Sí, pagando un bono de reemplazo por trabajador.",
            "Sí, desde el primer día de huelga, con trabajadores externos.",
            "Sí, con trabajadores de servicios transitorios.",
        ],
        "A",
        "Es la A porque el art. 345 prohíbe el reemplazo de los trabajadores en huelga y lo "
        "califica como práctica desleal grave (art. 403 letra d). La B no, porque la Ley "
        "20.940 eliminó el reemplazo con bono. La C no, porque el reemplazo está prohibido. "
        "La D no, porque la ley también prohíbe usar trabajadores de servicios transitorios "
        "para ese fin.",
        f"{CT}, arts. 345 y 403; Ley 20.940; {UC}, cap. III",
    ),
    (
        "Sindicatos, negociación colectiva y huelga",
        3,
        "¿Qué son los servicios mínimos en la huelga?",
        [
            "Los servicios estrictamente necesarios para proteger los bienes e instalaciones "
            "de la empresa, prevenir accidentes, garantizar servicios de utilidad pública o "
            "atender necesidades básicas de la población.",
            "Los servicios que el empleador puede exigir a todos los huelguistas.",
            "El número mínimo de trabajadores que debe votar la huelga.",
            "Los servicios que la empresa presta durante el feriado legal.",
        ],
        "A",
        "Es la A porque el art. 359 los define así; los trabajadores que los cumplen forman "
        "parte de los equipos de emergencia. La B no, porque no se aplican a todos los "
        "huelguistas. La C no, porque eso se refiere a la votación de la huelga. La D no, "
        "porque nada tiene que ver con el feriado.",
        f"{CT}, arts. 359 a 361; {UC}, cap. III",
    ),
    (
        "Sindicatos, negociación colectiva y huelga",
        2,
        "¿Qué procedimiento protege al trabajador cuando el empleador vulnera sus derechos "
        "fundamentales en la relación laboral?",
        [
            "El procedimiento de tutela laboral de los arts. 485 y siguientes.",
            "El recurso de amparo económico.",
            "El juicio ejecutivo laboral.",
            "La acción de nulidad de derecho público.",
        ],
        "A",
        "Es la A porque el procedimiento de tutela laboral se aplica a las cuestiones "
        "suscitadas por la vulneración de derechos fundamentales de los trabajadores en la "
        "relación laboral, incluidos los actos discriminatorios y la libertad sindical. La B "
        "no, porque el amparo económico protege la libertad para desarrollar actividades "
        "económicas. La C no, porque sirve para cobrar títulos ejecutivos laborales. La D "
        "no, porque se dirige contra actos de órganos del Estado.",
        f"{CT}, arts. 485 y siguientes; {UC}, cap. III",
    ),
]
