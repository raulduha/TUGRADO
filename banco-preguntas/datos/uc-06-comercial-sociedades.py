"""Cédula UC de Derecho Comercial I: sociedades (electiva)."""

JURISDICCION = "Chile"
PROGRAMA = "Cédulas UC (licenciatura, vigentes desde 2021)"
CEDULA = "Cédula 6: Derecho Comercial I, Sociedades (18-03-2021)"
MATERIA = "Derecho Comercial I (Sociedades)"

CC = "Código Civil"
CCOM = "Código de Comercio"
LSA = "Ley 18.046 sobre Sociedades Anónimas"
LSRL = "Ley 3.918 sobre Sociedades de Responsabilidad Limitada"
UC = "Cédula UC Derecho Comercial I"

PREGUNTAS = [
    # --------------------------------------------- concepto y personalidad
    (
        "La sociedad: concepto, naturaleza y personalidad jurídica",
        1,
        "Según el art. 2053 del Código Civil, ¿qué es la sociedad o compañía?",
        [
            "Un contrato en que dos o más personas estipulan poner algo en común con la mira "
            "de repartir entre sí los beneficios que de ello provengan.",
            "Una comunidad de bienes que nace sin acuerdo de las partes.",
            "Un acto unilateral por el que una persona destina bienes a un fin.",
            "Una asociación sin fines de lucro.",
        ],
        "A",
        "Es la A porque así la define el art. 2053, cuyo inciso 2.º agrega que la sociedad "
        "forma una persona jurídica distinta de los socios individualmente considerados. La B "
        "no, porque la comunidad no nace de un contrato de sociedad. La C no, porque la "
        "sociedad es un contrato y requiere, en principio, dos o más partes. La D no, porque "
        "el fin de repartir beneficios distingue a la sociedad de la corporación o "
        "asociación.",
        f"{CC}, art. 2053; {UC}, cap. I",
    ),
    (
        "La sociedad: concepto, naturaleza y personalidad jurídica",
        2,
        "¿Qué determina que una sociedad sea comercial y no civil, según el art. 2059 del "
        "Código Civil?",
        [
            "Que se forme para negocios que la ley califica de actos de comercio.",
            "Que tenga más de diez socios.",
            "Que sus socios sean comerciantes.",
            "Que su capital supere cierto monto.",
        ],
        "A",
        "Es la A porque el art. 2059 califica como comercial la sociedad formada para "
        "negocios que la ley califica de actos de comercio, y las demás son civiles. Hay "
        "sociedades mercantiles por su forma, como la anónima, aunque su objeto sea civil. "
        "La B no, porque el número de socios no determina su naturaleza. La C no, porque "
        "atiende al objeto, no a la calidad de los socios. La D no, porque el capital no es "
        "el criterio legal.",
        f"{CC}, art. 2059; {LSA}, art. 1; {UC}, cap. I",
    ),
    (
        "La sociedad: concepto, naturaleza y personalidad jurídica",
        2,
        "¿Cuáles son los elementos esenciales del contrato de sociedad según la doctrina?",
        [
            "Los aportes, la participación en los beneficios y la affectio societatis.",
            "La inscripción en el Registro de Comercio y la publicación en el Diario Oficial.",
            "El capital mínimo y el directorio.",
            "La responsabilidad ilimitada de los socios y la razón social.",
        ],
        "A",
        "Es la A porque toda sociedad exige que los socios aporten algo, que participen en "
        "los beneficios (art. 2055 CC) y que tengan la intención de asociarse en un plano de "
        "igualdad. La B no, porque esas son solemnidades de ciertos tipos sociales. La C no, "
        "porque el directorio es propio de la sociedad anónima y la ley no exige un capital "
        "mínimo general. La D no, porque la responsabilidad ilimitada es propia de algunos "
        "tipos, no de todos.",
        f"{CC}, arts. 2053 y 2055; {UC}, cap. I",
    ),
    # ---------------------------------------------------- sociedades de personas
    (
        "Colectiva civil y comercial",
        2,
        "¿Qué solemnidades exige la constitución de una sociedad colectiva comercial?",
        [
            "Escritura pública y la inscripción de un extracto en el Registro de Comercio del "
            "domicilio social dentro de 60 días.",
            "Solo un instrumento privado firmado por los socios.",
            "Escritura pública y aprobación de la Comisión para el Mercado Financiero.",
            "Un acuerdo verbal ante dos testigos.",
        ],
        "A",
        "Es la A porque así lo exigen los arts. 350 y 354 del Código de Comercio. La B no, "
        "porque el instrumento privado no basta (salvo que se protocolice o reduzca a "
        "escritura). La C no, porque la sociedad colectiva no requiere autorización de la "
        "Comisión. La D no, porque la ley exige solemnidades escritas.",
        f"{CCOM}, arts. 350 y 354; {UC}, cap. II",
    ),
    (
        "Colectiva civil y comercial",
        2,
        "¿Cómo responden los socios de una sociedad colectiva comercial por las obligaciones "
        "sociales?",
        [
            "Solidaria e ilimitadamente.",
            "Solo hasta el monto de sus aportes.",
            "A prorrata de sus aportes y sin solidaridad.",
            "No responden: solo responde la sociedad.",
        ],
        "A",
        "Es la A porque el art. 370 del Código de Comercio hace responsables solidariamente a "
        "los socios colectivos de todas las obligaciones legalmente contraídas bajo la razón "
        "social. La B no, porque la responsabilidad limitada es propia de otros tipos. La C "
        "no, porque esa es la regla de la colectiva civil (art. 2367 CC). La D no, porque los "
        "socios responden con su patrimonio personal.",
        f"{CCOM}, art. 370; {CC}, art. 2367; {UC}, cap. II",
    ),
    (
        "Colectiva civil y comercial",
        2,
        "Si en el contrato de sociedad colectiva no se designa administrador, ¿quién "
        "administra?",
        [
            "Todos los socios, por el mandato recíproco que se entiende conferido entre "
            "ellos.",
            "El socio con mayor aporte.",
            "Un administrador que nombra el juez.",
            "Nadie: la sociedad no puede actuar hasta que se designe administrador.",
        ],
        "A",
        "Es la A porque, a falta de designación, la ley entiende que los socios se confieren "
        "recíprocamente la facultad de administrar (art. 386 CCom y art. 2081 CC). La B no, "
        "porque el monto del aporte no confiere la administración. La C no, porque la ley "
        "resuelve el silencio sin intervención judicial. La D no, porque la ley suple la "
        "falta de designación.",
        f"{CCOM}, arts. 385 y 386; {CC}, art. 2081; {UC}, cap. II",
    ),
    (
        "Colectiva civil y comercial",
        2,
        "¿Cómo se forma la razón social de una sociedad colectiva comercial?",
        [
            "Con el nombre de todos los socios o de alguno de ellos, con la adición de la "
            "palabra «y compañía».",
            "Con cualquier nombre de fantasía, sin referencia a los socios.",
            "Con el nombre del objeto social seguido de la palabra «Limitada».",
            "Con las siglas «S.A.».",
        ],
        "A",
        "Es la A porque así lo dispone el art. 365 del Código de Comercio, y solo los nombres "
        "de los socios colectivos pueden figurar en ella. La B no, porque la razón social de "
        "la colectiva se forma con nombres de socios. La C no, porque la palabra «Limitada» "
        "identifica a la sociedad de responsabilidad limitada. La D no, porque esa sigla "
        "corresponde a la sociedad anónima.",
        f"{CCOM}, art. 365; {UC}, cap. II",
    ),
    (
        "Responsabilidad limitada",
        1,
        "¿Cuál es el número máximo de socios de una sociedad de responsabilidad limitada?",
        [
            "50.",
            "10.",
            "100.",
            "No tiene límite.",
        ],
        "A",
        "Es la A porque el art. 2 de la Ley 3.918 dispone que el número de socios no puede "
        "exceder de 50. La B no, porque el límite es mayor. La C no, porque el límite es "
        "menor. La D no, porque la ley sí fija un máximo.",
        f"{LSRL}, art. 2; {UC}, cap. II",
    ),
    (
        "Responsabilidad limitada",
        2,
        "¿Qué consecuencia tiene que la razón social de una sociedad de responsabilidad "
        "limitada no termine con la palabra «Limitada»?",
        [
            "Todos los socios quedan solidariamente responsables de las obligaciones "
            "sociales.",
            "La sociedad es nula de pleno derecho.",
            "La sociedad se transforma en anónima.",
            "Ninguna, porque es una mera formalidad.",
        ],
        "A",
        "Es la A porque el art. 4 de la Ley 3.918 dispone que, si se omite esa palabra, todos "
        "los socios quedan solidariamente responsables de las obligaciones sociales. La B "
        "no, porque la sanción no es la nulidad. La C no, porque no cambia el tipo social. "
        "La D no, porque la ley le asigna una sanción expresa.",
        f"{LSRL}, art. 4; {UC}, cap. II",
    ),
    (
        "Responsabilidad limitada",
        2,
        "¿Qué solemnidades exige la Ley 3.918 para constituir una sociedad de "
        "responsabilidad limitada?",
        [
            "Escritura pública, inscripción del extracto en el Registro de Comercio y su "
            "publicación en el Diario Oficial dentro de 60 días.",
            "Solo la inscripción en el Registro de Comercio, sin escritura.",
            "Escritura pública y aprobación municipal.",
            "Instrumento privado y aviso al Servicio de Impuestos Internos.",
        ],
        "A",
        "Es la A porque el art. 3 de la Ley 3.918 exige la publicación del extracto en el "
        "Diario Oficial, además de las solemnidades de la colectiva comercial, y todo dentro "
        "del plazo legal. La B no, porque se requiere escritura pública. La C no, porque no "
        "se requiere aprobación municipal. La D no, porque no basta un instrumento privado. "
        "Hoy también puede constituirse por el sistema simplificado de la Ley 20.659.",
        f"{LSRL}, art. 3; Ley 20.659; {UC}, cap. II",
    ),
    (
        "En comandita",
        2,
        "¿Qué caracteriza al socio comanditario en una sociedad en comandita?",
        [
            "Responde solo hasta el monto de su aporte y no puede administrar ni incluir su "
            "nombre en la razón social.",
            "Responde ilimitadamente y administra la sociedad.",
            "Es el único socio con derecho a las utilidades.",
            "Debe ser siempre una persona jurídica.",
        ],
        "A",
        "Es la A porque el comanditario aporta capital y limita su responsabilidad a su "
        "aporte, y la ley le prohíbe administrar e incluir su nombre en la razón social, so "
        "pena de responder como socio gestor (arts. 483 a 485 CCom). La B no, porque eso "
        "describe al socio gestor. La C no, porque todos los socios participan de las "
        "utilidades. La D no, porque puede ser persona natural o jurídica.",
        f"{CCOM}, arts. 474 y 483 a 485; {UC}, cap. II",
    ),
    (
        "Cuentas en participación",
        2,
        "¿Qué característica tiene la asociación o cuentas en participación (art. 507 del "
        "Código de Comercio)?",
        [
            "No forma una persona jurídica distinta y el gestor contrata a su nombre con los "
            "terceros.",
            "Forma una persona jurídica que debe inscribirse en el Registro de Comercio.",
            "Los partícipes responden solidariamente frente a terceros.",
            "Requiere escritura pública y publicación.",
        ],
        "A",
        "Es la A porque la participación es un contrato en que una o más personas toman "
        "interés en operaciones de un comerciante gestor, que las realiza a su nombre y bajo "
        "su crédito personal; carece de personalidad jurídica y de razón social, y los "
        "partícipes no tienen acción contra terceros ni estos contra ellos (art. 509). La B "
        "no, porque no forma persona jurídica. La C no, porque los terceros solo tienen "
        "acción contra el gestor. La D no, porque no está sujeta a solemnidades.",
        f"{CCOM}, arts. 507 a 509; {UC}, cap. II",
    ),
    # ------------------------------------------------------- sociedad anónima
    (
        "Constitución y capital",
        1,
        "Según el art. 1 de la Ley 18.046, ¿quién administra la sociedad anónima?",
        [
            "Un directorio integrado por miembros esencialmente revocables.",
            "Todos los accionistas en conjunto.",
            "El accionista con mayor número de acciones.",
            "Un gerente inamovible nombrado en los estatutos.",
        ],
        "A",
        "Es la A porque la ley define la sociedad anónima como una persona jurídica formada "
        "por un fondo común, suministrado por accionistas responsables solo por sus aportes, "
        "y administrada por un directorio integrado por miembros esencialmente revocables. "
        "La B no, porque los accionistas deciden en junta, pero no administran. La C no, "
        "porque el controlador no administra por sí solo. La D no, porque el gerente lo "
        "designa el directorio y no es inamovible.",
        f"{LSA}, arts. 1 y 31; {UC}, cap. III",
    ),
    (
        "Constitución y capital",
        2,
        "¿Dentro de qué plazo debe quedar suscrito y pagado el capital de una sociedad "
        "anónima?",
        [
            "Dentro de tres años; si no, queda reducido al monto efectivamente suscrito y "
            "pagado.",
            "Al momento de otorgar la escritura de constitución, en todo caso.",
            "Dentro de diez años.",
            "No hay plazo: el capital puede pagarse en cualquier momento.",
        ],
        "A",
        "Es la A porque la ley exige que el capital inicial y sus aumentos queden suscritos y "
        "pagados en un plazo no superior a tres años; vencido ese plazo, el capital queda "
        "reducido de pleno derecho al monto efectivamente suscrito y pagado. La B no, porque "
        "la ley admite que el pago quede pendiente dentro del plazo. La C no, porque el plazo "
        "es de tres años. La D no, porque la ley fija un plazo.",
        f"{LSA}, arts. 11 y 24; {UC}, cap. III",
    ),
    (
        "Acciones, directorio y juntas",
        2,
        "¿Qué materia corresponde a la junta extraordinaria de accionistas?",
        [
            "La reforma de los estatutos sociales.",
            "La aprobación de la memoria y el balance anual.",
            "La elección periódica del directorio.",
            "La distribución de las utilidades del ejercicio.",
        ],
        "A",
        "Es la A porque el art. 57 reserva a la junta extraordinaria materias como la "
        "disolución, la transformación, la fusión, la división y la reforma de estatutos. La "
        "B no, porque la memoria y el balance son materia de junta ordinaria (art. 56). La C "
        "no, porque la elección del directorio también es materia ordinaria. La D no, porque "
        "la distribución de utilidades también lo es.",
        f"{LSA}, arts. 56 y 57; {UC}, cap. III",
    ),
    (
        "Acciones, directorio y juntas",
        3,
        "En una sociedad anónima abierta, ¿qué porcentaje mínimo de las utilidades líquidas "
        "debe distribuirse anualmente como dividendo?",
        [
            "El 30 %, salvo acuerdo unánime de las acciones emitidas.",
            "El 50 %, sin excepción.",
            "El 10 %, salvo acuerdo del directorio.",
            "Ninguno: el dividendo es siempre facultativo.",
        ],
        "A",
        "Es la A porque el art. 79 obliga a las sociedades anónimas abiertas a distribuir "
        "anualmente como dividendo en dinero, a lo menos, el 30 % de las utilidades líquidas "
        "de cada ejercicio, salvo acuerdo diferente adoptado por la unanimidad de las "
        "acciones emitidas. La B no, porque el mínimo legal es menor. La C no, porque no lo "
        "decide el directorio. La D no, porque en las abiertas la ley fija un mínimo.",
        f"{LSA}, art. 79; {UC}, cap. III",
    ),
    (
        "Acciones, directorio y juntas",
        3,
        "¿Qué es el derecho a retiro en la sociedad anónima?",
        [
            "El derecho del accionista disidente de ciertos acuerdos de junta a retirarse "
            "de la sociedad, previo pago del valor de sus acciones.",
            "El derecho del director a renunciar a su cargo.",
            "El derecho de los acreedores a retirar sus créditos antes de una fusión.",
            "El derecho del accionista a retirar su aporte en cualquier momento.",
        ],
        "A",
        "Es la A porque el art. 69 concede ese derecho, entre otros casos, ante la "
        "transformación, la fusión, la enajenación del 50 % o más del activo y la creación "
        "de preferencias para una serie de acciones. La B no, porque esa es la renuncia del "
        "director. La C no, porque los acreedores no tienen ese derecho. La D no, porque el "
        "retiro solo procede en los casos que la ley señala.",
        f"{LSA}, art. 69; {UC}, cap. III",
    ),
    (
        "Transformación, fusión, división, disolución y liquidación",
        2,
        "¿Qué es la fusión por incorporación?",
        [
            "Una o más sociedades que se disuelven son absorbidas por otra ya existente, que "
            "adquiere todos sus activos y pasivos.",
            "Dos sociedades se disuelven para constituir una nueva.",
            "Una sociedad se divide en dos o más.",
            "Una sociedad cambia de tipo social sin disolverse.",
        ],
        "A",
        "Es la A porque así la define el art. 99 de la Ley 18.046. La B no, porque esa es la "
        "fusión por creación. La C no, porque esa es la división (art. 94). La D no, porque "
        "esa es la transformación (art. 96).",
        f"{LSA}, arts. 94, 96 y 99; {UC}, cap. III",
    ),
    (
        "Transformación, fusión, división, disolución y liquidación",
        2,
        "¿Qué efecto tiene la transformación de una sociedad?",
        [
            "Cambia su especie o tipo social manteniendo su personalidad jurídica.",
            "La disuelve y crea una persona jurídica nueva.",
            "Extingue todas sus deudas.",
            "Obliga a liquidar su patrimonio.",
        ],
        "A",
        "Es la A porque el art. 96 define la transformación como el cambio de especie o tipo "
        "social de una sociedad, efectuado por reforma de sus estatutos, subsistiendo su "
        "personalidad jurídica. La B no, porque la persona jurídica continúa. La C no, porque "
        "las obligaciones subsisten. La D no, porque no hay liquidación.",
        f"{LSA}, art. 96; {UC}, cap. III",
    ),
    # ------------------------------------- SpA y constitución simplificada
    (
        "Sociedades por acciones y constitución simplificada",
        1,
        "¿Puede constituirse una sociedad por acciones (SpA) con un solo accionista?",
        [
            "Sí, la SpA puede constituirse por una o más personas.",
            "No, requiere a lo menos dos accionistas.",
            "Solo si el accionista es una persona jurídica.",
            "Solo con autorización de la Comisión para el Mercado Financiero.",
        ],
        "A",
        "Es la A porque el art. 424 del Código de Comercio define la SpA como una persona "
        "jurídica creada por una o más personas mediante un acto de constitución, cuya "
        "participación en el capital es representada por acciones. La B no, porque la ley "
        "admite un solo accionista. La C no, porque también puede ser persona natural. La D "
        "no, porque no se requiere esa autorización.",
        f"{CCOM}, art. 424; {UC}, cap. IV",
    ),
    (
        "Sociedades por acciones y constitución simplificada",
        2,
        "¿Qué permite la Ley 20.659?",
        [
            "Constituir, modificar y disolver ciertas sociedades por vía electrónica en el "
            "Registro de Empresas y Sociedades, sin escritura pública.",
            "Constituir sociedades anónimas abiertas sin capital.",
            "Eximir a las sociedades de inscribirse en el Servicio de Impuestos Internos.",
            "Crear sociedades sin personalidad jurídica.",
        ],
        "A",
        "Es la A porque la Ley 20.659 creó un régimen simplificado, voluntario y gratuito, "
        "alternativo a las solemnidades tradicionales, mediante formularios electrónicos en "
        "el Registro de Empresas y Sociedades. La B no, porque no crea sociedades sin "
        "capital. La C no, porque no exime de las obligaciones tributarias. La D no, porque "
        "las sociedades así constituidas son personas jurídicas.",
        f"Ley 20.659; {UC}, cap. IV",
    ),
    # --------------------------------------------- nulidad y saneamiento
    (
        "Nulidad y saneamiento de sociedades",
        2,
        "¿Qué permite la Ley 19.499 sobre saneamiento de vicios de nulidad de sociedades?",
        [
            "Sanear los vicios formales en la constitución o modificación de una sociedad, "
            "mediante una escritura de saneamiento inscrita y publicada.",
            "Sanear cualquier objeto ilícito de la sociedad.",
            "Declarar nula una sociedad sin juicio.",
            "Convertir una sociedad de hecho en sociedad anónima abierta.",
        ],
        "A",
        "Es la A porque la Ley 19.499 regula el saneamiento de los vicios formales, por "
        "ejemplo errores en el extracto o en su publicación, sin afectar la existencia de la "
        "sociedad. La B no, porque el objeto ilícito es un vicio de fondo que no se sanea por "
        "esta vía. La C no, porque la ley trata del saneamiento, no de la declaración de "
        "nulidad. La D no, porque no regula esa conversión.",
        f"Ley 19.499; {UC}, cap. V",
    ),
    (
        "Nulidad y saneamiento de sociedades",
        3,
        "Una sociedad colectiva comercial no consta en escritura pública ni en instrumento "
        "reducido a escritura pública o protocolizado. ¿Qué efecto tiene?",
        [
            "Es nula de pleno derecho y no puede sanearse; si existe de hecho, da lugar a una "
            "comunidad cuyos miembros responden solidariamente ante los terceros con quienes "
            "contrataron.",
            "Es válida, porque la sociedad es un contrato consensual.",
            "Es válida entre los socios, pero no frente a terceros.",
            "Se transforma automáticamente en una SpA.",
        ],
        "A",
        "Es la A porque así lo dispone el art. 356 del Código de Comercio, en su texto "
        "fijado por la Ley 19.499: la falta de escritura no es un vicio formal saneable, y "
        "las ganancias y pérdidas de la comunidad se reparten según lo pactado o, a falta de "
        "pacto, según los aportes. La B no, porque la sociedad colectiva comercial es "
        "solemne. La C no, porque la nulidad opera de pleno derecho. La D no, porque la ley "
        "no contempla esa transformación.",
        f"{CCOM}, art. 356; Ley 19.499; {UC}, cap. V",
    ),
]
