"""Cédula UC de Derecho Civil, partes VI caps. II y III (Contratos), VII (Familia) y VIII
(Sucesorio)."""

JURISDICCION = "Chile"
PROGRAMA = "Cédulas UC (licenciatura, vigentes desde 2021)"
CEDULA = "Cédula 1: Derecho Civil (15-03-2021)"
MATERIA = "Derecho Civil"

CC = "Código Civil"
LMC = "Ley 19.947 de Matrimonio Civil"
UC = "Cédula UC Derecho Civil"

PREGUNTAS = [
    # ------------------------------------------------- VI. Teoría general del contrato
    (
        "Teoría general del contrato: concepto y elementos",
        1,
        "¿Cómo define el art. 1438 el contrato o convención?",
        [
            "Como el acto por el cual una parte se obliga para con otra a dar, hacer o no "
            "hacer alguna cosa.",
            "Como cualquier acuerdo, aunque no produzca efectos jurídicos.",
            "Como una declaración unilateral de voluntad.",
            "Como la sentencia que obliga a las partes.",
        ],
        "A",
        "Es la A porque es la definición del art. 1438, que agrega que cada parte puede ser "
        "una o muchas personas; la doctrina critica que trate como sinónimos contrato y "
        "convención. La B no, porque el contrato produce obligaciones. La C no, porque el "
        "contrato requiere el acuerdo de dos o más partes. La D no, porque la fuente es la "
        "voluntad de las partes, no una sentencia.",
        f"{CC}, art. 1438; {UC}, VI, cap. II, 1",
    ),
    (
        "Teoría general del contrato: concepto y elementos",
        2,
        "En una compraventa, ¿qué es la obligación de saneamiento según el art. 1444?",
        [
            "Una cosa de la esencia.",
            "Una cosa de la naturaleza: se entiende pertenecer al contrato sin necesidad de "
            "cláusula especial, pero las partes pueden excluirla.",
            "Un elemento accidental, que solo existe si se pacta.",
            "Una solemnidad.",
        ],
        "B",
        "Es la B porque el saneamiento de la evicción y de los vicios redhibitorios se "
        "entiende incorporado a la compraventa, aunque las partes pueden modificarlo o "
        "excluirlo (arts. 1839 y 1859), lo que corresponde a las cosas de la naturaleza del "
        "art. 1444. La A no, porque sin saneamiento el contrato sigue siendo compraventa. La "
        "C no, porque no requiere pacto. La D no, porque no es una formalidad.",
        f"{CC}, arts. 1444, 1839 y 1859; {UC}, VI, cap. II, 3",
    ),
    (
        "Principios y efectos del contrato",
        2,
        "Ana contrata un seguro con una compañía a favor de su hija, que no interviene en "
        "el contrato. ¿Quién puede demandar el pago del seguro?",
        [
            "Solo Ana, porque fue quien contrató.",
            "Solo la hija, como beneficiaria de una estipulación a favor de otro; mientras no "
            "la acepte, Ana y la compañía pueden revocar el contrato.",
            "Cualquier pariente de Ana.",
            "Nadie, porque la hija no firmó.",
        ],
        "B",
        "Es la B porque el art. 1449 permite estipular a favor de un tercero, aunque no se "
        "tenga derecho para representarlo, pero solo el tercero puede demandar lo estipulado; "
        "y mientras no intervenga su aceptación expresa o tácita, el contrato es revocable "
        "por la sola voluntad de las partes. La A no, porque la ley da la acción al tercero. "
        "La C no, porque no hay tal legitimación. La D no, porque es una excepción al efecto "
        "relativo de los contratos.",
        f"{CC}, art. 1449; {UC}, VI, cap. II, 5.2.1",
    ),
    (
        "Principios y efectos del contrato",
        3,
        "Bruno promete a Carla que su hermano le venderá un auto. El hermano se niega. ¿Qué "
        "puede hacer Carla?",
        [
            "Exigir al hermano que venda, porque Bruno lo obligó.",
            "Nada, porque el contrato es nulo.",
            "Demandar perjuicios a Bruno, porque el hermano no ratificó y, por lo tanto, no "
            "contrajo obligación alguna.",
            "Pedir al juez que fije el precio y obligue al hermano.",
        ],
        "C",
        "Es la C porque el art. 1450 regula la promesa de hecho ajeno: el tercero no contrae "
        "obligación alguna sino en virtud de su ratificación, y si no ratifica, el otro "
        "contratante tiene acción de perjuicios contra el que hizo la promesa. La A no, "
        "porque nadie queda obligado por la promesa ajena. La B no, porque la promesa es "
        "válida entre Bruno y Carla. La D no, porque el juez no puede imponer el contrato al "
        "tercero.",
        f"{CC}, art. 1450; {UC}, VI, cap. II, 5.2.2",
    ),
    (
        "Interpretación e integración del contrato",
        2,
        "¿Qué regla da el art. 1560 para interpretar los contratos?",
        [
            "Que prevalece siempre el tenor literal de las palabras.",
            "Que, conocida claramente la intención de los contratantes, debe estarse a ella "
            "más que a lo literal de las palabras.",
            "Que el juez debe aplicar la interpretación más equitativa.",
            "Que prevalece la interpretación que favorezca al acreedor.",
        ],
        "B",
        "Es la B porque el art. 1560 consagra la primacía de la intención común de las "
        "partes, a diferencia del art. 19, que en la interpretación de la ley da primacía al "
        "tenor literal claro. La A no, porque esa es la regla de la ley, no del contrato. La "
        "C no, porque la equidad no es la regla general. La D no, porque las cláusulas "
        "ambiguas se interpretan, en su caso, a favor del deudor (art. 1566).",
        f"{CC}, arts. 19, 1560 y 1566; {UC}, VI, cap. II, 6",
    ),
    (
        "Interpretación e integración del contrato",
        3,
        "Una cláusula ambigua de un contrato de adhesión fue redactada por la empresa "
        "proveedora, que no explicó su sentido. ¿Cómo debe interpretarse?",
        [
            "A favor de la empresa, porque la redactó.",
            "Contra la empresa, porque las cláusulas ambiguas extendidas o dictadas por una "
            "de las partes se interpretan contra ella, si la ambigüedad proviene de la falta "
            "de una explicación que debió dar.",
            "Siempre a favor del acreedor.",
            "Se tiene por no escrita en todo caso.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 1566 inc. 2 (interpretación contra el "
        "redactor o contra proferentem). A falta de otras reglas, las ambiguas se interpretan "
        "a favor del deudor (inc. 1). La A no, porque la ley la interpreta en su contra. La C "
        "no, porque la regla subsidiaria favorece al deudor y, en este caso, rige la regla "
        "contra el redactor. La D no, porque el art. 1566 interpreta la cláusula, no la "
        "elimina.",
        f"{CC}, art. 1566; {UC}, VI, cap. II, 6.1.6",
    ),
    # ------------------------------------------------- VI. Los contratos en particular
    (
        "Contrato de promesa y responsabilidad precontractual",
        2,
        "¿Cuál de estos es un requisito para que la promesa de celebrar un contrato produzca "
        "obligación?",
        [
            "Que conste en escritura pública siempre.",
            "Que conste por escrito, que el contrato prometido no sea de aquellos que las "
            "leyes declaran ineficaces, que contenga un plazo o condición que fije la época de "
            "su celebración y que especifique de tal manera el contrato prometido que solo "
            "falten la tradición de la cosa o las solemnidades.",
            "Que se pague una multa al firmarla.",
            "Que sea aprobada por un juez.",
        ],
        "B",
        "Es la B porque esos son los cuatro requisitos del art. 1554; concurriendo, habrá "
        "lugar a lo prevenido en el art. 1553 (cumplimiento forzado de una obligación de "
        "hacer). La A no, porque basta que conste por escrito, salvo que el contrato "
        "prometido exija otra cosa según la doctrina que se siga. La C no, porque la multa no "
        "es requisito. La D no, porque no requiere aprobación judicial.",
        f"{CC}, arts. 1553 y 1554; {UC}, VI, cap. III, 1.2",
    ),
    (
        "Contrato de promesa y responsabilidad precontractual",
        3,
        "Durante las negociaciones de un contrato, una parte las rompe sin motivo y de mala "
        "fe, después de haber generado en la otra la confianza de que se contrataría. ¿Qué "
        "sostiene la doctrina mayoritaria?",
        [
            "Que nunca hay responsabilidad, porque las partes son libres de no contratar.",
            "Que puede haber responsabilidad precontractual (culpa in contrahendo) por la "
            "infracción de la buena fe, aunque la libertad de no contratar es la regla.",
            "Que el contrato se entiende celebrado.",
            "Que la otra parte puede exigir el cumplimiento forzado del contrato.",
        ],
        "B",
        "Es la B porque la doctrina admite la responsabilidad por la ruptura injustificada y "
        "de mala fe de las tratativas, con apoyo en la buena fe y, en materia mercantil, en el "
        "art. 100 del Código de Comercio (retractación tempestiva). La A no, porque la "
        "libertad de no contratar no autoriza a actuar de mala fe. La C no, porque no hubo "
        "consentimiento. La D no, porque no hay contrato que cumplir.",
        f"{CC}, art. 1546; Código de Comercio, art. 100; {UC}, VI, cap. III, 1.1",
    ),
    (
        "Compraventa: concepto, cosa, precio y solemnidades",
        1,
        "Por regla general, ¿cuándo se reputa perfecta la compraventa?",
        [
            "Cuando se entrega la cosa.",
            "Cuando se paga el precio.",
            "Desde que las partes han convenido en la cosa y en el precio, salvo las "
            "excepciones legales.",
            "Cuando se inscribe en el Conservador de Bienes Raíces.",
        ],
        "C",
        "Es la C porque el art. 1801 inc. 1 dispone que la venta se reputa perfecta desde que "
        "las partes han convenido en la cosa y en el precio; las excepciones del inc. 2 son, "
        "entre otras, la venta de bienes raíces, servidumbres, censos y de una sucesión "
        "hereditaria, que requieren escritura pública. La A no, porque la compraventa es "
        "consensual, no real. La B no, porque el pago es una obligación que nace del "
        "contrato. La D no, porque la inscripción es la tradición del inmueble, no el "
        "perfeccionamiento del contrato.",
        f"{CC}, arts. 1793 y 1801; {UC}, VI, cap. III, 2.1 a 2.4",
    ),
    (
        "Compraventa: concepto, cosa, precio y solemnidades",
        2,
        "Andrés vende a Bárbara un auto que pertenece a un tercero. ¿Qué valor tiene la "
        "compraventa?",
        [
            "Es nula absolutamente por objeto ilícito.",
            "Vale, sin perjuicio de los derechos del dueño de la cosa vendida, mientras no se "
            "extingan por el lapso de tiempo.",
            "Es inexistente.",
            "Solo vale si el dueño la autoriza antes del contrato.",
        ],
        "B",
        "Es la B porque el art. 1815 dispone que la venta de cosa ajena vale, sin perjuicio "
        "de los derechos del dueño; es consecuencia de que la compraventa solo genere "
        "obligaciones. La A no, porque no hay objeto ilícito. La C no, porque el contrato "
        "reúne sus elementos esenciales. La D no, porque vale aun sin autorización; si el "
        "dueño ratifica después, el comprador adquiere el dominio desde la fecha de la venta "
        "(art. 1818).",
        f"{CC}, arts. 1815 y 1818; {UC}, VI, cap. III, 2.2",
    ),
    (
        "Obligaciones del vendedor y del comprador",
        2,
        "¿Cuáles son las obligaciones del vendedor según el art. 1824?",
        [
            "Solo entregar la cosa.",
            "La entrega o tradición, y el saneamiento de la cosa vendida.",
            "Pagar el precio.",
            "Asegurar la cosa contra todo riesgo.",
        ],
        "B",
        "Es la B porque el art. 1824 dispone que las obligaciones del vendedor se reducen en "
        "general a dos: la entrega o tradición, y el saneamiento; este comprende el amparo "
        "en la posesión pacífica (evicción) y la responsabilidad por los defectos ocultos "
        "(vicios redhibitorios), según el art. 1837. La A no, porque omite el saneamiento. "
        "La C no, porque el precio lo paga el comprador. La D no, porque no hay obligación "
        "legal de asegurar la cosa.",
        f"{CC}, arts. 1824 y 1837; {UC}, VI, cap. III, 2.6.1",
    ),
    (
        "Obligaciones del vendedor y del comprador",
        3,
        "Un comprador descubre, tres meses después de recibirlo, que el motor del auto usado "
        "que compró tenía un defecto oculto grave que existía al tiempo de la venta. ¿Qué "
        "acción tiene y en qué plazo prescribe?",
        [
            "Acción reivindicatoria; no prescribe.",
            "Acción redhibitoria, que prescribe en seis meses respecto de las cosas muebles y "
            "en un año respecto de los bienes raíces, contados desde la entrega real.",
            "Acción de nulidad por error, que prescribe en diez años.",
            "Acción de petición de herencia.",
        ],
        "B",
        "Es la B porque el defecto oculto, existente al tiempo de la venta y que impide o "
        "dificulta el uso natural de la cosa, es un vicio redhibitorio (art. 1858), y la "
        "acción redhibitoria prescribe en los plazos del art. 1866; la acción para pedir "
        "rebaja del precio tiene plazos mayores (art. 1869). La A no, porque el comprador es "
        "dueño y tiene la cosa. La C no, porque la nulidad relativa prescribe en cuatro años "
        "y aquí la ley da una acción específica. La D no, porque no hay herencia.",
        f"{CC}, arts. 1858, 1866 y 1869; {UC}, VI, cap. III, 2.6.1.3",
    ),
    (
        "Capacidad y pactos especiales en la compraventa",
        2,
        "¿Entre quiénes es nula la compraventa según el art. 1796?",
        [
            "Entre hermanos.",
            "Entre cónyuges no separados judicialmente, y entre el padre o madre y el hijo "
            "sujeto a patria potestad.",
            "Entre socios de una sociedad.",
            "Entre el arrendador y el arrendatario.",
        ],
        "B",
        "Es la B porque esa es la prohibición del art. 1796. La A no, porque los hermanos "
        "pueden comprarse y venderse. La C no, porque los socios no tienen esa prohibición "
        "legal. La D no, porque el arrendatario puede comprar la cosa arrendada.",
        f"{CC}, art. 1796; {UC}, VI, cap. III, 2.5",
    ),
    (
        "Capacidad y pactos especiales en la compraventa",
        2,
        "En un pacto de retroventa, ¿cuál es el plazo máximo para que el vendedor ejerza su "
        "facultad de recobrar la cosa?",
        [
            "Un año.",
            "Cuatro años contados desde la fecha del contrato.",
            "Diez años.",
            "No tiene plazo.",
        ],
        "B",
        "Es la B porque el art. 1885 dispone que el tiempo en que se podrá intentar la acción "
        "de retroventa no podrá pasar de cuatro años contados desde la fecha del contrato. En "
        "el pacto, el vendedor se reserva la facultad de recobrar la cosa reembolsando al "
        "comprador la cantidad estipulada o, a falta de estipulación, lo que le haya costado "
        "la compra (art. 1881). La A no, porque el plazo es mayor. La C no, porque excede el "
        "máximo legal. La D no, porque la ley sí fija un plazo.",
        f"{CC}, arts. 1881 y 1885; {UC}, VI, cap. III, 2.8.2",
    ),
    (
        "Arrendamiento",
        2,
        "El dueño de una casa arrendada por escritura pública la vende. ¿Debe el comprador "
        "respetar el arriendo?",
        [
            "No, porque el arrendamiento solo obliga a las partes.",
            "Sí, porque, si el arrendamiento ha sido contraído por escritura pública, está "
            "obligado a respetarlo aquel a quien se transfiere la cosa arrendada a título "
            "oneroso.",
            "Solo si el comprador es pariente del vendedor.",
            "Solo durante el primer mes.",
        ],
        "B",
        "Es la B porque el art. 1962 n.° 2 obliga a respetar el arriendo a todo aquel a quien "
        "se transfiere el derecho del arrendador a título oneroso, si el arrendamiento ha "
        "sido contraído por escritura pública; el adquirente por título lucrativo (gratuito) "
        "debe respetarlo siempre (n.° 1). La A no, porque la ley hace esta "
        "excepción. La C no, porque el parentesco es irrelevante. La D no, porque no existe "
        "esa limitación.",
        f"{CC}, arts. 1950 y 1962; {UC}, VI, cap. III, 3.4",
    ),
    (
        "Arrendamiento",
        3,
        "En un arriendo de un departamento urbano pactado mes a mes, el arrendatario lleva "
        "dos años completos en el inmueble. Si el arrendador lo desahucia, ¿de qué plazo "
        "dispone el arrendatario para restituir, según la Ley 18.101?",
        [
            "Quince días.",
            "Dos meses desde la notificación, más un mes por cada año completo de ocupación: "
            "en total, cuatro meses (con un máximo legal de seis).",
            "Un año.",
            "No hay plazo: debe restituir de inmediato.",
        ],
        "B",
        "Es la B porque el art. 3 de la Ley 18.101 fija un plazo de desahucio de dos meses "
        "desde la notificación, aumentado en un mes por cada año completo de ocupación, sin "
        "exceder en total de seis meses. La A no, porque el plazo es mayor. La C no, porque "
        "no es el plazo legal. La D no, porque la ley da un plazo al arrendatario.",
        f"Ley 18.101, art. 3; {UC}, VI, cap. III, 3.5",
    ),
    (
        "Mandato",
        1,
        "¿Qué es el mandato según el art. 2116?",
        [
            "Un contrato en que una persona confía la gestión de uno o más negocios a otra, "
            "que se hace cargo de ellos por cuenta y riesgo de la primera.",
            "Un contrato en que una persona presta dinero a otra.",
            "Un contrato en que una persona entrega una cosa para su custodia.",
            "Una orden judicial.",
        ],
        "A",
        "Es la A porque es la definición del art. 2116. La B no, porque eso es el mutuo (art. "
        "2196). La C no, porque eso es el depósito (art. 2211). La D no, porque el mandato es "
        "un contrato, no una orden judicial.",
        f"{CC}, art. 2116; {UC}, VI, cap. III, 4.1",
    ),
    (
        "Mandato",
        2,
        "¿Qué facultades confiere naturalmente un mandato redactado en términos generales?",
        [
            "Todas, incluida la de vender inmuebles.",
            "Solo las de efectuar actos de administración.",
            "Solo la de comparecer en juicio.",
            "Ninguna, mientras el mandante no las enumere.",
        ],
        "B",
        "Es la B porque el art. 2132 dispone que el mandato no confiere naturalmente al "
        "mandatario más que el poder de efectuar los actos de administración; para actos que "
        "salgan de estos límites se necesita poder especial. La A no, porque vender bienes "
        "excede la administración ordinaria. La C no, porque la representación judicial "
        "tiene sus propias reglas. La D no, porque el mandato general sí confiere facultades "
        "de administración.",
        f"{CC}, arts. 2130 y 2132; {UC}, VI, cap. III, 4.3",
    ),
    (
        "Transacción",
        2,
        "¿Qué es la transacción según el art. 2446?",
        [
            "Cualquier renuncia a un derecho.",
            "Un contrato en que las partes terminan extrajudicialmente un litigio pendiente o "
            "precaven un litigio eventual.",
            "Una sentencia de término.",
            "Un acuerdo para pagar en cuotas.",
        ],
        "B",
        "Es la B porque es la definición del art. 2446; el inc. 2 aclara que no es "
        "transacción el acto que solo consiste en la renuncia de un derecho que no se "
        "disputa. La doctrina agrega como elemento las concesiones recíprocas. La A no, "
        "porque la ley lo excluye expresamente. La C no, porque la transacción es un "
        "contrato, aunque produce el efecto de cosa juzgada en última instancia (art. 2460). "
        "La D no, porque un acuerdo de pago no supone necesariamente un litigio.",
        f"{CC}, arts. 2446 y 2460; {UC}, VI, cap. III, 5",
    ),
    (
        "Transacción",
        3,
        "¿Sobre cuál de estas materias NO se puede transigir según el Código Civil?",
        [
            "Sobre el monto de una indemnización.",
            "Sobre el estado civil de las personas.",
            "Sobre el precio de una compraventa discutida.",
            "Sobre los límites de un predio.",
        ],
        "B",
        "Es la B porque el art. 2450 prohíbe transigir sobre el estado civil de las personas, "
        "que es materia de orden público. La A no, porque las indemnizaciones son derechos "
        "patrimoniales disponibles. La C no, porque el precio es disponible. La D no, porque "
        "los conflictos de deslindes pueden transigirse.",
        f"{CC}, arts. 2449 y 2450; {UC}, VI, cap. III, 5",
    ),
    (
        "Contratos reales y mutuo",
        1,
        "¿Cuáles son los contratos reales típicos del Código Civil?",
        [
            "Compraventa, permuta, arrendamiento y mandato.",
            "Mutuo, comodato, depósito y prenda.",
            "Fianza, hipoteca, promesa y transacción.",
            "Sociedad, renta vitalicia, censo y donación.",
        ],
        "B",
        "Es la B porque esos son los contratos que se perfeccionan por la entrega de la cosa "
        "(arts. 1443, 2174, 2196, 2211 y 2384). La A no, porque son consensuales. La C no, "
        "porque la hipoteca y la promesa son solemnes y la fianza y la transacción son "
        "consensuales. La D no, porque ninguno de ellos es real en el Código.",
        f"{CC}, arts. 1443, 2174, 2196, 2211 y 2384; {UC}, VI, cap. III, 6",
    ),
    (
        "Contratos reales y mutuo",
        2,
        "En el mutuo de dinero, ¿qué efecto tiene la entrega del dinero al mutuario?",
        [
            "Le da la mera tenencia, con obligación de devolver los mismos billetes.",
            "Le transfiere el dominio del dinero, con cargo de restituir otro tanto del mismo "
            "género y calidad.",
            "Le da un usufructo sobre el dinero.",
            "No produce efecto hasta que se paguen los intereses.",
        ],
        "B",
        "Es la B porque el mutuo recae sobre cosas fungibles (art. 2196) y el art. 2197 "
        "dispone que no se perfecciona sino por la tradición, y que la tradición transfiere "
        "el dominio. La A no, porque eso sería un comodato o un depósito. La C no, porque no "
        "es usufructo. La D no, porque el contrato se perfecciona con la tradición.",
        f"{CC}, arts. 2196 y 2197; Ley 18.010; {UC}, VI, cap. III, 6.3",
    ),
    (
        "Fianza",
        2,
        "El acreedor demanda directamente al fiador sin haber cobrado antes al deudor "
        "principal, que tiene bienes. ¿Qué puede oponer el fiador?",
        [
            "Nada: debe pagar.",
            "El beneficio de excusión: exigir que antes de proceder contra él se persiga la "
            "deuda en los bienes del deudor principal.",
            "La nulidad de la fianza.",
            "La compensación con lo que le debe el acreedor al deudor.",
        ],
        "B",
        "Es la B porque el art. 2357 concede al fiador el beneficio de excusión, salvo que "
        "lo haya renunciado o se haya obligado como codeudor solidario, entre otros casos "
        "(art. 2358). La A no, porque la ley le da ese beneficio. La C no, porque nada indica "
        "un vicio de nulidad. La D no, porque la compensación requiere que el acreedor sea "
        "deudor del propio fiador o se den otros requisitos.",
        f"{CC}, arts. 2335, 2357 y 2358; {UC}, VI, cap. III, 7.2.1",
    ),
    (
        "Fianza",
        3,
        "Una persona se constituye en fiadora de una deuda de $1.000.000 y se obliga a "
        "pagar $1.500.000 si el deudor no paga. ¿Qué ocurre?",
        [
            "La fianza es válida por $1.500.000.",
            "La fianza es nula en su totalidad.",
            "El fiador no puede obligarse a más que el deudor principal: la fianza se reduce a "
            "los términos de la obligación principal.",
            "La fianza se convierte en cláusula penal.",
        ],
        "C",
        "Es la C porque el art. 2343 dispone que el fiador no puede obligarse a más de lo que "
        "debe el deudor principal, pero puede obligarse a menos; el art. 2344 ordena reducir "
        "la fianza que exceda de lo que debe el deudor principal. La A no, porque la fianza "
        "es accesoria. La B no, porque la fianza no se anula: se reduce. La D no, porque no "
        "hay tal conversión.",
        f"{CC}, arts. 2343 y 2344; {UC}, VI, cap. III, 7.2.1",
    ),
    (
        "Prenda e hipoteca",
        2,
        "¿Qué requisitos de forma debe cumplir la hipoteca según el Código Civil?",
        [
            "Basta un instrumento privado.",
            "Debe otorgarse por escritura pública y debe inscribirse en el Registro de "
            "Hipotecas del Conservador; sin la inscripción no tiene valor alguno.",
            "Basta la entrega de la propiedad al acreedor.",
            "Requiere aprobación judicial.",
        ],
        "B",
        "Es la B porque el art. 2409 exige escritura pública y el art. 2410 la inscripción en "
        "el Registro de Hipotecas, sin la cual no tiene valor alguno. La A no, porque la "
        "hipoteca es solemne. La C no, porque el inmueble hipotecado permanece en poder del "
        "deudor (art. 2407). La D no, porque no se exige aprobación judicial.",
        f"{CC}, arts. 2407, 2409 y 2410; {UC}, VI, cap. III, 7.3.2",
    ),
    (
        "Prenda e hipoteca",
        3,
        "En un contrato de prenda civil se pacta que, si el deudor no paga, el acreedor se "
        "quedará con la cosa empeñada. ¿Qué valor tiene esa cláusula?",
        [
            "Es válida, porque las partes son libres de pactarla.",
            "No vale: el acreedor solo puede pedir que la prenda se venda en pública subasta "
            "o, a falta de postura admisible, que se le adjudique en pago tras tasación de "
            "peritos.",
            "Es válida solo si la cosa vale menos que la deuda.",
            "Convierte la prenda en hipoteca.",
        ],
        "B",
        "Es la B porque el art. 2397 dispone que no vale estipulación alguna que permita al "
        "acreedor disponer de la prenda o apropiársela por otros medios que los que él señala "
        "(prohibición del pacto comisorio en la prenda). La A no, porque la ley lo prohíbe "
        "expresamente. La C no, porque la prohibición no depende del valor. La D no, porque "
        "no hay tal conversión.",
        f"{CC}, arts. 2384 y 2397; {UC}, VI, cap. III, 7.3.1",
    ),
    # --------------------------------------------------------- VII. Derecho de familia
    (
        "Familia y parentesco",
        1,
        "¿En qué grado son parientes dos hermanos?",
        [
            "En primer grado en línea recta.",
            "En segundo grado en línea colateral.",
            "En primer grado en línea colateral.",
            "En tercer grado en línea colateral.",
        ],
        "B",
        "Es la B porque los grados se cuentan por el número de generaciones (art. 27): en la "
        "línea colateral se sube hasta el tronco común y luego se baja. De un hermano al "
        "padre hay una generación y del padre al otro hermano otra: dos grados. La A no, "
        "porque los hermanos no descienden uno del otro. La C no, porque no hay parentesco "
        "colateral en primer grado. La D no, porque el tercer grado colateral corresponde, "
        "por ejemplo, a tío y sobrino.",
        f"{CC}, arts. 27 y 28; {UC}, VII, cap. I, 4",
    ),
    (
        "Familia y parentesco",
        2,
        "¿Qué parentesco hay entre una persona y el hermano de su cónyuge?",
        [
            "Consanguinidad en segundo grado colateral.",
            "Afinidad en segundo grado colateral.",
            "No hay parentesco alguno.",
            "Afinidad en primer grado en línea recta.",
        ],
        "B",
        "Es la B porque el parentesco por afinidad es el que existe entre una persona que "
        "está o ha estado casada y los consanguíneos de su cónyuge; la línea y el grado se "
        "califican por la línea y grado de consanguinidad del cónyuge (art. 31). Como el "
        "cónyuge es hermano de esa persona en segundo grado colateral, el cuñado es pariente "
        "por afinidad en segundo grado colateral. La A no, porque no comparten sangre. La C "
        "no, porque la ley reconoce la afinidad. La D no, porque el primer grado en línea "
        "recta por afinidad corresponde, por ejemplo, a los suegros.",
        f"{CC}, art. 31; {UC}, VII, cap. I, 4.2",
    ),
    (
        "Esponsales y requisitos del matrimonio",
        2,
        "Dos novios se prometen matrimonio y pactan una multa para quien rompa el "
        "compromiso. Uno lo rompe y paga voluntariamente la multa. ¿Puede pedir su "
        "devolución?",
        [
            "Sí, porque los esponsales no producen obligación alguna.",
            "No: aunque la multa no puede demandarse, si se pagó no puede pedirse su devolución.",
            "Sí, pero solo la mitad.",
            "No, y además el otro puede demandar que se celebre el matrimonio.",
        ],
        "B",
        "Es la B porque el art. 99 dispone que no puede pedirse la multa estipulada para el "
        "caso de no cumplirse lo prometido, pero si se hubiere pagado no podrá pedirse su "
        "devolución. Los esponsales son un hecho privado sometido al honor y conciencia del "
        "individuo (art. 98). La A no, porque la ley permite retener lo pagado. La C no, "
        "porque no hay tal regla. La D no, porque el art. 98 excluye la demanda para exigir "
        "el matrimonio.",
        f"{CC}, arts. 98 y 99; {UC}, VII, cap. II, 1",
    ),
    (
        "Esponsales y requisitos del matrimonio",
        3,
        "Dos personas se casan ante una entidad religiosa con personalidad jurídica de "
        "derecho público. ¿Qué deben hacer para que ese matrimonio produzca efectos civiles?",
        [
            "Nada: produce efectos civiles desde la ceremonia.",
            "Presentar el acta otorgada por la entidad religiosa ante un oficial del Registro "
            "Civil dentro de ocho días para su inscripción, ratificando ante él el "
            "consentimiento; si no se inscribe en ese plazo, no produce efecto civil alguno.",
            "Celebrar un nuevo matrimonio civil dentro de un año.",
            "Obtener la aprobación de un juez de familia.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 20 de la Ley de Matrimonio Civil. La A no, "
        "porque los efectos civiles requieren la inscripción. La C no, porque basta la "
        "inscripción dentro de plazo y no se exige otra ceremonia. La D no, porque no se "
        "requiere aprobación judicial.",
        f"{LMC}, art. 20; {UC}, VII, cap. II, 3.2.3.1.2",
    ),
    (
        "Efectos del matrimonio y bienes familiares",
        2,
        "Se declara bien familiar la casa que es residencia principal de la familia y que "
        "pertenece solo a uno de los cónyuges. ¿Qué efecto tiene esa declaración?",
        [
            "La casa pasa a ser de propiedad de ambos cónyuges.",
            "El cónyuge propietario no puede enajenarla ni gravarla voluntariamente, ni "
            "prometer gravarla o enajenarla, sin la autorización del cónyuge no propietario.",
            "La casa se vuelve inembargable para siempre.",
            "Solo tiene efecto si los cónyuges están casados en sociedad conyugal.",
        ],
        "B",
        "Es la B porque ese es el efecto que prevé el art. 142; la institución protege la "
        "vivienda familiar y se aplica cualquiera sea el régimen de bienes (art. 141). La A "
        "no, porque la declaración no cambia la propiedad. La C no, porque la ley prevé el "
        "beneficio de excusión (art. 148), no una inembargabilidad absoluta. La D no, porque "
        "se aplica a todos los regímenes.",
        f"{CC}, arts. 141, 142 y 148; {UC}, VII, cap. II, 5",
    ),
    (
        "Efectos del matrimonio y bienes familiares",
        3,
        "Tras la Ley 21.400 (2021), ¿qué ocurre con la «diversidad de sexos» que la "
        "doctrina tradicional enumeraba como requisito de existencia del matrimonio?",
        [
            "Sigue siendo requisito de existencia.",
            "Dejó de ser requisito: el matrimonio puede celebrarse entre dos personas, sin "
            "distinción de sexo.",
            "Pasó a ser requisito de validez sancionado con nulidad relativa.",
            "Solo se exige en los matrimonios religiosos.",
        ],
        "B",
        "Es la B porque la Ley 21.400, de matrimonio igualitario, modificó el art. 102 y la "
        "legislación de familia para permitir el matrimonio entre dos personas de igual o "
        "distinto sexo. Por eso hay que leer con cuidado los textos anteriores a 2021, "
        "incluido el temario de esta cédula. La A no, porque la ley lo eliminó. La C no, "
        "porque tampoco es requisito de validez. La D no, porque los efectos civiles del "
        "matrimonio religioso se rigen por la misma ley civil.",
        f"Ley 21.400; {CC}, art. 102; {UC}, VII, cap. II, 3.1",
    ),
    (
        "Separación, nulidad y divorcio",
        2,
        "Un cónyuge quiere divorciarse unilateralmente, sin alegar culpa del otro. ¿Qué "
        "plazo de cese de la convivencia debe acreditar, como regla general?",
        [
            "Seis meses.",
            "Un año.",
            "Tres años.",
            "Diez años.",
        ],
        "C",
        "Es la C porque el art. 55 inc. 3 de la Ley de Matrimonio Civil permite el divorcio "
        "pedido por uno de los cónyuges cuando se verifica un cese efectivo de la convivencia "
        "conyugal durante un lapso de, a lo menos, tres años. Si lo piden ambos de común "
        "acuerdo, basta un año (inc. 1). La A no, porque ese plazo no existe. La B no, porque "
        "un año corresponde al divorcio de común acuerdo. La D no, porque excede lo exigido.",
        f"{LMC}, art. 55; {UC}, VII, cap. II, 6.4",
    ),
    (
        "Separación, nulidad y divorcio",
        3,
        "Durante el matrimonio, uno de los cónyuges se dedicó al cuidado de los hijos y no "
        "pudo trabajar remuneradamente. Al divorciarse, ¿qué derecho tiene?",
        [
            "Ninguno, porque el divorcio pone fin a todos los derechos.",
            "Derecho a que se le compense el menoscabo económico sufrido por esta causa "
            "(compensación económica).",
            "Derecho a pensión de alimentos de por vida.",
            "Derecho a quedarse con todos los bienes del otro cónyuge.",
        ],
        "B",
        "Es la B porque el art. 61 de la Ley de Matrimonio Civil concede la compensación "
        "económica en caso de divorcio o nulidad al cónyuge que, por haberse dedicado al "
        "cuidado de los hijos o a las labores del hogar común, no pudo desarrollar una "
        "actividad remunerada o lucrativa, o lo hizo en menor medida de lo que podía y "
        "quería. La A no, porque la ley prevé este derecho. La C no, porque el divorcio pone "
        "fin, en general, al derecho de alimentos entre cónyuges. La D no, porque la "
        "compensación se fija según el menoscabo, no como entrega de todos los bienes.",
        f"{LMC}, arts. 61 y 62; {UC}, VII, cap. II, 6.4.3",
    ),
    (
        "Capitulaciones matrimoniales y sociedad conyugal",
        2,
        "Durante el matrimonio, ¿qué pueden pactar los cónyuges casados en sociedad "
        "conyugal respecto de su régimen de bienes?",
        [
            "Cualquier régimen inventado por ellos.",
            "Sustituir la sociedad conyugal por el régimen de separación total de bienes o "
            "por el de participación en los gananciales, por escritura pública subinscrita al "
            "margen de la inscripción matrimonial dentro de treinta días.",
            "Nada: el régimen es inmutable.",
            "Volver a la sociedad conyugal después de haberla sustituido, cuantas veces quieran.",
        ],
        "B",
        "Es la B porque el art. 1723 permite esa sustitución durante el matrimonio con esas "
        "solemnidades, y agrega que el pacto no puede dejarse sin efecto por el mutuo "
        "consentimiento de los cónyuges. La A no, porque los regímenes son los legales. La C "
        "no, porque el art. 1723 admite la sustitución. La D no, porque el pacto es "
        "irrevocable.",
        f"{CC}, arts. 1715, 1716 y 1723; {UC}, VII, cap. III, 2",
    ),
    (
        "Capitulaciones matrimoniales y sociedad conyugal",
        3,
        "En la sociedad conyugal, uno de los cónyuges recibe por herencia, durante el "
        "matrimonio, un departamento. ¿A qué haber ingresa?",
        [
            "Al haber absoluto de la sociedad conyugal.",
            "Al haber relativo, con cargo a recompensa.",
            "Al haber propio del cónyuge heredero, porque los inmuebles adquiridos a título "
            "gratuito durante el matrimonio no ingresan a la sociedad.",
            "Por mitades a cada cónyuge.",
        ],
        "C",
        "Es la C porque, según los arts. 1725 y 1726, los inmuebles adquiridos durante el "
        "matrimonio a título gratuito (herencia, donación, legado) pertenecen al cónyuge "
        "adquirente y no a la sociedad. En cambio, los muebles adquiridos a título gratuito "
        "ingresan al haber relativo, con cargo a recompensa (art. 1725 n.° 4). La A no, "
        "porque el haber absoluto comprende, entre otros, los bienes adquiridos a título "
        "oneroso. La B no, porque el haber relativo corresponde a muebles, no a inmuebles. "
        "La D no, porque no hay división por mitades.",
        f"{CC}, arts. 1725 y 1726; {UC}, VII, cap. III, 3.1 a 3.3",
    ),
    (
        "Separación de bienes y patrimonio reservado",
        2,
        "Una mujer casada en sociedad conyugal trabaja como médica, con independencia de su "
        "marido. ¿Cómo se considera respecto de lo que obtiene con ese trabajo?",
        [
            "Como parte del haber absoluto, administrado por el marido.",
            "Como separada de bienes respecto del ejercicio de esa profesión y de lo que en "
            "ella obtenga (patrimonio reservado).",
            "Como propiedad exclusiva del marido.",
            "Como bienes en comunidad con los hijos.",
        ],
        "B",
        "Es la B porque el art. 150 considera a la mujer casada que desempeña algún empleo o "
        "ejerce una profesión, oficio o industria separados de los de su marido como "
        "separada de bienes respecto de su ejercicio y de lo que en él obtenga. Es un caso "
        "de separación legal parcial. La A no, porque la ley excluye esos bienes de la "
        "administración del marido. La C no, porque no son del marido. La D no, porque los "
        "hijos no son comuneros.",
        f"{CC}, art. 150; {UC}, VII, cap. III, 3.11 y 4.2.2",
    ),
    (
        "Separación de bienes y patrimonio reservado",
        3,
        "Al disolverse la sociedad conyugal, ¿qué puede hacer la mujer con los bienes de su "
        "patrimonio reservado?",
        [
            "Nada: pasan automáticamente al marido.",
            "Si acepta los gananciales, esos bienes entran en la partición de gananciales; si "
            "renuncia a los gananciales, conserva los bienes del patrimonio reservado.",
            "Debe venderlos y repartir el precio con el marido.",
            "Debe donarlos a los hijos.",
        ],
        "B",
        "Es la B porque el art. 150 dispone que, a la disolución de la sociedad conyugal, "
        "los bienes reservados entran en la partición de gananciales, a menos que la mujer o "
        "sus herederos renuncien a estos, caso en que el marido no responde por las "
        "obligaciones contraídas por la mujer en su administración separada. La A no, porque "
        "la mujer conserva opciones. La C no, porque no hay tal obligación. La D no, porque "
        "no se impone esa donación.",
        f"{CC}, arts. 150 y 1781; {UC}, VII, cap. III, 3.11.6",
    ),
    (
        "Filiación",
        1,
        "¿Cuándo es matrimonial la filiación de un hijo?",
        [
            "Solo si los padres estaban casados al momento de la concepción.",
            "Cuando existe matrimonio entre sus padres al tiempo de la concepción o del "
            "nacimiento del hijo.",
            "Cuando los padres se casan en cualquier momento de la vida del hijo, sin otra "
            "exigencia.",
            "Solo si el hijo nace en un hospital público.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 180 inc. 1; es también matrimonial la "
        "filiación del hijo cuyos padres contraen matrimonio con posterioridad a su "
        "nacimiento, siempre que la paternidad y la maternidad hayan estado previamente "
        "determinadas o se determinen conforme al art. 180 inc. 2. La A no, porque basta el "
        "matrimonio al tiempo del nacimiento. La C no, porque el matrimonio posterior exige "
        "además la determinación de la filiación. La D no, porque el lugar del nacimiento es "
        "irrelevante.",
        f"{CC}, arts. 179 y 180; {UC}, VII, cap. IV, 1",
    ),
    (
        "Filiación",
        2,
        "¿Qué efecto tiene la adopción regulada por la Ley 19.620 sobre el estado civil del "
        "adoptado?",
        [
            "Ninguno: el adoptado conserva su filiación de origen.",
            "Le confiere el estado civil de hijo respecto del o los adoptantes, y extingue sus "
            "vínculos de filiación de origen, salvo para efectos de impedimentos para contraer "
            "matrimonio.",
            "Lo convierte en pupilo, con un tutor.",
            "Solo le da derecho a alimentos.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 37 de la Ley 19.620. La A no, porque la "
        "adopción cambia el estado civil. La C no, porque la adopción no es una guarda. La D "
        "no, porque el adoptado tiene todos los derechos de un hijo.",
        f"Ley 19.620, art. 37; {UC}, VII, cap. IV, 2",
    ),
    (
        "Derecho de alimentos",
        2,
        "Un hijo de 24 años estudia una profesión. ¿Puede seguir recibiendo alimentos de sus "
        "padres?",
        [
            "No, porque los alimentos a los hijos cesan siempre a los 18 años.",
            "Sí: los alimentos a los descendientes se deben hasta los 21 años, salvo que estén "
            "estudiando una profesión u oficio, caso en que cesan a los 28.",
            "Sí, de por vida.",
            "Solo si se casa.",
        ],
        "B",
        "Es la B porque el art. 332 inc. 2 dispone que los alimentos que se deben a los "
        "descendientes y a los hermanos se deben hasta los 21 años, salvo que estén "
        "estudiando una profesión u oficio, caso en que cesan a los 28 años; o que les afecte "
        "una incapacidad física o mental, o que el juez los considere indispensables por "
        "otras circunstancias. La A no, porque la mayoría de edad no pone fin a los "
        "alimentos. La C no, porque la regla tiene límite de edad. La D no, porque el "
        "matrimonio no es la condición.",
        f"{CC}, arts. 321 y 332; {UC}, VII, cap. V",
    ),
    (
        "Derecho de alimentos",
        3,
        "¿Puede una persona vender, ceder o renunciar su derecho a pedir alimentos futuros?",
        [
            "Sí, libremente.",
            "No: el derecho de pedir alimentos no puede transmitirse por causa de muerte, ni "
            "venderse o cederse de modo alguno, ni renunciarse; en cambio, las pensiones "
            "alimenticias atrasadas sí pueden renunciarse o compensarse.",
            "Solo puede renunciarlo con autorización del juez.",
            "Solo puede cederlo a sus hijos.",
        ],
        "B",
        "Es la B porque así lo disponen los arts. 334 y 336: el derecho a alimentos futuros "
        "es inalienable e irrenunciable por su carácter personalísimo y de orden público; las "
        "pensiones ya devengadas son créditos patrimoniales comunes. La A no, porque la ley "
        "lo prohíbe. La C no, porque ni con autorización judicial puede renunciarse; la "
        "transacción sobre alimentos futuros requiere aprobación judicial (art. 2451), lo que "
        "es distinto. La D no, porque la ley prohíbe toda cesión.",
        f"{CC}, arts. 334, 336 y 2451; {UC}, VII, cap. V",
    ),
    # ------------------------------------------------------- VIII. Derecho sucesorio
    (
        "Sucesión por causa de muerte: asignatarios, apertura y delación",
        1,
        "¿Qué diferencia hay entre un heredero y un legatario?",
        [
            "El heredero sucede en bienes determinados; el legatario, en todo el patrimonio.",
            "El heredero sucede en todos los bienes del difunto o en una cuota de ellos (título "
            "universal) y representa al causante; el legatario sucede en una o más especies o "
            "cuerpos ciertos, o en géneros determinados (título singular).",
            "No hay diferencia: son sinónimos.",
            "El heredero es siempre pariente y el legatario nunca.",
        ],
        "B",
        "Es la B porque así lo establecen los arts. 951 y 954; además, los herederos "
        "representan la persona del causante y suceden en sus obligaciones transmisibles "
        "(art. 1097), mientras que los legatarios no la representan (art. 1104). La A no, "
        "porque invierte los conceptos. La C no, porque son asignatarios distintos. La D no, "
        "porque cualquier persona capaz puede ser heredera o legataria por testamento.",
        f"{CC}, arts. 951, 954, 1097 y 1104; {UC}, VIII, cap. I, 3",
    ),
    (
        "Sucesión por causa de muerte: asignatarios, apertura y delación",
        2,
        "¿Dónde y cuándo se abre la sucesión de una persona?",
        [
            "En el lugar donde muere y en el momento en que se lee el testamento.",
            "En el momento de su muerte, en su último domicilio.",
            "En el lugar donde están sus bienes, cuando se concede la posesión efectiva.",
            "En el lugar donde nació, al inscribirse su defunción.",
        ],
        "B",
        "Es la B porque el art. 955 dispone que la sucesión en los bienes de una persona se "
        "abre al momento de su muerte en su último domicilio, salvo los casos expresamente "
        "exceptuados; y que la sucesión se regla por la ley del domicilio en que se abre. La "
        "A no, porque el lugar es el último domicilio y la lectura del testamento no marca la "
        "apertura. La C no, porque la posesión efectiva es posterior a la apertura. La D no, "
        "porque el lugar de nacimiento es irrelevante.",
        f"{CC}, art. 955; {UC}, VIII, cap. I, 4",
    ),
    (
        "Aceptación, repudiación, herencia yacente y beneficio de inventario",
        2,
        "Un heredero vende un inmueble de la herencia antes de declarar si acepta o "
        "repudia. ¿Qué efecto tiene esa venta respecto de su calidad de heredero?",
        [
            "Ninguno: puede repudiar después.",
            "Importa aceptación tácita de la herencia, porque es un acto que supone "
            "necesariamente su intención de aceptar y que no habría tenido derecho a ejecutar "
            "sino en calidad de heredero.",
            "Es nula, porque nadie puede vender bienes hereditarios.",
            "Importa repudiación de la herencia.",
        ],
        "B",
        "Es la B porque el art. 1241 define la aceptación tácita en esos términos, y el art. "
        "1244 agrega que la enajenación de cualquier efecto hereditario, aun para objetos de "
        "administración urgente, es acto de heredero si no ha sido autorizada por el juez. La "
        "A no, porque, aceptada la herencia, no puede repudiarse. La C no, porque el heredero "
        "puede disponer cumpliendo los requisitos legales. La D no, porque el acto denota lo "
        "contrario.",
        f"{CC}, arts. 1241 y 1244; {UC}, VIII, cap. I, 6.5",
    ),
    (
        "Aceptación, repudiación, herencia yacente y beneficio de inventario",
        3,
        "Un heredero acepta con beneficio de inventario una herencia cuyas deudas superan el "
        "valor de los bienes. ¿Hasta dónde responde de las deudas hereditarias?",
        [
            "Ilimitadamente, con todos sus bienes propios.",
            "Solo hasta concurrencia del valor total de los bienes que ha heredado.",
            "No responde de ninguna deuda.",
            "Por la mitad de las deudas.",
        ],
        "B",
        "Es la B porque el beneficio de inventario consiste en no hacer a los herederos que "
        "aceptan responsables de las obligaciones hereditarias y testamentarias sino hasta "
        "concurrencia del valor total de los bienes que han heredado (art. 1247). La A no, "
        "porque esa es la responsabilidad del heredero que acepta pura y simplemente. La C "
        "no, porque sí responde, con un límite. La D no, porque no existe esa regla.",
        f"{CC}, arts. 1247 y 1250; {UC}, VIII, cap. I, 8",
    ),
    (
        "Derecho de transmisión y derecho real de herencia",
        2,
        "Ana muere y su heredero, Bruno, muere después sin haber aceptado ni repudiado la "
        "herencia de Ana. ¿Qué derecho tienen los herederos de Bruno?",
        [
            "Ninguno: la herencia de Ana pasa a otros parientes de Ana.",
            "El derecho de transmisión: pueden aceptar o repudiar la herencia de Ana, siempre "
            "que acepten la herencia de Bruno.",
            "El derecho de representación respecto de Ana.",
            "El derecho de acrecimiento.",
        ],
        "B",
        "Es la B porque el art. 957 dispone que, si el heredero o legatario cuyos derechos a "
        "la sucesión no han prescrito fallece antes de haber aceptado o repudiado la "
        "herencia o legado que se le ha deferido, transmite a sus herederos el derecho de "
        "aceptarla o repudiarla, aun cuando fallezca sin saber que se le ha deferido; no se "
        "puede ejercer este derecho sin aceptar la herencia de la persona que lo transmite. "
        "La A no, porque la ley da ese derecho. La C no, porque la representación supone que "
        "el representado no quiso o no pudo suceder (por ejemplo, porque murió antes que el "
        "causante). La D no, porque el acrecimiento opera entre coasignatarios de un mismo "
        "objeto.",
        f"{CC}, arts. 957 y 984; {UC}, VIII, cap. I, 9",
    ),
    (
        "Derecho de transmisión y derecho real de herencia",
        3,
        "Un falso heredero obtuvo la posesión efectiva y ocupa la herencia. ¿En qué plazo "
        "puede adquirirla por prescripción frente al verdadero heredero?",
        [
            "En 2 años.",
            "En 5 años, porque al heredero putativo a quien se le ha concedido la posesión "
            "efectiva le sirve de justo título el decreto o resolución que la concede.",
            "En 30 años.",
            "Nunca: la herencia es imprescriptible.",
        ],
        "B",
        "Es la B porque el art. 704 inc. final da valor de justo título a la resolución de "
        "posesión efectiva respecto del heredero putativo, y el art. 1269 dispone que el "
        "derecho de petición de herencia expira en diez años, pero que el heredero putativo, "
        "en ese caso, puede oponer la prescripción de cinco años. La A no, porque dos años es "
        "el plazo para muebles en "
        "la prescripción ordinaria. La C no, porque no existe tal plazo. La D no, porque la "
        "herencia sí se adquiere por prescripción.",
        f"{CC}, arts. 704, 1264 y 1269; {UC}, VIII, cap. II, 5 y 6",
    ),
    (
        "Capacidad e indignidad para suceder",
        2,
        "¿Qué se necesita, como regla general, para ser capaz de suceder a una persona?",
        [
            "Ser mayor de edad.",
            "Existir al tiempo de abrirse la sucesión.",
            "Ser pariente del causante.",
            "Haber vivido con el causante.",
        ],
        "B",
        "Es la B porque el art. 962 dispone que para ser capaz de suceder es necesario "
        "existir al tiempo de abrirse la sucesión, salvo que se suceda por derecho de "
        "transmisión o bajo condición suspensiva (en este caso, se requiere existir al "
        "cumplirse la condición). La A no, porque los menores pueden heredar. La C no, porque "
        "un extraño puede suceder por testamento. La D no, porque la convivencia no es "
        "requisito.",
        f"{CC}, arts. 962 y 963; {UC}, VIII, cap. III, 2",
    ),
    (
        "Capacidad e indignidad para suceder",
        3,
        "Un heredero mató al causante, pero nadie ha pedido que se declare su indignidad. "
        "¿Puede suceder?",
        [
            "No, porque la indignidad opera de pleno derecho.",
            "Sí, mientras la indignidad no sea declarada en juicio a instancia de cualquiera "
            "de los interesados en su exclusión; además, la indignidad se purga en cinco años "
            "de posesión de la herencia.",
            "Sí, sin posibilidad de exclusión, porque ya heredó.",
            "No, y además sus hijos pierden todo derecho.",
        ],
        "B",
        "Es la B porque el art. 974 dispone que la indignidad no produce efecto alguno si no "
        "es declarada en juicio, y el art. 975 que se purga en cinco años de posesión de la "
        "herencia o legado. El homicidio es causal de indignidad (art. 968 n.° 1). La A no, "
        "porque la indignidad debe declararse judicialmente. La C no, porque puede ser "
        "excluido mientras no se purgue la indignidad. La D no, porque la indignidad es "
        "personal; los descendientes pueden suceder por derecho de representación (art. 987).",
        f"{CC}, arts. 968, 974, 975 y 987; {UC}, VIII, cap. III, 3",
    ),
    (
        "Sucesión intestada y derecho de representación",
        2,
        "Una persona muere sin testamento y deja cónyuge y dos hijos. ¿Cómo se reparte la "
        "herencia?",
        [
            "Todo para el cónyuge.",
            "Por partes iguales entre los tres.",
            "El cónyuge recibe el doble de lo que corresponde a cada hijo: la mitad para el "
            "cónyuge y una cuarta parte para cada hijo.",
            "Todo para los hijos.",
        ],
        "C",
        "Es la C porque, en el primer orden de sucesión, el art. 988 dispone que la porción "
        "del cónyuge equivale al doble de lo que por legítima rigorosa o efectiva corresponda "
        "a cada hijo (si hay un solo hijo, igual a la de este), sin que pueda ser inferior a "
        "la cuarta parte de la herencia. Con dos hijos: el cónyuge 2 partes y cada hijo 1, "
        "es decir, 2/4, 1/4 y 1/4. La A no, porque los hijos concurren con el cónyuge. La B "
        "no, porque el cónyuge recibe el doble. La D no, porque el cónyuge concurre en el "
        "primer orden.",
        f"{CC}, art. 988; {UC}, VIII, cap. IV, 3.3",
    ),
    (
        "Sucesión intestada y derecho de representación",
        3,
        "Una persona muere sin testamento. Uno de sus dos hijos había muerto antes y dejó "
        "dos nietos. ¿Cómo heredan los nietos?",
        [
            "No heredan, porque su padre murió antes.",
            "Por derecho de representación: ocupan el lugar de su padre y se reparten entre "
            "ellos la porción que a él le habría correspondido (sucesión por estirpes).",
            "Cada nieto recibe lo mismo que el hijo vivo (por cabezas).",
            "Heredan por derecho de transmisión.",
        ],
        "B",
        "Es la B porque el derecho de representación es la ficción legal por la que una "
        "persona ocupa el lugar y los derechos hereditarios que tendría su padre o madre si "
        "este no quisiese o no pudiese suceder (art. 984); los representantes suceden por "
        "estirpes (art. 985), y la representación procede en la descendencia del difunto "
        "(art. 986). La A no, porque la ley les da ese derecho. La C no, porque no heredan "
        "por cabezas. La D no, porque la transmisión supone que el heredero murió después "
        "del causante sin aceptar ni repudiar.",
        f"{CC}, arts. 984, 985 y 986; {UC}, VIII, cap. IV, 3.4",
    ),
    (
        "El testamento",
        1,
        "¿Cuál de estas es una característica del testamento según el art. 999?",
        [
            "Es irrevocable una vez otorgado.",
            "Es un acto más o menos solemne, que produce pleno efecto después de los días del "
            "testador, quien conserva la facultad de revocarlo mientras viva.",
            "Es un contrato entre el testador y sus herederos.",
            "Puede otorgarse por medio de mandatario.",
        ],
        "B",
        "Es la B porque esos rasgos están en la definición del art. 999. La A no, porque el "
        "testamento es esencialmente revocable. La C no, porque es un acto unilateral. La D "
        "no, porque la facultad de testar es indelegable (art. 1004): el testamento es un "
        "acto personalísimo.",
        f"{CC}, arts. 999 y 1004; {UC}, VIII, cap. V, 1.1",
    ),
    (
        "El testamento",
        2,
        "¿Qué solemnidades requiere el testamento solemne abierto otorgado en Chile?",
        [
            "Basta la firma del testador.",
            "Debe otorgarse ante competente escribano y tres testigos, o ante cinco testigos.",
            "Debe otorgarse ante un juez y dos testigos.",
            "Debe otorgarse ante el oficial del Registro Civil.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 1014 inc. 2. La A no, porque el testamento "
        "solemne requiere testigos. La C no, porque no se otorga ante un juez. La D no, "
        "porque no interviene el Registro Civil.",
        f"{CC}, arts. 1014 y 1015; {UC}, VIII, cap. V, 1.3.1.1",
    ),
    (
        "Asignaciones forzosas: legítimas y cuarta de mejoras",
        2,
        "Una persona deja hijos y cónyuge. ¿De qué porción de la herencia puede disponer "
        "libremente por testamento a favor de cualquier persona?",
        [
            "De toda la herencia.",
            "De la mitad.",
            "De una cuarta parte (cuarta de libre disposición).",
            "De nada.",
        ],
        "C",
        "Es la C porque, habiendo descendientes, ascendientes o cónyuge, el art. 1184 divide "
        "la herencia en una mitad legitimaria, una cuarta de mejoras (que solo puede "
        "asignarse al cónyuge, descendientes o ascendientes, art. 1195) y una cuarta de libre "
        "disposición. La A no, porque las asignaciones forzosas limitan la libertad de "
        "testar. La B no, porque la otra mitad se divide en mejoras y libre disposición. La D "
        "no, porque siempre queda la cuarta de libre disposición.",
        f"{CC}, arts. 1167, 1184 y 1195; {UC}, VIII, cap. V, 2.4",
    ),
    (
        "Asignaciones forzosas: legítimas y cuarta de mejoras",
        3,
        "¿Quiénes son legitimarios según el art. 1182?",
        [
            "Todos los parientes hasta el sexto grado.",
            "Los hijos, personalmente o representados por su descendencia; los ascendientes; "
            "y el cónyuge sobreviviente.",
            "Solo los hijos.",
            "Los hermanos y los sobrinos.",
        ],
        "B",
        "Es la B porque esa es la enumeración del art. 1182; la Ley 20.830 agregó al "
        "conviviente civil sobreviviente, con los mismos derechos que el cónyuge. La A no, "
        "porque los colaterales no son legitimarios. La C no, porque también lo son los "
        "ascendientes y el cónyuge. La D no, porque hermanos y sobrinos pueden heredar "
        "abintestato, pero no son legitimarios.",
        f"{CC}, art. 1182; Ley 20.830, art. 16; {UC}, VIII, cap. V, 2.4.3.2.2",
    ),
    (
        "Acción de reforma y desheredamiento",
        2,
        "Un padre deja toda su herencia a una fundación y nada a su hijo. ¿Qué acción "
        "tiene el hijo?",
        [
            "La acción de nulidad del testamento.",
            "La acción de reforma de testamento, para que se le asigne lo que por ley le "
            "corresponde; prescribe en cuatro años contados desde que tuvo conocimiento del "
            "testamento y de su calidad de legitimario.",
            "La acción reivindicatoria contra la fundación.",
            "Ninguna, porque el testador es libre.",
        ],
        "B",
        "Es la B porque el art. 1216 concede la acción de reforma a los legitimarios a "
        "quienes el testador no haya dejado lo que por ley les corresponde, con el plazo de "
        "prescripción indicado. La A no, porque el testamento no es nulo: solo vulnera las "
        "legítimas. La C no, porque la reforma es la acción específica. La D no, porque la "
        "libertad de testar está limitada por las asignaciones forzosas.",
        f"{CC}, arts. 1167 y 1216; {UC}, VIII, cap. V, 2.4.4",
    ),
    (
        "Acción de reforma y desheredamiento",
        3,
        "¿Qué requisitos debe cumplir el desheredamiento para ser válido?",
        [
            "Basta que el testador lo diga en el testamento.",
            "Que se haga por testamento, que se exprese la causa legal específica y que esta "
            "se haya probado judicialmente en vida del testador, o se pruebe después de su "
            "muerte por las personas a quienes interesa el desheredamiento.",
            "Que el legitimario lo acepte.",
            "Que lo apruebe un juez de familia en vida del testador, siempre.",
        ],
        "B",
        "Es la B porque el desheredamiento es la disposición testamentaria en que se ordena "
        "que un legitimario sea privado del todo o parte de su legítima (art. 1207), y el art. "
        "1209 exige que la causa esté especificada en el testamento y probada judicialmente, "
        "en vida del testador o después de su muerte. Las causales están en el art. 1208. La "
        "A no, porque se requiere causa legal y prueba. La C no, porque no se requiere la "
        "aceptación del desheredado. La D no, porque la prueba también puede rendirse "
        "después de la muerte del testador.",
        f"{CC}, arts. 1207, 1208 y 1209; {UC}, VIII, cap. V, 3",
    ),
    (
        "Partición, deudas hereditarias y beneficio de separación",
        2,
        "Tres herederos por partes iguales heredan una deuda de $900.000 del causante. Si "
        "no hay otra regla aplicable, ¿cuánto puede cobrar el acreedor a cada uno?",
        [
            "$900.000 a cualquiera.",
            "$300.000 a cada uno, porque las deudas hereditarias se dividen entre los "
            "herederos a prorrata de sus cuotas.",
            "Todo al heredero que tenga más bienes.",
            "Nada, porque las deudas se extinguen con la muerte.",
        ],
        "B",
        "Es la B porque el art. 1354 dispone que las deudas hereditarias se dividen entre "
        "los herederos a prorrata de sus cuotas; hay excepciones, como la acción hipotecaria "
        "o las obligaciones indivisibles (art. 1526). La A no, porque la deuda no es "
        "solidaria entre los herederos. La C no, porque no hay tal regla. La D no, porque las "
        "deudas se transmiten a los herederos.",
        f"{CC}, arts. 1354 y 1526; {UC}, VIII, cap. VII",
    ),
    (
        "Partición, deudas hereditarias y beneficio de separación",
        3,
        "Los acreedores del causante temen que el heredero, que tiene muchas deudas propias, "
        "confunda los bienes de la herencia con los suyos. ¿Qué pueden pedir?",
        [
            "La nulidad de la aceptación.",
            "El beneficio de separación: que no se confundan los bienes del difunto con los "
            "del heredero, para que con los bienes del difunto se les paguen sus créditos con "
            "preferencia a las deudas propias del heredero.",
            "El beneficio de inventario en nombre del heredero.",
            "La declaración de herencia yacente.",
        ],
        "B",
        "Es la B porque así lo establece el art. 1378. La A no, porque la aceptación es "
        "válida. La C no, porque el beneficio de inventario lo invoca el heredero en su "
        "propio favor. La D no, porque la herencia ya fue aceptada.",
        f"{CC}, arts. 1378 y 1382; {UC}, VIII, cap. VIII",
    ),
]
