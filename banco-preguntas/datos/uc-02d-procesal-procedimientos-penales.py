"""Cédula UC de Derecho Procesal, parte V (Procedimientos penales)."""

JURISDICCION = "Chile"
PROGRAMA = "Cédulas UC (licenciatura, vigentes desde 2021)"
CEDULA = "Cédula 2: Derecho Procesal (15-03-2021)"
MATERIA = "Derecho Procesal"

CPR = "Constitución Política"
CPP = "Código Procesal Penal"
UC = "Cédula UC Derecho Procesal"

PREGUNTAS = [
    # ------------------------------------------------ cap. II: acción penal y civil
    (
        "Acción penal y acción civil",
        2,
        "¿Cómo se persiguen los delitos de calumnia e injuria según el Código Procesal Penal?",
        [
            "Por acción penal pública, de oficio por el Ministerio Público.",
            "Por acción penal privada: solo puede ejercerla la víctima, mediante querella.",
            "Por acción penal pública previa instancia particular, con denuncia del Ministerio "
            "Público.",
            "No son perseguibles penalmente.",
        ],
        "B",
        "Es la B porque el art. 55 CPP incluye la calumnia y la injuria entre los delitos de "
        "acción penal privada, que solo pueden ser ejercidos por la víctima (art. 53) y se "
        "tramitan en un procedimiento especial iniciado por querella. La A no, porque el "
        "Ministerio Público no actúa de oficio en estos delitos. La C no, porque la previa "
        "instancia particular corresponde a otros delitos, como las lesiones menos graves o "
        "la violación de domicilio (art. 54). La D no, porque sí son perseguibles.",
        f"{CPP}, arts. 53 a 55; {UC}, V, cap. II, 1",
    ),
    (
        "Acción penal y acción civil",
        3,
        "En el proceso penal, ¿contra quién puede la víctima deducir la acción civil "
        "indemnizatoria y ante qué tribunal?",
        [
            "Contra cualquier persona, siempre ante el juez penal.",
            "Contra el imputado, ante el tribunal penal; las acciones contra terceros "
            "civilmente responsables deben deducirse ante el tribunal civil competente.",
            "Solo ante el tribunal civil, nunca en el proceso penal.",
            "Solo contra el Estado, ante la Corte Suprema.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 59 CPP: durante el proceso penal la víctima "
        "puede deducir respecto del imputado las acciones civiles que persigan la "
        "responsabilidad derivada del hecho punible, mientras que las dirigidas contra "
        "personas distintas del imputado van ante el tribunal civil. La A no, porque la "
        "acción contra terceros no se ventila en sede penal. La C no, porque la ley permite "
        "deducirla en el proceso penal contra el imputado. La D no, porque no se limita al "
        "Estado.",
        f"{CPP}, arts. 59 y 60; {UC}, V, cap. II, 2",
    ),
    # --------------------------------------------- cap. III: control de garantías
    (
        "Control de garantías",
        2,
        "Una persona detenida estima que su privación de libertad es ilegal. ¿Qué puede pedir "
        "según el art. 95 CPP?",
        [
            "Que la Corte Suprema la indemnice.",
            "Ser conducida sin demora ante un juez de garantía, con el objeto de que examine la "
            "legalidad de su privación de libertad y, en su caso, adopte las medidas que "
            "procedan (amparo ante el juez de garantía).",
            "Que el fiscal la libere sin intervención judicial, siempre.",
            "Nada hasta el juicio oral.",
        ],
        "B",
        "Es la B porque esa es la acción de amparo ante el juez de garantía del art. 95 CPP, "
        "que no excluye el amparo constitucional ante la Corte de Apelaciones. La A no, "
        "porque la indemnización por error judicial tiene otras reglas (art. 19 n.° 7 letra "
        "i de la Constitución). La C no, porque el control es judicial. La D no, porque el "
        "control procede sin demora.",
        f"{CPP}, art. 95; {CPR}, art. 21; {UC}, V, cap. III, 2",
    ),
    (
        "Control de garantías",
        2,
        "El fiscal quiere allanar un domicilio sin el consentimiento del dueño. ¿Qué exige el "
        "art. 9 CPP?",
        [
            "Nada: el fiscal dirige la investigación y puede hacerlo.",
            "Autorización judicial previa, porque toda actuación que prive, restrinja o perturbe "
            "derechos asegurados por la Constitución la requiere.",
            "Autorización del Fiscal Nacional.",
            "Una orden del Presidente de la República.",
        ],
        "B",
        "Es la B porque el art. 9 CPP exige autorización judicial previa para toda actuación "
        "que prive al imputado o a un tercero del ejercicio de derechos constitucionales, o "
        "los restrinja o perturbe; la entrega el juez de garantía. La A no, porque la "
        "dirección de la investigación no autoriza a afectar derechos sin control judicial. "
        "La C no, porque no basta una autorización interna. La D no, porque el Ejecutivo no "
        "interviene.",
        f"{CPP}, art. 9; {UC}, V, cap. III, 3",
    ),
    (
        "Nulidad procesal penal",
        2,
        "Según el art. 159 CPP, ¿qué actuaciones pueden anularse?",
        [
            "Todas las que infrinjan cualquier forma.",
            "Solo las actuaciones o diligencias judiciales defectuosas que ocasionen a los "
            "intervinientes un perjuicio reparable únicamente con la declaración de nulidad.",
            "Solo las del Ministerio Público.",
            "Solo las del tribunal oral.",
        ],
        "B",
        "Es la B porque el art. 159 CPP recoge el principio de trascendencia: existe "
        "perjuicio cuando la inobservancia de las formas atenta contra las posibilidades de "
        "actuación de cualquiera de los intervinientes. La A no, porque se requiere "
        "perjuicio. La C no, porque la norma se refiere a actuaciones judiciales. La D no, "
        "porque rige en todo el procedimiento.",
        f"{CPP}, art. 159; {UC}, V, cap. III, 5",
    ),
    (
        "Nulidad procesal penal",
        3,
        "¿En qué caso presume de derecho el Código Procesal Penal la existencia del perjuicio "
        "para la nulidad?",
        [
            "Cuando la actuación se realizó en día inhábil.",
            "Cuando la infracción impidió el pleno ejercicio de las garantías y de los derechos "
            "reconocidos en la Constitución o en las leyes.",
            "Cuando la víctima no estuvo presente.",
            "Nunca: el perjuicio siempre debe probarse.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 160 CPP: en ese caso no se admite prueba en "
        "contrario sobre el perjuicio. La A no, porque una actuación en día inhábil no "
        "configura por sí sola esa presunción. La C no, porque la ausencia de la víctima no "
        "es el supuesto legal. La D no, porque la ley establece esta presunción.",
        f"{CPP}, art. 160; {UC}, V, cap. III, 5",
    ),
    # ------------------------------------------------- cap. IV: sujetos procesales
    (
        "Imputado y defensor",
        2,
        "¿Desde cuándo tiene una persona la calidad de imputado y el derecho a ser defendida "
        "por un letrado?",
        [
            "Desde la formalización de la investigación.",
            "Desde la primera actuación del procedimiento dirigido en su contra.",
            "Desde la acusación.",
            "Desde el auto de apertura del juicio oral.",
        ],
        "B",
        "Es la B porque los arts. 7 y 8 CPP confieren la calidad de imputado y el derecho a "
        "defensa letrada desde la primera actuación del procedimiento dirigido en contra de "
        "una persona. Si no tiene abogado, se le designa uno de la Defensoría Penal Pública "
        "(art. 102). La A no, porque la formalización es posterior y no da origen a esos "
        "derechos. La C no, porque la acusación es muy posterior. La D no, porque el auto de "
        "apertura cierra la etapa intermedia.",
        f"{CPP}, arts. 7, 8, 93 y 102; {UC}, V, cap. IV, 2 y 3",
    ),
    (
        "Imputado y defensor",
        2,
        "¿Cuál de estos es un derecho del imputado según el art. 93 CPP?",
        [
            "Ser juzgado por un jurado.",
            "Guardar silencio, sin que ello se utilice en su contra, o declarar sin prestar "
            "juramento.",
            "Elegir al juez de garantía.",
            "Acceder a la investigación aun cuando el fiscal la haya declarado secreta respecto "
            "de él, sin ninguna excepción.",
        ],
        "B",
        "Es la B porque el art. 93 letra g) CPP le reconoce el derecho a guardar silencio o, "
        "si consiente en declarar, a hacerlo sin juramento. La A no, porque en Chile no hay "
        "juicio por jurados. La C no, porque el juez se determina por la ley (juez natural). "
        "La D no, porque el fiscal puede disponer el secreto de ciertas actuaciones por un "
        "tiempo limitado (art. 182).",
        f"{CPP}, arts. 93 y 182; {UC}, V, cap. IV, 2",
    ),
    (
        "Víctima, querellante y policía",
        2,
        "Fallece la víctima de un delito. ¿Quién puede ejercer sus derechos en el proceso "
        "penal según el art. 108 CPP?",
        [
            "Nadie: la acción se extingue.",
            "Las personas que la ley enumera en orden de prelación, comenzando por el cónyuge o "
            "el conviviente civil y los hijos.",
            "Solo el Ministerio Público.",
            "Cualquier persona que lo pida.",
        ],
        "B",
        "Es la B porque el art. 108 CPP considera víctima, cuando el ofendido muere o no puede "
        "ejercer sus derechos, a las personas que enumera según un orden de prelación "
        "(cónyuge o conviviente civil e hijos, ascendientes, conviviente, hermanos y adoptado "
        "o adoptante). La A no, porque la persecución sigue. La C no, porque la víctima y sus "
        "sustitutos tienen derechos propios. La D no, porque la ley limita a esas personas.",
        f"{CPP}, art. 108; {UC}, V, cap. IV, 4",
    ),
    (
        "Víctima, querellante y policía",
        3,
        "¿Cuál de estas actuaciones puede realizar la policía sin orden previa del fiscal "
        "según el art. 83 CPP?",
        [
            "Formalizar la investigación.",
            "Detener en caso de flagrancia, resguardar el sitio del suceso, identificar a los "
            "testigos y prestar auxilio a la víctima.",
            "Solicitar la prisión preventiva al juez.",
            "Acusar al imputado.",
        ],
        "B",
        "Es la B porque esas son algunas de las actuaciones autónomas del art. 83 CPP; fuera "
        "de ellas, la policía actúa bajo la dirección del Ministerio Público. La A no, porque "
        "la formalización es una actuación del fiscal ante el juez. La C no, porque la "
        "prisión preventiva la solicita el fiscal o el querellante. La D no, porque acusar es "
        "función del fiscal.",
        f"{CPP}, arts. 79 a 83; {UC}, V, cap. IV, 6",
    ),
    # -------------------------------------- cap. V: salidas anticipadas y alternativas
    (
        "Archivo provisional, facultad de no investigar y oportunidad",
        2,
        "¿Cuándo puede el fiscal archivar provisionalmente una investigación según el art. 167 "
        "CPP?",
        [
            "En cualquier momento, aunque haya formalizado.",
            "Mientras no se haya producido la intervención del juez de garantía, cuando no "
            "aparezcan antecedentes que permitan desarrollar actividades conducentes al "
            "esclarecimiento de los hechos.",
            "Solo con acuerdo del imputado.",
            "Solo después de la acusación.",
        ],
        "B",
        "Es la B porque esos son los requisitos del art. 167 CPP; la víctima puede pedir la "
        "reapertura y la realización de diligencias. La A no, porque la formalización hace "
        "perder esa facultad (art. 233). La C no, porque no requiere acuerdo del imputado. "
        "La D no, porque es una decisión de la etapa inicial.",
        f"{CPP}, arts. 167 y 233; {UC}, V, cap. V, 1.1",
    ),
    (
        "Archivo provisional, facultad de no investigar y oportunidad",
        3,
        "Antes de la intervención del juez, el fiscal concluye que los hechos denunciados no "
        "constituyen delito. ¿Qué puede hacer?",
        [
            "Aplicar el principio de oportunidad.",
            "Abstenerse de toda investigación mediante una decisión fundada que se somete a la "
            "aprobación del juez de garantía (facultad para no iniciar la investigación).",
            "Dictar sobreseimiento definitivo él mismo.",
            "Acusar igual al imputado.",
        ],
        "B",
        "Es la B porque el art. 168 CPP permite abstenerse de toda investigación cuando los "
        "hechos no son constitutivos de delito o los antecedentes permiten establecer que se "
        "encuentra extinguida la responsabilidad penal del imputado; la decisión se somete a "
        "la aprobación del juez de garantía. La A no, porque la oportunidad supone un hecho "
        "delictivo que no compromete gravemente el interés público. La C no, porque el "
        "sobreseimiento lo dicta el juez. La D no, porque no hay delito que acusar.",
        f"{CPP}, arts. 168 y 170; {UC}, V, cap. V, 1.2",
    ),
    (
        "Suspensión condicional y acuerdos reparatorios",
        2,
        "¿Cuál de estos es un requisito de la suspensión condicional del procedimiento?",
        [
            "Que el imputado confiese el delito.",
            "Que la pena que pudiere imponerse no exceda de tres años de privación de libertad "
            "y que el imputado no haya sido condenado anteriormente por crimen o simple delito.",
            "Que la víctima lo pida por escrito.",
            "Que el delito sea de acción penal privada.",
        ],
        "B",
        "Es la B porque esos son requisitos del art. 237 CPP, junto con que el imputado no "
        "tenga vigente otra suspensión al momento de los hechos; se decreta por un plazo de "
        "entre uno y tres años y, cumplido sin revocación, se extingue la acción penal (art. "
        "240). La A no, porque no se exige confesión. La C no, porque la propone el fiscal "
        "con acuerdo del imputado; la víctima es oída. La D no, porque se aplica a delitos de "
        "acción pública.",
        f"{CPP}, arts. 237 y 240; {UC}, V, cap. V, 2.2",
    ),
    (
        "Suspensión condicional y acuerdos reparatorios",
        3,
        "¿Sobre qué hechos pueden celebrarse acuerdos reparatorios según el art. 241 CPP?",
        [
            "Sobre cualquier delito.",
            "Sobre hechos que afecten bienes jurídicos disponibles de carácter patrimonial, que "
            "consistan en lesiones menos graves o que constituyan delitos culposos.",
            "Solo sobre delitos sexuales.",
            "Solo sobre delitos cometidos por funcionarios públicos.",
        ],
        "B",
        "Es la B porque esa es la regla del art. 241 CPP; el juez puede negar la aprobación, "
        "entre otros casos, si existe un interés público prevalente en la continuación de la "
        "persecución. La A no, porque la ley limita los hechos. La C no, porque no se trata "
        "de bienes disponibles. La D no, porque no es un requisito.",
        f"{CPP}, art. 241; {UC}, V, cap. V, 2.1",
    ),
    # --------------------------------------------------- cap. VI: investigación
    (
        "Inicio de la investigación y formalización",
        2,
        "¿Qué es la formalización de la investigación según el art. 229 CPP?",
        [
            "La acusación del fiscal.",
            "La comunicación que el fiscal efectúa al imputado, en presencia del juez de "
            "garantía, de que desarrolla actualmente una investigación en su contra respecto de "
            "uno o más delitos determinados.",
            "La denuncia de la víctima.",
            "La sentencia del juez de garantía.",
        ],
        "B",
        "Es la B porque es la definición del art. 229 CPP. La A no, porque la acusación es "
        "posterior, al cierre de la investigación. La C no, porque la denuncia es una forma "
        "de inicio de la investigación (art. 172). La D no, porque la formalización no es una "
        "resolución judicial que decida algo sobre el fondo.",
        f"{CPP}, arts. 172 y 229; {UC}, V, cap. VI, 1 y 2",
    ),
    (
        "Inicio de la investigación y formalización",
        3,
        "¿Qué efectos produce la formalización según el art. 233 CPP?",
        [
            "Ninguno.",
            "Suspende el curso de la prescripción de la acción penal, hace comenzar a correr el "
            "plazo para el cierre de la investigación y el fiscal pierde la facultad de archivar "
            "provisionalmente.",
            "Obliga al juez a decretar la prisión preventiva.",
            "Pone término al proceso.",
        ],
        "B",
        "Es la B porque esos son los efectos del art. 233 CPP; el plazo máximo de la "
        "investigación es de dos años desde la formalización (art. 247). La A no, porque "
        "produce efectos relevantes. La C no, porque la prisión preventiva requiere "
        "solicitud y requisitos propios. La D no, porque el proceso continúa.",
        f"{CPP}, arts. 233 y 247; {UC}, V, cap. VI, 2.2",
    ),
    (
        "Cierre de la investigación",
        2,
        "Cerrada la investigación, ¿qué puede hacer el fiscal dentro de los diez días "
        "siguientes según el art. 248 CPP?",
        [
            "Solo acusar.",
            "Solicitar el sobreseimiento definitivo o temporal, formular acusación o comunicar "
            "la decisión de no perseverar en el procedimiento.",
            "Reabrir la investigación por sí solo, sin límite.",
            "Dictar sentencia.",
        ],
        "B",
        "Es la B porque esas son las tres opciones del art. 248 CPP; la decisión de no "
        "perseverar deja sin efecto la formalización. La A no, porque tiene otras opciones. "
        "La C no, porque la reapertura tiene reglas propias (art. 257). La D no, porque el "
        "fiscal no ejerce funciones jurisdiccionales.",
        f"{CPP}, arts. 247, 248 y 257; {UC}, V, cap. VI, 3",
    ),
    (
        "Cierre de la investigación",
        3,
        "El fiscal solicita el sobreseimiento, pero el querellante quiere que el caso llegue a "
        "juicio. ¿Qué institución le permite intentarlo?",
        [
            "El recurso de queja.",
            "El forzamiento de la acusación: si el fiscal regional, consultado por el juez, "
            "mantiene la decisión de no acusar, el juez puede disponer que la acusación la "
            "formule el querellante.",
            "La acción de revisión.",
            "El amparo ante el juez de garantía.",
        ],
        "B",
        "Es la B porque así lo regula el art. 258 CPP. La A no, porque la queja procede "
        "contra faltas o abusos graves en ciertas resoluciones. La C no, porque la revisión "
        "procede contra sentencias firmes. La D no, porque el amparo protege la libertad "
        "personal del privado de ella.",
        f"{CPP}, art. 258; {UC}, V, cap. VI, 3.4",
    ),
    # ------------------------------------------------ cap. VII: medidas cautelares
    (
        "Detención y prisión preventiva",
        2,
        "Una persona es detenida en flagrancia. ¿En qué plazo máximo debe ser puesta a "
        "disposición del juez de garantía?",
        [
            "En 5 días.",
            "En 24 horas.",
            "En 72 horas, siempre.",
            "En una semana.",
        ],
        "B",
        "Es la B porque el art. 131 CPP fija un plazo máximo de veinticuatro horas desde la "
        "detención para conducir al detenido ante el juez; cualquier persona puede detener a "
        "quien sorprenda en delito flagrante (art. 129). La A no, porque excede el plazo. La "
        "C no, porque las 72 horas corresponden a la posible ampliación de la detención "
        "para preparar la formalización, no al plazo para presentarlo ante el juez. La D no, "
        "porque es muy superior al legal.",
        f"{CPP}, arts. 129 a 132; {UC}, V, cap. VII, 1.2",
    ),
    (
        "Detención y prisión preventiva",
        3,
        "¿Cuándo procede la prisión preventiva según el Código Procesal Penal?",
        [
            "Siempre que el delito sea grave.",
            "Solo cuando las demás medidas cautelares personales sean insuficientes para "
            "asegurar los fines del procedimiento, y siempre que existan antecedentes que "
            "justifiquen la existencia del delito, que permitan presumir fundadamente la "
            "participación del imputado y que la hagan indispensable por las necesidades de "
            "cautela que señala la ley.",
            "Cuando la víctima lo pide.",
            "Automáticamente con la formalización.",
        ],
        "B",
        "Es la B porque la prisión preventiva es la última ratio (art. 139 CPP) y el art. 140 "
        "exige esos requisitos: que sea indispensable para el éxito de diligencias precisas "
        "de la investigación, o que la libertad del imputado sea peligrosa para la seguridad "
        "de la sociedad o del ofendido, o que exista peligro de fuga. La A no, porque la "
        "gravedad por sí sola no basta. La C no, porque la solicitud de la víctima no la "
        "hace procedente. La D no, porque no es automática.",
        f"{CPP}, arts. 139, 140 y 155; {UC}, V, cap. VII, 1.3",
    ),
    # ------------------------------------------------ cap. VIII: etapa preparatoria
    (
        "Etapa intermedia: acusación y excepciones",
        2,
        "¿Ante qué tribunal se realiza la audiencia de preparación del juicio oral?",
        [
            "Ante el tribunal de juicio oral en lo penal.",
            "Ante el juez de garantía.",
            "Ante la Corte de Apelaciones.",
            "Ante el fiscal regional.",
        ],
        "B",
        "Es la B porque la audiencia de preparación del juicio oral la dirige el juez de "
        "garantía (arts. 260 y 266 CPP y art. 14 COT), quien al final dicta el auto de "
        "apertura del juicio oral. La A no, porque el tribunal oral recibe el caso después. "
        "La C no, porque conoce de recursos. La D no, porque el fiscal es parte, no tribunal.",
        f"{CPP}, arts. 260, 266 y 277; {UC}, V, cap. VIII",
    ),
    (
        "Etapa intermedia: acusación y excepciones",
        3,
        "¿Cuál de estas es una excepción de previo y especial pronunciamiento según el art. "
        "264 CPP?",
        [
            "La falta de prueba de cargo.",
            "La litis pendencia.",
            "La legítima defensa.",
            "La falta de dolo.",
        ],
        "B",
        "Es la B porque el art. 264 CPP enumera la incompetencia del juez de garantía, la "
        "litis pendencia, la falta de autorización para proceder criminalmente, la cosa "
        "juzgada y la extinción de la responsabilidad penal. La A no, porque la suficiencia "
        "de la prueba se discute en el juicio. La C no, porque la legítima defensa es una "
        "defensa de fondo. La D no, porque la falta de dolo también es una cuestión de fondo.",
        f"{CPP}, arts. 263 y 264; {UC}, V, cap. VIII, 2.2",
    ),
    (
        "Etapa intermedia: convenciones y exclusión de prueba",
        2,
        "¿Qué son las convenciones probatorias?",
        [
            "Acuerdos sobre la pena.",
            "Acuerdos entre fiscal, querellante e imputado, aprobados por el juez, sobre hechos "
            "que se dan por acreditados y no pueden ser discutidos en el juicio oral.",
            "Contratos entre el fiscal y los testigos.",
            "Pactos para suspender el juicio.",
        ],
        "B",
        "Es la B porque así las regula el art. 275 CPP. La A no, porque no se refieren a la "
        "pena. La C no, porque no son contratos con testigos. La D no, porque no suspenden "
        "el juicio.",
        f"{CPP}, art. 275; {UC}, V, cap. VIII, 3.1",
    ),
    (
        "Etapa intermedia: convenciones y exclusión de prueba",
        3,
        "El juez de garantía excluye una prueba del fiscal por haberse obtenido con "
        "inobservancia de garantías fundamentales. ¿Qué recurso procede contra el auto de "
        "apertura en ese punto?",
        [
            "Ninguno: el auto de apertura es siempre irrecurrible.",
            "Apelación, solo cuando la interpone el Ministerio Público por esa exclusión de "
            "prueba.",
            "Casación en el fondo ante la Corte Suprema.",
            "Reposición ante el tribunal oral.",
        ],
        "B",
        "Es la B porque el art. 277 inc. final CPP dispone que el auto de apertura solo es "
        "apelable cuando lo interpone el Ministerio Público por la exclusión de pruebas "
        "decretada conforme al art. 276 inc. 3 (prueba ilícita o proveniente de actuaciones "
        "declaradas nulas). La A no, porque la ley admite esa apelación. La C no, porque la "
        "casación no existe en el proceso penal. La D no, porque el tribunal oral no revisa "
        "el auto de apertura.",
        f"{CPP}, arts. 276 y 277; {UC}, V, cap. VIII, 3.2",
    ),
    # --------------------------------------------------------- cap. IX: juicio oral
    (
        "Juicio oral",
        2,
        "¿Qué estándar de convicción exige el art. 340 CPP para condenar?",
        [
            "Que la condena sea más probable que la absolución.",
            "Que el tribunal adquiera, más allá de toda duda razonable, la convicción de que "
            "realmente se cometió el hecho punible y de que en él correspondió al acusado una "
            "participación culpable y penada por la ley.",
            "Que el acusado confiese.",
            "Que existan al menos dos testigos.",
        ],
        "B",
        "Es la B porque esa es la exigencia del art. 340 CPP; además, nadie puede ser "
        "condenado con el solo mérito de su propia declaración. La A no, porque la mera "
        "probabilidad no basta. La C no, porque la confesión no es requisito. La D no, porque "
        "rige la libertad de prueba y no un número mínimo de testigos.",
        f"{CPP}, arts. 295 y 340; {UC}, V, cap. IX, 5 y 6",
    ),
    (
        "Juicio oral",
        3,
        "¿Cómo valora la prueba el tribunal de juicio oral en lo penal?",
        [
            "Según la prueba legal o tasada.",
            "Con libertad, pero sin contradecir los principios de la lógica, las máximas de la "
            "experiencia y los conocimientos científicamente afianzados, y debe hacerse cargo "
            "en la fundamentación de toda la prueba producida, incluso la desestimada.",
            "Según su íntima convicción, sin fundamentar.",
            "Solo según la declaración de la víctima.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 297 CPP (sana crítica). La A no, porque el "
        "proceso penal no sigue la prueba tasada. La C no, porque la sentencia debe "
        "fundamentarse. La D no, porque toda la prueba debe valorarse.",
        f"{CPP}, art. 297; {UC}, V, cap. IX, 5.3",
    ),
    # ------------------------------------------------- cap. X: recursos penales
    (
        "Recursos en materia penal",
        2,
        "¿Procede el recurso de apelación contra la sentencia definitiva de un tribunal de "
        "juicio oral en lo penal?",
        [
            "Sí, ante la Corte de Apelaciones, en todo caso.",
            "No: las resoluciones del tribunal de juicio oral en lo penal son inapelables; contra "
            "la sentencia definitiva procede el recurso de nulidad.",
            "Sí, ante la Corte Suprema.",
            "Sí, pero solo el Ministerio Público.",
        ],
        "B",
        "Es la B porque el art. 364 CPP declara inapelables las resoluciones del tribunal de "
        "juicio oral en lo penal; la vía de impugnación de la sentencia definitiva es el "
        "recurso de nulidad (art. 372). La A no, porque la apelación no procede. La C no, "
        "porque la Corte Suprema conoce del recurso de nulidad por ciertas causales. La D no, "
        "porque la inapelabilidad rige para todos los intervinientes.",
        f"{CPP}, arts. 364 y 372; {UC}, V, cap. X, 2",
    ),
    (
        "Recursos en materia penal",
        3,
        "Se interpone recurso de nulidad por infracción sustancial de derechos o garantías "
        "asegurados por la Constitución en la tramitación del juicio. ¿Qué tribunal lo conoce "
        "y en qué plazo debe interponerse?",
        [
            "La Corte de Apelaciones, dentro de cinco días.",
            "La Corte Suprema, dentro de diez días desde la notificación de la sentencia "
            "definitiva.",
            "El mismo tribunal oral, dentro de tres días.",
            "El juez de garantía, sin plazo.",
        ],
        "B",
        "Es la B porque la causal del art. 373 letra a) CPP la conoce la Corte Suprema (art. "
        "376), y el recurso se interpone dentro de diez días desde la notificación de la "
        "sentencia definitiva (art. 372). Las demás causales (errónea aplicación del derecho "
        "y motivos absolutos) las conoce la Corte de Apelaciones. La A no, porque ni el "
        "tribunal ni el plazo son los correctos. La C no, porque el tribunal oral no conoce "
        "de su propia sentencia. La D no, porque el juez de garantía no conoce del recurso.",
        f"{CPP}, arts. 372, 373, 374 y 376; {UC}, V, cap. X, 2.4",
    ),
    # ---------------------------------------------- cap. XI: procedimientos especiales
    (
        "Procedimiento abreviado y simplificado",
        2,
        "¿Qué exige el procedimiento abreviado respecto del imputado?",
        [
            "Que confiese ante la policía.",
            "Que, conociendo los hechos de la acusación y los antecedentes de la investigación, "
            "los acepte expresamente y manifieste su conformidad con la aplicación de este "
            "procedimiento.",
            "Que pague una multa.",
            "Que renuncie a su defensor.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 406 CPP; además, el juez no puede imponer una "
        "pena superior ni más desfavorable que la requerida por el fiscal, y la sentencia "
        "condenatoria no puede fundarse exclusivamente en la aceptación de los hechos (art. "
        "412). La A no, porque la aceptación se presta ante el juez. La C no, porque no es "
        "un requisito. La D no, porque el imputado conserva su defensor.",
        f"{CPP}, arts. 406 y 412; {UC}, V, cap. XI, 1",
    ),
    (
        "Procedimiento abreviado y simplificado",
        3,
        "¿Para qué hechos se aplica el procedimiento simplificado según el art. 388 CPP?",
        [
            "Para todos los crímenes.",
            "Para las faltas y para los simples delitos respecto de los cuales el fiscal requiera "
            "una pena que no exceda de presidio o reclusión menores en su grado mínimo.",
            "Solo para delitos de acción privada.",
            "Para los delitos cometidos por menores de edad, exclusivamente.",
        ],
        "B",
        "Es la B porque así lo establece el art. 388 CPP; lo conoce el juez de garantía, y "
        "si el imputado admite responsabilidad en los hechos del requerimiento, el juez "
        "dicta sentencia de inmediato (art. 395). La A no, porque los crímenes van, en "
        "principio, al juicio oral. La C no, porque la acción privada tiene su propio "
        "procedimiento. La D no, porque la responsabilidad penal adolescente se rige por "
        "otra ley.",
        f"{CPP}, arts. 388 y 395; {UC}, V, cap. XI, 2",
    ),
]
