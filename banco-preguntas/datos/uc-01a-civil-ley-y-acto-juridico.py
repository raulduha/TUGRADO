"""Cédula UC de Derecho Civil, partes I (Teoría de la ley) y II (Teoría del acto jurídico)."""

JURISDICCION = "Chile"
PROGRAMA = "Cédulas UC (licenciatura, vigentes desde 2021)"
CEDULA = "Cédula 1: Derecho Civil (15-03-2021)"
MATERIA = "Derecho Civil"

CC = "Código Civil"
UC = "Cédula UC Derecho Civil"

PREGUNTAS = [
    # ------------------------------------------------------------- I. Teoría de la ley
    (
        "La ley: definición y fuentes del Derecho",
        1,
        "Según el Código Civil, ¿qué es la ley?",
        [
            "Una declaración de la voluntad soberana que, manifestada en la forma prescrita por "
            "la Constitución, manda, prohíbe o permite.",
            "Toda norma de conducta obligatoria que dicte cualquier autoridad pública.",
            "La costumbre reiterada que la comunidad considera obligatoria.",
            "La sentencia de los tribunales superiores que fija el sentido de una norma.",
        ],
        "A",
        "Es la A porque es la definición literal del art. 1 del Código Civil. La B no, porque "
        "no toda norma de una autoridad es ley: los decretos y reglamentos, por ejemplo, son "
        "normas de otra jerarquía. La C no, porque la costumbre es una fuente distinta, que en "
        "materia civil solo vale cuando la ley se remite a ella (art. 2). La D no, porque las "
        "sentencias solo obligan en las causas en que se dictan (art. 3 inc. 2).",
        f"{CC}, arts. 1, 2 y 3; {UC}, I.1 y I.2.1",
    ),
    (
        "La ley: definición y fuentes del Derecho",
        2,
        "Una persona alega que no debe cumplir una ley porque nunca supo que existía. "
        "¿Qué responde el Código Civil?",
        [
            "Que la ignorancia de la ley excusa si la persona prueba que actuó de buena fe.",
            "Que la ley solo obliga a quienes fueron notificados personalmente de ella.",
            "Que nadie puede alegar ignorancia de la ley después de que esta haya entrado en "
            "vigencia.",
            "Que la ignorancia excusa solo a los extranjeros que residen en Chile.",
        ],
        "C",
        "Es la C porque el art. 8 establece que nadie podrá alegar ignorancia de la ley "
        "después de que esta haya entrado en vigencia; la doctrina discute si es una "
        "presunción o una ficción, pero el efecto es el mismo. La A no, porque la buena fe no "
        "exime del cumplimiento. La B no, porque la ley se da a conocer por su publicación en "
        "el Diario Oficial (art. 7), no por notificación personal. La D no, porque la ley es "
        "obligatoria para todos los habitantes, incluso los extranjeros (art. 14).",
        f"{CC}, arts. 7, 8 y 14; {UC}, I.2.3",
    ),
    (
        "Interpretación de la ley",
        1,
        "Según el art. 19 del Código Civil, cuando el sentido de la ley es claro, ¿qué "
        "debe hacer el intérprete?",
        [
            "Buscar la intención del legislador en la historia fidedigna de su establecimiento.",
            "No desatender su tenor literal a pretexto de consultar su espíritu.",
            "Aplicar la interpretación que resulte más equitativa para el caso.",
            "Pedir a la Corte Suprema que fije su sentido con efecto general.",
        ],
        "B",
        "Es la B porque el art. 19 inc. 1 ordena que, cuando el sentido de la ley es claro, no "
        "se desatienda su tenor literal a pretexto de consultar su espíritu. La A no, porque "
        "la historia fidedigna sirve para interpretar una expresión oscura (art. 19 inc. 2), "
        "no para apartarse de un texto claro. La C no, porque la equidad natural es el último "
        "recurso, para pasajes oscuros o contradictorios (art. 24). La D no, porque solo el "
        "legislador interpreta la ley de un modo generalmente obligatorio (art. 3 inc. 1).",
        f"{CC}, arts. 3, 19 y 24; {UC}, I.2.2",
    ),
    (
        "Interpretación de la ley",
        2,
        "Una ley usa la palabra «tradición» sin definirla. ¿En qué sentido debe "
        "entenderse esa palabra?",
        [
            "En su sentido natural y obvio, según el uso general de las palabras.",
            "En el sentido que le den los que profesan la ciencia o arte respectiva, si es una "
            "palabra técnica, salvo que aparezca que se tomó en sentido diverso.",
            "En el sentido que le asigne el juez según su criterio de equidad.",
            "En el sentido que tenga en el derecho comparado.",
        ],
        "B",
        "Es la B porque «tradición» es una palabra técnica del derecho (un modo de adquirir "
        "el dominio) y el art. 21 manda tomar las palabras técnicas de toda ciencia o arte en "
        "el sentido que les den quienes profesan esa ciencia, salvo que aparezca claramente "
        "que se tomaron en sentido diverso. La A no, porque el sentido natural y obvio (art. "
        "20) es la regla para las palabras comunes, no para las técnicas. La C no, porque el "
        "Código fija reglas de interpretación y no deja el sentido de las palabras al arbitrio "
        "judicial. La D no, porque el derecho comparado no es un elemento de interpretación "
        "previsto en los arts. 19 a 24.",
        f"{CC}, arts. 20 y 21; {UC}, I.2.2.3",
    ),
    (
        "Efectos de la ley en el tiempo",
        2,
        "¿Qué establece el art. 9 del Código Civil sobre la retroactividad?",
        [
            "Que la ley nunca puede tener efecto retroactivo, ni siquiera por disposición expresa.",
            "Que la ley solo dispone para lo futuro y no tiene jamás efecto retroactivo; pero "
            "las leyes interpretativas se entienden incorporadas en las que interpretan, sin "
            "afectar las sentencias ejecutoriadas en el tiempo intermedio.",
            "Que toda ley civil es retroactiva salvo que diga lo contrario.",
            "Que las leyes interpretativas pueden dejar sin efecto las sentencias ejecutoriadas "
            "dictadas antes de su publicación.",
        ],
        "B",
        "Es la B porque reproduce el art. 9: la irretroactividad es la regla y las leyes "
        "interpretativas se incorporan a la ley interpretada, respetando las sentencias "
        "ejecutoriadas del tiempo intermedio. La A no, porque el art. 9 obliga al juez, no al "
        "legislador: una ley puede ser retroactiva si lo dice expresamente, con los límites "
        "constitucionales (por ejemplo, en materia penal y de propiedad). La C no, porque "
        "invierte la regla. La D no, porque el inc. 2 protege expresamente esas sentencias.",
        f"{CC}, art. 9; {UC}, I.2.5.1",
    ),
    (
        "Efectos de la ley en el tiempo",
        3,
        "Se celebra un contrato y después se dicta una ley que cambia las reglas sobre los "
        "efectos de ese tipo de contrato. Según la Ley sobre Efecto Retroactivo de las Leyes, "
        "¿qué ley rige los efectos del contrato?",
        [
            "La nueva, porque las leyes de orden público rigen in actum todos los contratos.",
            "La que elija el acreedor, por ser la parte protegida.",
            "La vigente al tiempo de su celebración, porque se entiende incorporada al "
            "contrato; se exceptúan las leyes sobre el modo de reclamar en juicio los derechos "
            "y las que señalan penas por la infracción del contrato.",
            "La vigente al tiempo en que se demande su cumplimiento.",
        ],
        "C",
        "Es la C porque el art. 22 de la Ley sobre Efecto Retroactivo de las Leyes dispone "
        "que en todo contrato se entienden incorporadas las leyes vigentes al tiempo de su "
        "celebración, con esas dos excepciones (las leyes procesales y las que fijan penas "
        "por la infracción, que se castiga con arreglo a la ley bajo la cual se cometió). La A "
        "no, porque esa es la regla general de efecto inmediato que el art. 22 justamente "
        "excluye para los contratos. La B no, porque no hay tal elección. La D no, porque la "
        "fecha de la demanda solo importa para las leyes procesales.",
        f"Ley sobre Efecto Retroactivo de las Leyes, art. 22; {UC}, I.2.5.1.6",
    ),
    (
        "Efectos de la ley en el espacio",
        2,
        "Un chileno que vive en España otorga allá un testamento ante notario, cumpliendo "
        "la ley española. ¿Qué ley rige la forma de ese instrumento?",
        [
            "La ley chilena, porque el testador es chileno.",
            "La ley española, porque la forma de los instrumentos públicos se determina por la "
            "ley del país en que se otorgan.",
            "La ley del lugar donde estén los bienes.",
            "La ley que el testador declare elegir.",
        ],
        "B",
        "Es la B porque el art. 17 recoge el principio lex locus regit actum: la forma de los "
        "instrumentos públicos se determina por la ley del país en que se otorgan, y su "
        "autenticidad se prueba según el Código de Procedimiento Civil. La A no, porque el "
        "estatuto personal (art. 15) se refiere al estado, la capacidad y las obligaciones de "
        "familia, no a la forma. La C no, porque el estatuto real (art. 16) se refiere a los "
        "bienes situados en Chile, no a la forma del acto. La D no, porque la ley aplicable a "
        "la forma no queda a elección del otorgante.",
        f"{CC}, arts. 15, 16 y 17; {UC}, I.2.5.2",
    ),
    (
        "Efectos de la ley en el espacio",
        3,
        "Un chileno domiciliado en el extranjero quiere celebrar allá un acto que producirá "
        "efectos en Chile. ¿En qué materias sigue sujeto a la ley chilena según el art. 15?",
        [
            "En todas, porque la ley chilena acompaña siempre a sus nacionales.",
            "Solo en materia penal.",
            "En lo relativo a su estado y su capacidad para ejecutar actos que hayan de tener "
            "efecto en Chile, y en las obligaciones y derechos que nacen de las relaciones de "
            "familia, pero solo respecto de su cónyuge y parientes chilenos.",
            "En lo relativo a la forma de los actos que celebre.",
        ],
        "C",
        "Es la C porque el art. 15 limita la extraterritorialidad de la ley chilena a esas "
        "materias (el llamado estatuto personal). La A no, porque fuera de esos casos rige la "
        "ley del lugar. La B no, porque el art. 15 es una norma civil y no se refiere a la "
        "materia penal. La D no, porque la forma se rige por la ley del lugar de otorgamiento "
        "(art. 17).",
        f"{CC}, arts. 15 y 17; {UC}, I.2.5.2.2",
    ),
    (
        "Costumbre, doctrina y jurisprudencia",
        1,
        "¿Qué valor tiene la costumbre en materia civil según el Código Civil?",
        [
            "Tiene la misma fuerza que la ley y puede derogarla.",
            "Constituye derecho cuando la ley se remite a ella.",
            "Constituye derecho siempre que la ley guarde silencio.",
            "No tiene ningún valor en materia civil.",
        ],
        "B",
        "Es la B porque el art. 2 dispone que la costumbre no constituye derecho sino en los "
        "casos en que la ley se remite a ella (costumbre según ley). La A no, porque la "
        "costumbre contra ley no tiene valor. La C no, porque esa es la regla de la costumbre "
        "mercantil (art. 4 del Código de Comercio), no de la civil. La D no, porque sí vale "
        "cuando la ley se remite a ella, por ejemplo en los arts. 1546 y 1563.",
        f"{CC}, arts. 2, 1546 y 1563; Código de Comercio, art. 4; {UC}, I.3",
    ),
    (
        "Costumbre, doctrina y jurisprudencia",
        2,
        "La Corte Suprema falla un caso interpretando de cierto modo un artículo del Código "
        "Civil. Al año siguiente, un juez de letras debe resolver un caso parecido. ¿Está "
        "obligado a seguir ese criterio?",
        [
            "Sí, porque las sentencias de la Corte Suprema tienen efecto general.",
            "Sí, pero solo si la sentencia se publicó en el Diario Oficial.",
            "No, porque las sentencias judiciales no tienen fuerza obligatoria sino respecto "
            "de las causas en que actualmente se pronunciaren, aunque el criterio pueda tener "
            "valor persuasivo.",
            "No, porque la jurisprudencia está prohibida como fuente en Chile.",
        ],
        "C",
        "Es la C porque el art. 3 inc. 2 limita la fuerza obligatoria de las sentencias a la "
        "causa en que se dictan; la jurisprudencia es una fuente material o persuasiva, no "
        "formal. La A no, porque Chile no sigue el sistema del precedente obligatorio. La B "
        "no, porque la publicación no cambia ese efecto relativo. La D no, porque no está "
        "prohibida: orienta a los jueces y a la doctrina, aunque no los obliga.",
        f"{CC}, art. 3; {UC}, I.5",
    ),
    # ------------------------------------------------------- II. Teoría del acto jurídico
    (
        "Autonomía privada y hechos jurídicos",
        1,
        "¿Qué distingue a un acto jurídico de un simple hecho jurídico?",
        [
            "Que el acto jurídico produce efectos y el hecho jurídico no.",
            "Que el acto jurídico es una manifestación de voluntad hecha con la intención de "
            "crear, modificar o extinguir derechos, y produce esos efectos porque la ley "
            "reconoce esa voluntad.",
            "Que el hecho jurídico siempre proviene de la naturaleza y el acto jurídico del "
            "hombre.",
            "Que el acto jurídico siempre requiere el acuerdo de dos o más partes.",
        ],
        "B",
        "Es la B porque lo propio del acto jurídico es la voluntad dirigida a producir efectos "
        "jurídicos, que el ordenamiento reconoce en virtud de la autonomía privada. La A no, "
        "porque los hechos jurídicos también producen efectos (por eso son jurídicos), por "
        "ejemplo el nacimiento o la muerte. La C no, porque también hay hechos del hombre que "
        "no son actos jurídicos, como los delitos civiles, cuyos efectos no los busca el autor. "
        "La D no, porque existen actos jurídicos unilaterales, como el testamento.",
        f"{CC}, arts. 999, 1437 y 1445; {UC}, II, caps. I y II",
    ),
    (
        "Autonomía privada y hechos jurídicos",
        2,
        "¿Cuál de las siguientes es una expresión del principio de autonomía privada en el "
        "Código Civil?",
        [
            "Que todo contrato legalmente celebrado es una ley para los contratantes.",
            "Que la costumbre no constituye derecho sino cuando la ley se remite a ella.",
            "Que las leyes de procedimiento rigen in actum.",
            "Que la buena fe se presume en la posesión.",
        ],
        "A",
        "Es la A porque el art. 1545 da fuerza obligatoria a lo que las partes acuerdan "
        "libremente, que es la consecuencia central de la autonomía privada (libertad para "
        "contratar, para elegir con quién y para fijar el contenido). La B no, porque se "
        "refiere al valor de la costumbre como fuente (art. 2). La C no, porque es una regla "
        "sobre el efecto de la ley en el tiempo. La D no, porque es una presunción en materia "
        "posesoria (art. 707), ajena a la autonomía privada.",
        f"{CC}, arts. 1545 y 1546; {UC}, II, cap. I",
    ),
    (
        "Estructura y clasificaciones del acto jurídico",
        1,
        "Según el art. 1444, en una compraventa, ¿qué son la cosa y el precio?",
        [
            "Cosas de la naturaleza del contrato.",
            "Elementos accidentales, que las partes agregan por cláusulas especiales.",
            "Cosas de la esencia: sin ellas el contrato no produce efecto alguno o degenera en "
            "otro contrato diferente.",
            "Requisitos de publicidad del contrato.",
        ],
        "C",
        "Es la C porque son cosas de la esencia aquellas sin las cuales el contrato no produce "
        "efecto alguno o degenera en otro diferente (art. 1444); sin precio en dinero, por "
        "ejemplo, no hay compraventa. La A no, porque las de la naturaleza se entienden "
        "pertenecerle sin cláusula especial pero pueden excluirse, como la obligación de "
        "saneamiento. La B no, porque las accidentales (por ejemplo, un plazo o una "
        "condición) solo existen si se agregan. La D no, porque la cosa y el precio no son "
        "formalidades de publicidad.",
        f"{CC}, arts. 1444 y 1793; {UC}, II, caps. II y III",
    ),
    (
        "Estructura y clasificaciones del acto jurídico",
        2,
        "¿Cómo se clasifica el contrato de comodato (préstamo de uso) según los arts. 1439 y 1443?",
        [
            "Unilateral y real.",
            "Bilateral y consensual.",
            "Unilateral y solemne.",
            "Bilateral y real.",
        ],
        "A",
        "Es la A porque en el comodato solo se obliga el comodatario, a restituir la cosa "
        "(contrato unilateral, art. 1439), y se perfecciona por la entrega de la cosa "
        "(contrato real, arts. 1443 y 2174). La B no, porque no nacen obligaciones recíprocas "
        "ni basta el solo consentimiento. La C no, porque no exige una solemnidad sino la "
        "entrega. La D no, porque, aunque eventualmente el comodante pueda quedar obligado "
        "(por ejemplo, a indemnizar), la doctrina lo clasifica como unilateral, pues al "
        "perfeccionarse solo resulta obligado el comodatario.",
        f"{CC}, arts. 1439, 1443 y 2174; {UC}, II, cap. III",
    ),
    (
        "Manifestación de voluntad y silencio",
        2,
        "Como regla general, ¿qué valor tiene el silencio en la formación de un acto "
        "jurídico en el derecho chileno?",
        [
            "Equivale siempre a aceptación: quien calla otorga.",
            "Equivale siempre a rechazo.",
            "No constituye manifestación de voluntad, salvo que la ley, las partes o las "
            "circunstancias le den ese valor.",
            "Equivale a aceptación solo en los contratos solemnes.",
        ],
        "C",
        "Es la C porque, como regla general, el silencio no es manifestación de voluntad; "
        "solo la tiene cuando la ley lo dispone, cuando las partes lo pactaron o cuando "
        "circunstancias concretas lo hacen inequívoco (silencio circunstanciado). Un caso "
        "legal es el art. 2125. La A no, porque el adagio «quien calla otorga» no es la regla "
        "jurídica. La B no, porque tampoco se le atribuye en general un valor negativo. La D "
        "no, porque en los contratos solemnes se exige precisamente una forma y no puede "
        "suplirse con el silencio.",
        f"{CC}, art. 2125; {UC}, II, cap. IV, 1.1.1",
    ),
    (
        "Manifestación de voluntad y silencio",
        3,
        "Un abogado que habitualmente gestiona negocios ajenos recibe por correo el encargo "
        "de un cliente ausente y no contesta nada. ¿Qué dispone el art. 2125 para este caso?",
        [
            "Que su silencio no produce efecto alguno, porque el mandato es solemne.",
            "Que debe declarar lo antes posible si acepta o no el encargo, y transcurrido un "
            "término razonable su silencio se mirará como aceptación.",
            "Que su silencio equivale a rechazo y el cliente debe buscar otro mandatario.",
            "Que el encargo se entiende aceptado solo si el abogado empieza a ejecutarlo.",
        ],
        "B",
        "Es la B porque el art. 2125 dispone que las personas que por su profesión u oficio "
        "se encargan de negocios ajenos están obligadas a declarar lo más pronto posible si "
        "aceptan o no el encargo, y transcurrido un término razonable su silencio se mirará "
        "como aceptación. Es el ejemplo clásico de silencio con valor legal. La A no, porque "
        "el mandato es por regla general consensual. La C no, porque la ley le da el valor "
        "opuesto. La D no, porque la ejecución es una forma de aceptación tácita (art. 2124), "
        "pero aquí la ley va más lejos y atribuye efecto al solo silencio.",
        f"{CC}, arts. 2124 y 2125; {UC}, II, cap. IV, 1.1.1",
    ),
    (
        "Formación del consentimiento",
        2,
        "Ana envía una oferta por correo electrónico. Bruno la acepta pura y simplemente. "
        "Según el Código de Comercio, ¿cuándo queda perfeccionado el contrato?",
        [
            "Cuando Ana recibe la aceptación.",
            "Cuando Ana toma conocimiento efectivo de la aceptación.",
            "En el momento en que Bruno da su aceptación pura y simple, aunque Ana aún no la "
            "conozca.",
            "Cuando ambas partes firman un documento común.",
        ],
        "C",
        "Es la C porque el art. 101 del Código de Comercio dispone que, dada la contestación, "
        "si en ella se aprueba pura y simplemente la propuesta, el contrato queda en el acto "
        "perfeccionado: Chile sigue la teoría de la declaración. La A no, porque esa es la "
        "teoría de la recepción, que no adopta el Código. La B no, porque esa es la teoría "
        "del conocimiento. La D no, porque, salvo solemnidad legal o convencional, basta el "
        "acuerdo de voluntades y no se exige un documento común.",
        f"Código de Comercio, arts. 97 a 101; {UC}, II, cap. IV, 1.2.2",
    ),
    (
        "Formación del consentimiento",
        3,
        "Carla ofrece por escrito vender su auto. Diego responde aceptando, pero «siempre que "
        "el precio se pague en cuatro cuotas». ¿Qué efecto tiene esa respuesta?",
        [
            "Perfecciona el contrato con la modificación propuesta por Diego.",
            "Perfecciona el contrato en los términos originales de Carla.",
            "Importa una nueva propuesta, de modo que no hay contrato mientras Carla no la acepte.",
            "Obliga a Carla a indemnizar a Diego si no acepta las cuotas.",
        ],
        "C",
        "Es la C porque el art. 102 del Código de Comercio dispone que la aceptación "
        "condicional, o que modifica la oferta, se considera una nueva propuesta: los roles se "
        "invierten y ahora es Carla quien debe aceptar. La A no, porque Carla no ha consentido "
        "en esa modificación. La B no, porque Diego no aceptó pura y simplemente. La D no, "
        "porque Carla no queda obligada por una propuesta ajena.",
        f"Código de Comercio, arts. 101 y 102; {UC}, II, cap. IV, 1.2.2",
    ),
    (
        "Error como vicio de la voluntad",
        2,
        "Elena compra un cuadro creyendo que es un original de un pintor famoso; en realidad "
        "es una copia, y el vendedor también lo ignoraba. ¿Qué tipo de error sufrió?",
        [
            "Error de derecho, que no vicia el consentimiento.",
            "Error en la persona, que solo vicia si la persona fue la causa principal.",
            "Error accidental, que nunca vicia el consentimiento.",
            "Error sustancial, porque recae sobre una calidad esencial del objeto, y vicia el "
            "consentimiento.",
        ],
        "D",
        "Es la D porque el art. 1454 inc. 1 considera error sustancial el que recae sobre la "
        "sustancia o calidad esencial del objeto, y la autenticidad es lo que se buscaba al "
        "comprar; la sanción es la nulidad relativa. La A no, porque Elena no se equivocó "
        "sobre una norma (art. 1452). La B no, porque el error no recae en la persona del "
        "vendedor (art. 1455). La C no, porque una calidad accidental solo vicia si fue el "
        "principal motivo y la otra parte lo conocía (art. 1454 inc. 2), y aquí la calidad es "
        "esencial.",
        f"{CC}, arts. 1452, 1454, 1455 y 1682; {UC}, II, cap. IV, 1.3.1",
    ),
    (
        "Error como vicio de la voluntad",
        3,
        "Fernando cree que le están donando un terreno, mientras que quien se lo entrega cree "
        "que se lo está vendiendo. ¿Cómo califica el Código este error y qué discute la "
        "doctrina sobre su sanción?",
        [
            "Es error esencial u obstáculo (sobre la especie del acto); la doctrina discute si "
            "su sanción es la inexistencia, la nulidad absoluta o la nulidad relativa.",
            "Es error sustancial, sancionado sin discusión con la nulidad relativa.",
            "Es error en la persona, que no vicia el consentimiento.",
            "Es error común, que valida el acto.",
        ],
        "A",
        "Es la A porque el art. 1453 vicia el consentimiento cuando el error recae sobre la "
        "especie de acto o contrato (como cuando una parte entiende empréstito y la otra "
        "donación). Como no hay acuerdo alguno, parte de la doctrina sostiene que el acto es "
        "inexistente o absolutamente nulo; otra parte, por la letra del art. 1453 («vicia el "
        "consentimiento») y del art. 1682, defiende la nulidad relativa. La B no, porque no "
        "recae sobre la sustancia del objeto. La C no, porque no se trata de la persona. La D "
        "no, porque el error común es otra figura, que en ciertos casos valida actos "
        "realizados con un error compartido por todos.",
        f"{CC}, arts. 1453, 1454 y 1682; {UC}, II, cap. IV, 1.3.1.2.1",
    ),
    (
        "Fuerza y dolo",
        2,
        "Gabriel firma un contrato porque un tercero, ajeno al negocio, lo amenazó "
        "gravemente. La otra parte no sabía nada. ¿Puede Gabriel pedir la nulidad?",
        [
            "No, porque la fuerza solo vicia si proviene de la parte beneficiada.",
            "Sí, porque para que la fuerza vicie el consentimiento no es necesario que la "
            "emplee el beneficiado: basta que se haya empleado por cualquier persona para "
            "obtener el consentimiento.",
            "No, porque la fuerza de un tercero solo da derecho a indemnización.",
            "Sí, pero solo si prueba que la otra parte actuó de mala fe.",
        ],
        "B",
        "Es la B porque el art. 1457 dispone que para que la fuerza vicie el consentimiento "
        "no es necesario que la ejerza aquel que es beneficiado por ella, sino que basta que "
        "se haya empleado por cualquier persona con el objeto de obtener el consentimiento. "
        "La A no, porque esa exigencia corresponde al dolo (art. 1458), no a la fuerza. La C "
        "no, porque confunde la fuerza con el dolo de un tercero. La D no, porque la mala fe "
        "de la contraparte no es requisito.",
        f"{CC}, arts. 1456, 1457 y 1458; {UC}, II, cap. IV, 1.3.2",
    ),
    (
        "Fuerza y dolo",
        3,
        "Héctor compra una casa porque un vecino, sin relación con el vendedor, le mintió "
        "sobre el valor de la zona. Sin esa mentira no habría comprado. ¿Qué puede hacer "
        "Héctor?",
        [
            "Pedir la nulidad relativa de la compraventa, porque el dolo fue determinante.",
            "Pedir la nulidad absoluta, porque el dolo es un delito civil.",
            "No puede pedir la nulidad, porque el dolo no es obra de una de las partes; solo "
            "tiene acción de perjuicios contra quien lo fraguó o se aprovechó de él.",
            "Nada, porque el dolo de terceros no produce ningún efecto.",
        ],
        "C",
        "Es la C porque el art. 1458 exige, para que el dolo vicie el consentimiento, que sea "
        "obra de una de las partes y que aparezca claramente que sin él no se habría "
        "contratado; en los demás casos solo da lugar a la acción de perjuicios contra quienes "
        "lo fraguaron (por el total) o se aprovecharon de él (hasta el provecho). La A no, "
        "porque falta el requisito de que el dolo provenga de una parte. La B no, porque el "
        "dolo, cuando vicia, produce nulidad relativa. La D no, porque sí produce efecto: la "
        "acción indemnizatoria.",
        f"{CC}, arts. 1458 y 1459; {UC}, II, cap. IV, 1.3.3",
    ),
    (
        "Lesión",
        2,
        "En una compraventa de un inmueble, ¿cuándo sufre lesión enorme el vendedor?",
        [
            "Cuando el precio que recibe es inferior a la mitad del justo precio de la cosa.",
            "Cuando el precio es inferior en cualquier medida al valor de mercado.",
            "Cuando el precio es inferior a dos tercios del avalúo fiscal.",
            "Cuando el comprador revende la cosa con ganancia.",
        ],
        "A",
        "Es la A porque el art. 1889 dispone que el vendedor sufre lesión enorme cuando el "
        "precio que recibe es inferior a la mitad del justo precio de la cosa vendida, que se "
        "refiere al tiempo del contrato. La B no, porque la ley exige una desproporción "
        "calificada, no cualquier diferencia. La C no, porque el parámetro es el justo precio, "
        "no el avalúo fiscal. La D no, porque la reventa posterior no es el criterio legal.",
        f"{CC}, arts. 1888, 1889 y 1891; {UC}, II, cap. IV, 1.4",
    ),
    (
        "Lesión",
        3,
        "Se declara la rescisión por lesión enorme a favor del vendedor de un inmueble. "
        "¿Qué opción tiene el comprador?",
        [
            "Ninguna: debe restituir el inmueble.",
            "Consentir en la rescisión o completar el justo precio con deducción de una décima "
            "parte.",
            "Completar el justo precio más un interés del diez por ciento.",
            "Pagar al vendedor una indemnización equivalente a la mitad del justo precio.",
        ],
        "B",
        "Es la B porque el art. 1890 da al comprador contra quien se pronuncia la rescisión la "
        "opción de consentir en ella o completar el justo precio con deducción de una décima "
        "parte (al vendedor, en el caso inverso, se le permite restituir el exceso aumentado "
        "en una décima parte). La A no, porque la ley le da la opción de mantener el "
        "contrato. La C no, porque la décima parte se deduce, no se agrega. La D no, porque "
        "no existe esa indemnización.",
        f"{CC}, arts. 1889 y 1890; {UC}, II, cap. IV, 1.4",
    ),
    (
        "Objeto del acto jurídico",
        1,
        "¿Qué requisitos debe reunir el objeto de un acto jurídico cuando consiste en una cosa?",
        [
            "Que sea corporal y de valor superior a una UTM.",
            "Que exista actualmente y esté en poder de quien se obliga.",
            "Que sea inmueble.",
            "Que sea real (exista o se espere que exista), comerciable y determinada o "
            "determinable.",
        ],
        "D",
        "Es la D porque el art. 1461 exige que la cosa exista o se espere que exista, que sea "
        "comerciable y que esté determinada, a lo menos en cuanto a su género, pudiendo la "
        "cantidad ser incierta si el acto fija reglas para determinarla. La A no, porque "
        "también pueden ser objeto las cosas incorporales y no hay un valor mínimo. La B no, "
        "porque se admiten cosas futuras y cosas que no están en poder del que se obliga "
        "(incluso la venta de cosa ajena vale, art. 1815). La C no, porque también pueden ser "
        "objeto los muebles.",
        f"{CC}, arts. 1460, 1461 y 1815; {UC}, II, cap. IV, 2",
    ),
    (
        "Objeto del acto jurídico",
        3,
        "Un inmueble está embargado por decreto judicial y el deudor lo vende, sin "
        "autorización del juez ni consentimiento del acreedor. Según la doctrina mayoritaria, "
        "¿qué ocurre?",
        [
            "La compraventa es nula absolutamente por objeto ilícito, porque la venta es "
            "enajenación.",
            "La compraventa es válida, porque el art. 1464 se refiere a la enajenación y la "
            "venta solo genera obligaciones; el problema se presenta al hacer la tradición, "
            "que adolece de objeto ilícito.",
            "La compraventa es inexistente.",
            "La compraventa es válida y la tradición también, porque el embargo solo afecta "
            "al acreedor.",
        ],
        "B",
        "Es la B porque, según la doctrina mayoritaria, enajenar es transferir el dominio o "
        "constituir un derecho real, lo que ocurre con la tradición; la compraventa, que solo "
        "genera obligaciones, no es enajenación, de modo que vale. Lo que adolece de objeto "
        "ilícito es la tradición (art. 1464 n.° 3), sancionada con nulidad absoluta (art. "
        "1682). La A no, porque esa es la posición minoritaria, que se apoya en el art. 1810. "
        "La C no, porque el objeto existe. La D no, porque la tradición de la cosa embargada "
        "sin autorización ni consentimiento del acreedor adolece de objeto ilícito.",
        f"{CC}, arts. 1464 n.° 3, 1682 y 1810; {UC}, II, cap. IV, 2.3",
    ),
    (
        "Causa del acto jurídico",
        2,
        "¿Qué entiende el art. 1467 por causa?",
        [
            "El objeto material del contrato.",
            "La forma que exige la ley para el acto.",
            "El motivo que induce al acto o contrato.",
            "La capacidad de las partes.",
        ],
        "C",
        "Es la C porque el art. 1467 inc. 2 define la causa como el motivo que induce al acto "
        "o contrato, y agrega que la pura liberalidad o beneficencia es causa suficiente. "
        "Además exige que la causa sea real y lícita, aunque no es necesario expresarla. La A "
        "no, porque el objeto es un requisito distinto (arts. 1460 y siguientes). La B no, "
        "porque la forma es la solemnidad. La D no, porque la capacidad es otro requisito del "
        "art. 1445.",
        f"{CC}, arts. 1445 y 1467; {UC}, II, cap. IV, 3",
    ),
    (
        "Causa del acto jurídico",
        3,
        "Según los ejemplos del propio art. 1467, ¿en cuál de estos casos la obligación "
        "carece de causa o tiene causa ilícita?",
        [
            "La promesa de dar algo en pago de una deuda que no existe carece de causa, y la "
            "promesa de dar algo en recompensa de un crimen tiene causa ilícita.",
            "La donación hecha por pura liberalidad carece de causa.",
            "La compraventa de un auto usado tiene causa ilícita.",
            "El mutuo con intereses carece de causa.",
        ],
        "A",
        "Es la A porque son los dos ejemplos que da el art. 1467 inc. final: la promesa de "
        "dar algo en pago de una deuda que no existe carece de causa, y la promesa de dar "
        "algo en recompensa de un crimen o hecho inmoral tiene causa ilícita. La B no, porque "
        "la pura liberalidad es causa suficiente (art. 1467 inc. 1). La C no, porque no hay "
        "nada ilícito en ese motivo. La D no, porque en el mutuo la causa existe y es lícita.",
        f"{CC}, art. 1467; {UC}, II, cap. IV, 3.4",
    ),
    (
        "Capacidad",
        1,
        "¿Quiénes son absolutamente incapaces según el art. 1447?",
        [
            "Los menores adultos y los disipadores interdictos.",
            "Los dementes, los impúberes y los sordos o sordomudos que no pueden darse a "
            "entender claramente.",
            "Todos los menores de 18 años.",
            "Las personas jurídicas.",
        ],
        "B",
        "Es la B porque esa es la enumeración del art. 1447 inc. 1; sus actos no producen ni "
        "aun obligaciones naturales ni admiten caución, y adolecen de nulidad absoluta (art. "
        "1682). La A no, porque menores adultos y disipadores interdictos son relativamente "
        "incapaces (art. 1447 inc. 3). La C no, porque solo los impúberes son absolutamente "
        "incapaces; los menores adultos son relativamente incapaces. La D no, porque las "
        "personas jurídicas son capaces y actúan por medio de sus representantes.",
        f"{CC}, arts. 26, 1446, 1447 y 1682; {UC}, II, cap. IV, 4",
    ),
    (
        "Capacidad",
        2,
        "¿Qué diferencia hay entre capacidad de goce y capacidad de ejercicio?",
        [
            "Ninguna: son sinónimos.",
            "La de goce es la aptitud para ejercer derechos por sí mismo; la de ejercicio, "
            "para adquirirlos.",
            "La de goce es la aptitud para adquirir derechos y es un atributo de toda persona; "
            "la de ejercicio es la aptitud para ejercerlos por sí mismo, sin el ministerio o "
            "autorización de otra.",
            "La de goce solo la tienen los mayores de edad.",
        ],
        "C",
        "Es la C porque toda persona tiene capacidad de goce (es un atributo de la "
        "personalidad), mientras que la capacidad de ejercicio, que define el art. 1445 inc. "
        "final, consiste en poder obligarse por sí misma, sin el ministerio o la autorización "
        "de otra, y puede faltar. La A no, porque son conceptos distintos. La B no, porque "
        "invierte los conceptos. La D no, porque incluso un recién nacido tiene capacidad de "
        "goce.",
        f"{CC}, arts. 1445 y 1446; {UC}, II, cap. IV, 4.2",
    ),
    (
        "Formalidades",
        2,
        "La compraventa de un inmueble se celebra por instrumento privado firmado ante "
        "testigos. ¿Qué ocurre?",
        [
            "Es válida, porque la compraventa es consensual.",
            "Es válida entre las partes, pero inoponible a terceros.",
            "No se reputa perfecta ante la ley, porque la escritura pública es una solemnidad "
            "y su falta no puede suplirse por otra prueba.",
            "Es válida, pero solo puede probarse con testigos.",
        ],
        "C",
        "Es la C porque el art. 1801 inc. 2 exige escritura pública para la venta de bienes "
        "raíces, y el art. 1701 dispone que la falta de instrumento público no puede suplirse "
        "por otra prueba en los actos y contratos en que la ley lo requiere como solemnidad; "
        "se mirarán como no ejecutados o celebrados. La A no, porque la consensualidad es la "
        "regla general, con esta excepción. La B no, porque no se trata de una formalidad de "
        "publicidad sino de una solemnidad. La D no, porque la solemnidad no puede suplirse.",
        f"{CC}, arts. 1443, 1701 y 1801; {UC}, II, cap. IV, 5.2",
    ),
    (
        "Formalidades",
        3,
        "¿Cuál de estos es un ejemplo de formalidad por vía de publicidad?",
        [
            "La escritura pública en la compraventa de un inmueble.",
            "La notificación al deudor de la cesión de un crédito, sin la cual la cesión no "
            "produce efecto contra el deudor ni contra terceros.",
            "La autorización judicial para enajenar bienes raíces de un pupilo.",
            "La exigencia de prueba escrita para obligaciones de más de dos UTM.",
        ],
        "B",
        "Es la B porque la notificación o aceptación del deudor (art. 1902) busca que la "
        "cesión sea conocida y oponible; su omisión no anula la cesión entre cedente y "
        "cesionario, sino que la hace inoponible. La A no, porque es una solemnidad de "
        "existencia. La C no, porque es una formalidad habilitante, exigida en protección de "
        "incapaces. La D no, porque es una formalidad por vía de prueba (arts. 1708 y 1709).",
        f"{CC}, arts. 1708, 1709, 1801 y 1902; {UC}, II, cap. IV, 5.3 a 5.5",
    ),
    (
        "Efectos de los actos jurídicos",
        1,
        "Como regla general, ¿a quiénes afectan los efectos de un contrato?",
        [
            "A todas las personas, porque el contrato es ley.",
            "Solo a las partes que lo celebraron (efecto relativo), sin perjuicio de que los "
            "terceros deban respetar su existencia.",
            "A las partes y a todos sus vecinos.",
            "Solo al acreedor.",
        ],
        "B",
        "Es la B porque el contrato es una ley para los contratantes (art. 1545), no para los "
        "terceros: es el efecto relativo de los contratos. Con todo, su existencia es "
        "oponible a todos, que no pueden desconocerla. La A no, porque el art. 1545 habla "
        "solo de los contratantes. La C no, porque no hay tal extensión. La D no, porque el "
        "contrato vincula a todas las partes, incluido el deudor.",
        f"{CC}, art. 1545; {UC}, II, cap. V",
    ),
    (
        "Efectos de los actos jurídicos",
        2,
        "¿A quiénes se transmiten, como regla general, los derechos y obligaciones de un "
        "contrato cuando muere una de las partes?",
        [
            "A nadie: el contrato se extingue con la muerte.",
            "Solo a los legatarios.",
            "A sus herederos, que lo representan y suceden en todos sus derechos y "
            "obligaciones transmisibles.",
            "Al Fisco.",
        ],
        "C",
        "Es la C porque los herederos suceden al causante en todos sus derechos y "
        "obligaciones transmisibles (art. 1097), de modo que no se consideran terceros "
        "respecto de los contratos del causante. Se exceptúan los contratos intuito personae, "
        "como el mandato, que termina con la muerte (art. 2163). La A no, porque eso solo "
        "ocurre con los contratos personalísimos. La B no, porque los legatarios suceden en "
        "bienes determinados, no en las obligaciones. La D no, porque el Fisco solo hereda en "
        "último lugar, a falta de otros herederos.",
        f"{CC}, arts. 1097 y 2163; {UC}, II, cap. V",
    ),
    (
        "Inexistencia",
        2,
        "¿Qué argumento usa la doctrina que sostiene que la inexistencia sí está recogida "
        "en el Código Civil chileno?",
        [
            "Que el art. 1681 menciona expresamente la inexistencia como sanción.",
            "Que el Código distingue requisitos de existencia y de validez, y en algunas "
            "normas dice que el acto «no produce efecto alguno» o «no se reputa perfecto» "
            "(por ejemplo, arts. 1444, 1701 y 1801).",
            "Que la Corte Suprema la ha declarado obligatoria.",
            "Que la inexistencia se sanea en diez años.",
        ],
        "B",
        "Es la B porque los partidarios de la inexistencia (por ejemplo, Claro Solar) se "
        "apoyan en esas expresiones, que aludirían a un acto que ni siquiera nace. Los "
        "detractores (por ejemplo, Alessandri) responden que el Código solo regula la nulidad "
        "(art. 1682 sanciona con nulidad absoluta la omisión de requisitos exigidos en "
        "consideración a la naturaleza del acto). La A no, porque el art. 1681 regula la "
        "nulidad, no la inexistencia. La C no, porque no hay tal jurisprudencia obligatoria. "
        "La D no, porque, para sus partidarios, el acto inexistente no se sanea con el tiempo.",
        f"{CC}, arts. 1444, 1681, 1682, 1701 y 1801; {UC}, II, cap. VI, 3",
    ),
    (
        "Inexistencia",
        3,
        "Según los partidarios de la teoría de la inexistencia, ¿cuál de estas es una "
        "diferencia entre el acto inexistente y el absolutamente nulo?",
        [
            "El acto nulo produce efectos mientras no se declare la nulidad; el inexistente no "
            "produce efecto alguno y no requiere declaración judicial ni se sanea por el "
            "transcurso del tiempo.",
            "El inexistente se sanea por ratificación; el nulo no.",
            "Solo el inexistente puede ser alegado por el Ministerio Público.",
            "No hay diferencia alguna entre ellos.",
        ],
        "A",
        "Es la A porque esas son las diferencias que se suelen enumerar: el acto nulo existe "
        "y produce efectos hasta que la nulidad se declara judicialmente, y se sanea por el "
        "transcurso de diez años (art. 1683); el inexistente, en cambio, no produciría efecto "
        "alguno ni se sanearía nunca. La B no, porque el inexistente tampoco se sanea por "
        "ratificación. La C no, porque la nulidad absoluta también puede pedirla el "
        "Ministerio Público (art. 1683). La D no, porque, para esta doctrina, sí hay "
        "diferencias relevantes.",
        f"{CC}, art. 1683; {UC}, II, cap. VI, 3.4",
    ),
    (
        "Nulidad absoluta y relativa",
        2,
        "¿Cuáles son las causales de nulidad absoluta según el art. 1682?",
        [
            "El error, la fuerza y el dolo.",
            "Los actos de los menores adultos.",
            "El objeto ilícito, la causa ilícita, la omisión de requisitos o formalidades "
            "exigidos en consideración a la naturaleza del acto y los actos de personas "
            "absolutamente incapaces.",
            "Cualquier incumplimiento del contrato.",
        ],
        "C",
        "Es la C porque el art. 1682 enumera esas causales; la doctrina agrega, para quienes "
        "no aceptan la inexistencia, la falta de objeto, de causa o de voluntad. Cualquier "
        "otra especie de vicio produce nulidad relativa. La A no, porque los vicios del "
        "consentimiento producen nulidad relativa. La B no, porque los menores adultos son "
        "relativamente incapaces. La D no, porque el incumplimiento no es causa de nulidad, "
        "sino de resolución, cumplimiento forzado o indemnización.",
        f"{CC}, art. 1682; {UC}, II, cap. VI, 4.2",
    ),
    (
        "Nulidad absoluta y relativa",
        3,
        "Un contrato adolece de un vicio que produce nulidad relativa. ¿Cuál de estas "
        "afirmaciones es correcta?",
        [
            "El juez debe declararla de oficio si aparece de manifiesto en el acto.",
            "Puede pedirla cualquier persona que tenga interés en ello.",
            "No puede sanearse.",
            "Solo pueden alegarla aquellos en cuyo beneficio la han establecido las leyes, o "
            "sus herederos o cesionarios, y puede sanearse por el transcurso del tiempo o por "
            "ratificación.",
        ],
        "D",
        "Es la D porque así lo dispone el art. 1684; el plazo para pedirla es de cuatro años "
        "(art. 1691). La A no, porque la declaración de oficio es propia de la nulidad "
        "absoluta (art. 1683). La B no, porque la legitimación amplia también es propia de la "
        "nulidad absoluta. La C no, porque la nulidad relativa sí se sanea, por ratificación o "
        "por el transcurso del tiempo.",
        f"{CC}, arts. 1683, 1684 y 1691; {UC}, II, cap. VI, 4.2.2",
    ),
    (
        "Efectos de la nulidad y conversión",
        2,
        "Se declara judicialmente la nulidad de una compraventa. ¿Qué efecto tiene entre "
        "las partes?",
        [
            "Ninguno: el contrato sigue vigente.",
            "Las partes tienen derecho a ser restituidas al mismo estado en que se hallarían "
            "si no hubiese existido el acto nulo.",
            "Solo el comprador debe devolver la cosa, sin derecho a recuperar el precio.",
            "El contrato se convierte automáticamente en arrendamiento.",
        ],
        "B",
        "Es la B porque el art. 1687 da a las partes derecho a ser restituidas al estado "
        "anterior, con las reglas sobre prestaciones mutuas (frutos, mejoras, deterioros), "
        "sin perjuicio de lo dispuesto sobre el objeto o la causa ilícita (art. 1468). La A "
        "no, porque la nulidad declarada priva de efectos al acto. La C no, porque las "
        "restituciones son recíprocas. La D no, porque la conversión no opera así: exige que "
        "el acto nulo reúna los requisitos de otro acto y que las partes lo hubieran querido.",
        f"{CC}, arts. 1468 y 1687; {UC}, II, cap. VI, 4.4",
    ),
    (
        "Efectos de la nulidad y conversión",
        3,
        "Una escritura pública de compraventa de un auto es defectuosa porque el notario era "
        "incompetente, pero está firmada por las partes. ¿Qué dispone el art. 1701 inc. 2?",
        [
            "Que la escritura es inexistente y no tiene valor alguno.",
            "Que vale como instrumento privado si está firmada por las partes: es un caso de "
            "conversión del acto nulo.",
            "Que el notario debe responder del precio.",
            "Que la venta del auto es nula absolutamente.",
        ],
        "B",
        "Es la B porque el art. 1701 inc. 2 dispone que el instrumento defectuoso por "
        "incompetencia del funcionario o por otra falta en la forma vale como instrumento "
        "privado si estuviere firmado por las partes; la doctrina lo cita como caso de "
        "conversión. Como la compraventa de un mueble es consensual, la venta vale. La A no, "
        "porque la ley le reconoce valor. La C no, porque el artículo no establece esa "
        "responsabilidad. La D no, porque la compraventa de muebles no requiere escritura "
        "pública.",
        f"{CC}, arts. 1701 y 1801; {UC}, II, cap. VI, 4.5",
    ),
    (
        "Simulación",
        2,
        "¿Qué distingue a la simulación relativa de la absoluta?",
        [
            "En la relativa las partes celebran un acto aparente para ocultar otro acto "
            "verdadero (por ejemplo, una compraventa que encubre una donación); en la absoluta "
            "no quieren celebrar acto alguno.",
            "En la relativa el acto es válido y en la absoluta siempre es inexistente por "
            "ley expresa.",
            "En la relativa solo hay una parte y en la absoluta hay dos.",
            "No hay diferencia: son sinónimos.",
        ],
        "A",
        "Es la A porque esa es la distinción doctrinaria: en la absoluta el acto aparente no "
        "esconde nada (por ejemplo, una venta ficticia para eludir a los acreedores); en la "
        "relativa disfraza otro acto real. La B no, porque el Código no regula expresamente la "
        "sanción de la simulación absoluta, que la doctrina discute. La C no, porque la "
        "simulación supone un acuerdo entre las partes. La D no, porque son figuras "
        "distintas.",
        f"{CC}, art. 1707; {UC}, II, cap. VII",
    ),
    (
        "Simulación",
        3,
        "Las partes otorgan una escritura pública de compraventa y, en una contraescritura "
        "privada, declaran que el precio no se pagó. ¿Qué efecto tiene esa contraescritura "
        "respecto de terceros?",
        [
            "Produce efecto contra todos, porque refleja la verdad.",
            "Produce efecto contra terceros solo si se presenta en juicio.",
            "No produce efecto contra terceros.",
            "Produce efecto contra terceros si se anota al margen de la escritura matriz.",
        ],
        "C",
        "Es la C porque el art. 1707 inc. 1 dispone que las escrituras privadas hechas por "
        "los contratantes para alterar lo pactado en escritura pública no producen efecto "
        "contra terceros. La A no, porque la ley protege a los terceros que confían en el "
        "acto ostensible. La B no, porque esa no es una condición legal de oponibilidad. La D "
        "no, porque la anotación al margen es exigencia para las contraescrituras públicas "
        "(art. 1707 inc. 2), no para las privadas.",
        f"{CC}, art. 1707; {UC}, II, cap. VII",
    ),
    (
        "Representación",
        1,
        "¿Qué efecto produce el acto que una persona ejecuta a nombre de otra, estando "
        "facultada por ella o por la ley para representarla?",
        [
            "Produce efectos solo respecto del representante.",
            "Produce respecto del representado iguales efectos que si hubiese contratado él mismo.",
            "Es nulo si el representado no lo firma.",
            "Solo produce efectos si lo ratifica un juez.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 1448: los efectos se radican directamente en "
        "el representado. La A no, porque el representante no queda obligado personalmente. "
        "La C no, porque la firma del representado no es necesaria si el representante tenía "
        "poder. La D no, porque no se requiere intervención judicial.",
        f"{CC}, art. 1448; {UC}, II, cap. VIII",
    ),
    (
        "Representación",
        3,
        "Una persona vende a nombre de otra un inmueble sin tener poder para hacerlo. ¿Qué "
        "situación jurídica se produce respecto del supuesto representado?",
        [
            "La venta es nula absolutamente.",
            "La venta es inoponible al supuesto representado, que puede ratificarla y así "
            "hacerla suya.",
            "La venta obliga siempre al supuesto representado.",
            "La venta es válida solo si el comprador estaba de buena fe.",
        ],
        "B",
        "Es la B porque la doctrina y la jurisprudencia consideran que el acto celebrado por "
        "quien no tiene poder, o excediéndolo, no es nulo sino inoponible al supuesto "
        "representado, quien puede ratificarlo (art. 2160) y radicar en sí sus efectos. La A "
        "no, porque no falta un requisito de validez del acto. La C no, porque nadie queda "
        "obligado por un acto que no autorizó. La D no, porque la buena fe del comprador no "
        "suple la falta de poder.",
        f"{CC}, arts. 1448 y 2160; {UC}, II, cap. VIII",
    ),
]
