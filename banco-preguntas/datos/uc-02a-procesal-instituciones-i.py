"""Cédula UC de Derecho Procesal, parte I (Instituciones procesales I)."""

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
    # ------------------------------------------- cap. I: el conflicto y su solución
    (
        "Autotutela, autocomposición y heterocomposición",
        1,
        "¿Cuál de estas es una forma de autocomposición del conflicto?",
        [
            "La transacción.",
            "La sentencia judicial.",
            "El laudo de un árbitro.",
            "La legítima defensa.",
        ],
        "A",
        "Es la A porque en la autocomposición son las propias partes las que solucionan el "
        "conflicto, por acuerdo o por renuncia de una de ellas; la transacción es un contrato "
        "en que las partes terminan extrajudicialmente un litigio pendiente o precaven uno "
        "eventual (art. 2446 CC). La B no, porque la sentencia es heterocomposición: un "
        "tercero imparcial (el juez) resuelve. La C no, porque el árbitro también es un "
        "tercero que resuelve: es heterocomposición. La D no, porque la legítima defensa es "
        "un caso excepcional de autotutela permitida.",
        f"Código Civil, art. 2446; {UC}, I, cap. I, 1",
    ),
    (
        "Autotutela, autocomposición y heterocomposición",
        2,
        "La autotutela está proscrita, en general, en un Estado de Derecho. ¿Cuál de estos es "
        "un caso en que la ley chilena la admite excepcionalmente?",
        [
            "Que el acreedor retire por su cuenta bienes del deudor moroso.",
            "Que el dueño de un predio corte las raíces de un árbol vecino que penetran en su "
            "suelo.",
            "Que el arrendador cambie la chapa para echar al arrendatario que no paga.",
            "Que la víctima de un robo recupere por la fuerza lo robado días después.",
        ],
        "B",
        "Es la B porque el art. 942 del Código Civil autoriza al dueño del suelo a cortar por "
        "sí mismo las raíces que penetran en él; otros ejemplos son la legítima defensa y el "
        "derecho legal de retención. La A no, porque el acreedor debe obtener la ejecución por "
        "medio de los tribunales. La C no, porque el lanzamiento del arrendatario requiere un "
        "juicio. La D no, porque, pasado el momento de la agresión, recuperar la cosa por la "
        "fuerza es hacerse justicia por mano propia.",
        f"Código Civil, art. 942; {UC}, I, cap. I, 1.2",
    ),
    (
        "Medios autocompositivos en materia civil",
        2,
        "¿Qué diferencia la conciliación del avenimiento?",
        [
            "No hay diferencia: son sinónimos.",
            "En la conciliación el juez interviene y propone bases de arreglo; el avenimiento "
            "es un acuerdo al que llegan directamente las partes y que luego presentan al "
            "tribunal.",
            "La conciliación solo procede en materia penal y el avenimiento en materia civil.",
            "El avenimiento siempre lo propone el juez.",
        ],
        "B",
        "Es la B porque en la conciliación el juez actúa como amigable componedor y propone "
        "bases de arreglo (art. 263 CPC), y el acta de conciliación se estima sentencia "
        "ejecutoriada (art. 267 CPC); el avenimiento es un acuerdo directo de las partes, que "
        "pasado ante tribunal competente y autorizado por un ministro de fe es título "
        "ejecutivo (art. 434 n.° 3 CPC). La A no, porque son figuras distintas. La C no, "
        "porque ambas operan en materia civil. La D no, porque el avenimiento es obra de las "
        "partes.",
        f"{CPC}, arts. 262, 263, 267 y 434 n.° 3; {UC}, I, cap. I, 2.1",
    ),
    (
        "Medios autocompositivos en materia civil",
        3,
        "Notificada la demanda, el demandado acepta llanamente las peticiones del demandante. "
        "¿Qué efecto procesal tiene ese allanamiento?",
        [
            "Pone término inmediato al juicio sin sentencia.",
            "Obliga a abrir igual un término probatorio.",
            "Se omite la prueba y el tribunal manda citar a las partes para oír sentencia una "
            "vez evacuado el último escrito.",
            "Transforma el juicio en un procedimiento sumario.",
        ],
        "C",
        "Es la C porque el art. 313 CPC dispone que si el demandado acepta llanamente las "
        "peticiones del demandante, o no contradice en materia substancial y pertinente los "
        "hechos, el tribunal mandará citar para oír sentencia definitiva una vez evacuado el "
        "último escrito: no hay hechos controvertidos que probar. La A no, porque igual se "
        "dicta sentencia. La B no, porque la prueba se omite. La D no, porque no cambia el "
        "procedimiento.",
        f"{CPC}, art. 313; {UC}, I, cap. I, 2.1.4",
    ),
    (
        "Medios autocompositivos en materia penal",
        2,
        "¿Qué efecto tiene el cumplimiento de un acuerdo reparatorio aprobado por el juez de "
        "garantía?",
        [
            "Ninguno: el juicio sigue igual.",
            "Extingue, total o parcialmente, la responsabilidad penal del imputado que lo hubiere "
            "celebrado, y el tribunal dicta sobreseimiento definitivo.",
            "Rebaja la pena a la mitad.",
            "Solo extingue la responsabilidad civil.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 242 CPP: cumplidas las obligaciones contraídas "
        "o garantizadas debidamente, se dicta sobreseimiento definitivo, total o parcial, y "
        "se extingue la responsabilidad penal del imputado que lo celebró. La A no, porque el "
        "acuerdo es una salida alternativa al juicio. La C no, porque no es una rebaja de "
        "pena. La D no, porque produce efecto penal.",
        f"{CPP}, arts. 241 y 242; {UC}, I, cap. I, 2.2.2",
    ),
    (
        "Medios autocompositivos en materia penal",
        3,
        "¿En qué caso no puede el fiscal aplicar el principio de oportunidad?",
        [
            "Cuando el hecho no compromete gravemente el interés público.",
            "Cuando la pena mínima asignada al delito excede la de presidio o reclusión menores "
            "en su grado mínimo, o se trata de un delito cometido por un funcionario público en "
            "el ejercicio de sus funciones.",
            "Cuando la víctima no se opone.",
            "Cuando el imputado no tiene antecedentes penales.",
        ],
        "B",
        "Es la B porque el art. 170 CPP permite no iniciar o abandonar la persecución de un "
        "hecho que no comprometa gravemente el interés público, a menos que la pena mínima "
        "exceda la de presidio o reclusión menores en su grado mínimo o se trate de un delito "
        "de funcionario público en el ejercicio de sus funciones. La A no, porque ese es "
        "justamente el supuesto en que procede. La C no, porque la falta de oposición de la "
        "víctima no la impide. La D no, porque la ausencia de antecedentes no es un "
        "impedimento.",
        f"{CPP}, art. 170; {UC}, I, cap. I, 2.2.3",
    ),
    # ------------------------------------------------------ cap. II: la jurisdicción
    (
        "La jurisdicción: bases, concepto y momentos",
        1,
        "Según el art. 76 de la Constitución, ¿a quién pertenece la facultad de conocer de las "
        "causas civiles y criminales, resolverlas y hacer ejecutar lo resuelto?",
        [
            "Al Presidente de la República y al Congreso.",
            "Exclusivamente a los tribunales establecidos por la ley.",
            "A cualquier autoridad pública que la ley determine, incluidos los ministerios.",
            "Solo a la Corte Suprema.",
        ],
        "B",
        "Es la B porque el art. 76 inc. 1 de la Constitución (y el art. 1 del COT) atribuye "
        "esa facultad exclusivamente a los tribunales establecidos por la ley, y agrega que ni "
        "el Presidente ni el Congreso pueden ejercer funciones judiciales, avocarse causas "
        "pendientes, revisar los fundamentos o contenido de sus resoluciones o hacer revivir "
        "procesos fenecidos. La A no, porque la norma lo prohíbe expresamente. La C no, porque "
        "la función es de los tribunales. La D no, porque la ejercen todos los tribunales "
        "establecidos por la ley.",
        f"{CPR}, art. 76; {COT}, art. 1; {UC}, I, cap. II, 1 y 2.2",
    ),
    (
        "La jurisdicción: bases, concepto y momentos",
        2,
        "¿Cuáles son los momentos jurisdiccionales que se desprenden del art. 76 de la "
        "Constitución?",
        [
            "Demanda, contestación y prueba.",
            "Conocimiento, decisión (juzgamiento) y ejecución.",
            "Investigación, acusación y juicio.",
            "Notificación, apelación y casación.",
        ],
        "B",
        "Es la B porque la norma habla de conocer las causas, resolverlas y hacer ejecutar lo "
        "resuelto. La A no, porque son trámites de un procedimiento civil, no momentos de la "
        "jurisdicción. La C no, porque son etapas del procedimiento penal. La D no, porque "
        "son actuaciones y recursos.",
        f"{CPR}, art. 76; {UC}, I, cap. II, 2.3",
    ),
    (
        "Características y facultades anexas de la jurisdicción",
        2,
        "¿Qué significa que la jurisdicción sea indelegable?",
        [
            "Que solo puede ejercerla la Corte Suprema.",
            "Que el tribunal no puede traspasar a otro órgano el ejercicio de la función que la "
            "ley le confió, sin perjuicio de los exhortos para diligencias determinadas.",
            "Que las partes no pueden someter sus conflictos a árbitros.",
            "Que el juez no puede excusarse de fallar.",
        ],
        "B",
        "Es la B porque la indelegabilidad impide que el tribunal entregue a otro el ejercicio "
        "de su función; los exhortos solo encargan diligencias concretas a otro tribunal. La "
        "A no, porque todos los tribunales ejercen jurisdicción. La C no, porque el arbitraje "
        "es una forma legal de jurisdicción. La D no, porque eso es la inexcusabilidad (art. "
        "76 inc. 2 CPR y art. 10 COT).",
        f"{CPR}, art. 76; {COT}, art. 10; {CPC}, art. 71; {UC}, I, cap. II, 3",
    ),
    (
        "Características y facultades anexas de la jurisdicción",
        2,
        "La Corte de Apelaciones conoce un recurso de protección para resguardar un derecho "
        "constitucional amenazado. ¿Qué facultad anexa a la jurisdicción se manifiesta ahí?",
        [
            "La facultad económica.",
            "La facultad disciplinaria.",
            "La facultad conservadora.",
            "La facultad de imperio.",
        ],
        "C",
        "Es la C porque las facultades conservadoras (art. 3 COT) son las que tienen los "
        "tribunales para velar por el respeto de la Constitución y la protección de las "
        "garantías individuales; sus manifestaciones típicas son el recurso de protección y "
        "el de amparo. La A no, porque la económica se refiere a la buena administración de "
        "justicia (autos acordados, por ejemplo). La B no, porque la disciplinaria busca "
        "mantener el orden y la disciplina judicial. La D no, porque el imperio es la "
        "facultad de hacer cumplir lo resuelto con la fuerza pública.",
        f"{COT}, art. 3; {CPR}, arts. 20 y 21; {UC}, I, cap. II, 7",
    ),
    # ------------------------------------------ cap. III: tutela, acción y pretensión
    (
        "Acción, pretensión y excepción",
        2,
        "¿Qué diferencia hay, según la doctrina, entre acción y pretensión?",
        [
            "Son sinónimos.",
            "La acción es el derecho a requerir la actividad jurisdiccional; la pretensión es "
            "la petición concreta que una parte formula frente a otra y que el juez debe acoger "
            "o rechazar.",
            "La acción solo existe en materia penal y la pretensión en materia civil.",
            "La pretensión es el derecho a defenderse del demandado.",
        ],
        "B",
        "Es la B porque la doctrina moderna separa el derecho abstracto de acudir a los "
        "tribunales (acción) del reclamo concreto contra otro sujeto (pretensión), que puede "
        "ser fundado o infundado. La A no, porque son conceptos distintos. La C no, porque "
        "ambos existen en todo tipo de procesos. La D no, porque la defensa del demandado es "
        "el derecho a la reacción, que se expresa en excepciones y defensas.",
        f"{UC}, I, cap. III, 1 y 2",
    ),
    (
        "Acción, pretensión y excepción",
        3,
        "Una persona afirma públicamente que es dueña de un inmueble que posee otro, pero no lo "
        "demanda. ¿Qué puede hacer el poseedor según el Código de Procedimiento Civil?",
        [
            "Nada: debe esperar a que lo demanden.",
            "Pedir que se le obligue a deducir demanda dentro de diez días, bajo apercibimiento "
            "de no ser oído después (demanda de jactancia).",
            "Pedir que se le condene penalmente por injurias.",
            "Inscribir el inmueble a su nombre sin juicio.",
        ],
        "B",
        "Es la B porque el art. 269 CPC regula la jactancia: cuando alguien manifiesta "
        "corresponderle un derecho de que no está gozando, todo aquel a quien su jactancia "
        "pueda afectar puede pedir que se le obligue a demandar dentro de diez días, bajo "
        "apercibimiento de no ser oído después. La acción prescribe en seis meses desde que "
        "tuvieron lugar los hechos (art. 272). La A no, porque la ley da esta herramienta. La "
        "C no, porque no es una materia penal. La D no, porque no hay inscripción sin título.",
        f"{CPC}, arts. 269 a 272; {UC}, I, cap. III, 3.6.1",
    ),
    (
        "Tipos de tutela jurisdiccional",
        2,
        "¿Qué tipo de tutela pide quien demanda el divorcio?",
        [
            "Mero declarativa.",
            "Constitutiva: busca crear, modificar o extinguir una situación jurídica (el estado "
            "civil).",
            "Cautelar.",
            "Ejecutiva.",
        ],
        "B",
        "Es la B porque la sentencia de divorcio pone fin al matrimonio y cambia el estado "
        "civil: no se limita a declarar algo que ya existía. La A no, porque la mero "
        "declarativa solo busca certeza sobre una situación preexistente. La C no, porque la "
        "cautelar asegura provisionalmente el resultado de otro proceso. La D no, porque la "
        "ejecutiva supone un derecho ya reconocido que se hace cumplir.",
        f"{UC}, I, cap. III, 3.2",
    ),
    (
        "Tipos de tutela jurisdiccional",
        3,
        "¿Qué distingue a la tutela cautelar de la tutela anticipada?",
        [
            "Son lo mismo.",
            "La cautelar asegura provisionalmente la eficacia de la sentencia futura sin "
            "satisfacer todavía la pretensión; la anticipada concede provisionalmente, en todo "
            "o en parte, lo mismo que se pide en la demanda.",
            "La anticipada solo existe en materia penal.",
            "La cautelar es definitiva y la anticipada provisional.",
        ],
        "B",
        "Es la B porque la cautelar sirve al proceso principal (por ejemplo, una retención de "
        "bienes), mientras que la anticipada adelanta la satisfacción de la pretensión (por "
        "ejemplo, alimentos provisorios). La A no, porque la doctrina las distingue. La C no, "
        "porque también existe en materia civil y de familia. La D no, porque ambas son "
        "provisionales.",
        f"{CPC}, art. 290; {UC}, I, cap. III, 3.5 y 3.8; II, cap. V, 4.1.1",
    ),
    # --------------------------- cap. IV: contenido del derecho a la tutela jurisdiccional
    (
        "Competencia y juez natural",
        2,
        "¿Qué diferencia hay entre jurisdicción y competencia?",
        [
            "Son sinónimos.",
            "La jurisdicción es el poder-deber de resolver conflictos que tienen todos los "
            "tribunales; la competencia es la medida de esa jurisdicción que la ley asigna a "
            "cada tribunal.",
            "La competencia es mayor que la jurisdicción.",
            "La jurisdicción solo la tienen los tribunales superiores.",
        ],
        "B",
        "Es la B porque el art. 108 COT define la competencia como la facultad que tiene cada "
        "juez o tribunal para conocer de los negocios que la ley ha colocado dentro de la "
        "esfera de sus atribuciones: todo tribunal tiene jurisdicción, pero solo es "
        "competente para ciertos asuntos. La A no, porque son conceptos distintos. La C no, "
        "porque la competencia es una parte de la jurisdicción. La D no, porque todos los "
        "tribunales tienen jurisdicción.",
        f"{COT}, art. 108; {UC}, I, cap. IV, IV.1, 1.1.2",
    ),
    (
        "Competencia y juez natural",
        3,
        "Un demandante presenta su demanda ante un juez de letras de otra comuna del mismo "
        "grado, que no es el territorialmente competente, y el demandado contesta sin alegar "
        "la incompetencia. ¿Qué ocurre?",
        [
            "El juicio es nulo por incompetencia absoluta.",
            "Opera la prórroga tácita de la competencia: el juez pasa a ser competente, porque "
            "se trata del factor territorio, en primera instancia, entre tribunales ordinarios "
            "de igual jerarquía y en un asunto contencioso civil.",
            "El juez debe declararse incompetente de oficio.",
            "La sentencia solo vale si la confirma la Corte Suprema.",
        ],
        "B",
        "Es la B porque la competencia relativa (territorio) es prorrogable: la prórroga "
        "procede solo en primera instancia, entre tribunales ordinarios de igual jerarquía y "
        "en negocios contenciosos civiles (art. 182 COT), y es tácita para el demandado que "
        "hace cualquier gestión en el juicio que no sea reclamar la incompetencia (art. 187 "
        "COT). La A no, porque la incompetencia territorial no es absoluta. La C no, porque la "
        "competencia relativa no se declara de oficio. La D no, porque no existe tal "
        "requisito.",
        f"{COT}, arts. 181, 182, 186 y 187; {UC}, I, cap. IV, IV.1, 1.1.2.7",
    ),
    (
        "Reglas generales de la competencia",
        2,
        "Se presenta una demanda ante un tribunal competente. Después, el demandado cambia su "
        "domicilio a otra ciudad. ¿Qué tribunal sigue conociendo del juicio?",
        [
            "El del nuevo domicilio del demandado.",
            "El mismo, por la regla de la radicación: radicado con arreglo a la ley el "
            "conocimiento de un negocio ante tribunal competente, no se altera por causa "
            "sobreviniente.",
            "La Corte de Apelaciones respectiva.",
            "El que elija el demandante.",
        ],
        "B",
        "Es la B porque esa es la regla del art. 109 COT (radicación o fijeza). La A no, "
        "porque el cambio posterior de domicilio no altera la competencia. La C no, porque la "
        "Corte no pasa a conocer en primera instancia. La D no, porque el demandante no puede "
        "cambiar el tribunal a su arbitrio.",
        f"{COT}, art. 109; {UC}, I, cap. IV, IV.1, 1.1.2.8",
    ),
    (
        "Reglas generales de la competencia",
        3,
        "El tribunal que conoce de una demanda de cobro, ¿puede conocer también de la "
        "reconvención y de la excepción de compensación que oponga el demandado?",
        [
            "No, deben tramitarse ante otro tribunal.",
            "Sí, por la regla de la extensión: el tribunal competente para conocer de un "
            "asunto lo es igualmente para conocer de las incidencias, la reconvención y la "
            "compensación, aunque estas, por su cuantía, deban ser conocidas por un juez "
            "inferior.",
            "Solo si las partes lo pactan.",
            "Solo si la Corte de Apelaciones lo autoriza.",
        ],
        "B",
        "Es la B porque esa es la regla de la extensión del art. 111 COT. La A no, porque la "
        "ley amplía la competencia del tribunal para estos asuntos. La C no, porque opera por "
        "el solo ministerio de la ley. La D no, porque no se requiere autorización.",
        f"{COT}, art. 111; {UC}, I, cap. IV, IV.1, 1.1.2.8",
    ),
    (
        "Independencia, inexcusabilidad e imparcialidad",
        2,
        "Un juez se niega a fallar un caso argumentando que no existe ley que lo resuelva. "
        "¿Qué principio infringe?",
        [
            "El de inavocabilidad.",
            "El de inexcusabilidad: reclamada su intervención en forma legal y en negocios de "
            "su competencia, no puede excusarse de ejercer su autoridad ni aun por falta de ley "
            "que resuelva la contienda.",
            "El de publicidad.",
            "El de radicación.",
        ],
        "B",
        "Es la B porque así lo disponen el art. 76 inc. 2 de la Constitución y el art. 10 "
        "inc. 2 del COT; a falta de ley, el juez falla conforme al espíritu general de la "
        "legislación y la equidad natural (art. 170 n.° 5 CPC). La A no, porque la "
        "inavocabilidad prohíbe a un tribunal tomar causas pendientes ante otro (art. 8 COT). "
        "La C no, porque la publicidad se refiere a los actos de los tribunales. La D no, "
        "porque la radicación fija la competencia.",
        f"{CPR}, art. 76; {COT}, art. 10; {UC}, I, cap. IV, IV.1, 1.2",
    ),
    (
        "Independencia, inexcusabilidad e imparcialidad",
        3,
        "¿Qué diferencia hay entre una implicancia y una recusación?",
        [
            "No hay diferencia.",
            "Las implicancias son causales más graves, de orden público e irrenunciables; las "
            "recusaciones son de interés privado y pueden renunciarse por la parte a quien "
            "favorecen.",
            "La implicancia la declara la parte y la recusación el juez.",
            "La recusación solo procede en materia penal.",
        ],
        "B",
        "Es la B porque ambas buscan asegurar la imparcialidad del juez (arts. 195 y 196 "
        "COT), pero la implicancia es irrenunciable y el juez que se sabe implicado debe "
        "abstenerse, mientras que la recusación puede renunciarse expresa o tácitamente. La A "
        "no, porque la ley las distingue. La C no, porque ambas pueden hacerse valer por las "
        "partes y el juez debe declarar las que le afecten. La D no, porque ambas existen en "
        "materia civil.",
        f"{COT}, arts. 194 a 200; {UC}, I, cap. IV, IV.1, 1.4",
    ),
    (
        "Responsabilidad de los jueces y continuidad de los tribunales",
        2,
        "¿Por qué delitos son personalmente responsables los jueces según el art. 79 de la "
        "Constitución?",
        [
            "Solo por los delitos comunes que cometan fuera del cargo.",
            "Por cohecho, falta de observancia en materia sustancial de las leyes que reglan el "
            "procedimiento, denegación y torcida administración de justicia y, en general, toda "
            "prevaricación en que incurran en el desempeño de sus funciones.",
            "Por cualquier error en la apreciación de la prueba.",
            "No son responsables: la Constitución les da inmunidad absoluta.",
        ],
        "B",
        "Es la B porque esa es la responsabilidad ministerial que establece el art. 79 de la "
        "Constitución; para perseguirla, la ley exige como trámite previo la querella de "
        "capítulos. La A no, porque se trata de delitos ministeriales, cometidos en el "
        "ejercicio del cargo. La C no, porque un simple error no es delito. La D no, porque "
        "la Constitución establece expresamente esa responsabilidad.",
        f"{CPR}, art. 79; {COT}, art. 324; {CPP}, art. 424; {UC}, I, cap. IV, IV.1, 1.5",
    ),
    (
        "Responsabilidad de los jueces y continuidad de los tribunales",
        3,
        "¿Qué diferencia hay entre la subrogación y la integración?",
        [
            "Son sinónimos.",
            "La subrogación es el reemplazo del juez que falta o está inhabilitado; la "
            "integración es completar la sala de un tribunal colegiado con otros miembros "
            "(por ejemplo, fiscales judiciales o abogados integrantes).",
            "La integración solo procede en juzgados de letras.",
            "La subrogación la decide el Presidente de la República.",
        ],
        "B",
        "Es la B porque ambas instituciones buscan que el tribunal funcione en forma continua, "
        "pero la subrogación reemplaza a un juez (típicamente en tribunales unipersonales) y "
        "la integración completa el quórum de un tribunal colegiado. La A no, porque son "
        "figuras distintas. La C no, porque la integración es propia de los tribunales "
        "colegiados. La D no, porque las reglas están en el COT y no dependen del Presidente.",
        f"{COT}, arts. 211 a 221; {UC}, I, cap. IV, IV.1, 1.6",
    ),
    (
        "Debido proceso",
        1,
        "¿Qué exige el art. 19 n.° 3 de la Constitución respecto de las sentencias?",
        [
            "Que las dicte siempre un tribunal colegiado.",
            "Que toda sentencia de un órgano que ejerza jurisdicción se funde en un proceso "
            "previo legalmente tramitado, y que el legislador establezca siempre las garantías "
            "de un procedimiento y una investigación racionales y justos.",
            "Que todas sean apelables.",
            "Que se dicten en un plazo máximo de 30 días.",
        ],
        "B",
        "Es la B porque esa es la consagración constitucional del debido proceso (art. 19 n.° "
        "3 inc. 6 CPR). La A no, porque no exige tribunales colegiados. La C no, porque el "
        "derecho al recurso no significa que toda resolución sea apelable. La D no, porque la "
        "Constitución no fija ese plazo.",
        f"{CPR}, art. 19 n.° 3; {UC}, I, cap. IV, IV.2, 1",
    ),
    (
        "Debido proceso",
        2,
        "En materia penal, ¿qué garantía del debido proceso establece que ninguna persona será "
        "considerada culpable ni tratada como tal mientras no se dicte en su contra una "
        "sentencia firme?",
        [
            "El derecho a la prueba.",
            "La presunción de inocencia.",
            "El derecho al recurso.",
            "El principio de publicidad.",
        ],
        "B",
        "Es la B porque así la formula el art. 4 CPP; en el juicio, la condena exige "
        "convicción más allá de toda duda razonable (art. 340 CPP). La A no, porque el "
        "derecho a la prueba es la facultad de rendir prueba sobre los hechos. La C no, "
        "porque el derecho al recurso permite impugnar las resoluciones. La D no, porque la "
        "publicidad se refiere a la apertura de las actuaciones.",
        f"{CPP}, arts. 4 y 340; {UC}, I, cap. IV, IV.2, 2.4",
    ),
    (
        "Eficacia de la sentencia: cosa juzgada y ejecución",
        2,
        "¿Qué requisitos deben concurrir para que prospere la excepción de cosa juzgada según "
        "el art. 177 CPC?",
        [
            "Identidad de juez, de abogado y de fecha.",
            "Identidad legal de personas, identidad de la cosa pedida e identidad de la causa "
            "de pedir.",
            "Que la primera sentencia haya sido confirmada por la Corte Suprema.",
            "Que hayan pasado diez años desde la primera sentencia.",
        ],
        "B",
        "Es la B porque esa es la triple identidad del art. 177 CPC. La A no, porque no se "
        "compara al juez ni al abogado. La C no, porque basta que la sentencia esté firme o "
        "ejecutoriada. La D no, porque la cosa juzgada no depende del tiempo transcurrido.",
        f"{CPC}, arts. 175 a 177; {UC}, I, cap. IV, IV.3, 1; II, cap. II, 6.4.3",
    ),
    (
        "Eficacia de la sentencia: cosa juzgada y ejecución",
        3,
        "¿Qué es la facultad de imperio?",
        [
            "La facultad del Presidente de la República de indultar.",
            "La facultad de los tribunales de impartir órdenes directas a la fuerza pública "
            "para hacer ejecutar sus resoluciones y practicar actos de instrucción.",
            "La facultad del juez de aumentar la pena.",
            "La facultad de las partes de elegir el tribunal.",
        ],
        "B",
        "Es la B porque el art. 76 incs. 3 y 4 de la Constitución dispone que, para hacer "
        "ejecutar sus resoluciones, los tribunales pueden impartir órdenes directas a la "
        "fuerza pública, y la autoridad requerida debe cumplir sin más trámite, sin calificar "
        "su fundamento u oportunidad. La A no, porque el indulto es otra figura. La C no, "
        "porque no se relaciona con la pena. La D no, porque las partes no eligen el tribunal "
        "por esta vía.",
        f"{CPR}, art. 76; {COT}, art. 11; {UC}, I, cap. IV, IV.3, 2.1",
    ),
    # ----------------------------------------- caps. V y VI: proceso y procedimiento
    (
        "El proceso y los presupuestos procesales",
        2,
        "¿Qué diferencia hay entre proceso y procedimiento?",
        [
            "Son sinónimos.",
            "El proceso es el medio para resolver un conflicto por la vía jurisdiccional; el "
            "procedimiento es el conjunto de formalidades y trámites a que se sujeta ese "
            "proceso.",
            "El procedimiento solo existe en materia penal.",
            "El proceso es solo la sentencia.",
        ],
        "B",
        "Es la B porque el proceso es el fin (la solución del conflicto con fuerza de cosa "
        "juzgada) y el procedimiento, la forma en que se desarrolla. La A no, porque la "
        "doctrina los distingue. La C no, porque existen procedimientos civiles y penales. La "
        "D no, porque la sentencia es solo un acto del proceso.",
        f"{UC}, I, cap. V, 1.1",
    ),
    (
        "El proceso y los presupuestos procesales",
        3,
        "Se dicta sentencia en un «juicio» en el que nunca se notificó la demanda al demandado. "
        "¿Qué sostiene la doctrina que considera el emplazamiento como presupuesto de "
        "existencia?",
        [
            "Que la sentencia es válida, pero anulable por casación.",
            "Que no hay proceso y, por lo tanto, la sentencia solo tiene la apariencia de cosa "
            "juzgada (cosa juzgada aparente).",
            "Que la sentencia es válida y no puede impugnarse.",
            "Que el juicio se convierte en un acto no contencioso.",
        ],
        "B",
        "Es la B porque los presupuestos de existencia (tribunal, partes, conflicto y, para "
        "esta doctrina, emplazamiento) son necesarios para que haya proceso; sin ellos, la "
        "sentencia es inexistente y solo produce una cosa juzgada aparente. La A no, porque "
        "eso correspondería a la falta de un presupuesto de validez. La C no, porque la "
        "doctrina sostiene lo contrario. La D no, porque el conflicto sigue siendo "
        "contencioso.",
        f"{UC}, I, cap. V, 2.1",
    ),
    (
        "Principios formativos del procedimiento",
        2,
        "¿Qué es la preclusión?",
        [
            "La facultad del juez de dictar sentencia sin prueba.",
            "La pérdida o extinción de una facultad procesal por no haberse ejercido dentro del "
            "plazo, por haberse realizado un acto incompatible con ella o por haberse ejercido "
            "ya válidamente.",
            "La suspensión del procedimiento de común acuerdo.",
            "La obligación de notificar todas las resoluciones.",
        ],
        "B",
        "Es la B porque esas son las tres formas de preclusión que reconoce la doctrina; un "
        "caso típico es el plazo fatal (art. 64 CPC) o la regla del art. 84 CPC sobre "
        "incidentes. La A no, porque nada tiene que ver con dictar sentencia. La C no, "
        "porque la suspensión es otra institución. La D no, porque las notificaciones son "
        "otra materia.",
        f"{CPC}, arts. 64 y 84; {UC}, I, cap. VI, 2.4",
    ),
    (
        "Principios formativos del procedimiento",
        2,
        "¿Qué exige el principio de inmediación?",
        [
            "Que el juez resuelva lo más rápido posible.",
            "Que el juez tome contacto directo y personal con las partes y con la prueba.",
            "Que todas las actuaciones se hagan por escrito.",
            "Que las partes actúen siempre representadas por abogado.",
        ],
        "B",
        "Es la B porque la inmediación supone que el juez que falla es el mismo que recibió "
        "la prueba en forma directa; es central en el juicio oral penal, que exige la "
        "presencia ininterrumpida de los jueces (art. 284 CPP). La A no, porque la rapidez es "
        "propia de la celeridad o economía procesal. La C no, porque la escrituración es otro "
        "principio, más bien opuesto. La D no, porque la representación es una regla de "
        "comparecencia.",
        f"{CPP}, art. 284; {UC}, I, cap. VI, 2.7",
    ),
]
