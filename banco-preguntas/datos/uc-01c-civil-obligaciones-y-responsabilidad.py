"""Cédula UC de Derecho Civil, partes V (Obligaciones) y VI cap. I (Responsabilidad
extracontractual)."""

JURISDICCION = "Chile"
PROGRAMA = "Cédulas UC (licenciatura, vigentes desde 2021)"
CEDULA = "Cédula 1: Derecho Civil (15-03-2021)"
MATERIA = "Derecho Civil"

CC = "Código Civil"
UC = "Cédula UC Derecho Civil"

PREGUNTAS = [
    # ---------------------------------------------------------------- V. Obligaciones
    (
        "La obligación: concepto, elementos y fuentes",
        1,
        "¿Cuáles son las fuentes de las obligaciones que enumera el art. 1437?",
        [
            "Solo el contrato y la ley.",
            "El contrato, el cuasicontrato, el delito, el cuasidelito y la ley.",
            "El contrato, la costumbre y la jurisprudencia.",
            "La voluntad unilateral y el enriquecimiento sin causa, exclusivamente.",
        ],
        "B",
        "Es la B porque el art. 1437 dice que las obligaciones nacen del concurso real de "
        "voluntades (contratos o convenciones), de un hecho voluntario de la persona que se "
        "obliga (cuasicontratos), de un hecho ilícito con intención de dañar (delitos) o sin "
        "ella (cuasidelitos), y por disposición de la ley. La A no, porque omite tres "
        "fuentes. La C no, porque ni la costumbre ni la jurisprudencia figuran en el art. "
        "1437. La D no, porque la declaración unilateral de voluntad y el enriquecimiento sin "
        "causa son fuentes que propone la doctrina moderna, no la enumeración legal.",
        f"{CC}, arts. 1437 y 2284; {UC}, V, cap. I, 3",
    ),
    (
        "La obligación: concepto, elementos y fuentes",
        2,
        "¿Cuáles son los elementos de toda obligación?",
        [
            "Sujetos (acreedor y deudor), objeto (la prestación) y vínculo jurídico.",
            "Precio, cosa y consentimiento.",
            "Solemnidad, plazo y condición.",
            "Demanda, sentencia y ejecución.",
        ],
        "A",
        "Es la A porque toda obligación supone un sujeto activo (acreedor), un sujeto pasivo "
        "(deudor), una prestación de dar, hacer o no hacer (objeto) y el vínculo jurídico que "
        "los une y que permite al acreedor exigir el cumplimiento. La B no, porque esos son "
        "elementos esenciales de la compraventa, no de toda obligación. La C no, porque el "
        "plazo y la condición son modalidades accidentales. La D no, porque son etapas de un "
        "juicio, no elementos de la obligación.",
        f"{CC}, arts. 1438 y 1460; {UC}, V, cap. I, 2",
    ),
    (
        "Obligaciones civiles y naturales",
        2,
        "¿Qué efecto principal tiene una obligación natural?",
        [
            "Da acción para exigir su cumplimiento, igual que una civil.",
            "No confiere acción para exigir su cumplimiento, pero, cumplida, autoriza para "
            "retener lo que se ha dado o pagado en razón de ella.",
            "Es nula y obliga a devolver lo pagado.",
            "Solo puede cumplirse por un tercero.",
        ],
        "B",
        "Es la B porque así las define el art. 1470: el acreedor no puede demandar, pero si "
        "el deudor paga voluntariamente, no puede repetir lo pagado. La A no, porque esa es "
        "la obligación civil. La C no, porque la obligación natural es válida y su pago no se "
        "restituye. La D no, porque la puede pagar el propio deudor.",
        f"{CC}, art. 1470; {UC}, V, cap. II, 1",
    ),
    (
        "Obligaciones civiles y naturales",
        3,
        "Una deuda prescribió. El deudor, sabiendo que está prescrita, la paga "
        "voluntariamente y luego pide la devolución. ¿Qué ocurre?",
        [
            "Debe devolvérsele lo pagado, porque pagó lo que no debía.",
            "No puede repetir, porque las obligaciones civiles extinguidas por la prescripción "
            "son obligaciones naturales y su pago voluntario autoriza al acreedor a retener.",
            "Puede repetir solo la mitad.",
            "El pago es nulo absolutamente.",
        ],
        "B",
        "Es la B porque el art. 1470 n.° 2 incluye entre las obligaciones naturales las "
        "civiles extinguidas por la prescripción. Para retener, el pago debe hacerse "
        "voluntariamente por el que tenía la libre administración de sus bienes (art. 1470 "
        "inc. final). La A no, porque no hay pago de lo no debido: existía una obligación "
        "natural. La C no, porque no hay restitución parcial. La D no, porque el pago es "
        "válido.",
        f"{CC}, art. 1470 n.° 2; {UC}, V, cap. II, 1.2.3",
    ),
    (
        "Obligaciones de dar, hacer y no hacer",
        1,
        "Un pintor se obliga a pintar un retrato. ¿Qué clase de obligación es?",
        [
            "De dar.",
            "De hacer.",
            "De no hacer.",
            "Natural.",
        ],
        "B",
        "Es la B porque la prestación consiste en ejecutar un hecho distinto de la entrega o "
        "tradición de una cosa. La A no, porque la obligación de dar tiene por objeto "
        "transferir el dominio o constituir un derecho real. La C no, porque la de no hacer "
        "consiste en abstenerse de un hecho. La D no, porque nada indica que carezca de "
        "acción; es una obligación civil.",
        f"{CC}, arts. 1460, 1553 y 1555; {UC}, V, cap. II, 2",
    ),
    (
        "Obligaciones de dar, hacer y no hacer",
        2,
        "Un deudor se obligó a no construir un muro y lo construyó. Si la destrucción del "
        "muro es necesaria para el objeto que se tuvo en mira al contratar, ¿qué puede pedir "
        "el acreedor?",
        [
            "Solo una indemnización de perjuicios.",
            "Que el deudor sea obligado a destruir el muro o que se le autorice para hacerlo "
            "destruir a expensas del deudor.",
            "Que se encarcele al deudor.",
            "Nada, porque el muro ya existe.",
        ],
        "B",
        "Es la B porque el art. 1555 dispone que, si puede destruirse la cosa hecha y su "
        "destrucción es necesaria para el objeto que se tuvo en mira al contratar, el deudor "
        "será obligado a ella o el acreedor autorizado para llevarla a efecto a expensas del "
        "deudor. Si no es necesaria, solo se debe la indemnización. La A no, porque aquí la "
        "destrucción sí procede. La C no, porque no existe prisión por deudas civiles. La D "
        "no, porque la ley da remedios al acreedor.",
        f"{CC}, art. 1555; {UC}, V, cap. II, 2.3",
    ),
    (
        "Obligaciones conjuntas y solidaridad",
        1,
        "Tres personas deben $300 a un acreedor, sin que se haya pactado solidaridad. "
        "¿Cuánto puede cobrar el acreedor a cada una?",
        [
            "$300 a cualquiera de ellas.",
            "$100 a cada una, porque la obligación es simplemente conjunta.",
            "$300 a la que tenga más bienes.",
            "Nada, mientras no se haga la partición.",
        ],
        "B",
        "Es la B porque, en general, cuando hay varios deudores de una cosa divisible, cada "
        "uno es obligado solamente a su parte o cuota (art. 1511 inc. 1). La solidaridad no "
        "se presume: debe ser expresamente declarada en los casos en que no la establece la "
        "ley (art. 1511 inc. 3). La A no, porque eso supondría solidaridad. La C no, porque "
        "no hay tal regla. La D no, porque la obligación es exigible y no hay partición que "
        "hacer.",
        f"{CC}, art. 1511; {UC}, V, cap. II, 3.1",
    ),
    (
        "Obligaciones conjuntas y solidaridad",
        2,
        "¿Cuáles son las fuentes de la solidaridad según el art. 1511?",
        [
            "Solo la ley.",
            "La convención, el testamento o la ley.",
            "La costumbre mercantil.",
            "La sentencia judicial, exclusivamente.",
        ],
        "B",
        "Es la B porque el art. 1511 inc. 2 dispone que, en virtud de la convención, del "
        "testamento o de la ley, puede exigirse a cada uno de los deudores o por cada uno de "
        "los acreedores el total de la deuda. La A no, porque también la convención y el "
        "testamento la generan; un ejemplo legal es el art. 2317. La C no, porque la "
        "costumbre no figura entre las fuentes. La D no, porque la sentencia no es fuente de "
        "la solidaridad.",
        f"{CC}, arts. 1511 y 2317; {UC}, V, cap. II, 3.2",
    ),
    (
        "Efectos de la solidaridad pasiva",
        2,
        "El acreedor de una deuda solidaria cobra el total a uno de los tres codeudores, que "
        "paga. Si la deuda interesaba a los tres por igual, ¿qué puede hacer el que pagó?",
        [
            "Nada: pierde lo pagado.",
            "Cobrar el total a cualquiera de los otros dos.",
            "Dirigirse contra los otros codeudores, pero solo por la parte o cuota que a cada "
            "uno corresponde en la deuda, subrogándose en la acción del acreedor.",
            "Pedir la nulidad del pago.",
        ],
        "C",
        "Es la C porque el art. 1522 dispone que el deudor solidario que ha pagado la deuda "
        "queda subrogado en la acción del acreedor, pero limitada respecto de cada uno de los "
        "codeudores a la parte o cuota que tenga este codeudor en la deuda: la solidaridad no "
        "sigue entre ellos. La A no, porque la ley le da acción. La B no, porque entre los "
        "codeudores la deuda se divide. La D no, porque el pago fue válido.",
        f"{CC}, arts. 1514, 1522 y 1610 n.° 3; {UC}, V, cap. II, 3.2.3.5.2",
    ),
    (
        "Efectos de la solidaridad pasiva",
        3,
        "Muere uno de los deudores solidarios y deja dos herederos. ¿Cómo responden estos "
        "frente al acreedor?",
        [
            "Cada heredero responde del total de la deuda, porque la solidaridad se transmite "
            "íntegramente.",
            "Los herederos, en conjunto, responden del total de la deuda, pero cada uno solo "
            "a prorrata de su cuota hereditaria.",
            "No responden, porque la solidaridad se extingue con la muerte.",
            "Responde solo el heredero mayor.",
        ],
        "B",
        "Es la B porque el art. 1523 dispone que los herederos de cada uno de los deudores "
        "solidarios son, entre todos, obligados al total de la deuda, pero cada heredero solo "
        "es responsable de aquella cuota de la deuda que corresponda a su porción "
        "hereditaria. La A no, porque la solidaridad no pasa individualmente a cada "
        "heredero. La C no, porque la deuda no se extingue y sigue siendo de los herederos. "
        "La D no, porque no hay tal preferencia.",
        f"{CC}, art. 1523; {UC}, V, cap. II, 3.2.3.6.2",
    ),
    (
        "Obligaciones indivisibles",
        2,
        "Dos personas se obligan a constituir una servidumbre de tránsito. ¿Cómo responden?",
        [
            "Cada una solo por la mitad, porque la obligación se divide.",
            "Cada una es obligada a satisfacerla en su totalidad, porque la obligación es "
            "indivisible.",
            "Solo responde la que firmó primero.",
            "No responden, porque las servidumbres no pueden ser objeto de obligaciones.",
        ],
        "B",
        "Es la B porque la obligación de constituir una servidumbre es indivisible (el art. "
        "1524 da justamente ese ejemplo) y, según el art. 1527, cada uno de los que han "
        "contraído unidamente una obligación indivisible es obligado a satisfacerla en el "
        "todo. La A no, porque la división no es posible. La C no, porque no existe esa "
        "regla. La D no, porque la constitución de una servidumbre sí puede ser objeto de una "
        "obligación.",
        f"{CC}, arts. 1524 y 1527; {UC}, V, cap. II, 3.3",
    ),
    (
        "Obligaciones indivisibles",
        3,
        "Una obligación indivisible no se cumple y el acreedor demanda la indemnización de "
        "perjuicios. ¿Cómo responden los codeudores de esa indemnización?",
        [
            "Por el total cada uno, porque la indivisibilidad se extiende a la indemnización.",
            "A prorrata, porque la acción de perjuicios que resulta del incumplimiento de una "
            "obligación indivisible es divisible; solo el codeudor culpable responde de todo "
            "el perjuicio que su hecho cause.",
            "No responden, porque la indivisibilidad extingue la indemnización.",
            "Solo responde el que tenga más bienes.",
        ],
        "B",
        "Es la B porque el art. 1533 dispone que es divisible la acción de perjuicios que "
        "resulta de no haberse cumplido o de haberse retardado la obligación indivisible: "
        "ninguno de los deudores es responsable sino de su cuota, salvo aquel por cuyo hecho "
        "o culpa se hizo imposible el cumplimiento. La A no, porque la indemnización, que es "
        "dinero, se divide. La C no, porque sí se deben perjuicios. La D no, porque no existe "
        "esa regla.",
        f"{CC}, art. 1533; {UC}, V, cap. II, 3.3.2.2.5",
    ),
    (
        "Obligaciones a plazo",
        2,
        "Un deudor tiene un plazo de un año para pagar, pero durante ese año cae en un "
        "procedimiento concursal de liquidación. ¿Qué pasa con el plazo?",
        [
            "Se mantiene, porque el plazo es un derecho del deudor.",
            "Caduca, y el acreedor puede exigir el pago antes de su vencimiento.",
            "Se duplica para proteger al deudor.",
            "Se suspende hasta que el deudor salga de la liquidación.",
        ],
        "B",
        "Es la B porque el art. 1496 dispone que el pago de la obligación no puede exigirse "
        "antes de expirar el plazo, salvo al deudor constituido en liquidación o que se "
        "encuentre en notoria insolvencia, y al deudor cuyas cauciones, por hecho o culpa "
        "suya, se han extinguido o disminuido considerablemente de valor. La A no, porque la "
        "ley prevé la caducidad. La C no, porque no existe esa regla. La D no, porque la "
        "liquidación hace exigibles las deudas.",
        f"{CC}, art. 1496; {UC}, V, cap. II, 4.2.4.3",
    ),
    (
        "Obligaciones a plazo",
        3,
        "Un deudor debe pagar en seis meses un préstamo de dinero con intereses y quiere "
        "pagar antes. ¿Puede renunciar al plazo?",
        [
            "Sí, siempre, porque el plazo está establecido solo en su favor.",
            "No, nunca puede renunciar a un plazo.",
            "Puede renunciar, salvo que el testador o las partes lo hayan prohibido, o que la "
            "anticipación cause perjuicio al acreedor que por medio del plazo se propuso "
            "manifiestamente evitar; en el mutuo con interés rige lo dispuesto en su regla "
            "especial.",
            "Puede renunciar solo si paga el doble.",
        ],
        "C",
        "Es la C porque el art. 1497 permite al deudor renunciar al plazo, salvo esas "
        "excepciones, y agrega que en el mutuo a interés se observará lo dispuesto en el art. "
        "2204 (para las operaciones de crédito de dinero rige, además, la Ley 18.010). El "
        "plazo con intereses beneficia también al acreedor. La A no, porque el plazo no "
        "siempre está solo en su favor. La B no, porque la regla general es que puede "
        "renunciar. La D no, porque no existe tal sanción.",
        f"{CC}, arts. 1497 y 2204; Ley 18.010; {UC}, V, cap. II, 4.2.4.2",
    ),
    (
        "Obligaciones condicionales",
        1,
        "¿Qué es una condición?",
        [
            "Un hecho futuro y cierto del que depende el ejercicio de un derecho.",
            "Un hecho futuro e incierto del cual depende el nacimiento o la extinción de un "
            "derecho.",
            "Una carga impuesta al beneficiario de una liberalidad.",
            "Un hecho pasado que las partes ignoran.",
        ],
        "B",
        "Es la B porque la condición es un acontecimiento futuro que puede suceder o no "
        "(arts. 1473 y 1479): si suspende la adquisición del derecho es suspensiva; si "
        "extingue el derecho, resolutoria. La A no, porque esa es la definición de plazo "
        "(art. 1494). La C no, porque esa es el modo (art. 1089). La D no, porque el hecho "
        "debe ser futuro: si ya ocurrió, no hay propiamente condición (art. 1071).",
        f"{CC}, arts. 1071, 1089, 1473, 1479 y 1494; {UC}, V, cap. II, 4.3",
    ),
    (
        "Obligaciones condicionales",
        3,
        "En un contrato se pacta: «te pagaré $1.000.000 si yo quiero». ¿Qué valor tiene "
        "esta obligación?",
        [
            "Es válida: es una condición potestativa simple.",
            "Es nula, porque es una condición meramente potestativa que depende de la sola "
            "voluntad del deudor.",
            "Es válida pero inoponible a terceros.",
            "Se convierte en obligación pura y simple.",
        ],
        "B",
        "Es la B porque el art. 1478 inc. 1 declara nulas las obligaciones contraídas bajo "
        "una condición potestativa que consista en la mera voluntad de la persona que se "
        "obliga: no hay verdadero vínculo. En cambio, la que depende de un hecho voluntario "
        "del deudor (por ejemplo, «si viajo a Santiago») vale. La A no, porque es meramente "
        "potestativa del deudor. La C no, porque el problema es de validez, no de "
        "oponibilidad. La D no, porque la ley no la transforma: la anula.",
        f"{CC}, arts. 1477 y 1478; {UC}, V, cap. II, 4.3.3.6",
    ),
    (
        "Condición resolutoria tácita y pacto comisorio",
        2,
        "En una compraventa, el comprador no paga el precio. Sin cláusula especial, ¿qué "
        "puede pedir el vendedor?",
        [
            "Solo el cumplimiento, porque no se pactó nada sobre resolución.",
            "A su arbitrio, la resolución o el cumplimiento del contrato, con indemnización "
            "de perjuicios.",
            "Solo una indemnización, sin poder pedir el cumplimiento.",
            "La nulidad del contrato.",
        ],
        "B",
        "Es la B porque el art. 1489 dispone que en los contratos bilaterales va envuelta la "
        "condición resolutoria de no cumplirse por uno de los contratantes lo pactado, y en "
        "tal caso el otro puede pedir a su arbitrio o la resolución o el cumplimiento del "
        "contrato, con indemnización de perjuicios; el art. 1873 lo repite para la "
        "compraventa. La A no, porque la condición resolutoria tácita no necesita pacto. La C "
        "no, porque el acreedor puede pedir el cumplimiento. La D no, porque el "
        "incumplimiento no es causal de nulidad.",
        f"{CC}, arts. 1489 y 1873; {UC}, V, cap. II, 4.3.5.4.2",
    ),
    (
        "Condición resolutoria tácita y pacto comisorio",
        3,
        "En una compraventa se pactó que, si el comprador no paga el precio en el plazo, el "
        "contrato se resolverá ipso facto. El vendedor demanda. ¿Qué puede hacer el comprador?",
        [
            "Nada: el contrato ya está resuelto de pleno derecho.",
            "Hacerlo subsistir pagando el precio, lo más tarde, en las veinticuatro horas "
            "subsiguientes a la notificación judicial de la demanda.",
            "Pagar dentro de los treinta días siguientes a la sentencia.",
            "Pedir la nulidad del pacto.",
        ],
        "B",
        "Es la B porque es la regla del pacto comisorio calificado en la compraventa por no "
        "pago del precio (art. 1879). La A no, porque, pese a la cláusula, la ley concede ese "
        "plazo para enervar la resolución. La C no, porque el plazo es de veinticuatro horas "
        "desde la notificación de la demanda. La D no, porque el pacto es válido.",
        f"{CC}, arts. 1877, 1879 y 1880; {UC}, V, cap. II, 4.3.5.4.3",
    ),
    (
        "El pago",
        1,
        "¿Puede pagar una deuda un tercero ajeno a la obligación?",
        [
            "No, solo puede pagar el deudor.",
            "Sí, cualquier persona puede pagar a nombre del deudor, aun sin su conocimiento o "
            "contra su voluntad, y aun a pesar del acreedor.",
            "Solo si el acreedor lo autoriza por escrito.",
            "Solo los parientes del deudor.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 1572 inc. 1; la excepción son las "
        "obligaciones de hacer en que se ha tomado en consideración la aptitud o talento del "
        "deudor (art. 1572 inc. 2). La A no, porque la ley admite el pago por terceros. La C "
        "no, porque el pago puede hacerse aun contra la voluntad del acreedor. La D no, "
        "porque la ley no limita el pago a los parientes.",
        f"{CC}, arts. 1568 y 1572; {UC}, V, cap. III, 2.2.2",
    ),
    (
        "El pago",
        2,
        "Un deudor debe capital e intereses y hace un pago que no alcanza para todo. Si no "
        "hay acuerdo, ¿a qué se imputa el pago?",
        [
            "Primero al capital.",
            "Primero a los intereses, salvo que el acreedor consienta expresamente que se "
            "impute al capital.",
            "A prorrata entre capital e intereses.",
            "A lo que elija libremente el deudor, sin límite alguno.",
        ],
        "B",
        "Es la B porque el art. 1595 inc. 1 dispone que, si se deben capital e intereses, el "
        "pago se imputará primeramente a los intereses, salvo que el acreedor consienta "
        "expresamente que se impute al capital. La A no, porque invierte la regla. La C no, "
        "porque la ley no prevé un reparto proporcional. La D no, porque el deudor no puede "
        "imputar al capital sin consentimiento del acreedor.",
        f"{CC}, arts. 1595 y 1596; {UC}, V, cap. III, 2.2.8",
    ),
    (
        "Dación en pago y novación",
        2,
        "El deudor y el acreedor acuerdan sustituir una deuda por otra nueva, pero no "
        "manifiestan intención de extinguir la primera. ¿Qué ocurre?",
        [
            "Hay novación igual, porque la nueva obligación siempre extingue la anterior.",
            "No hay novación: se miran las dos obligaciones como coexistentes, valiendo la "
            "obligación primitiva en todo aquello en que la posterior no se opusiere a ella.",
            "Ambas obligaciones se extinguen.",
            "La segunda obligación es nula.",
        ],
        "B",
        "Es la B porque el art. 1634 exige que las partes manifiesten su intención de novar "
        "(animus novandi) o que aparezca indudablemente que su intención ha sido novar; si "
        "no, ambas obligaciones coexisten. La A no, porque la novación no se presume. La C "
        "no, porque no hay causa de extinción de ambas. La D no, porque la segunda obligación "
        "es válida.",
        f"{CC}, arts. 1628 y 1634; {UC}, V, cap. III, 2.4",
    ),
    (
        "Dación en pago y novación",
        3,
        "El acreedor acepta voluntariamente del deudor principal, en pago de la deuda, un "
        "auto en lugar del dinero adeudado. ¿Qué efecto tiene esa dación en pago sobre la "
        "fianza que garantizaba la deuda?",
        [
            "Ninguno: la fianza sigue vigente.",
            "La fianza se extingue irrevocablemente, aunque después sobrevenga evicción del "
            "objeto.",
            "La fianza se transforma en hipoteca.",
            "La fianza solo se extingue si el fiador lo pide judicialmente.",
        ],
        "B",
        "Es la B porque el art. 2382 dispone que, si el acreedor acepta voluntariamente del "
        "deudor principal, en descargo de la deuda, un objeto distinto del que este deba "
        "darle en pago, queda irrevocablemente extinguida la fianza, aunque después sobrevenga "
        "evicción del objeto. Es una de las pocas normas que aluden a la dación en pago, que "
        "el Código no regula en general. La A no, porque la ley extingue la fianza. La C no, "
        "porque no hay tal transformación. La D no, porque la extinción opera por la sola "
        "aceptación.",
        f"{CC}, art. 2382; {UC}, V, cap. III, 2.3",
    ),
    (
        "Compensación y prescripción extintiva",
        2,
        "¿Qué requisitos deben reunir dos deudas para que opere la compensación legal?",
        [
            "Que ambas consten en escritura pública.",
            "Que ambas sean de dinero o de cosas fungibles o indeterminadas de igual género y "
            "calidad, que ambas sean líquidas y que ambas sean actualmente exigibles; además, "
            "las partes deben ser recíprocamente deudoras.",
            "Que el juez la declare de oficio.",
            "Que ambas deudas sean del mismo monto exacto.",
        ],
        "B",
        "Es la B porque esos son los requisitos de los arts. 1656 y 1657; la compensación "
        "opera por el solo ministerio de la ley, aun sin conocimiento de los deudores, hasta "
        "la concurrencia de sus valores (aunque debe alegarse, art. 1660). La A no, porque no "
        "se exige forma alguna. La C no, porque el juez no la declara de oficio. La D no, "
        "porque las deudas se extinguen hasta la concurrencia de la menor.",
        f"{CC}, arts. 1655 a 1657 y 1660; {UC}, V, cap. III, 2.5",
    ),
    (
        "Compensación y prescripción extintiva",
        2,
        "¿En qué plazo prescriben, como regla general, las acciones ejecutivas y las ordinarias?",
        [
            "Ejecutivas: 5 años; ordinarias: 10 años.",
            "Ejecutivas: 3 años; ordinarias: 5 años. La acción ejecutiva se convierte en "
            "ordinaria por el lapso de 3 años y, convertida en ordinaria, dura solamente "
            "otros 2.",
            "Ambas en 1 año.",
            "No prescriben nunca.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 2515; el tiempo se cuenta desde que la "
        "obligación se haya hecho exigible (art. 2514). La A no, porque esos plazos no son "
        "los vigentes. La C no, porque un año es plazo de ciertas prescripciones de corto "
        "tiempo (art. 2522). La D no, porque las acciones sí prescriben, por regla general.",
        f"{CC}, arts. 2514 y 2515; {UC}, V, cap. III, 2.7",
    ),
    (
        "Incumplimiento y cumplimiento forzado",
        2,
        "Un pintor famoso se obligó a pintar un retrato y se niega. Además de la "
        "indemnización, ¿qué puede pedir el acreedor según el art. 1553?",
        [
            "Solo la indemnización: nunca puede exigirse el hecho.",
            "Que se apremie al deudor para la ejecución del hecho convenido, o que se le "
            "autorice para hacerlo ejecutar por un tercero a expensas del deudor; o la "
            "indemnización de perjuicios.",
            "Que el pintor sea encarcelado por diez días.",
            "La nulidad del contrato.",
        ],
        "B",
        "Es la B porque el art. 1553 da al acreedor de una obligación de hacer, si el deudor "
        "se constituye en mora, esas tres opciones, a su elección. Cuando lo que importa es "
        "el talento del deudor, la ejecución por un tercero no satisface al acreedor y le "
        "quedan el apremio o la indemnización. La A no, porque la ley sí permite exigir el "
        "hecho. La C no, porque el apremio no es una pena fija de cárcel. La D no, porque el "
        "incumplimiento no anula el contrato.",
        f"{CC}, art. 1553; {UC}, V, cap. IV, 5.2",
    ),
    (
        "Incumplimiento y cumplimiento forzado",
        3,
        "En un contrato bilateral, el comprador demanda al vendedor por no entregar la cosa, "
        "pero él tampoco ha pagado ni se ha allanado a pagar. ¿Qué puede oponer el vendedor?",
        [
            "Nada: debe cumplir primero.",
            "La excepción de contrato no cumplido: ninguno de los contratantes está en mora "
            "dejando de cumplir lo pactado mientras el otro no lo cumple por su parte o no se "
            "allana a cumplirlo en la forma y tiempo debidos.",
            "La nulidad del contrato.",
            "La prescripción, siempre.",
        ],
        "B",
        "Es la B porque esa regla, que la doctrina llama excepción de contrato no cumplido "
        "(«la mora purga la mora»), está en el art. 1552. La A no, porque la ley lo protege. "
        "La C no, porque el incumplimiento no es causal de nulidad. La D no, porque la "
        "prescripción depende del tiempo transcurrido y nada indica que haya operado.",
        f"{CC}, arts. 1489 y 1552; {UC}, V, cap. IV, 4",
    ),
    (
        "Resolución del contrato y terceros",
        2,
        "El comprador de un auto no pagó el precio y, antes de que se declare la "
        "resolución, vendió el auto a un tercero de buena fe. Declarada la resolución, "
        "¿puede el vendedor original recuperar el auto de manos del tercero?",
        [
            "Sí, siempre, porque la resolución opera retroactivamente contra todos.",
            "No, porque, tratándose de muebles, la resolución no da derecho contra terceros "
            "poseedores de buena fe.",
            "Sí, pero solo si el tercero no ha pagado.",
            "No, porque la resolución nunca afecta a los muebles.",
        ],
        "B",
        "Es la B porque el art. 1490 dispone que si el que debe una cosa mueble bajo "
        "condición la enajena, no habrá derecho de reivindicarla contra terceros poseedores "
        "de buena fe; los arts. 1490 y 1491 se aplican a la condición resolutoria tácita. La "
        "A no, porque la ley protege a los terceros de buena fe. La C no, porque el pago del "
        "tercero no es el criterio legal. La D no, porque el art. 1490 sí permite reivindicar "
        "contra terceros de mala fe.",
        f"{CC}, arts. 1487, 1490 y 1491; {UC}, V, cap. IV, 6.2",
    ),
    (
        "Resolución del contrato y terceros",
        3,
        "En la compraventa de un inmueble, la escritura pública dice que el precio queda "
        "adeudado. El comprador vende a un tercero y luego se resuelve la primera venta por "
        "no pago. ¿Afecta la resolución al tercero?",
        [
            "No, porque el tercero inscribió a su nombre.",
            "Sí, porque la condición constaba en el título respectivo, inscrito u otorgado "
            "por escritura pública: el saldo de precio adeudado indica que la obligación "
            "estaba pendiente.",
            "Solo si el tercero era pariente del comprador.",
            "No, porque la resolución solo produce efectos entre las partes.",
        ],
        "B",
        "Es la B porque el art. 1491 permite resolver las enajenaciones de inmuebles cuando "
        "la condición constaba en el título respectivo, inscrito u otorgado por escritura "
        "pública; la jurisprudencia entiende que consta la condición resolutoria tácita "
        "cuando la escritura deja constancia de un saldo de precio adeudado. La A no, porque "
        "la inscripción no lo protege si la condición constaba. La C no, porque no existe esa "
        "regla. La D no, porque la ley prevé efectos contra terceros.",
        f"{CC}, arts. 1489 y 1491; {UC}, V, cap. IV, 6.2.3.3",
    ),
    (
        "Indemnización de perjuicios: requisitos, dolo y culpa",
        2,
        "En un contrato que beneficia a ambas partes (como la compraventa), ¿de qué grado de "
        "culpa responde el deudor?",
        [
            "De culpa grave o lata.",
            "De culpa leve.",
            "De culpa levísima.",
            "Solo de dolo.",
        ],
        "B",
        "Es la B porque el art. 1547 dispone que el deudor responde de culpa leve en los "
        "contratos que se hacen para beneficio recíproco de las partes; de culpa lata en los "
        "que solo son útiles al acreedor; y de culpa levísima en los que el deudor es el "
        "único que reporta beneficio. La A no, porque la lata corresponde a los contratos "
        "útiles solo al acreedor, como el depósito. La C no, porque la levísima corresponde a "
        "los que benefician solo al deudor, como el comodato. La D no, porque el deudor "
        "responde de su culpa, no solo del dolo.",
        f"{CC}, arts. 44 y 1547; {UC}, V, cap. IV, 7.4.3.2",
    ),
    (
        "Indemnización de perjuicios: requisitos, dolo y culpa",
        3,
        "Un vendedor incumple dolosamente el contrato. ¿De qué perjuicios responde?",
        [
            "Solo de los previstos o que pudieron preverse al tiempo del contrato.",
            "De todos los perjuicios que fueron consecuencia inmediata o directa de no "
            "haberse cumplido la obligación, aunque no se hayan previsto.",
            "Solo del daño emergente, nunca del lucro cesante.",
            "De todos los perjuicios, incluidos los indirectos.",
        ],
        "B",
        "Es la B porque el art. 1558 dispone que, si no se puede imputar dolo al deudor, "
        "solo es responsable de los perjuicios que se previeron o pudieron preverse al tiempo "
        "del contrato; pero si hay dolo, responde de todos los que fueron consecuencia "
        "inmediata o directa del incumplimiento. La A no, porque esa es la regla del deudor "
        "culpable. La C no, porque la indemnización comprende el daño emergente y el lucro "
        "cesante (art. 1556). La D no, porque aun con dolo no se indemnizan los perjuicios "
        "indirectos.",
        f"{CC}, arts. 1556 y 1558; {UC}, V, cap. IV, 7.5.1.3",
    ),
    (
        "La mora",
        2,
        "Un contrato fija un plazo para pagar y el deudor no paga al vencimiento. ¿Cuándo "
        "queda en mora?",
        [
            "Solo cuando el acreedor lo demande judicialmente.",
            "Cuando no ha cumplido la obligación dentro del término estipulado, salvo que la "
            "ley en casos especiales exija que se requiera al deudor para constituirlo en "
            "mora.",
            "Cuando el acreedor le envíe una carta certificada.",
            "Nunca, mientras el acreedor no pruebe perjuicios.",
        ],
        "B",
        "Es la B porque el art. 1551 n.° 1 dispone que el deudor está en mora cuando no ha "
        "cumplido la obligación dentro del término estipulado (interpelación contractual "
        "expresa); los otros casos son cuando la cosa no ha podido ser dada sino dentro de "
        "cierto tiempo y el deudor lo ha dejado pasar, y, en los demás casos, cuando el "
        "deudor ha sido judicialmente reconvenido. La A no, porque la reconvención judicial "
        "solo es necesaria a falta de plazo. La C no, porque una carta no es la forma legal. "
        "La D no, porque la mora no depende de la prueba de perjuicios.",
        f"{CC}, art. 1551; {UC}, V, cap. IV, 7.4.5",
    ),
    (
        "La mora",
        3,
        "Un deudor en mora de entregar un caballo no lo entrega y el caballo muere por un "
        "caso fortuito que también lo habría matado en poder del acreedor. ¿Responde el "
        "deudor?",
        [
            "Sí, siempre, porque estaba en mora.",
            "No, porque el caso fortuito habría dañado igualmente la cosa si hubiese sido "
            "entregada al acreedor.",
            "Sí, pero solo por la mitad del valor.",
            "No, porque la mora del deudor extingue la obligación.",
        ],
        "B",
        "Es la B porque el art. 1547 inc. 2 dispone que el deudor no es responsable del caso "
        "fortuito, a menos que se haya constituido en mora siendo el caso fortuito de "
        "aquellos que no hubieran dañado a la cosa debida si hubiese sido entregada al "
        "acreedor (en el mismo sentido, art. 1672). Aquí el caso fortuito habría ocurrido "
        "igual. La A no, porque la mora no basta si el daño era inevitable. La C no, porque "
        "no hay tal regla. La D no, porque la mora no extingue la obligación.",
        f"{CC}, arts. 1547, 1550 y 1672; {UC}, V, cap. IV, 7.4.5.3",
    ),
    (
        "Avaluación de perjuicios y cláusula penal",
        2,
        "Un contrato tiene una cláusula penal. El deudor incumple. ¿Debe el acreedor probar "
        "que sufrió perjuicios para cobrar la pena?",
        [
            "Sí, siempre.",
            "No: habrá lugar a exigir la pena en todos los casos en que se hubiere "
            "estipulado, sin que pueda alegarse por el deudor que la inejecución de lo "
            "pactado no ha inferido perjuicio al acreedor o le ha producido beneficio.",
            "Solo si el contrato consta en escritura pública.",
            "Sí, y además debe probar dolo.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 1542: la cláusula penal es una avaluación "
        "anticipada y convencional de los perjuicios. La A no, porque esa es justamente la "
        "ventaja de la cláusula penal. La C no, porque no requiere forma especial. La D no, "
        "porque no es necesario probar dolo.",
        f"{CC}, arts. 1535 y 1542; {UC}, V, cap. IV, 7.5.3",
    ),
    (
        "Avaluación de perjuicios y cláusula penal",
        3,
        "Un acreedor quiere cobrar a la vez la obligación principal y la pena. ¿Puede hacerlo?",
        [
            "Sí, siempre.",
            "No, salvo que aparezca haberse estipulado la pena por el simple retardo, o que "
            "se haya estipulado que por el pago de la pena no se entiende extinguida la "
            "obligación principal.",
            "Solo si el deudor lo autoriza después del incumplimiento.",
            "No, nunca.",
        ],
        "B",
        "Es la B porque el art. 1537 dispone que, antes de constituirse el deudor en mora, "
        "el acreedor no puede demandar a su arbitrio la obligación principal o la pena, sino "
        "solo la principal; constituido en mora, puede pedir una u otra, pero no ambas, con "
        "esas dos excepciones. La A no, porque la acumulación es excepcional. La C no, porque "
        "las excepciones son las del art. 1537. La D no, porque hay casos en que sí procede.",
        f"{CC}, art. 1537; {UC}, V, cap. IV, 7.5.3",
    ),
    (
        "Derechos auxiliares del acreedor y prelación de créditos",
        2,
        "Un deudor insolvente dona su único inmueble a un amigo para que sus acreedores no "
        "puedan embargarlo. ¿Qué acción tienen los acreedores?",
        [
            "Ninguna: el deudor puede disponer libremente de sus bienes.",
            "La acción pauliana o revocatoria: tratándose de un acto gratuito, basta la mala "
            "fe del deudor y el perjuicio de los acreedores.",
            "La acción reivindicatoria, porque los acreedores son dueños del inmueble.",
            "La acción de petición de herencia.",
        ],
        "B",
        "Es la B porque el art. 2468 n.° 2 permite rescindir los actos y contratos no "
        "comprendidos en el n.° 1 (que trata los onerosos) probándose la mala fe del deudor y "
        "el perjuicio de los acreedores; en los onerosos se exige además la mala fe del "
        "adquirente. La acción prescribe en un año contado desde la fecha del acto (art. 2468 "
        "n.° 3). La A no, porque el derecho de prenda general (art. 2465) protege a los "
        "acreedores frente a actos fraudulentos. La C no, porque los acreedores no son "
        "dueños. La D no, porque no hay herencia de por medio.",
        f"{CC}, arts. 2465 y 2468; {UC}, V, cap. IV, 8.1",
    ),
    (
        "Derechos auxiliares del acreedor y prelación de créditos",
        3,
        "En la prelación de créditos, ¿cómo se pagan los créditos de la quinta clase (valistas)?",
        [
            "Antes que todos los demás.",
            "A prorrata sobre el sobrante de la masa concursable, sin consideración a su "
            "fecha, después de pagados los créditos preferentes.",
            "Por orden de antigüedad, del más antiguo al más reciente.",
            "No se pagan nunca.",
        ],
        "B",
        "Es la B porque el art. 2489 dispone que la quinta y última clase comprende los "
        "créditos que no gozan de preferencia, y que se cubren a prorrata sobre el sobrante "
        "de la masa concursable, sin consideración a su fecha. La A no, porque se pagan en "
        "último lugar. La C no, porque no se atiende a la fecha. La D no, porque se pagan con "
        "lo que quede.",
        f"{CC}, arts. 2470, 2471 y 2489; {UC}, V, cap. IV, 8.3",
    ),
    # --------------------------------------- VI. Responsabilidad extracontractual
    (
        "Responsabilidad extracontractual: concepto y requisitos",
        1,
        "¿Qué diferencia hay entre un delito y un cuasidelito civil?",
        [
            "El delito causa daño y el cuasidelito no.",
            "El delito es un hecho ilícito cometido con intención de dañar; el cuasidelito, "
            "un hecho culpable cometido sin intención de dañar.",
            "El delito siempre es penal y el cuasidelito siempre es civil.",
            "No hay diferencia en cuanto a su definición.",
        ],
        "B",
        "Es la B porque así los distingue el art. 2284 inc. final. En materia civil, ambos "
        "obligan a indemnizar el daño (art. 2314). La A no, porque ambos suponen un daño "
        "indemnizable. La C no, porque ambos son categorías civiles, independientes de la "
        "responsabilidad penal. La D no, porque se distinguen por la intención.",
        f"{CC}, arts. 2284 y 2314; {UC}, VI, cap. I, 1",
    ),
    (
        "Responsabilidad extracontractual: concepto y requisitos",
        2,
        "¿Cuáles son los requisitos de la responsabilidad extracontractual por el hecho propio?",
        [
            "Contrato, incumplimiento y mora.",
            "Una acción u omisión, dolo o culpa, daño, relación de causalidad entre el hecho "
            "y el daño, y capacidad del autor.",
            "Solo el daño.",
            "Solo la culpa.",
        ],
        "B",
        "Es la B porque esos son los requisitos que la doctrina extrae de los arts. 2314, "
        "2319 y 2329. La A no, porque esos son elementos de la responsabilidad contractual. "
        "La C no, porque no basta el daño: el régimen general es de responsabilidad por "
        "culpa. La D no, porque la culpa sin daño no genera responsabilidad civil.",
        f"{CC}, arts. 2314, 2319 y 2329; {UC}, VI, cap. I, 5",
    ),
    (
        "El daño y la relación de causalidad",
        2,
        "¿Qué partidas comprende, en general, el daño indemnizable en sede extracontractual?",
        [
            "Solo el daño emergente.",
            "El daño emergente, el lucro cesante y el daño moral.",
            "Solo el daño moral.",
            "Solo los perjuicios previstos al tiempo del hecho.",
        ],
        "B",
        "Es la B porque el art. 2329 ordena reparar «todo daño», lo que comprende el daño "
        "emergente (pérdida efectiva), el lucro cesante (ganancia frustrada) y el daño moral, "
        "que la jurisprudencia indemniza sin discusión en esta sede. La A no, porque la "
        "reparación es integral. La C no, porque también se indemniza el daño patrimonial. La "
        "D no, porque la distinción entre perjuicios previstos e imprevistos es propia de la "
        "responsabilidad contractual (art. 1558).",
        f"{CC}, arts. 1558 y 2329; {UC}, VI, cap. I, 5.2",
    ),
    (
        "El daño y la relación de causalidad",
        3,
        "La víctima de un accidente se expuso imprudentemente al daño (por ejemplo, cruzó "
        "la calle sin mirar). ¿Qué efecto tiene esa conducta?",
        [
            "Ninguno: el autor debe indemnizar todo.",
            "La apreciación del daño está sujeta a reducción.",
            "Exime totalmente al autor en todos los casos.",
            "Obliga a la víctima a indemnizar al autor.",
        ],
        "B",
        "Es la B porque el art. 2330 dispone que la apreciación del daño está sujeta a "
        "reducción si el que lo ha sufrido se expuso a él imprudentemente. La A no, porque la "
        "ley prevé la reducción. La C no, porque la reducción no es una exención total, salvo "
        "que la conducta de la víctima sea la causa exclusiva del daño. La D no, porque no "
        "hay tal inversión.",
        f"{CC}, art. 2330; {UC}, VI, cap. I, 5.3.5",
    ),
    (
        "Capacidad delictual",
        2,
        "Un niño de 6 años rompe con una piedra el vidrio de un auto. ¿Quién responde?",
        [
            "El niño, con sus propios bienes.",
            "Nadie, porque el niño es incapaz de delito o cuasidelito; pero responden las "
            "personas a cuyo cargo esté, si pudiere imputárseles negligencia.",
            "El Estado.",
            "El dueño del auto, por no haberlo cuidado.",
        ],
        "B",
        "Es la B porque el art. 2319 dispone que no son capaces de delito o cuasidelito los "
        "menores de siete años ni los dementes, pero serán responsables de los daños causados "
        "por ellos las personas a cuyo cargo estén, si pudiere imputárseles negligencia. La A "
        "no, porque el niño es incapaz. La C no, porque no hay responsabilidad del Estado. La "
        "D no, porque nada indica una culpa de la víctima.",
        f"{CC}, art. 2319; {UC}, VI, cap. I, 5.5",
    ),
    (
        "Capacidad delictual",
        3,
        "Un adolescente de 15 años causa un daño. ¿Cómo se determina su capacidad delictual?",
        [
            "Es siempre capaz.",
            "Es siempre incapaz.",
            "Queda a la prudencia del juez determinar si ha cometido el delito o cuasidelito "
            "sin discernimiento; si así fuere, se aplica la regla de los incapaces.",
            "Depende de lo que digan sus padres.",
        ],
        "C",
        "Es la C porque el art. 2319 inc. 2 dispone que queda a la prudencia del juez "
        "determinar si el menor de dieciséis años ha cometido el delito o cuasidelito sin "
        "discernimiento. La A no, porque entre los siete y los dieciséis años la capacidad no "
        "se presume de pleno derecho. La B no, porque la incapacidad absoluta es solo de los "
        "menores de siete y los dementes. La D no, porque decide el juez.",
        f"{CC}, art. 2319; {UC}, VI, cap. I, 5.5.1",
    ),
    (
        "Presunciones de responsabilidad",
        2,
        "Un trabajador de una empresa, en el ejercicio de sus funciones, causa un daño a un "
        "tercero. ¿Puede la víctima demandar a la empresa?",
        [
            "No, solo al trabajador.",
            "Sí, porque los empresarios responden del hecho de sus dependientes que estén "
            "bajo su cuidado; la responsabilidad cesa si prueban que, con la autoridad y el "
            "cuidado que su calidad les confiere, no hubieran podido impedir el hecho.",
            "Sí, pero solo si la empresa ordenó causar el daño.",
            "No, porque las personas jurídicas no responden civilmente.",
        ],
        "B",
        "Es la B porque el art. 2320 establece la responsabilidad por el hecho ajeno, entre "
        "otros casos, de los empresarios por el hecho de sus dependientes, con la posibilidad "
        "de liberarse probando que no pudieron impedir el hecho (inc. final); el art. 2322 "
        "contiene una regla similar. La A no, porque la ley permite demandar también al "
        "empresario. La C no, porque basta la presunción de culpa en el cuidado. La D no, "
        "porque las personas jurídicas sí responden.",
        f"{CC}, arts. 2320, 2322 y 2325; {UC}, VI, cap. I, 6.2",
    ),
    (
        "Presunciones de responsabilidad",
        3,
        "Una maceta cae desde un balcón de un edificio y lesiona a un peatón. No se sabe "
        "quién la dejó allí. ¿Quiénes responden según el art. 2328?",
        [
            "Nadie, porque no se identificó al culpable.",
            "Todas las personas que habitan la misma parte del edificio, a prorrata, salvo "
            "que se pruebe que el hecho se debe a la culpa o mala intención de alguna persona "
            "exclusivamente, en cuyo caso será responsable ella sola.",
            "Solo el administrador del edificio.",
            "La municipalidad.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 2328, que regula el daño causado por una cosa "
        "que cae o se arroja de la parte superior de un edificio. La A no, porque la ley "
        "atribuye responsabilidad aunque no se identifique al culpable. La C no, porque la "
        "ley no se dirige al administrador. La D no, porque no responde la municipalidad.",
        f"{CC}, art. 2328; {UC}, VI, cap. I, 6.3",
    ),
    (
        "Acción de responsabilidad extracontractual",
        2,
        "¿En qué plazo prescribe la acción de responsabilidad extracontractual?",
        [
            "En 5 años desde que se demanda.",
            "En 4 años contados desde la perpetración del acto.",
            "En 1 año desde que la víctima conoce al autor.",
            "No prescribe.",
        ],
        "B",
        "Es la B porque el art. 2332 dispone que las acciones que concede este título por "
        "daño o dolo prescriben en cuatro años contados desde la perpetración del acto; la "
        "jurisprudencia y parte de la doctrina discuten si el plazo corre desde el hecho o "
        "desde que se manifiesta el daño. La A no, porque el plazo es de cuatro años. La C "
        "no, porque no hay tal regla. La D no, porque la acción sí prescribe.",
        f"{CC}, art. 2332; {UC}, VI, cap. I, 9",
    ),
    (
        "Acción de responsabilidad extracontractual",
        3,
        "Dos personas cometen juntas un cuasidelito civil. ¿Cómo responden frente a la víctima?",
        [
            "Cada una por la mitad.",
            "Solidariamente: cada una puede ser obligada al total del perjuicio.",
            "Solo responde la que tenga más culpa.",
            "No responden si no hubo intención de dañar.",
        ],
        "B",
        "Es la B porque el art. 2317 dispone que, si un delito o cuasidelito ha sido "
        "cometido por dos o más personas, cada una de ellas será solidariamente responsable "
        "de todo perjuicio procedente del mismo delito o cuasidelito, salvas las excepciones "
        "de los arts. 2323 y 2328. Es un caso de solidaridad legal. La A no, porque la ley "
        "establece solidaridad. La C no, porque ambas responden del total. La D no, porque el "
        "cuasidelito supone culpa, no intención, y genera igualmente responsabilidad.",
        f"{CC}, arts. 2317 y 1511; {UC}, VI, cap. I, 5",
    ),
]
