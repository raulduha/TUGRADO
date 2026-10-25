"""Cédula UC de Derecho Penal (electiva)."""

JURISDICCION = "Chile"
PROGRAMA = "Cédulas UC (licenciatura, vigentes desde 2021)"
CEDULA = "Cédula 14: Derecho Penal (18-03-2021)"
MATERIA = "Derecho Penal"

CP = "Código Penal"
CPR = "Constitución Política"
UC = "Cédula UC Derecho Penal"

PREGUNTAS = [
    # ------------------------------------------------------------- la ley penal
    (
        "La ley penal: legalidad y ley penal en el tiempo",
        1,
        "¿Qué exige el principio de tipicidad consagrado en el art. 19 n.º 3 de la "
        "Constitución?",
        [
            "Que la conducta sancionada esté expresamente descrita en la ley.",
            "Que la pena la determine libremente el juez según la gravedad del hecho.",
            "Que el delito sea descrito en un reglamento dictado por el Presidente.",
            "Que la costumbre complete las conductas que la ley no describe.",
        ],
        "A",
        "Es la A porque la Constitución dispone que ninguna ley podrá establecer penas sin "
        "que la conducta que se sanciona esté expresamente descrita en ella. La B no, porque "
        "la pena también debe estar señalada en la ley. La C no, porque la descripción de la "
        "conducta es materia de ley, no de reglamento. La D no, porque la costumbre no es "
        "fuente de delitos ni de penas.",
        f"{CPR}, art. 19 n.º 3; {UC}, cap. I",
    ),
    (
        "La ley penal: legalidad y ley penal en el tiempo",
        2,
        "Después de una condena ejecutoriada, se promulga una ley que impone una pena menos "
        "rigurosa para ese delito. Según el art. 18 del Código Penal, ¿qué ocurre?",
        [
            "El tribunal de primera instancia que dictó la sentencia debe modificarla, de "
            "oficio o a petición de parte.",
            "Nada, porque la cosa juzgada impide aplicar la ley nueva.",
            "La nueva ley se aplica solo si el condenado no ha empezado a cumplir la pena.",
            "Solo el Presidente puede rebajar la pena mediante un indulto.",
        ],
        "A",
        "Es la A porque el art. 18 inciso 2.º ordena aplicar retroactivamente la ley más "
        "favorable aun después de la sentencia firme, y encarga al tribunal de primera "
        "instancia modificarla; esa modificación no afecta las indemnizaciones pagadas o "
        "cumplidas. La B no, porque la ley exceptúa expresamente la cosa juzgada en favor del "
        "condenado. La C no, porque la ley no pone ese límite. La D no, porque el indulto es "
        "otra institución y aquí la rebaja procede por mandato legal.",
        f"{CP}, art. 18; {CPR}, art. 19 n.º 3; {UC}, cap. I",
    ),
    (
        "La ley penal: legalidad y ley penal en el tiempo",
        1,
        "Según el art. 1 del Código Penal, ¿qué es delito?",
        [
            "Toda acción u omisión voluntaria penada por la ley.",
            "Todo hecho que cause daño a otra persona.",
            "Toda conducta contraria a la moral y a las buenas costumbres.",
            "Toda infracción a un reglamento administrativo.",
        ],
        "A",
        "Es la A porque así lo define el art. 1 del Código Penal, que agrega que las acciones "
        "u omisiones penadas por la ley se reputan siempre voluntarias, a no ser que conste lo "
        "contrario. La B no, porque el daño sin tipo penal puede ser solo un ilícito civil. La "
        "C no, porque la inmoralidad no es delito si la ley no la pena. La D no, porque la "
        "infracción reglamentaria es, por regla general, un ilícito administrativo.",
        f"{CP}, art. 1; {UC}, cap. I",
    ),
    (
        "La ley penal: legalidad y ley penal en el tiempo",
        2,
        "¿Cómo clasifica el Código Penal los delitos según su gravedad?",
        [
            "En crímenes, simples delitos y faltas, según la pena que se les asigna.",
            "En delitos dolosos y culposos, solamente.",
            "En delitos de acción pública y de acción privada.",
            "En delitos comunes y delitos militares.",
        ],
        "A",
        "Es la A porque el art. 3 del Código Penal divide los delitos en crímenes, simples "
        "delitos y faltas, y los califica según la pena que les está asignada en la escala "
        "del art. 21. La B no, porque esa distinción atiende al elemento subjetivo, no a la "
        "gravedad. La C no, porque esa distinción atiende al ejercicio de la acción penal. La "
        "D no, porque atiende a la jurisdicción competente.",
        f"{CP}, arts. 3 y 21; {UC}, cap. I",
    ),
    # --------------------------------------------------------------- tipicidad
    (
        "Imputación objetiva y causalidad",
        3,
        "¿Qué exige, en esencia, la teoría de la imputación objetiva para atribuir un "
        "resultado a una conducta?",
        [
            "Que la conducta haya creado un riesgo jurídicamente desaprobado y que ese riesgo "
            "se haya realizado en el resultado.",
            "Que la conducta sea una condición sin la cual el resultado no se habría producido, "
            "y nada más.",
            "Que el autor haya querido el resultado.",
            "Que el resultado sea previsible para cualquier persona, aunque el riesgo esté "
            "permitido.",
        ],
        "A",
        "Es la A porque la imputación objetiva añade a la causalidad un juicio normativo: la "
        "conducta debe crear o aumentar un riesgo no permitido, y el resultado debe ser la "
        "realización de ese riesgo dentro del ámbito de protección de la norma. La B no, "
        "porque la sola condición sine qua non es la teoría de la equivalencia, que la "
        "imputación objetiva corrige. La C no, porque querer el resultado pertenece al dolo, "
        "que es parte del tipo subjetivo. La D no, porque un riesgo permitido no se imputa "
        "aunque el resultado sea previsible.",
        f"{UC}, cap. II",
    ),
    (
        "Dolo, error de tipo e imprudencia",
        2,
        "Quien se representa como posible el resultado típico y, aun así, actúa aceptándolo, "
        "obra con:",
        [
            "Dolo eventual.",
            "Culpa consciente.",
            "Dolo directo de primer grado.",
            "Culpa inconsciente.",
        ],
        "A",
        "Es la A porque en el dolo eventual el sujeto se representa el resultado como posible "
        "y lo acepta o se conforma con él. La B no, porque en la culpa consciente el sujeto "
        "también se lo representa, pero confía en que no ocurrirá. La C no, porque en el dolo "
        "directo de primer grado el resultado es el objetivo perseguido. La D no, porque en "
        "la culpa inconsciente el sujeto ni siquiera se representa el resultado previsible.",
        f"{CP}, arts. 1 y 2; {UC}, cap. II",
    ),
    (
        "Dolo, error de tipo e imprudencia",
        3,
        "¿Qué efecto tiene un error de tipo vencible?",
        [
            "Excluye el dolo, pero deja subsistente la responsabilidad por imprudencia si el "
            "hecho se castiga en forma culposa.",
            "Excluye toda responsabilidad penal, en todo caso.",
            "No tiene efecto alguno, porque nadie puede alegar ignorancia de la ley.",
            "Solo atenúa la pena del delito doloso.",
        ],
        "A",
        "Es la A porque el error sobre un elemento del tipo elimina el conocimiento propio del "
        "dolo; si era evitable con el debido cuidado, el hecho puede castigarse como "
        "cuasidelito cuando la ley lo pena (arts. 2, 4 y 10 n.º 13). La B no, porque esa es "
        "la consecuencia del error de tipo invencible. La C no, porque el error de tipo no es "
        "ignorancia de la ley, sino de los hechos. La D no, porque el dolo desaparece; no "
        "queda un delito doloso que atenuar.",
        f"{CP}, arts. 2, 4 y 10 n.º 13; {UC}, cap. II",
    ),
    (
        "Dolo, error de tipo e imprudencia",
        2,
        "¿Cuándo se castigan los cuasidelitos según el Código Penal?",
        [
            "Solo en los casos expresamente penados por la ley.",
            "Siempre, con la misma pena del delito doloso.",
            "Nunca, porque solo hay delitos dolosos.",
            "Solo cuando el autor es empleado público.",
        ],
        "A",
        "Es la A porque el art. 10 n.º 13 declara exento de responsabilidad al que comete un "
        "cuasidelito, salvo en los casos expresamente penados por la ley, y el art. 4 los "
        "remite a las disposiciones especiales. La B no, porque su pena es distinta y menor. "
        "La C no, porque el Código sí castiga cuasidelitos, por ejemplo contra las personas "
        "(arts. 490 y siguientes). La D no, porque la regla no depende de la calidad del autor.",
        f"{CP}, arts. 4, 10 n.º 13 y 490; {UC}, cap. II",
    ),
    (
        "Dolo, error de tipo e imprudencia",
        2,
        "A dispara para matar a B, pero por error en la identidad mata a C. Según el art. 1 "
        "del Código Penal:",
        [
            "A responde por el delito cometido, aunque el mal recayó sobre una persona "
            "distinta.",
            "A queda impune porque no quería matar a C.",
            "A responde solo por un cuasidelito de homicidio.",
            "A responde por tentativa respecto de B y por nada respecto de C.",
        ],
        "A",
        "Es la A porque el art. 1 inciso 3.º dispone que el que comete delito responde de él "
        "aunque el mal recaiga sobre persona distinta de la que se proponía ofender; no se "
        "consideran las circunstancias desconocidas que agravarían su responsabilidad, pero sí "
        "las que la atenúen. La B no, porque el error en la persona es irrelevante cuando "
        "ambas víctimas tienen igual protección. La C no, porque A actuó con dolo de matar. "
        "La D no, porque la ley atribuye el delito consumado sobre la persona efectivamente "
        "ofendida.",
        f"{CP}, art. 1 inc. 3.º; {UC}, cap. II",
    ),
    # ---------------------------------------------------------- antijuridicidad
    (
        "Legítima defensa y estado de necesidad",
        1,
        "¿Cuáles son los requisitos de la legítima defensa propia (art. 10 n.º 4 del Código "
        "Penal)?",
        [
            "Agresión ilegítima, necesidad racional del medio empleado para impedirla o "
            "repelerla, y falta de provocación suficiente de quien se defiende.",
            "Agresión de cualquier tipo, uso de un medio idéntico al del agresor y aviso "
            "previo a la policía.",
            "Que el defensor sea más débil que el agresor y que no pueda huir.",
            "Que exista un mal inminente sobre la propiedad ajena.",
        ],
        "A",
        "Es la A porque esos son los tres requisitos del art. 10 n.º 4. La B no, porque la "
        "agresión debe ser ilegítima y se exige racionalidad del medio, no identidad. La C "
        "no, porque la ley no exige inferioridad física ni imposibilidad de huir. La D no, "
        "porque se refiere al estado de necesidad del art. 10 n.º 7.",
        f"{CP}, art. 10 n.º 4; {UC}, cap. III",
    ),
    (
        "Legítima defensa y estado de necesidad",
        3,
        "¿Qué naturaleza tiene la llamada legítima defensa privilegiada del art. 10 n.º 6 "
        "inciso 2.º del Código Penal?",
        [
            "Es una presunción simplemente legal de que concurren los requisitos de la "
            "legítima defensa en ciertas situaciones descritas por la ley.",
            "Es una presunción de derecho, que no admite prueba en contrario.",
            "Es una causal de atenuación de la pena.",
            "Es una excusa legal absolutoria aplicable solo a los parientes.",
        ],
        "A",
        "Es la A porque la ley presume que concurren los requisitos de la legítima defensa, "
        "por ejemplo al rechazar de noche el escalamiento de una casa habitada, y la doctrina "
        "y la jurisprudencia la entienden como presunción simplemente legal. La B no, porque "
        "se admite prueba en contrario. La C no, porque, si opera, exime de responsabilidad, "
        "no la atenúa. La D no, porque no es una excusa absolutoria ni se limita a parientes.",
        f"{CP}, art. 10 n.º 6; {UC}, cap. III",
    ),
    (
        "Causas de justificación",
        2,
        "Para evitar que un incendio alcance su casa, A derriba la reja de su vecino. ¿Qué "
        "causal del Código Penal puede justificar su conducta?",
        [
            "El estado de necesidad justificante del art. 10 n.º 7.",
            "La legítima defensa de terceros.",
            "El cumplimiento de un deber.",
            "La obediencia debida.",
        ],
        "A",
        "Es la A porque el art. 10 n.º 7 justifica al que, para evitar un mal, causa daño en "
        "la propiedad ajena, si el mal que se evita es real o su peligro inminente, es mayor "
        "que el causado y no hay otro medio practicable y menos perjudicial. La B no, porque "
        "no hay una agresión ilegítima de una persona. La C no, porque A no actúa en "
        "cumplimiento de un deber jurídico. La D no, porque no hay una orden de un superior.",
        f"{CP}, art. 10 n.º 7; {UC}, cap. III",
    ),
    # ------------------------------------------------------------- culpabilidad
    (
        "Imputabilidad",
        1,
        "Según el Código Penal y la Ley 20.084, ¿desde qué edad puede una persona responder "
        "penalmente en Chile?",
        [
            "Desde los 14 años, conforme al sistema de responsabilidad penal adolescente "
            "hasta los 18.",
            "Desde los 10 años.",
            "Desde los 16 años, si obró con discernimiento.",
            "Solo desde los 18 años, sin excepción.",
        ],
        "A",
        "Es la A porque el art. 10 n.º 2 exime al menor de 18 años, cuya responsabilidad se "
        "rige por la Ley 20.084, que se aplica a quienes al cometer el delito eran mayores de "
        "14 y menores de 18. La B no, porque bajo 14 años no hay responsabilidad penal. La C "
        "no, porque el examen de discernimiento fue eliminado por la Ley 20.084. La D no, "
        "porque entre 14 y 18 hay responsabilidad penal adolescente.",
        f"{CP}, art. 10 n.º 2; Ley 20.084, art. 3; {UC}, cap. IV",
    ),
    (
        "Imputabilidad",
        2,
        "¿A quién exime de responsabilidad el art. 10 n.º 1 del Código Penal?",
        [
            "Al loco o demente, salvo que haya obrado en un intervalo lúcido, y al que, por "
            "cualquier causa independiente de su voluntad, se halla privado totalmente de "
            "razón.",
            "A quien se embriaga voluntariamente para darse ánimo.",
            "A quien actúa en estado de ira provocada.",
            "A quien desconoce que su conducta está prohibida.",
        ],
        "A",
        "Es la A porque así lo dispone el art. 10 n.º 1, que regula la inimputabilidad por "
        "enajenación o trastorno mental. La B no, porque la privación de razón provocada "
        "voluntariamente no exime. La C no, porque el arrebato u obcecación es, a lo más, una "
        "atenuante (art. 11 n.º 5). La D no, porque ese es un error de prohibición, que es "
        "otra cuestión de culpabilidad.",
        f"{CP}, arts. 10 n.º 1 y 11 n.º 5; {UC}, cap. IV",
    ),
    (
        "Error de prohibición",
        3,
        "¿Cómo se trata en Chile el error de prohibición invencible?",
        [
            "No está regulado expresamente, pero la doctrina y la jurisprudencia aceptan que "
            "excluye la culpabilidad.",
            "Está regulado expresamente como atenuante en el art. 11 del Código Penal.",
            "Es irrelevante, porque la ley se presume conocida de todos.",
            "Transforma el delito doloso en cuasidelito.",
        ],
        "A",
        "Es la A porque, aunque el Código no lo regula, desde fines de los años noventa la "
        "Corte Suprema y la doctrina mayoritaria reconocen que quien no pudo conocer la "
        "ilicitud de su conducta no es culpable. La B no, porque no figura entre las "
        "atenuantes del art. 11. La C no, porque la presunción de conocimiento del art. 8 del "
        "Código Civil no excluye en materia penal el principio de culpabilidad. La D no, "
        "porque eso describe el efecto del error de tipo vencible.",
        f"{CP}, arts. 1 y 11; {UC}, cap. IV",
    ),
    (
        "Exigibilidad de otra conducta",
        3,
        "¿Qué distingue el estado de necesidad exculpante del art. 10 n.º 11 del justificante "
        "del art. 10 n.º 7?",
        [
            "Puede proteger cualquier bien jurídico y admite que el mal causado no sea "
            "sustancialmente superior al evitado, cuando no era razonablemente exigible el "
            "sacrificio del bien amenazado.",
            "Solo se aplica a daños en la propiedad ajena.",
            "Exige que el mal evitado sea mayor que el causado, igual que el justificante.",
            "Fue derogado en 2010 por la Ley 20.480.",
        ],
        "A",
        "Es la A porque el art. 10 n.º 11, introducido por la Ley 20.480, exige actualidad o "
        "inminencia del mal, falta de otro medio practicable y menos perjudicial, que el mal "
        "causado no sea sustancialmente superior al evitado y que el sacrificio no pudiera "
        "razonablemente exigirse; excluye la culpabilidad, no la antijuridicidad. La B no, "
        "porque esa limitación es propia del n.º 7. La C no, porque basta que el mal causado "
        "no sea sustancialmente superior. La D no, porque esa ley lo introdujo.",
        f"{CP}, art. 10 n.º 7 y n.º 11; Ley 20.480; {UC}, cap. IV",
    ),
    (
        "Exigibilidad de otra conducta",
        2,
        "El art. 10 n.º 9 del Código Penal exime al que obra violentado por una fuerza "
        "irresistible o impulsado por un miedo insuperable. ¿Qué elemento del delito excluye, "
        "según la doctrina mayoritaria?",
        [
            "La culpabilidad, por no ser exigible otra conducta.",
            "La tipicidad, porque falta la conducta.",
            "La antijuridicidad, porque el hecho es conforme a derecho.",
            "La punibilidad, como excusa legal absolutoria.",
        ],
        "A",
        "Es la A porque la doctrina mayoritaria entiende el miedo insuperable y la fuerza "
        "irresistible moral como causas de inexigibilidad: el hecho sigue siendo ilícito, "
        "pero no se le puede reprochar al autor. La B no, porque el sujeto sí actúa. La C no, "
        "porque no se autoriza lesionar el bien jurídico. La D no, porque no es una excusa "
        "absolutoria, sino una causa de exculpación.",
        f"{CP}, art. 10 n.º 9; {UC}, cap. IV",
    ),
    # -------------------------------------------- etapas, autoría y participación
    (
        "Etapas del delito, autoría y participación",
        2,
        "¿Cuándo hay delito frustrado según el art. 7 del Código Penal?",
        [
            "Cuando el delincuente pone de su parte todo lo necesario para que el crimen o "
            "simple delito se consume, y esto no se verifica por causas independientes de su "
            "voluntad.",
            "Cuando el culpable da principio a la ejecución por hechos directos, pero faltan "
            "uno o más para su complemento.",
            "Cuando dos o más personas se conciertan para cometer el delito.",
            "Cuando el autor desiste voluntariamente antes de consumarlo.",
        ],
        "A",
        "Es la A porque así define el art. 7 el delito frustrado. La B no, porque esa es la "
        "definición de tentativa. La C no, porque esa es la conspiración del art. 8, punible "
        "solo cuando la ley lo dispone. La D no, porque el desistimiento voluntario excluye "
        "la punibilidad de la tentativa o frustración.",
        f"{CP}, arts. 7 y 8; {UC}, cap. V",
    ),
    (
        "Etapas del delito, autoría y participación",
        2,
        "¿Cuándo se castigan las faltas según el art. 9 del Código Penal?",
        [
            "Solo cuando han sido consumadas.",
            "También en grado de tentativa.",
            "También en grado de frustración, pero no de tentativa.",
            "Nunca, porque son infracciones administrativas.",
        ],
        "A",
        "Es la A porque el art. 9 dispone que las faltas solo se castigan cuando han sido "
        "consumadas, salvo que la ley disponga otra cosa. La B no, porque la tentativa de "
        "falta no se castiga por regla general. La C no, porque la frustración tampoco. La D "
        "no, porque las faltas son delitos penales, la categoría menos grave del art. 3.",
        f"{CP}, arts. 3 y 9; {UC}, cap. V",
    ),
    (
        "Etapas del delito, autoría y participación",
        2,
        "¿Cuál de estas personas es autor según el art. 15 n.º 2 del Código Penal?",
        [
            "Quien induce directamente a otro a ejecutar el delito.",
            "Quien, sin concierto previo, presta ayuda menor después del delito.",
            "Quien oculta los efectos del delito sabiendo de su origen.",
            "Quien conoce el plan delictivo y no lo denuncia.",
        ],
        "A",
        "Es la A porque el art. 15 n.º 2 considera autores a quienes fuerzan o inducen "
        "directamente a otro a ejecutarlo. La B no, porque la ayuda posterior sin concierto "
        "es, a lo más, encubrimiento. La C no, porque ocultar los efectos es una forma de "
        "encubrimiento (art. 17). La D no, porque el mero conocimiento sin intervención no es "
        "autoría.",
        f"{CP}, arts. 15 y 17; {UC}, cap. V",
    ),
    (
        "Etapas del delito, autoría y participación",
        3,
        "¿Quiénes quedan exentos de la pena del encubrimiento según el art. 17 del Código "
        "Penal?",
        [
            "Los que encubren a su cónyuge, conviviente civil o a ciertos parientes, salvo si "
            "se aprovechan o ayudan a aprovecharse de los efectos del delito.",
            "Todos los que actúan por amistad con el autor.",
            "Los empleados públicos que conocen el delito en el ejercicio de sus funciones.",
            "Nadie: el encubrimiento siempre se castiga.",
        ],
        "A",
        "Es la A porque el inciso final del art. 17 exime a quienes encubren a esas personas, "
        "con la sola excepción de quienes incurren en el n.º 1, es decir, el aprovechamiento "
        "de los efectos. La B no, porque la amistad no exime. La C no, porque su calidad no "
        "los exime y puede agravar su situación. La D no, porque la ley sí contempla la "
        "exención.",
        f"{CP}, art. 17; {UC}, cap. V",
    ),
    # ----------------------------------------------------------- parte especial
    (
        "Homicidio simple",
        2,
        "¿Cuál de estas circunstancias NO califica el homicidio según el art. 391 n.º 1 del "
        "Código Penal?",
        [
            "Que el autor sea cónyuge de la víctima.",
            "La alevosía.",
            "El premio o la promesa remuneratoria.",
            "El ensañamiento.",
        ],
        "A",
        "Es la A porque el vínculo con la víctima configura el parricidio o el femicidio "
        "(arts. 390 y siguientes), no una calificante del homicidio. La B no, porque la "
        "alevosía es la primera circunstancia del art. 391 n.º 1. La C no, porque el premio o "
        "promesa remuneratoria también lo califica. La D no, porque el ensañamiento, aumentar "
        "deliberada e inhumanamente el dolor del ofendido, también lo califica.",
        f"{CP}, arts. 390 y 391; {UC}, cap. VI",
    ),
    (
        "Robo con violencia o intimidación",
        1,
        "¿Qué diferencia el robo con violencia o intimidación del hurto?",
        [
            "En el robo, la apropiación se comete con violencia o intimidación en las "
            "personas.",
            "En el hurto, la cosa debe ser inmueble.",
            "El robo exige que la cosa sea propia del autor.",
            "El hurto exige que la víctima esté presente.",
        ],
        "A",
        "Es la A porque ambos delitos consisten en apropiarse de una cosa mueble ajena sin la "
        "voluntad de su dueño y con ánimo de lucro, pero hay robo cuando se emplea violencia o "
        "intimidación en las personas o fuerza en las cosas, y hurto cuando no (art. 432). La "
        "B no, porque ambos recaen sobre cosas muebles. La C no, porque la cosa debe ser "
        "ajena. La D no, porque el hurto no exige la presencia de la víctima.",
        f"{CP}, arts. 432, 436 y 446; {UC}, cap. VI",
    ),
    (
        "Estafa",
        2,
        "¿Cuáles son los elementos de la estafa según la doctrina chilena?",
        [
            "Engaño, error, disposición patrimonial y perjuicio.",
            "Violencia, apropiación y ánimo de lucro.",
            "Abuso de confianza y apropiación de dinero recibido en depósito.",
            "Falsificación de un instrumento público y su uso.",
        ],
        "A",
        "Es la A porque la estafa exige un engaño que provoca error en la víctima, quien por "
        "ese error realiza una disposición patrimonial que le causa perjuicio (arts. 468 y "
        "473). La B no, porque la violencia es propia del robo. La C no, porque eso describe "
        "la apropiación indebida del art. 470 n.º 1. La D no, porque eso corresponde a las "
        "falsedades documentales.",
        f"{CP}, arts. 468, 470 y 473; {UC}, cap. VI",
    ),
    (
        "Cohecho",
        2,
        "¿Quién comete cohecho activo según el art. 250 del Código Penal?",
        [
            "El particular que da, ofrece o consiente en dar a un empleado público un "
            "beneficio económico o de otra naturaleza indebido.",
            "El empleado público que solicita o acepta el beneficio.",
            "El empleado público que se apropia de caudales que administra.",
            "El juez que falla contra ley expresa.",
        ],
        "A",
        "Es la A porque el art. 250 castiga al que da, ofrece o consiente en dar a un empleado "
        "público un beneficio indebido en razón de su cargo o para que realice ciertos actos "
        "u omisiones. La B no, porque esa es la conducta del empleado público, el cohecho "
        "pasivo (arts. 248 y siguientes). La C no, porque eso es malversación de caudales "
        "públicos. La D no, porque eso es prevaricación.",
        f"{CP}, arts. 248, 250 y 223; {UC}, cap. VI",
    ),
]
