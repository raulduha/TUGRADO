"""Cédula UC de Derecho Constitucional II: constitucional orgánico (electiva)."""

JURISDICCION = "Chile"
PROGRAMA = "Cédulas UC (licenciatura, vigentes desde 2021)"
CEDULA = "Cédula 10: Derecho Constitucional II, Constitucional Orgánico (18-03-2021)"
MATERIA = "Derecho Constitucional II (Orgánico)"

CPR = "Constitución Política"
UC = "Cédula UC Derecho Constitucional II"

PREGUNTAS = [
    # -------------------------------------------------- fuentes y bases
    (
        "Fuentes del Derecho Constitucional",
        2,
        "¿Qué cambio introdujo la reforma constitucional de 2005 (Ley 20.050) en la "
        "composición del Senado?",
        [
            "Eliminó a los senadores designados y vitalicios.",
            "Creó los senadores designados por las Fuerzas Armadas.",
            "Redujo el Senado a 20 miembros.",
            "Estableció que los senadores fueran elegidos por la Cámara de Diputados.",
        ],
        "A",
        "Es la A porque la Ley 20.050 suprimió los senadores designados y vitalicios, y desde "
        "entonces el Senado se integra solo con miembros elegidos en votación directa. La B "
        "no, porque esos senadores existían antes y la reforma los eliminó. La C no, porque "
        "no redujo el Senado a ese número; hoy tiene 50 miembros. La D no, porque los "
        "senadores se eligen por votación directa.",
        f"{CPR}, art. 49; Ley 20.050; {UC}, cap. I",
    ),
    (
        "Bases de la institucionalidad",
        2,
        "¿Qué autoridad dirige hoy el gobierno regional como órgano ejecutivo, según la "
        "Constitución?",
        [
            "El gobernador regional, elegido por sufragio universal.",
            "El intendente, nombrado por el Presidente de la República.",
            "El delegado presidencial regional.",
            "El alcalde de la capital regional.",
        ],
        "A",
        "Es la A porque, desde la reforma de 2017 y la primera elección de 2021, el gobernador "
        "regional, elegido por votación directa, es el órgano ejecutivo del gobierno "
        "regional. La B no, porque la figura del intendente fue reemplazada. La C no, porque "
        "el delegado presidencial regional, de exclusiva confianza del Presidente, ejerce el "
        "gobierno interior en la región, no la administración regional. La D no, porque el "
        "alcalde dirige la municipalidad.",
        f"{CPR}, arts. 111 y 115 bis; Ley 20.990; {UC}, cap. II",
    ),
    # ---------------------------------------------------- función gubernativa
    (
        "Presidente de la República",
        1,
        "¿Por cuánto tiempo dura en su cargo el Presidente de la República y puede ser "
        "reelegido para el período siguiente?",
        [
            "Cuatro años, sin posibilidad de reelección para el período siguiente.",
            "Seis años, con reelección inmediata por una vez.",
            "Cuatro años, con reelección inmediata por una vez.",
            "Ocho años, sin reelección.",
        ],
        "A",
        "Es la A porque el art. 25 fija un período de cuatro años y prohíbe la reelección "
        "para el período siguiente. La B no, porque el período de seis años rigió antes de la "
        "reforma de 2005. La C no, porque la reelección inmediata está prohibida. La D no, "
        "porque el período es de cuatro años.",
        f"{CPR}, art. 25; {UC}, cap. III",
    ),
    (
        "Presidente de la República",
        2,
        "¿Qué edad mínima exige el art. 25 de la Constitución para ser elegido Presidente de "
        "la República?",
        [
            "35 años.",
            "40 años.",
            "30 años.",
            "21 años.",
        ],
        "A",
        "Es la A porque el art. 25 exige tener cumplidos 35 años, además de la nacionalidad "
        "chilena según los n.os 1 o 2 del art. 10 y poseer las demás calidades para ser "
        "ciudadano con derecho a sufragio. La B no, porque los 40 años rigieron antes de la "
        "reforma de 2005. La C no, porque no es la edad exigida. La D no, porque 21 años es "
        "la edad exigida para ser diputado.",
        f"{CPR}, art. 25; {UC}, cap. III",
    ),
    (
        "Presidente de la República",
        2,
        "Si ningún candidato a Presidente obtiene la mayoría absoluta de los votos válidamente "
        "emitidos, ¿qué ocurre?",
        [
            "Se realiza una segunda votación entre los dos candidatos con las más altas "
            "mayorías relativas.",
            "El Congreso Pleno elige entre los tres candidatos más votados.",
            "Asume el candidato con más votos, aunque no tenga mayoría absoluta.",
            "Se repite la elección con todos los candidatos.",
        ],
        "A",
        "Es la A porque el art. 26 ordena una segunda votación entre las dos más altas "
        "mayorías relativas; para calcular la mayoría absoluta, los votos en blanco y nulos "
        "se consideran no emitidos. La B no, porque la elección por el Congreso Pleno rigió "
        "en la Constitución de 1925. La C no, porque se exige mayoría absoluta. La D no, "
        "porque la segunda vuelta es solo entre dos candidatos.",
        f"{CPR}, art. 26; {UC}, cap. III",
    ),
    (
        "Presidente de la República",
        2,
        "¿Qué es la potestad reglamentaria autónoma del Presidente de la República?",
        [
            "La facultad de dictar reglamentos, decretos e instrucciones en las materias que "
            "no sean propias del dominio legal.",
            "La facultad de dictar normas con rango de ley sin autorización del Congreso.",
            "La facultad de reglamentar la ejecución de las leyes, exclusivamente.",
            "La facultad de modificar leyes por decreto en casos urgentes.",
        ],
        "A",
        "Es la A porque el art. 32 n.º 6 distingue la potestad autónoma, en materias que no "
        "son de dominio legal, de la potestad de ejecución, que permite dictar reglamentos "
        "para la ejecución de las leyes. La B no, porque las normas con rango de ley "
        "requieren delegación del Congreso (art. 64). La C no, porque esa es la potestad de "
        "ejecución. La D no, porque el Presidente no puede modificar leyes por decreto.",
        f"{CPR}, arts. 32 n.º 6, 63 y 64; {UC}, cap. III",
    ),
    (
        "Presidente de la República",
        3,
        "¿Qué límite tiene la delegación de facultades legislativas al Presidente (decretos "
        "con fuerza de ley)?",
        [
            "No puede exceder de un año ni extenderse a materias como nacionalidad, "
            "ciudadanía, elecciones, plebiscito o garantías constitucionales.",
            "Puede otorgarse por tiempo indefinido sobre cualquier materia.",
            "Solo puede referirse a materias tributarias.",
            "La otorga la Corte Suprema a petición del Presidente.",
        ],
        "A",
        "Es la A porque el art. 64 permite que el Congreso autorice al Presidente a dictar "
        "disposiciones con fuerza de ley por un plazo no superior a un año, y excluye esas "
        "materias y las de leyes orgánicas constitucionales o de quórum calificado. La B no, "
        "porque hay límite de tiempo y de materias. La C no, porque no se limita a lo "
        "tributario. La D no, porque la autorización la da el Congreso por ley.",
        f"{CPR}, art. 64; {UC}, cap. III",
    ),
    (
        "Ministros de Estado",
        2,
        "¿Qué son los Ministros de Estado según el art. 33 de la Constitución?",
        [
            "Colaboradores directos e inmediatos del Presidente en el gobierno y "
            "administración del Estado.",
            "Representantes del Congreso ante el Gobierno.",
            "Funcionarios inamovibles nombrados por concurso público.",
            "Miembros del Poder Judicial con funciones administrativas.",
        ],
        "A",
        "Es la A porque así los define el art. 33; son de exclusiva confianza del Presidente "
        "y para ser nombrado se requiere ser chileno, tener 21 años y cumplir los requisitos "
        "generales de ingreso a la Administración (art. 34). La B no, porque no representan "
        "al Congreso. La C no, porque el Presidente los nombra y remueve a su voluntad. La D "
        "no, porque pertenecen al Gobierno, no al Poder Judicial.",
        f"{CPR}, arts. 33 y 34; {UC}, cap. III",
    ),
    # ---------------------------------------------------- función legislativa
    (
        "Congreso Nacional",
        1,
        "¿Cuántos miembros tiene la Cámara de Diputados?",
        [
            "155.",
            "120.",
            "50.",
            "200.",
        ],
        "A",
        "Es la A porque el art. 47 dispone que la Cámara se integra por 155 miembros elegidos "
        "en votación directa por distritos electorales. La B no, porque 120 era el número "
        "antes de la reforma electoral de 2015. La C no, porque 50 es el número de "
        "senadores. La D no, porque no es el número fijado.",
        f"{CPR}, art. 47; Ley 20.840; {UC}, cap. IV",
    ),
    (
        "Congreso Nacional",
        2,
        "¿Cuál es una atribución exclusiva de la Cámara de Diputados?",
        [
            "Fiscalizar los actos del Gobierno.",
            "Conocer de las acusaciones constitucionales como jurado y declarar la "
            "culpabilidad.",
            "Otorgar la rehabilitación de la ciudadanía.",
            "Prestar su acuerdo para el nombramiento del Fiscal Nacional.",
        ],
        "A",
        "Es la A porque el art. 52 n.º 1 entrega a la Cámara la fiscalización de los actos "
        "del Gobierno, y el n.º 2 le encarga declarar si han o no lugar las acusaciones "
        "constitucionales. La B no, porque conocer y resolver la acusación corresponde al "
        "Senado (art. 53 n.º 1). La C no, porque la rehabilitación de la ciudadanía la otorga "
        "el Senado. La D no, porque el acuerdo para nombrar al Fiscal Nacional lo presta el "
        "Senado.",
        f"{CPR}, arts. 52 y 53; {UC}, cap. IV",
    ),
    (
        "Congreso Nacional",
        2,
        "¿Qué protege el fuero parlamentario del art. 61 de la Constitución?",
        [
            "Que ningún diputado o senador pueda ser acusado o privado de libertad, salvo "
            "delito flagrante, sin que la Corte de Apelaciones respectiva, en pleno, autorice "
            "previamente la acusación.",
            "Que los parlamentarios no puedan ser juzgados nunca por delitos comunes.",
            "Que los parlamentarios no paguen impuestos durante su período.",
            "Que solo el Senado pueda juzgar penalmente a los diputados.",
        ],
        "A",
        "Es la A porque el fuero exige el desafuero previo por la Corte de Apelaciones en "
        "pleno, con apelación ante la Corte Suprema; además, el mismo artículo consagra la "
        "inviolabilidad por las opiniones y votos emitidos en el desempeño del cargo. La B "
        "no, porque, desaforado, el parlamentario puede ser juzgado. La C no, porque el fuero "
        "no tiene contenido tributario. La D no, porque el juzgamiento corresponde a los "
        "tribunales ordinarios.",
        f"{CPR}, art. 61; {UC}, cap. IV",
    ),
    (
        "Congreso Nacional",
        3,
        "En una acusación constitucional contra el Presidente de la República, ¿qué quórum "
        "exige el Senado para declararlo culpable?",
        [
            "Los dos tercios de los senadores en ejercicio.",
            "La mayoría de los senadores presentes.",
            "La mayoría absoluta de los senadores en ejercicio.",
            "La unanimidad de los senadores.",
        ],
        "A",
        "Es la A porque el art. 53 n.º 1 exige los dos tercios de los senadores en ejercicio "
        "cuando se trata del Presidente, y la mayoría de los senadores en ejercicio en los "
        "demás casos. La B no, porque no basta la mayoría de los presentes. La C no, porque "
        "esa mayoría rige para las demás autoridades. La D no, porque no se exige "
        "unanimidad.",
        f"{CPR}, arts. 52 n.º 2 y 53 n.º 1; {UC}, cap. IV",
    ),
    (
        "La ley",
        2,
        "¿Qué sistema adopta el art. 63 de la Constitución respecto de las materias de ley?",
        [
            "El de dominio legal máximo: solo son materias de ley las que la Constitución "
            "enumera.",
            "El de dominio legal mínimo: la ley puede regular cualquier materia.",
            "El de dominio reglamentario exclusivo del Presidente.",
            "El de legislación por plebiscito.",
        ],
        "A",
        "Es la A porque el art. 63 enumera taxativamente las materias de ley y deja las demás "
        "a la potestad reglamentaria autónoma del Presidente. La B no, porque ese sistema "
        "regía en la Constitución de 1925. La C no, porque el Presidente no tiene dominio "
        "exclusivo sobre todas las materias. La D no, porque la ley se forma en el Congreso.",
        f"{CPR}, arts. 32 n.º 6 y 63; {UC}, cap. IV",
    ),
    (
        "La ley",
        2,
        "¿Cuál de estas materias es de iniciativa exclusiva del Presidente de la República?",
        [
            "Imponer, suprimir, reducir o condonar tributos.",
            "Reformar el Código Civil en materia de familia.",
            "Conceder amnistías generales.",
            "Modificar el Código Penal.",
        ],
        "A",
        "Es la A porque el art. 65 reserva al Presidente la iniciativa de las leyes sobre "
        "tributos, creación de servicios públicos, administración financiera del Estado, "
        "entre otras. La B no, porque esa materia admite moción parlamentaria. La C no, "
        "porque las amnistías pueden originarse en moción y su cámara de origen es el "
        "Senado. La D no, porque las leyes penales no son de iniciativa exclusiva.",
        f"{CPR}, art. 65; {UC}, cap. IV",
    ),
    (
        "La ley",
        2,
        "¿En qué cámara deben tener su origen las leyes sobre tributos?",
        [
            "En la Cámara de Diputados.",
            "En el Senado.",
            "En cualquiera de las dos, indistintamente.",
            "En el Congreso Pleno.",
        ],
        "A",
        "Es la A porque el art. 65 inciso 2.º dispone que las leyes sobre tributos, "
        "presupuestos y reclutamiento solo pueden tener origen en la Cámara de Diputados, y "
        "las de amnistía e indultos generales, solo en el Senado. La B no, porque al Senado "
        "le corresponden la amnistía y los indultos generales. La C no, porque la "
        "Constitución fija la cámara de origen. La D no, porque el Congreso Pleno no es "
        "cámara de origen.",
        f"{CPR}, art. 65; {UC}, cap. IV",
    ),
    (
        "La ley",
        3,
        "Si el Presidente veta un proyecto de ley y las cámaras no aprueban sus "
        "observaciones, ¿cómo puede el Congreso imponer su texto?",
        [
            "Insistiendo por los dos tercios de los miembros presentes de cada cámara.",
            "Por mayoría simple de cada cámara.",
            "Pidiendo al Tribunal Constitucional que deje sin efecto el veto.",
            "No puede: el veto presidencial es absoluto.",
        ],
        "A",
        "Es la A porque el art. 73 permite al Congreso insistir por los dos tercios de sus "
        "miembros presentes en la totalidad o parte del proyecto aprobado por él, y entonces "
        "se devuelve al Presidente para su promulgación. La B no, porque se exige un quórum "
        "reforzado. La C no, porque el Tribunal Constitucional no resuelve el desacuerdo "
        "político sobre el veto. La D no, porque el veto es suspensivo.",
        f"{CPR}, art. 73; {UC}, cap. IV",
    ),
    # ------------------------------------------------------- función judicial
    (
        "Función judicial",
        2,
        "¿Cómo se nombra a los ministros de la Corte Suprema?",
        [
            "Los nombra el Presidente de una quina propuesta por la Corte, con acuerdo del "
            "Senado adoptado por los dos tercios de sus miembros en ejercicio.",
            "Los elige la Cámara de Diputados por mayoría absoluta.",
            "Los elige la propia Corte Suprema por cooptación, sin intervención de otros "
            "poderes.",
            "Los nombra el Presidente libremente.",
        ],
        "A",
        "Es la A porque así lo dispone el art. 78; cinco de los ministros deben ser abogados "
        "extraños a la administración de justicia. La B no, porque la Cámara no interviene. "
        "La C no, porque intervienen el Presidente y el Senado. La D no, porque el "
        "nombramiento exige quina y acuerdo del Senado.",
        f"{CPR}, art. 78; {UC}, cap. V",
    ),
    (
        "Función judicial",
        2,
        "¿Qué tribunales quedan excluidos de la superintendencia directiva, correccional y "
        "económica de la Corte Suprema?",
        [
            "El Tribunal Constitucional, el Tribunal Calificador de Elecciones y los "
            "tribunales electorales regionales.",
            "Las Cortes de Apelaciones.",
            "Los juzgados de garantía y los tribunales de juicio oral en lo penal.",
            "Los juzgados de letras del trabajo.",
        ],
        "A",
        "Es la A porque el art. 82 exceptúa expresamente a esos tribunales. La B no, porque "
        "las Cortes de Apelaciones están bajo esa superintendencia. La C no, porque los "
        "tribunales penales también lo están. La D no, porque los juzgados del trabajo "
        "también.",
        f"{CPR}, art. 82; {UC}, cap. V",
    ),
    (
        "Función judicial",
        2,
        "¿Qué órgano conoce del escrutinio general y la calificación de las elecciones de "
        "Presidente, diputados y senadores?",
        [
            "El Tribunal Calificador de Elecciones.",
            "El Servicio Electoral.",
            "La Corte Suprema.",
            "El Tribunal Constitucional.",
        ],
        "A",
        "Es la A porque el art. 95 le entrega el escrutinio general y la calificación de "
        "esas elecciones y de los plebiscitos, y la proclamación de los electos. La B no, "
        "porque el Servicio Electoral administra el proceso, sin calificarlo. La C no, porque "
        "no tiene esa competencia. La D no, porque el Tribunal Constitucional controla la "
        "constitucionalidad de las normas.",
        f"{CPR}, art. 95; {UC}, cap. V",
    ),
    # ---------------------------- Contraloría, Tribunal Constitucional y Banco Central
    (
        "Contraloría, Tribunal Constitucional y Banco Central",
        2,
        "¿Cuántos ministros integran el Tribunal Constitucional?",
        [
            "Diez.",
            "Siete.",
            "Quince.",
            "Cinco.",
        ],
        "A",
        "Es la A porque el art. 92 lo integra con diez ministros: tres designados por el "
        "Presidente, cuatro elegidos por el Congreso y tres elegidos por la Corte Suprema; "
        "duran nueve años. La B no, porque siete era su composición antes de 2005. La C no, "
        "porque no es el número fijado. La D no, porque tampoco lo es.",
        f"{CPR}, art. 92; {UC}, cap. VI",
    ),
    (
        "Contraloría, Tribunal Constitucional y Banco Central",
        3,
        "¿Qué se requiere para que el Tribunal Constitucional declare inconstitucional un "
        "precepto legal con efectos generales (art. 93 n.º 7)?",
        [
            "Que antes haya sido declarado inaplicable y que lo acuerden los cuatro quintos de "
            "sus integrantes en ejercicio.",
            "Basta una sentencia de la Corte Suprema que lo considere inconstitucional.",
            "Solo la petición del Presidente de la República.",
            "La mayoría simple de los ministros presentes, sin requisitos previos.",
        ],
        "A",
        "Es la A porque la declaración de inconstitucionalidad exige una previa declaración "
        "de inaplicabilidad conforme al n.º 6 y un quórum de cuatro quintos de los "
        "integrantes en ejercicio; el precepto se entiende derogado desde la publicación de "
        "la sentencia. La B no, porque la Corte Suprema ya no conoce de la inaplicabilidad. "
        "La C no, porque hay acción pública y el tribunal puede actuar de oficio. La D no, "
        "porque el quórum es reforzado.",
        f"{CPR}, arts. 93 n.os 6 y 7, y 94; {UC}, cap. VI",
    ),
    (
        "Contraloría, Tribunal Constitucional y Banco Central",
        2,
        "Si la Contraloría representa un decreto por ilegal, ¿qué puede hacer el Presidente?",
        [
            "Insistir con la firma de todos sus ministros, salvo que el decreto sea "
            "inconstitucional o sea un decreto con fuerza de ley que exceda la delegación.",
            "Insistir siempre, incluso si el decreto es inconstitucional.",
            "Nada: la representación es definitiva.",
            "Recurrir de protección ante la Corte de Apelaciones.",
        ],
        "A",
        "Es la A porque el art. 99 permite el decreto de insistencia ante una representación "
        "por ilegalidad, pero no ante un decreto inconstitucional o un decreto con fuerza de "
        "ley que exceda la delegación; en esos casos, el Presidente puede recurrir al "
        "Tribunal Constitucional. La B no, porque la insistencia no procede por "
        "inconstitucionalidad. La C no, porque la insistencia está prevista. La D no, porque "
        "no es la vía constitucional para la toma de razón.",
        f"{CPR}, arts. 98, 99 y 93 n.º 9; {UC}, cap. VI",
    ),
    (
        "Contraloría, Tribunal Constitucional y Banco Central",
        2,
        "¿Qué prohibición establece la Constitución al Banco Central respecto del gasto "
        "público?",
        [
            "Ningún gasto público o préstamo puede financiarse con créditos directos o "
            "indirectos del Banco Central, salvo en caso de guerra exterior o peligro de ella.",
            "No puede comprar títulos emitidos por bancos privados en ningún caso.",
            "Debe financiar el déficit fiscal cuando el Presidente lo solicite.",
            "No puede fijar las tasas de interés.",
        ],
        "A",
        "Es la A porque así lo dispone el art. 109, que permite esa excepción calificada por "
        "decreto supremo; el Banco Central es un organismo autónomo de rango constitucional "
        "(art. 108). La B no, porque la Constitución no lo prohíbe en esos términos y su ley "
        "orgánica le permite operar con instituciones financieras. La C no, porque esa "
        "posibilidad está prohibida. La D no, porque la política monetaria, incluidas las "
        "tasas, es parte de sus funciones.",
        f"{CPR}, arts. 108 y 109; {UC}, cap. VI",
    ),
    # --------------------------------------------------- reforma constitucional
    (
        "Reforma constitucional",
        3,
        "Tras la Ley 21.481 de 2022, ¿qué quórum exige el art. 127 para aprobar un proyecto "
        "de reforma constitucional en cada cámara?",
        [
            "Los cuatro séptimos de los diputados y senadores en ejercicio.",
            "Los dos tercios de los diputados y senadores en ejercicio, en todos los "
            "capítulos.",
            "La mayoría simple de los presentes.",
            "La unanimidad del Congreso Pleno.",
        ],
        "A",
        "Es la A porque la Ley 21.481 unificó el quórum de reforma constitucional en cuatro "
        "séptimos de los diputados y senadores en ejercicio; antes se exigían tres quintos y, "
        "para ciertos capítulos, dos tercios. La B no, porque ese quórum reforzado se "
        "eliminó. La C no, porque la reforma exige un quórum especial. La D no, porque no se "
        "exige unanimidad.",
        f"{CPR}, art. 127; Ley 21.481; {UC}, cap. VII",
    ),
]
