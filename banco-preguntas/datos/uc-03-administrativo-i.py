"""Cédula UC de Derecho Administrativo I (electiva)."""

JURISDICCION = "Chile"
PROGRAMA = "Cédulas UC (licenciatura, vigentes desde 2021)"
CEDULA = "Cédula 3: Derecho Administrativo I (18-03-2021)"
MATERIA = "Derecho Administrativo I"

CPR = "Constitución Política"
LBGAE = "Ley 18.575 orgánica constitucional de Bases Generales de la Administración del Estado"
LBPA = "Ley 19.880 de Bases de los Procedimientos Administrativos"
UC = "Cédula UC Derecho Administrativo I"

PREGUNTAS = [
    # ------------------------------------------- introducción y juridicidad
    (
        "Introducción al Derecho Administrativo. Principio de juridicidad",
        1,
        "¿Qué exige el principio de juridicidad a los órganos de la Administración del "
        "Estado, según el art. 2 de la Ley 18.575?",
        [
            "Someter su acción a la Constitución y las leyes, actuar dentro de su competencia "
            "y no tener más atribuciones que las que expresamente les confiere el "
            "ordenamiento.",
            "Actuar según su criterio en todo lo que la ley no prohíba expresamente.",
            "Obedecer solo los reglamentos internos de cada servicio.",
            "Someterse a la ley únicamente cuando actúan frente a particulares.",
        ],
        "A",
        "Es la A porque así lo dispone el art. 2 de la Ley 18.575, en concordancia con los "
        "arts. 6 y 7 de la Constitución; todo abuso o exceso en el ejercicio de sus "
        "potestades da lugar a las acciones y recursos correspondientes. La B no, porque esa "
        "es la regla de libertad de los particulares, no de los órganos públicos. La C no, "
        "porque los reglamentos internos están subordinados a la Constitución y la ley. La D "
        "no, porque el principio rige en toda la actuación administrativa.",
        f"{CPR}, arts. 6 y 7; {LBGAE}, art. 2; {UC}, cap. I",
    ),
    (
        "Introducción al Derecho Administrativo. Principio de juridicidad",
        3,
        "Según la jurisprudencia reciente de la Corte Suprema, ¿prescribe la acción de "
        "nulidad de derecho público?",
        [
            "La declaración de nulidad es imprescriptible, pero las acciones patrimoniales "
            "que se derivan de ella prescriben según las reglas del Código Civil.",
            "Prescribe siempre en seis meses desde la publicación del acto.",
            "Prescribe en dos años, igual que la invalidación.",
            "Es imprescriptible en todos sus efectos, incluidos los patrimoniales.",
        ],
        "A",
        "Es la A porque la Corte Suprema ha distinguido entre la acción declarativa de "
        "nulidad, que considera imprescriptible por su fundamento en el art. 7 de la "
        "Constitución, y las acciones de contenido patrimonial, que sujeta a la prescripción "
        "del derecho común. La B no, porque la Constitución no fija ese plazo. La C no, "
        "porque los dos años son el plazo de la Administración para invalidar (art. 53 Ley "
        "19.880). La D no, porque las consecuencias patrimoniales sí prescriben.",
        f"{CPR}, art. 7; Código Civil, arts. 2332 y 2515; {UC}, cap. I",
    ),
    (
        "Introducción al Derecho Administrativo. Principio de juridicidad",
        2,
        "¿Cuál de estos principios NO figura entre los que el art. 3 de la Ley 18.575 impone "
        "a la Administración?",
        [
            "El de reserva de todos sus actos.",
            "El de probidad.",
            "El de impulsión de oficio del procedimiento.",
            "El de impugnabilidad de los actos administrativos.",
        ],
        "A",
        "Es la A porque el art. 3 consagra, al contrario, los principios de transparencia y "
        "publicidad, junto con responsabilidad, eficiencia, eficacia, coordinación, "
        "impulsión de oficio, impugnabilidad, control, probidad y participación ciudadana. "
        "La B no, porque la probidad está expresamente. La C no, porque la impulsión de "
        "oficio también. La D no, porque la impugnabilidad también.",
        f"{LBGAE}, art. 3; {CPR}, art. 8; {UC}, cap. I",
    ),
    (
        "Introducción al Derecho Administrativo. Principio de juridicidad",
        2,
        "¿En qué consiste el principio de probidad administrativa según el art. 52 de la Ley "
        "18.575?",
        [
            "En observar una conducta funcionaria intachable y un desempeño honesto y leal de "
            "la función, con preeminencia del interés general sobre el particular.",
            "En cumplir el horario de trabajo sin atrasos.",
            "En obedecer toda orden del superior jerárquico, aunque sea ilegal.",
            "En mantener reserva de todas las actuaciones del servicio.",
        ],
        "A",
        "Es la A porque así lo define el art. 52 de la Ley 18.575, aplicable a todas las "
        "autoridades y funcionarios de la Administración. La B no, porque la probidad no se "
        "agota en el cumplimiento del horario. La C no, porque la probidad no exige obedecer "
        "órdenes ilegales. La D no, porque la regla general es la publicidad (art. 8 CPR).",
        f"{LBGAE}, art. 52; {CPR}, art. 8; {UC}, cap. I",
    ),
    # --------------------------------------- organización administrativa
    (
        "La Ley 18.575 y los principios organizativos",
        1,
        "¿Cuál de estos órganos NO integra la Administración del Estado según el art. 1 de la "
        "Ley 18.575?",
        [
            "El Congreso Nacional.",
            "Los ministerios.",
            "Las municipalidades.",
            "La Contraloría General de la República.",
        ],
        "A",
        "Es la A porque el Congreso ejerce la función legislativa y no forma parte de la "
        "Administración. La B no, porque los ministerios están expresamente mencionados. La "
        "C no, porque las municipalidades también lo están. La D no, porque la Contraloría "
        "también figura en el art. 1, aunque es autónoma.",
        f"{LBGAE}, art. 1; {UC}, cap. II",
    ),
    (
        "La Ley 18.575 y los principios organizativos",
        2,
        "Según el art. 22 de la Ley 18.575, ¿qué son los ministerios?",
        [
            "Los órganos superiores de colaboración del Presidente en las funciones de "
            "gobierno y administración de sus respectivos sectores.",
            "Órganos autónomos, sin dependencia del Presidente.",
            "Servicios públicos descentralizados con patrimonio propio.",
            "Órganos asesores del Congreso Nacional.",
        ],
        "A",
        "Es la A porque así los define el art. 22, que les encarga proponer y evaluar las "
        "políticas y planes de su sector. La B no, porque dependen del Presidente. La C no, "
        "porque los ministerios actúan con la personalidad jurídica del Fisco. La D no, "
        "porque colaboran con el Presidente, no con el Congreso.",
        f"{LBGAE}, art. 22; {CPR}, art. 33; {UC}, cap. II",
    ),
    (
        "La Ley 18.575 y los principios organizativos",
        2,
        "¿Qué control deben ejercer las autoridades y jefaturas sobre el personal de su "
        "dependencia, según el art. 11 de la Ley 18.575?",
        [
            "Un control jerárquico permanente del funcionamiento de los órganos y de la "
            "actuación del personal.",
            "Ningún control: el control corresponde solo a la Contraloría.",
            "Un control ocasional, solo cuando hay denuncias.",
            "Un control exclusivamente financiero.",
        ],
        "A",
        "Es la A porque el art. 11 encarga a las autoridades y jefaturas, dentro de su "
        "competencia, un control jerárquico permanente que se extiende a la eficiencia y "
        "eficacia en el cumplimiento de los fines y a la legalidad y oportunidad de las "
        "actuaciones. La B no, porque el control externo de la Contraloría no excluye el "
        "jerárquico. La C no, porque el control es permanente. La D no, porque abarca "
        "también la legalidad y la oportunidad.",
        f"{LBGAE}, art. 11; {UC}, cap. II",
    ),
    (
        "Administración centralizada y descentralizada",
        2,
        "¿Qué distingue a un servicio público descentralizado de uno centralizado?",
        [
            "El descentralizado tiene personalidad jurídica y patrimonio propios, y está "
            "sometido a la supervigilancia del Presidente a través del ministerio respectivo.",
            "El descentralizado no está sometido a la ley.",
            "El centralizado tiene patrimonio propio y el descentralizado actúa con el del "
            "Fisco.",
            "El descentralizado es siempre una empresa privada.",
        ],
        "A",
        "Es la A porque así lo disponen los arts. 29 y 30 de la Ley 18.575; los servicios "
        "centralizados, en cambio, actúan con la personalidad jurídica y los bienes del "
        "Fisco y están sometidos a la dependencia del Presidente. La B no, porque ambos "
        "están sometidos a la ley. La C no, porque es al revés. La D no, porque el servicio "
        "descentralizado es un órgano público.",
        f"{LBGAE}, arts. 28 a 30; {UC}, cap. II",
    ),
    (
        "Administración centralizada y descentralizada",
        3,
        "¿Qué es la desconcentración según el art. 33 de la Ley 18.575?",
        [
            "La atribución por ley de competencias propias a órganos inferiores de un mismo "
            "servicio, sin que adquieran personalidad jurídica distinta.",
            "La creación de una nueva persona jurídica de derecho público.",
            "La delegación de funciones en un particular mediante contrato.",
            "La transferencia de un servicio a una municipalidad.",
        ],
        "A",
        "Es la A porque el art. 33 permite a la ley desconcentrar territorial o "
        "funcionalmente determinados órganos, que quedan sometidos a la dependencia "
        "jerárquica general del jefe superior del servicio, sin personalidad propia. La B "
        "no, porque eso es descentralización. La C no, porque la desconcentración opera "
        "dentro de la Administración. La D no, porque la desconcentración no traspasa "
        "competencias a otra persona jurídica.",
        f"{LBGAE}, art. 33; {UC}, cap. II",
    ),
    (
        "Empresas del Estado",
        2,
        "¿Qué exige la Constitución para que el Estado y sus organismos desarrollen "
        "actividades empresariales?",
        [
            "Que una ley de quórum calificado los autorice.",
            "Un decreto supremo fundado del Presidente.",
            "La aprobación de la Contraloría.",
            "Nada especial: pueden desarrollarlas libremente.",
        ],
        "A",
        "Es la A porque el art. 19 n.º 21 inciso 2.º exige ley de quórum calificado; esas "
        "actividades quedan sometidas a la legislación común aplicable a los particulares, "
        "salvo las excepciones que la misma ley establezca por motivos justificados. La B "
        "no, porque un decreto no basta. La C no, porque la Contraloría no da esa "
        "autorización. La D no, porque la Constitución exige autorización legal.",
        f"{CPR}, art. 19 n.º 21; {UC}, cap. II",
    ),
    (
        "La Ley 18.575 y los principios organizativos",
        2,
        "¿En qué casos responde el Estado por los daños que causen los órganos de la "
        "Administración, según el art. 42 de la Ley 18.575?",
        [
            "Por falta de servicio, sin perjuicio de su derecho a repetir contra el "
            "funcionario que hubiere incurrido en falta personal.",
            "Solo cuando el funcionario actúa con dolo comprobado.",
            "Nunca: los daños los paga solo el funcionario.",
            "Solo si el daño supera cierto monto fijado por ley.",
        ],
        "A",
        "Es la A porque el art. 42 establece la responsabilidad del Estado por falta de "
        "servicio y reconoce el derecho de repetición contra el funcionario con falta "
        "personal; el art. 4 consagra en general la responsabilidad del Estado. La B no, "
        "porque la falta de servicio no exige dolo del funcionario. La C no, porque responde "
        "el órgano. La D no, porque la ley no fija un monto mínimo.",
        f"{LBGAE}, arts. 4 y 42; {CPR}, art. 38; {UC}, cap. II",
    ),
    # ------------------------------------------------- acto administrativo
    (
        "Teoría del acto administrativo",
        1,
        "¿Cómo define el art. 3 de la Ley 19.880 el acto administrativo?",
        [
            "Como las decisiones formales que emiten los órganos de la Administración, en las "
            "que se contienen declaraciones de voluntad realizadas en el ejercicio de una "
            "potestad pública.",
            "Como cualquier contrato que celebra el Estado con un particular.",
            "Como las sentencias que dictan los tribunales contencioso-administrativos.",
            "Como las leyes que aprueba el Congreso sobre materias administrativas.",
        ],
        "A",
        "Es la A porque así lo define el art. 3, que agrega que también son actos "
        "administrativos los dictámenes o declaraciones de juicio, constancia o "
        "conocimiento; toman la forma de decretos supremos y resoluciones. La B no, porque "
        "el contrato administrativo es bilateral. La C no, porque las sentencias son actos "
        "jurisdiccionales. La D no, porque las leyes son actos legislativos.",
        f"{LBPA}, art. 3; {UC}, cap. III",
    ),
    (
        "Teoría del acto administrativo",
        2,
        "¿Qué presunciones favorecen a los actos administrativos según el art. 3 de la Ley "
        "19.880?",
        [
            "Presunción de legalidad, de imperio y exigibilidad frente a sus destinatarios, "
            "desde su entrada en vigencia.",
            "Presunción de derecho de que son válidos, que no admite prueba en contrario.",
            "Presunción de ilegalidad mientras no los apruebe un tribunal.",
            "Ninguna presunción: el particular decide si los cumple.",
        ],
        "A",
        "Es la A porque así lo dispone el inciso final del art. 3, salvo que se ordene su "
        "suspensión por la autoridad administrativa al resolver un recurso o por el juez "
        "conociendo por la vía jurisdiccional. La B no, porque la presunción admite prueba en "
        "contrario e impugnación. La C no, porque la presunción es de legalidad. La D no, "
        "porque los actos son exigibles.",
        f"{LBPA}, art. 3; {UC}, cap. III",
    ),
    (
        "Teoría del acto administrativo",
        2,
        "¿Qué regla establece el art. 51 de la Ley 19.880 sobre la ejecución de los actos "
        "administrativos?",
        [
            "Los actos causan inmediata ejecutoriedad, salvo disposición en contrario o que "
            "requieran aprobación o autorización superior.",
            "Los actos solo se ejecutan cuando el particular los acepta.",
            "Los actos solo se ejecutan tras una sentencia judicial que los confirme.",
            "Los actos se ejecutan treinta días después de su notificación.",
        ],
        "A",
        "Es la A porque así lo establece el art. 51, y los actos que afecten derechos de los "
        "particulares no pueden tener efecto retroactivo, salvo que produzcan consecuencias "
        "favorables y no lesionen derechos de terceros (art. 52). La B no, porque no depende "
        "de la aceptación del destinatario. La C no, porque no se requiere sentencia. La D "
        "no, porque la ley no fija ese plazo.",
        f"{LBPA}, arts. 51 y 52; {UC}, cap. III",
    ),
    (
        "Teoría del acto administrativo",
        3,
        "¿Dentro de qué plazo puede la autoridad invalidar un acto contrario a derecho, según "
        "el art. 53 de la Ley 19.880?",
        [
            "Dentro de dos años contados desde su notificación o publicación, previa "
            "audiencia del interesado.",
            "En cualquier tiempo y sin audiencia.",
            "Dentro de seis meses, sin audiencia.",
            "Dentro de cinco años, solo con autorización judicial.",
        ],
        "A",
        "Es la A porque así lo dispone el art. 53, y el acto invalidatorio es impugnable ante "
        "los tribunales en procedimiento breve y sumario. La B no, porque hay plazo y "
        "audiencia previa. La C no, porque el plazo es de dos años y la audiencia es "
        "obligatoria. La D no, porque la invalidación la hace la propia Administración.",
        f"{LBPA}, art. 53; {UC}, cap. III",
    ),
    (
        "Teoría del acto administrativo",
        3,
        "¿En qué caso NO procede la revocación de un acto administrativo, según el art. 61 de "
        "la Ley 19.880?",
        [
            "Cuando se trate de actos declarativos o creadores de derechos adquiridos "
            "legítimamente.",
            "Cuando el acto ya no es conveniente para el interés público.",
            "Cuando el acto es de mero trámite.",
            "Cuando la autoridad que lo dictó cambió.",
        ],
        "A",
        "Es la A porque el art. 61 excluye la revocación de los actos declarativos o "
        "creadores de derechos adquiridos legítimamente, de los que la ley ha determinado "
        "otra forma de extinción y de aquellos cuya naturaleza no permite dejarlos sin "
        "efecto. La B no, porque la inconveniencia es justamente el fundamento de la "
        "revocación. La C no, porque no figura entre las excepciones. La D no, porque el "
        "cambio de titular no impide revocar.",
        f"{LBPA}, art. 61; {UC}, cap. III",
    ),
    # ------------------------------------------- procedimiento administrativo
    (
        "Procedimiento administrativo: la Ley 19.880",
        1,
        "¿Cuál es el plazo máximo de duración del procedimiento administrativo según el art. "
        "27 de la Ley 19.880?",
        [
            "Seis meses desde su iniciación hasta la decisión final, salvo caso fortuito o "
            "fuerza mayor.",
            "Treinta días corridos.",
            "Dos años.",
            "No tiene plazo máximo.",
        ],
        "A",
        "Es la A porque así lo dispone el art. 27. La B no, porque treinta días es el plazo "
        "para resolver ciertos recursos. La C no, porque no es el plazo del procedimiento. La "
        "D no, porque la ley fija un máximo.",
        f"{LBPA}, art. 27; {UC}, cap. III",
    ),
    (
        "Procedimiento administrativo: la Ley 19.880",
        1,
        "¿Cómo se cuentan los plazos de días en la Ley 19.880?",
        [
            "Son de días hábiles, entendiéndose inhábiles los sábados, domingos y festivos.",
            "Son de días corridos, sin excepción.",
            "Son de días hábiles, pero los sábados son hábiles.",
            "Los fija libremente cada servicio.",
        ],
        "A",
        "Es la A porque así lo establece el art. 25 de la Ley 19.880. La B no, porque la "
        "regla es la contraria. La C no, porque los sábados son inhábiles en esta ley. La D "
        "no, porque la ley fija la regla general.",
        f"{LBPA}, art. 25; {UC}, cap. III",
    ),
    (
        "Procedimiento administrativo: la Ley 19.880",
        2,
        "¿Ante quién y en qué plazo se interpone el recurso de reposición?",
        [
            "Ante el mismo órgano que dictó el acto, dentro de cinco días.",
            "Ante la Contraloría, dentro de treinta días.",
            "Ante la Corte de Apelaciones, dentro de diez días.",
            "Ante el superior jerárquico, dentro de un año.",
        ],
        "A",
        "Es la A porque el art. 59 dispone que la reposición se interpone dentro de cinco "
        "días ante el mismo órgano que dictó el acto, y en subsidio puede interponerse el "
        "jerárquico ante el superior. La B no, porque la Contraloría no conoce de este "
        "recurso. La C no, porque es un recurso administrativo, no judicial. La D no, porque "
        "un año es el plazo de la revisión extraordinaria.",
        f"{LBPA}, art. 59; {UC}, cap. III",
    ),
    (
        "Procedimiento administrativo: la Ley 19.880",
        3,
        "¿Qué efecto tiene, por regla general, la interposición de un recurso administrativo "
        "sobre la ejecución del acto?",
        [
            "No la suspende, aunque la autoridad puede suspenderla si el cumplimiento causa "
            "daño irreparable o hace imposible el cumplimiento de lo que se resuelva.",
            "La suspende siempre hasta que se resuelva el recurso.",
            "Deja sin efecto el acto de pleno derecho.",
            "Obliga a remitir el acto al Tribunal Constitucional.",
        ],
        "A",
        "Es la A porque así lo dispone el art. 57 de la Ley 19.880, en coherencia con la "
        "ejecutoriedad de los actos administrativos. La B no, porque la suspensión es "
        "excepcional. La C no, porque el recurso no extingue el acto. La D no, porque el "
        "Tribunal Constitucional no conoce de recursos administrativos.",
        f"{LBPA}, arts. 51 y 57; {UC}, cap. III",
    ),
    (
        "Procedimiento administrativo: la Ley 19.880",
        3,
        "¿Qué ocurre si la Administración no resuelve una solicitud dentro de plazo, en un "
        "caso en que procede el silencio positivo?",
        [
            "El interesado denuncia el incumplimiento y, si la autoridad no se pronuncia en "
            "cinco días, la solicitud se entiende aceptada.",
            "La solicitud se entiende rechazada automáticamente.",
            "El interesado debe presentar una nueva solicitud.",
            "La solicitud se entiende aceptada desde el día siguiente al vencimiento, sin "
            "más trámite.",
        ],
        "A",
        "Es la A porque así lo regula el art. 64; el silencio es negativo, en cambio, cuando "
        "la solicitud afecta el patrimonio fiscal, cuando la Administración actúa de oficio "
        "o cuando se ejerce el derecho de petición (art. 65). La B no, porque eso describe el "
        "silencio negativo. La C no, porque la ley da efecto al silencio. La D no, porque "
        "primero hay que denunciar el incumplimiento.",
        f"{LBPA}, arts. 64 y 65; {UC}, cap. III",
    ),
    (
        "Procedimiento administrativo: la Ley 19.880",
        3,
        "¿Qué es el recurso extraordinario de revisión del art. 60 de la Ley 19.880?",
        [
            "Un recurso ante el superior jerárquico, o ante quien dictó el acto si no lo hay, "
            "contra actos firmes, por causales taxativas y dentro de un año.",
            "Un recurso ordinario contra cualquier acto, en cualquier tiempo.",
            "Un recurso ante la Corte Suprema contra actos administrativos.",
            "El nombre que recibe la reposición cuando se interpone fuera de plazo.",
        ],
        "A",
        "Es la A porque el art. 60 lo concede contra actos firmes por causales como la "
        "falta de emplazamiento, el error de hecho manifiesto o el uso de documentos o "
        "testimonios falsos, y fija un plazo de un año. La B no, porque es extraordinario y "
        "tiene plazo y causales. La C no, porque es un recurso administrativo. La D no, "
        "porque es un recurso distinto.",
        f"{LBPA}, art. 60; {UC}, cap. III",
    ),
    (
        "Procedimiento administrativo: la Ley 19.880",
        2,
        "¿Qué principio del procedimiento administrativo obliga a la autoridad a abstenerse "
        "de intervenir cuando tiene interés personal en el asunto?",
        [
            "El de imparcialidad, desarrollado en las causales de abstención del art. 12.",
            "El de celeridad.",
            "El de economía procedimental.",
            "El de escrituración.",
        ],
        "A",
        "Es la A porque el art. 11 consagra el principio de imparcialidad y el art. 12 "
        "obliga a abstenerse a las autoridades y funcionarios con interés personal, "
        "parentesco o amistad íntima con los interesados, entre otras causales. La B no, "
        "porque la celeridad busca la rapidez del procedimiento. La C no, porque la economía "
        "procedimental busca evitar trámites dilatorios. La D no, porque la escrituración se "
        "refiere a la forma del procedimiento.",
        f"{LBPA}, arts. 4, 11 y 12; {UC}, cap. III",
    ),
]
