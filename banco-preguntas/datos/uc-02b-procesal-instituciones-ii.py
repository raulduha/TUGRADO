"""Cédula UC de Derecho Procesal, parte II (Instituciones procesales II)."""

JURISDICCION = "Chile"
PROGRAMA = "Cédulas UC (licenciatura, vigentes desde 2021)"
CEDULA = "Cédula 2: Derecho Procesal (15-03-2021)"
MATERIA = "Derecho Procesal"

CPR = "Constitución Política"
COT = "Código Orgánico de Tribunales"
CPC = "Código de Procedimiento Civil"
CPP = "Código Procesal Penal"
UC = "Cédula UC Derecho Procesal"

PREGUNTAS = [
    # ------------------------------------------------- cap. I: sujetos procesales
    (
        "Tribunales: concepto y clasificación",
        1,
        "Según el art. 5 del COT, ¿cómo se clasifican los tribunales chilenos?",
        [
            "En civiles y penales, únicamente.",
            "En ordinarios, especiales y arbitrales.",
            "En públicos y privados.",
            "En nacionales e internacionales.",
        ],
        "B",
        "Es la B porque el art. 5 COT distingue los tribunales ordinarios (Corte Suprema, "
        "Cortes de Apelaciones, juzgados de letras, tribunales orales en lo penal, juzgados "
        "de garantía…), los especiales (por ejemplo, de familia o del trabajo) y los "
        "arbitrales. La A no, porque la clasificación legal no es por materia. La C no, "
        "porque los arbitrales también ejercen jurisdicción y no son «privados» en ese "
        "sentido. La D no, porque el COT regula los tribunales nacionales.",
        f"{COT}, art. 5; {UC}, II, cap. I, 1.2",
    ),
    (
        "Tribunales: concepto y clasificación",
        2,
        "¿Cuál de estos tribunales es colegiado?",
        [
            "El juzgado de letras.",
            "El juzgado de garantía.",
            "El tribunal de juicio oral en lo penal, que funciona en salas de tres jueces.",
            "El juez árbitro único.",
        ],
        "C",
        "Es la C porque el tribunal de juicio oral en lo penal resuelve en salas integradas "
        "por tres jueces. La A no, porque el juzgado de letras es unipersonal. La B no, "
        "porque el juez de garantía actúa en forma unipersonal. La D no, porque un árbitro "
        "único es, por definición, unipersonal.",
        f"{COT}, art. 17; {UC}, II, cap. I, 1.2.3",
    ),
    (
        "Tribunales ordinarios superiores",
        1,
        "¿Por cuántos ministros está compuesta la Corte Suprema?",
        [
            "Por 9 ministros.",
            "Por 15 ministros.",
            "Por 21 ministros.",
            "Por 30 ministros.",
        ],
        "C",
        "Es la C porque la Corte Suprema se compone de 21 ministros, uno de los cuales es su "
        "presidente (art. 78 de la Constitución y art. 93 COT). Las demás alternativas no "
        "corresponden a la composición legal. La A no, porque 9 es menos de la mitad. La B "
        "no, porque 15 no es el número legal. La D no, porque excede la composición fijada "
        "por la Constitución.",
        f"{CPR}, art. 78; {COT}, art. 93; {UC}, II, cap. I, 1.3.1",
    ),
    (
        "Tribunales ordinarios superiores",
        2,
        "¿Qué tribunal conoce en primera instancia del recurso de protección?",
        [
            "El juez de letras del domicilio del recurrente.",
            "La Corte de Apelaciones respectiva, y de la apelación conoce la Corte Suprema.",
            "Directamente la Corte Suprema, en única instancia.",
            "El Tribunal Constitucional.",
        ],
        "B",
        "Es la B porque el art. 20 de la Constitución entrega el recurso de protección a la "
        "Corte de Apelaciones respectiva, y su sentencia es apelable ante la Corte Suprema. "
        "La A no, porque no lo conoce un juez de letras. La C no, porque la Corte Suprema "
        "conoce en segunda instancia. La D no, porque el Tribunal Constitucional no conoce de "
        "la protección.",
        f"{CPR}, art. 20; {COT}, art. 63; {UC}, II, cap. I, 1.3.2",
    ),
    (
        "Jueces de letras, juzgados de garantía y tribunales orales",
        2,
        "¿Cuál de estas es una función del juez de garantía?",
        [
            "Conocer de la apelación contra las sentencias del tribunal oral.",
            "Asegurar los derechos del imputado y demás intervinientes, y dirigir la audiencia "
            "de preparación del juicio oral.",
            "Investigar los delitos.",
            "Conocer de los juicios civiles de mayor cuantía.",
        ],
        "B",
        "Es la B porque el art. 14 COT encarga al juez de garantía asegurar los derechos del "
        "imputado y demás intervinientes, dirigir la audiencia de preparación del juicio oral "
        "y conocer, entre otros, del procedimiento abreviado y del simplificado. La A no, "
        "porque las sentencias del tribunal oral son inapelables (art. 364 CPP). La C no, "
        "porque la investigación la dirige en forma exclusiva el Ministerio Público (art. 83 "
        "CPR). La D no, porque esos juicios los conocen los jueces de letras.",
        f"{COT}, art. 14; {CPP}, art. 364; {UC}, II, cap. I, 1.3.6",
    ),
    (
        "Jueces de letras, juzgados de garantía y tribunales orales",
        1,
        "¿Qué tribunal conoce y falla los juicios orales por crímenes y simples delitos?",
        [
            "El juzgado de garantía.",
            "La Corte de Apelaciones.",
            "El tribunal de juicio oral en lo penal.",
            "El juzgado de letras en lo civil.",
        ],
        "C",
        "Es la C porque el art. 18 COT entrega al tribunal de juicio oral en lo penal el "
        "conocimiento y fallo de las causas por crimen o simple delito, salvo las que deban "
        "conocerse en el procedimiento abreviado o simplificado (que van ante el juez de "
        "garantía). La A no, porque el juez de garantía prepara el juicio oral, no lo falla. "
        "La B no, porque la Corte conoce de recursos. La D no, porque no es un tribunal "
        "penal.",
        f"{COT}, art. 18; {UC}, II, cap. I, 1.3.5",
    ),
    (
        "Tribunales arbitrales",
        2,
        "¿Qué distingue a un árbitro arbitrador de un árbitro de derecho?",
        [
            "El arbitrador debe ser siempre abogado.",
            "El arbitrador falla obedeciendo a lo que su prudencia y la equidad le dictaren y "
            "tramita según lo que las partes hayan acordado; el de derecho falla conforme a la "
            "ley y se somete a las reglas de procedimiento de los jueces ordinarios.",
            "El de derecho no puede ser recusado.",
            "El arbitrador solo puede conocer asuntos penales.",
        ],
        "B",
        "Es la B porque así los define el art. 223 COT; el mixto tramita como arbitrador y "
        "falla conforme a derecho. La A no, porque es el árbitro de derecho el que debe ser "
        "abogado (art. 225 COT). La C no, porque los árbitros pueden ser inhabilitados. La D "
        "no, porque las causas criminales son materia de arbitraje prohibido (art. 230 COT).",
        f"{COT}, arts. 222, 223, 225 y 230; {UC}, II, cap. I, 1.4",
    ),
    (
        "Tribunales arbitrales",
        3,
        "¿Qué diferencia hay entre el compromiso y la cláusula compromisoria?",
        [
            "Son lo mismo.",
            "En el compromiso las partes someten un asunto a un árbitro determinado; en la "
            "cláusula compromisoria acuerdan someterlo a arbitraje, pero sin designar todavía "
            "al árbitro.",
            "La cláusula compromisoria solo procede en materia penal.",
            "El compromiso no necesita constar por escrito ni en forma alguna.",
        ],
        "B",
        "Es la B porque esa es la distinción doctrinaria y legal: el compromiso debe "
        "contener, entre otras menciones, el nombre del árbitro (art. 234 COT), mientras que "
        "la cláusula compromisoria obliga a las partes a someter el asunto a arbitraje y "
        "deja la designación para después. La A no, porque se distinguen por la designación "
        "del árbitro. La C no, porque el arbitraje en materia penal está prohibido. La D no, "
        "porque el compromiso debe constar por escrito (art. 234 COT).",
        f"{COT}, arts. 232 y 234; {UC}, II, cap. I, 1.4.2",
    ),
    (
        "Partes, litisconsorcio y terceros",
        2,
        "¿Cuándo pueden varias personas demandar o ser demandadas en un mismo juicio según el "
        "art. 18 CPC?",
        [
            "Nunca: cada una debe iniciar un juicio distinto.",
            "Siempre que se deduzca la misma acción, o acciones que emanen directa e "
            "inmediatamente de un mismo hecho, o que se proceda conjuntamente por muchos o "
            "contra muchos en los casos que autoriza la ley.",
            "Solo si son parientes.",
            "Solo con autorización de la Corte Suprema.",
        ],
        "B",
        "Es la B porque esas son las hipótesis de litisconsorcio del art. 18 CPC; si obran "
        "conjuntamente y deducen las mismas acciones, deben constituir un procurador común "
        "(art. 19). La A no, porque la ley admite el litisconsorcio. La C no, porque el "
        "parentesco es irrelevante. La D no, porque no se requiere autorización.",
        f"{CPC}, arts. 18 y 19; {UC}, II, cap. I, 2.5",
    ),
    (
        "Partes, litisconsorcio y terceros",
        3,
        "¿Qué caracteriza al litisconsorcio necesario?",
        [
            "Que depende solo de la voluntad del demandante.",
            "Que la naturaleza de la relación jurídica exige que todos sus titulares estén en "
            "el juicio, porque la sentencia no puede pronunciarse válidamente respecto de unos "
            "sin afectar a los otros (por ejemplo, la nulidad de un contrato frente a todos los "
            "contratantes).",
            "Que solo existe en materia penal.",
            "Que exige que todos los litisconsortes sean representados por el mismo abogado, "
            "sin excepción.",
        ],
        "B",
        "Es la B porque la doctrina caracteriza así el litisconsorcio necesario, que el CPC "
        "no regula en forma general pero que se desprende de la naturaleza de ciertas "
        "relaciones. En el voluntario, en cambio, la acumulación depende de las partes. La A "
        "no, porque eso describe el voluntario. La C no, porque es una figura civil. La D "
        "no, porque el procurador común es otra regla (art. 19 CPC) y admite excepciones.",
        f"{CPC}, arts. 18 a 21; {UC}, II, cap. I, 2.5.2",
    ),
    (
        "Comparecencia y capacidad procesal",
        2,
        "Según la Ley 18.120, ¿qué exigencia tiene la primera presentación de cada parte en un "
        "asunto ante los tribunales?",
        [
            "Ninguna: cualquiera puede presentarse sin abogado.",
            "Debe ser patrocinada por un abogado habilitado para el ejercicio de la profesión.",
            "Debe ser firmada ante notario.",
            "Debe presentarse en papel sellado.",
        ],
        "B",
        "Es la B porque el art. 1 de la Ley 18.120 exige que la primera presentación de cada "
        "parte o interesado en asuntos contenciosos o no contenciosos sea patrocinada por un "
        "abogado habilitado, salvo las excepciones legales. Además, la parte debe comparecer "
        "por medio de un mandatario judicial habilitado (art. 2). La A no, porque la regla "
        "general es la contraria. La C no, porque no se exige firma ante notario. La D no, "
        "porque no hay tal exigencia.",
        f"Ley 18.120, arts. 1 y 2; {UC}, II, cap. I, 2.3 y 2.4",
    ),
    (
        "Comparecencia y capacidad procesal",
        3,
        "¿Qué diferencia hay entre la capacidad para ser parte y la capacidad procesal?",
        [
            "Son lo mismo.",
            "La capacidad para ser parte es la aptitud para ser titular de derechos y "
            "obligaciones procesales (la tiene toda persona); la capacidad procesal es la "
            "aptitud para actuar válidamente por sí mismo en el proceso.",
            "La capacidad procesal la tienen solo los abogados.",
            "La capacidad para ser parte se adquiere con la mayoría de edad.",
        ],
        "B",
        "Es la B porque esa distinción equivale a la civil entre capacidad de goce y de "
        "ejercicio: un menor puede ser parte, pero debe actuar representado. El ius "
        "postulandi, a su vez, es la aptitud técnica para actuar ante los tribunales, que la "
        "ley reserva en general a los abogados y mandatarios habilitados. La A no, porque son "
        "distintas. La C no, porque eso se acerca al ius postulandi. La D no, porque toda "
        "persona puede ser parte.",
        f"{UC}, II, cap. I, 2.3",
    ),
    (
        "Ministerio Público, Defensoría Penal Pública y Policía",
        1,
        "Según el art. 83 de la Constitución, ¿qué función tiene el Ministerio Público?",
        [
            "Juzgar los delitos.",
            "Dirigir en forma exclusiva la investigación de los hechos constitutivos de delito, "
            "ejercer la acción penal pública y proteger a víctimas y testigos; en ningún caso "
            "puede ejercer funciones jurisdiccionales.",
            "Defender a los imputados que no tienen abogado.",
            "Dictar las sentencias en el procedimiento abreviado.",
        ],
        "B",
        "Es la B porque esa es la definición constitucional del Ministerio Público. La A no, "
        "porque juzgar es función de los tribunales. La C no, porque esa es la función de la "
        "Defensoría Penal Pública. La D no, porque en el procedimiento abreviado falla el juez "
        "de garantía.",
        f"{CPR}, art. 83; {UC}, II, cap. I, 3",
    ),
    (
        "Ministerio Público, Defensoría Penal Pública y Policía",
        2,
        "¿Qué exige el principio de objetividad al Ministerio Público?",
        [
            "Que acuse siempre que haya una denuncia.",
            "Que investigue con igual celo no solo los hechos y circunstancias que funden o "
            "agraven la responsabilidad del imputado, sino también los que la eximan, extingan "
            "o atenúen.",
            "Que no se comunique con la víctima.",
            "Que delegue la investigación en la policía.",
        ],
        "B",
        "Es la B porque así lo establecen el art. 3 de la Ley 19.640 y el art. 77 CPP. La A "
        "no, porque el fiscal puede no acusar (por ejemplo, decidir no perseverar). La C no, "
        "porque el Ministerio Público debe proteger a la víctima. La D no, porque la policía "
        "actúa bajo su dirección, pero no puede delegarle la conducción de la investigación.",
        f"Ley 19.640, art. 3; {CPP}, art. 77; {UC}, II, cap. I, 3.1.2",
    ),
    # --------------------------------------- cap. II: actos procesales y su eficacia
    (
        "Actuaciones judiciales y plazos",
        2,
        "Según el art. 64 CPC, ¿qué carácter tienen los plazos de días establecidos en el "
        "Código de Procedimiento Civil?",
        [
            "Son prorrogables por simple solicitud.",
            "Son fatales, cualquiera sea la forma en que se expresen, salvo los establecidos "
            "para la realización de actuaciones propias del tribunal: vencido el plazo, la "
            "posibilidad de ejercer el derecho se extingue por el solo ministerio de la ley.",
            "Se cuentan siempre de corrido, incluidos los feriados.",
            "Solo obligan al tribunal.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 64 CPC; además, los plazos de días del CPC se "
        "suspenden durante los días feriados (art. 66). La A no, porque la regla general es "
        "la fatalidad. La C no, porque se suspenden en los feriados. La D no, porque los "
        "plazos fatales obligan a las partes.",
        f"{CPC}, arts. 64 y 66; {UC}, II, cap. II, 3.4",
    ),
    (
        "Actuaciones judiciales y plazos",
        3,
        "Como regla general, ¿en qué días y horas deben practicarse las actuaciones judiciales "
        "en materia civil?",
        [
            "En cualquier día y hora.",
            "En días y horas hábiles: son días hábiles los no feriados, y horas hábiles las "
            "que median entre las 8 y las 20 horas, sin perjuicio de que el tribunal pueda "
            "habilitar días u horas inhábiles por causa urgente.",
            "Solo de lunes a viernes, entre las 9 y las 14 horas.",
            "Solo los días que fije la Corte Suprema cada año.",
        ],
        "B",
        "Es la B porque así lo disponen los arts. 59 y 60 CPC. La A no, porque la regla son "
        "los días y horas hábiles. La C no, porque el horario legal es más amplio. La D no, "
        "porque la regla está en la ley.",
        f"{CPC}, arts. 59 y 60; {UC}, II, cap. II, 3",
    ),
    (
        "Resoluciones judiciales",
        2,
        "Según el art. 158 CPC, ¿qué es una sentencia definitiva?",
        [
            "La que resuelve un incidente.",
            "La que pone fin a la instancia, resolviendo la cuestión o asunto que ha sido objeto "
            "del juicio.",
            "La que no admite recurso alguno.",
            "La que dicta la Corte Suprema.",
        ],
        "B",
        "Es la B porque es la definición del art. 158 CPC. La A no, porque fallar un "
        "incidente es propio de las sentencias interlocutorias o de los autos. La C no, "
        "porque eso describe una resolución ejecutoriada, no un tipo de resolución. La D no, "
        "porque cualquier tribunal dicta sentencias definitivas.",
        f"{CPC}, art. 158; {UC}, II, cap. II, 6.2",
    ),
    (
        "Resoluciones judiciales",
        3,
        "Una resolución acoge el abandono del procedimiento alegado por el demandado. ¿Cómo se "
        "clasifica según el art. 158 CPC?",
        [
            "Como decreto.",
            "Como auto.",
            "Como sentencia interlocutoria de primer grado: falla un incidente estableciendo "
            "derechos permanentes a favor de las partes.",
            "Como sentencia definitiva.",
        ],
        "C",
        "Es la C porque la resolución que resuelve el incidente de abandono establece un "
        "derecho permanente (el procedimiento queda abandonado). La A no, porque el decreto "
        "solo arregla la sustanciación del proceso. La B no, porque el auto falla un "
        "incidente sin establecer derechos permanentes. La D no, porque no resuelve la "
        "cuestión objeto del juicio.",
        f"{CPC}, arts. 152, 153 y 158; {UC}, II, cap. II, 6.2",
    ),
    (
        "Desasimiento y ejecutoriedad",
        2,
        "Notificada una sentencia definitiva a una de las partes, el juez advierte que debió "
        "fallar de otra manera. ¿Puede modificarla?",
        [
            "Sí, en cualquier momento.",
            "No, por el desasimiento: notificada una sentencia definitiva o interlocutoria a "
            "alguna de las partes, el tribunal que la dictó no puede alterarla o modificarla, "
            "salvo para aclarar puntos oscuros, salvar omisiones o rectificar errores de copia, "
            "referencia o cálculo.",
            "Sí, si las partes no han apelado.",
            "Sí, pero solo dentro de los tres días siguientes.",
        ],
        "B",
        "Es la B porque esa es la regla del art. 182 CPC, que deja a salvo la aclaración, "
        "rectificación y enmienda. Si el fallo es erróneo, las partes deben recurrir. La A "
        "no, porque el desasimiento lo impide. La C no, porque la falta de apelación no "
        "habilita al juez. La D no, porque no existe ese plazo.",
        f"{CPC}, art. 182; {UC}, II, cap. II, 6.4.1",
    ),
    (
        "Desasimiento y ejecutoriedad",
        2,
        "¿Cuándo se entiende firme o ejecutoriada una resolución según el art. 174 CPC?",
        [
            "Desde que se dicta.",
            "Desde que se notifica a las partes, si no procede recurso alguno; si procede, "
            "desde que se notifica el decreto que la manda cumplir una vez terminados los "
            "recursos o desde que transcurren los plazos sin interponerlos.",
            "Solo cuando la confirma la Corte Suprema.",
            "Cuando han pasado seis meses desde su dictación.",
        ],
        "B",
        "Es la B porque esa es la regla del art. 174 CPC. La A no, porque la resolución debe "
        "estar notificada. La C no, porque no todas las causas llegan a la Corte Suprema. La "
        "D no, porque no se fija un plazo de seis meses.",
        f"{CPC}, art. 174; {UC}, II, cap. II, 6.3",
    ),
    (
        "Notificaciones",
        2,
        "En un juicio civil, ¿cómo debe hacerse la primera notificación a las partes?",
        [
            "Por el estado diario.",
            "Personalmente, entregando copia íntegra de la resolución y de la solicitud en que "
            "recae.",
            "Por avisos en el diario.",
            "Por correo electrónico simple, sin más formalidades.",
        ],
        "B",
        "Es la B porque el art. 40 CPC exige que la primera notificación a las partes o "
        "personas a quienes hayan de afectar sus resultados se haga personalmente. Si la "
        "persona no es habida en dos días distintos y se cumplen los requisitos del art. 44, "
        "procede la notificación personal subsidiaria. La A no, porque el estado diario es la "
        "regla general para las resoluciones posteriores (art. 50). La C no, porque los "
        "avisos son excepcionales (art. 54). La D no, porque no es la forma legal de la "
        "primera notificación.",
        f"{CPC}, arts. 40, 44 y 50; {UC}, II, cap. II, 7.2.1",
    ),
    (
        "Notificaciones",
        3,
        "¿Qué resoluciones deben notificarse por cédula según el art. 48 CPC?",
        [
            "Todas las resoluciones del juicio.",
            "Las sentencias definitivas, las resoluciones en que se reciba la causa a prueba y "
            "las que ordenen la comparecencia personal de las partes.",
            "Solo los decretos.",
            "Solo las resoluciones de la Corte Suprema.",
        ],
        "B",
        "Es la B porque esa es la enumeración del art. 48 CPC; el tribunal puede ordenar "
        "además esta forma de notificación para otras resoluciones. La A no, porque la regla "
        "general es el estado diario. La C no, porque los decretos se notifican por el estado "
        "diario. La D no, porque la norma rige en todos los tribunales civiles.",
        f"{CPC}, arts. 48 y 50; {UC}, II, cap. II, 7.2.1",
    ),
    (
        "Nulidad procesal",
        2,
        "Según el art. 83 CPC, ¿cuándo procede la nulidad procesal?",
        [
            "Ante cualquier vicio de forma, aunque no cause perjuicio.",
            "En los casos que la ley establezca expresamente y en todos aquellos en que exista "
            "un vicio que irrogue a alguna de las partes un perjuicio reparable solo con la "
            "declaración de nulidad.",
            "Solo cuando lo pide la Corte Suprema.",
            "Solo en materia penal.",
        ],
        "B",
        "Es la B porque el art. 83 CPC recoge el principio de trascendencia: no hay nulidad "
        "sin perjuicio. La nulidad debe impetrarse dentro de cinco días contados desde que "
        "aparezca o se acredite que quien deba reclamarla tuvo conocimiento del vicio, salvo "
        "la incompetencia absoluta. La A no, porque se exige perjuicio. La C no, porque la "
        "declaran los tribunales de la causa, a petición de parte o de oficio. La D no, "
        "porque existe también en el proceso civil.",
        f"{CPC}, art. 83; {UC}, II, cap. II, 8.2",
    ),
    (
        "Nulidad procesal",
        3,
        "Una parte advierte un vicio de procedimiento, pero en lugar de alegarlo realiza otras "
        "gestiones en el juicio. Después quiere pedir la nulidad. ¿Qué ocurre, como regla "
        "general?",
        [
            "Puede pedirla en cualquier momento.",
            "Su derecho precluye y el vicio queda saneado, porque la parte que ha originado el "
            "vicio o concurrido a materializarlo, o que lo ha convalidado tácita o expresamente, "
            "no puede demandar la nulidad.",
            "El juez debe anular todo el proceso de oficio.",
            "Debe pedirla mediante un recurso de queja.",
        ],
        "B",
        "Es la B porque el art. 83 inc. 2 CPC impide pedir la nulidad a la parte que originó "
        "el vicio o lo convalidó, y el art. 84 exige promover los incidentes tan pronto como "
        "el hecho llegue a conocimiento de la parte. La A no, porque rige la preclusión. La C "
        "no, porque el juez solo debe corregir de oficio los vicios que anulen el proceso. La "
        "D no, porque la queja procede contra faltas o abusos graves en ciertas resoluciones.",
        f"{CPC}, arts. 83 y 84; {UC}, II, cap. II, 8.2.2",
    ),
    # ---------------------------------------------------- cap. III: teoría de la prueba
    (
        "Objeto, tema y carga de la prueba",
        2,
        "¿Cuál de estos hechos no necesita ser probado en un juicio?",
        [
            "Un hecho controvertido y pertinente.",
            "Un hecho notorio.",
            "El monto de los perjuicios que se demandan.",
            "La existencia del contrato que se discute.",
        ],
        "B",
        "Es la B porque los hechos notorios, los no controvertidos y los amparados por una "
        "presunción legal no son tema de prueba. La A no, porque los hechos sustanciales, "
        "pertinentes y controvertidos son justamente los que fija el tribunal para la prueba "
        "(art. 318 CPC). La C no, porque los perjuicios deben acreditarse. La D no, porque un "
        "contrato discutido debe probarse.",
        f"{CPC}, art. 318; {UC}, II, cap. III, 6",
    ),
    (
        "Objeto, tema y carga de la prueba",
        2,
        "¿Quién debe probar en materia civil según el art. 1698 del Código Civil?",
        [
            "Siempre el demandado.",
            "Siempre el juez.",
            "Incumbe probar las obligaciones o su extinción al que alega aquellas o esta.",
            "Quien tenga más recursos económicos.",
        ],
        "C",
        "Es la C porque esa es la regla general de la carga de la prueba del art. 1698 CC: "
        "el acreedor prueba la obligación y el deudor que alega haberla extinguido prueba la "
        "extinción. La A no, porque la carga se distribuye según lo que cada parte alega. La "
        "B no, porque el juez no tiene la carga de probar. La D no, porque no es un criterio "
        "legal.",
        f"Código Civil, art. 1698; {UC}, II, cap. III, 7",
    ),
    (
        "Admisión y valoración de la prueba",
        2,
        "¿Qué caracteriza al sistema de la sana crítica?",
        [
            "El juez valora la prueba según su íntima convicción, sin necesidad de fundamentar.",
            "La ley fija de antemano el valor de cada medio de prueba.",
            "El juez aprecia libremente la prueba, pero sin contradecir los principios de la "
            "lógica, las máximas de la experiencia y los conocimientos científicamente "
            "afianzados, y debe fundamentar su decisión.",
            "Solo vale la confesión.",
        ],
        "C",
        "Es la C porque así se describe la sana crítica, que recoge, por ejemplo, el art. 297 "
        "CPP. La A no, porque la íntima convicción no exige fundamentación (sistema de "
        "jurados). La B no, porque esa es la prueba legal o tasada, predominante en el CPC. "
        "La D no, porque ningún sistema vigente se limita a la confesión.",
        f"{CPP}, art. 297; {UC}, II, cap. III, 10",
    ),
    (
        "Admisión y valoración de la prueba",
        3,
        "¿Qué diferencia hay entre fuente y medio de prueba?",
        [
            "Son sinónimos.",
            "La fuente es el elemento que existe con independencia del proceso (la persona que "
            "presenció el hecho, el documento); el medio es la actividad por la cual esa fuente "
            "se incorpora al proceso (la declaración del testigo, la agregación del documento).",
            "La fuente solo existe en materia penal.",
            "El medio es el resultado de la valoración del juez.",
        ],
        "B",
        "Es la B porque esa es la distinción clásica de la doctrina (Carnelutti, Sentís "
        "Melendo). La A no, porque son conceptos distintos. La C no, porque existe en todo "
        "proceso. La D no, porque la valoración es una actividad posterior del juez.",
        f"{UC}, II, cap. III, 4",
    ),
    # ----------------------------------------------- cap. IV: sistema recursivo
    (
        "Teoría de los recursos",
        2,
        "¿Qué prohíbe el principio de la reformatio in peius?",
        [
            "Que el recurrente se desista del recurso.",
            "Que el tribunal superior, conociendo solo del recurso de una parte, modifique la "
            "resolución en perjuicio de esa misma parte recurrente.",
            "Que se dicte sentencia en segunda instancia.",
            "Que se presenten nuevos documentos.",
        ],
        "B",
        "Es la B porque la prohibición de reformar en perjuicio protege al único recurrente: "
        "su recurso no puede empeorar su situación. Se vincula con el principio tantum "
        "devolutum quantum appellatum (el superior conoce solo de lo apelado). La A no, "
        "porque el desistimiento es otra institución. La C no, porque la segunda instancia es "
        "precisamente donde opera. La D no, porque la oportunidad de los documentos es otra "
        "materia.",
        f"{UC}, II, cap. IV, 5.1.4",
    ),
    (
        "Teoría de los recursos",
        3,
        "¿Qué distingue a los recursos de mérito (como la apelación) de los recursos de "
        "nulidad (como la casación)?",
        [
            "No hay diferencias.",
            "Los de mérito permiten al superior revisar los hechos y el derecho y dictar una "
            "nueva decisión; los de nulidad buscan invalidar la resolución por causales "
            "específicas y estrictas de derecho.",
            "Los de nulidad solo proceden contra decretos.",
            "Los de mérito solo los conoce la Corte Suprema.",
        ],
        "B",
        "Es la B porque esa es la distinción doctrinaria: la apelación es un recurso ordinario "
        "y amplio, mientras que la casación es extraordinaria y de derecho estricto, con "
        "causales taxativas. La A no, porque se distinguen. La C no, porque la casación "
        "procede contra sentencias definitivas y ciertas interlocutorias. La D no, porque la "
        "apelación la conocen normalmente las Cortes de Apelaciones.",
        f"{CPC}, arts. 186, 764 y 766; {UC}, II, cap. IV, 4",
    ),
    # ----------------------------------------------- cap. V: sistema cautelar
    (
        "Medidas cautelares: características y presupuestos",
        2,
        "¿Cuáles son los presupuestos clásicos de toda medida cautelar?",
        [
            "Sentencia firme y pago previo.",
            "El peligro en la demora (periculum in mora) y la verosimilitud o apariencia de "
            "buen derecho (fumus boni iuris).",
            "Que el demandado lo consienta.",
            "Que se haya dictado sentencia de primera instancia.",
        ],
        "B",
        "Es la B porque la cautelar se justifica por el riesgo de que la sentencia futura "
        "pierda eficacia y por la apariencia de que la pretensión es fundada; el CPC exige, "
        "por ejemplo, comprobantes que constituyan presunción grave del derecho que se "
        "reclama (art. 298). La A no, porque las cautelares se piden antes de la sentencia. "
        "La C no, porque no se requiere el consentimiento del afectado. La D no, porque "
        "pueden decretarse en cualquier estado del juicio e incluso como prejudiciales.",
        f"{CPC}, arts. 290 y 298; {UC}, II, cap. V, 3",
    ),
    (
        "Medidas cautelares: características y presupuestos",
        3,
        "¿Qué significa que las medidas precautorias sean esencialmente provisionales?",
        [
            "Que duran exactamente seis meses.",
            "Que deben hacerse cesar siempre que desaparezca el peligro que se ha procurado "
            "evitar o se otorguen cauciones suficientes.",
            "Que solo pueden decretarse una vez.",
            "Que no pueden sustituirse por otras.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 301 CPC. La A no, porque no tienen un plazo "
        "fijo de duración. La C no, porque pueden decretarse en cualquier estado del juicio y "
        "acumularse. La D no, porque son sustituibles, por ejemplo por cauciones.",
        f"{CPC}, art. 301; {UC}, II, cap. V, 2",
    ),
    (
        "Medidas precautorias civiles",
        1,
        "¿Cuál de estas es una medida precautoria enumerada en el art. 290 CPC?",
        [
            "La prisión preventiva.",
            "La retención de bienes determinados.",
            "El arresto domiciliario.",
            "La suspensión condicional del procedimiento.",
        ],
        "B",
        "Es la B porque el art. 290 CPC enumera el secuestro de la cosa objeto de la demanda, "
        "el nombramiento de interventores, la retención de bienes determinados y la "
        "prohibición de celebrar actos o contratos sobre bienes determinados. La A no, porque "
        "la prisión preventiva es una cautelar personal penal. La C no, porque el arresto "
        "domiciliario también es una cautelar penal (art. 155 CPP). La D no, porque es una "
        "salida alternativa penal.",
        f"{CPC}, art. 290; {UC}, II, cap. V, 4.1.2",
    ),
    (
        "Medidas precautorias civiles",
        3,
        "Se decreta una prohibición de celebrar actos y contratos sobre un inmueble. ¿Qué se "
        "requiere para que produzca efecto respecto de terceros?",
        [
            "Nada: produce efecto contra todos desde que se dicta.",
            "Que se inscriba en el registro del Conservador de Bienes Raíces respectivo.",
            "Que se publique en el Diario Oficial.",
            "Que el demandado la acepte por escrito.",
        ],
        "B",
        "Es la B porque el art. 297 CPC dispone que, cuando la prohibición recae sobre bienes "
        "raíces, debe inscribirse en el registro del Conservador respectivo, y sin este "
        "requisito no produce efecto respecto de terceros. La A no, porque la inscripción es "
        "necesaria frente a terceros. La C no, porque no se publica en el Diario Oficial. La "
        "D no, porque no se requiere su aceptación.",
        f"{CPC}, art. 297; {UC}, II, cap. V, 4.1.2.4",
    ),
]
