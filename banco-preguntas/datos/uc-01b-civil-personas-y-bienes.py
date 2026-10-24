"""Cédula UC de Derecho Civil, partes III (Personas) y IV (Bienes)."""

JURISDICCION = "Chile"
PROGRAMA = "Cédulas UC (licenciatura, vigentes desde 2021)"
CEDULA = "Cédula 1: Derecho Civil (15-03-2021)"
MATERIA = "Derecho Civil"

CC = "Código Civil"
UC = "Cédula UC Derecho Civil"

PREGUNTAS = [
    # ------------------------------------------------------------------ III. Personas
    (
        "Persona natural y atributos de la personalidad",
        1,
        "¿Cuál de los siguientes NO es un atributo de la personalidad?",
        [
            "El nombre.",
            "El domicilio.",
            "La profesión u oficio.",
            "La capacidad de goce.",
        ],
        "C",
        "Es la C porque la profesión u oficio no es una cualidad inherente a toda persona; "
        "los atributos de la personalidad, según la doctrina, son la capacidad de goce, la "
        "nacionalidad, el nombre, el estado civil, el domicilio y el patrimonio. La A no, "
        "porque toda persona tiene un nombre que la individualiza. La B no, porque el "
        "domicilio es la sede jurídica de la persona. La D no, porque la capacidad de goce es "
        "el atributo por excelencia: la aptitud para adquirir derechos.",
        f"{CC}, arts. 55 y 59; {UC}, III, cap. I, 2.1",
    ),
    (
        "Persona natural y atributos de la personalidad",
        2,
        "Según la Ley 17.344, ¿en cuál de estos casos una persona puede pedir el cambio de "
        "su nombre?",
        [
            "Cuando simplemente prefiere un nombre más moderno.",
            "Cuando ha sido conocida durante más de cinco años, por motivos plausibles, con un "
            "nombre diferente del propio.",
            "Cuando su nombre coincide con el de una persona famosa.",
            "Nunca: el nombre es inmutable.",
        ],
        "B",
        "Es la B porque es una de las causales del art. 1 de la Ley 17.344; las otras incluyen "
        "nombres ridículos, risibles o que menoscaben moral o materialmente al solicitante. "
        "La A no, porque la sola preferencia no es causal. La C no, porque la coincidencia "
        "con un nombre ajeno no está prevista como tal. La D no, porque el nombre puede "
        "cambiarse por las causales legales, aunque es en principio inmutable.",
        f"Ley 17.344, art. 1; {UC}, III, cap. I, 2.4.3",
    ),
    (
        "Domicilio",
        1,
        "¿Cómo define el Código Civil el domicilio?",
        [
            "El lugar donde la persona nació.",
            "La residencia acompañada, real o presuntivamente, del ánimo de permanecer en ella.",
            "El lugar donde la persona se encuentra en un momento dado.",
            "El lugar donde la persona está inscrita para votar.",
        ],
        "B",
        "Es la B porque es la definición del art. 59: el domicilio tiene un elemento material "
        "(la residencia) y uno psicológico (el ánimo de permanecer). La A no, porque el lugar "
        "de nacimiento no determina el domicilio. La C no, porque la mera habitación o "
        "residencia ocasional no es domicilio. La D no, porque el domicilio electoral es un "
        "concepto distinto del domicilio civil.",
        f"{CC}, arts. 59 y 62; {UC}, III, cap. I, 2.7",
    ),
    (
        "Domicilio",
        2,
        "Una persona se traslada temporalmente por dos años a otra ciudad por trabajo, pero "
        "conserva allá su familia y el asiento principal de sus negocios. ¿Cambia su "
        "domicilio civil?",
        [
            "Sí, porque reside en la nueva ciudad.",
            "Sí, pero solo después de un año de residencia.",
            "No, porque el domicilio civil no se muda por residir largo tiempo en otra parte, "
            "si se conserva la familia y el asiento principal de los negocios en el domicilio "
            "anterior.",
            "No, porque el domicilio nunca puede cambiar.",
        ],
        "C",
        "Es la C porque así lo dispone el art. 65: falta el ánimo de permanecer en el nuevo "
        "lugar. La A no, porque la residencia por sí sola no basta. La B no, porque la ley no "
        "fija un plazo para mudar el domicilio. La D no, porque el domicilio sí puede cambiar "
        "cuando concurren residencia y ánimo de permanecer.",
        f"{CC}, arts. 59 y 65; {UC}, III, cap. I, 2.7",
    ),
    (
        "Patrimonio",
        2,
        "Según la teoría clásica del patrimonio (Aubry y Rau), ¿cuál de estas afirmaciones "
        "es correcta?",
        [
            "Una persona puede tener varios patrimonios generales.",
            "El patrimonio es un atributo de la personalidad: toda persona tiene un "
            "patrimonio y solo uno, y es inalienable mientras viva.",
            "El patrimonio solo comprende los bienes, no las deudas.",
            "Solo las personas ricas tienen patrimonio.",
        ],
        "B",
        "Es la B porque la teoría clásica concibe el patrimonio como emanación de la "
        "personalidad: toda persona tiene uno, solo uno, y no puede enajenarlo entre vivos. "
        "La teoría del patrimonio-afectación, en cambio, admite patrimonios destinados a un "
        "fin. La A no, porque contradice la unidad del patrimonio. La C no, porque el "
        "patrimonio comprende derechos y obligaciones avaluables en dinero. La D no, porque "
        "aun quien no tiene bienes tiene un patrimonio, aunque esté vacío.",
        f"{UC}, III, cap. I, 2.6",
    ),
    (
        "Patrimonio",
        3,
        "¿Qué institución del derecho chileno suele citarse como argumento a favor de la "
        "teoría del patrimonio-afectación?",
        [
            "El patrimonio reservado de la mujer casada en sociedad conyugal (art. 150).",
            "La compraventa de bienes muebles.",
            "El domicilio convencional.",
            "La capacidad de goce de los recién nacidos.",
        ],
        "A",
        "Es la A porque el patrimonio reservado es un conjunto de bienes separado, afecto a "
        "la actividad de la mujer y con reglas propias de administración y responsabilidad, "
        "lo que se aviene mal con la unidad del patrimonio de la teoría clásica. Suele "
        "citarse también el beneficio de inventario. La B no, porque la compraventa no "
        "supone patrimonios separados. La C no, porque el domicilio convencional no tiene "
        "relación con el patrimonio. La D no, porque la capacidad de goce de todos es, más "
        "bien, compatible con la teoría clásica.",
        f"{CC}, arts. 150 y 1247; {UC}, III, cap. I, 2.6",
    ),
    (
        "Inicio de la persona y protección del que está por nacer",
        1,
        "¿Cuándo principia la existencia legal de una persona según el Código Civil?",
        [
            "Desde la concepción.",
            "Al nacer, esto es, al separarse completamente de su madre.",
            "Al inscribirse en el Registro Civil.",
            "A las 24 horas de nacida.",
        ],
        "B",
        "Es la B porque el art. 74 inc. 1 dispone que la existencia legal de toda persona "
        "principia al nacer, esto es, al separarse completamente de su madre; si la criatura "
        "muere en el vientre materno o antes de estar completamente separada, o no sobrevive "
        "un momento siquiera, se reputa no haber existido jamás (inc. 2). La A no, porque la "
        "concepción marca el inicio de la protección del que está por nacer (art. 75), no la "
        "existencia legal. La C no, porque la inscripción solo prueba el nacimiento. La D no, "
        "porque el Código chileno no exige viabilidad ni un plazo de sobrevida.",
        f"{CC}, arts. 74 y 75; {UC}, III, cap. I, 3",
    ),
    (
        "Inicio de la persona y protección del que está por nacer",
        2,
        "Un hombre muere y en su testamento deja un legado a su hija, que está en el vientre "
        "materno. ¿Qué ocurre con ese derecho?",
        [
            "Se pierde, porque la hija aún no es persona.",
            "Se suspende hasta que el nacimiento se efectúe; si la criatura nace y constituye "
            "persona, entra en el goce del derecho como si hubiese existido al tiempo en que "
            "se le defirió.",
            "Pasa inmediatamente a la madre en propiedad.",
            "Se entrega al Fisco hasta que la hija cumpla 18 años.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 77: los derechos que se deferirían a la "
        "criatura que está en el vientre materno quedan suspensos hasta que el nacimiento se "
        "efectúe. Si nace y constituye persona, entra en su goce retroactivamente; si no, "
        "pasan a otras personas como si la criatura no hubiese existido jamás. La A no, "
        "porque la ley protege esos derechos. La C no, porque la madre no los adquiere. La D "
        "no, porque no hay intervención del Fisco.",
        f"{CC}, art. 77; {UC}, III, cap. I, 3.1.2.2",
    ),
    (
        "Término de la persona: muerte real y presunta",
        2,
        "En la declaración de muerte presunta, ¿qué día fija el juez como día presuntivo de "
        "la muerte, como regla general?",
        [
            "El día en que se dicta la sentencia.",
            "El día de las últimas noticias.",
            "El último día del primer bienio contado desde la fecha de las últimas noticias.",
            "El día en que el desaparecido cumpliría 70 años.",
        ],
        "C",
        "Es la C porque el art. 81 n.° 6 dispone que el juez fijará como día presuntivo de la "
        "muerte el último del primer bienio contado desde la fecha de las últimas noticias "
        "(hay reglas especiales para casos como la herida grave en la guerra o el naufragio). "
        "La A no, porque la fecha de la sentencia no es la del fallecimiento presunto. La B "
        "no, porque la ley da un margen de dos años. La D no, porque la edad de 70 años "
        "importa para conceder la posesión definitiva, no para fijar el día presuntivo.",
        f"{CC}, art. 81; {UC}, III, cap. I, 4.2",
    ),
    (
        "Término de la persona: muerte real y presunta",
        3,
        "Han transcurrido diez años desde las últimas noticias de un desaparecido. ¿Qué "
        "puede hacer el juez?",
        [
            "Nada, porque deben pasar treinta años.",
            "Conceder la posesión definitiva de sus bienes, cualquiera que fuese, a la "
            "expiración de esos diez años, la edad del desaparecido si viviese.",
            "Solo conceder la posesión provisoria.",
            "Declarar la muerte real del desaparecido.",
        ],
        "B",
        "Es la B porque el art. 82 permite conceder la posesión definitiva transcurridos diez "
        "años desde la fecha de las últimas noticias, cualquiera que fuese la edad del "
        "desaparecido; también puede concederla cumplidos cinco años si se prueba que han "
        "transcurrido setenta desde su nacimiento. La A no, porque la ley no exige treinta "
        "años. La C no, porque, pasado ese plazo, procede la posesión definitiva. La D no, "
        "porque la muerte presunta no se transforma en real; la muerte real requiere otra "
        "prueba.",
        f"{CC}, arts. 81 y 82; {UC}, III, cap. I, 4.2.2",
    ),
    (
        "Personas jurídicas",
        1,
        "¿Qué diferencia principal hay entre una corporación y una fundación?",
        [
            "La corporación persigue fines de lucro y la fundación no.",
            "La corporación es una agrupación de personas que se unen para un fin común; la "
            "fundación es un conjunto de bienes destinado por su fundador a un fin de interés "
            "general.",
            "La corporación es de derecho público y la fundación de derecho privado.",
            "No hay diferencia: son sinónimos.",
        ],
        "B",
        "Es la B porque esa es la distinción clásica: en la corporación (o asociación) el "
        "elemento esencial son las personas; en la fundación, el patrimonio afecto a un fin. "
        "La A no, porque ambas son personas jurídicas sin fines de lucro (Título XXXIII del "
        "Libro I). La C no, porque ambas son de derecho privado. La D no, porque son figuras "
        "distintas.",
        f"{CC}, arts. 545 y siguientes; {UC}, III, cap. II, 2.2.1",
    ),
    (
        "Personas jurídicas",
        2,
        "¿Cómo define el art. 545 a la persona jurídica?",
        [
            "Como una persona ficticia, capaz de ejercer derechos y contraer obligaciones "
            "civiles, y de ser representada judicial y extrajudicialmente.",
            "Como toda agrupación de personas, aunque no tenga reconocimiento legal.",
            "Como una persona natural que ejerce una actividad comercial.",
            "Como un órgano del Estado.",
        ],
        "A",
        "Es la A porque es la definición del art. 545 inc. 1, que recoge la teoría de la "
        "ficción. La B no, porque la personalidad jurídica requiere reconocimiento conforme a "
        "la ley. La C no, porque una persona natural comerciante sigue siendo persona "
        "natural. La D no, porque el Código regula personas jurídicas de derecho privado; las "
        "de derecho público se rigen por leyes especiales (art. 547).",
        f"{CC}, arts. 545 y 547; {UC}, III, cap. II, 1",
    ),
    # ------------------------------------------------------------------- IV. Bienes
    (
        "Cosas corporales e incorporales; derechos reales y personales",
        1,
        "¿Qué es un derecho real según el Código Civil?",
        [
            "El que solo puede reclamarse de ciertas personas que han contraído la obligación "
            "correlativa.",
            "El que tenemos sobre una cosa sin respecto a determinada persona.",
            "El que corresponde exclusivamente al Estado.",
            "El que recae sobre hechos y no sobre cosas.",
        ],
        "B",
        "Es la B porque es la definición del art. 577; son derechos reales el dominio, la "
        "herencia, el usufructo, el uso o habitación, las servidumbres activas, la prenda y "
        "la hipoteca. La A no, porque es la definición del derecho personal o crédito (art. "
        "578). La C no, porque los particulares son titulares de derechos reales. La D no, "
        "porque los hechos que se deben son objeto de derechos personales (art. 581).",
        f"{CC}, arts. 577, 578 y 581; {UC}, IV, cap. II, 1.2.2",
    ),
    (
        "Cosas corporales e incorporales; derechos reales y personales",
        2,
        "¿Qué dispone el art. 583 sobre las cosas incorporales?",
        [
            "Que no pueden ser objeto de ningún derecho.",
            "Que sobre ellas hay también una especie de propiedad: por ejemplo, el usufructuario "
            "tiene la propiedad de su derecho de usufructo.",
            "Que solo el Estado puede ser dueño de ellas.",
            "Que se reputan siempre inmuebles.",
        ],
        "B",
        "Es la B porque el art. 583 dispone que sobre las cosas incorporales hay también una "
        "especie de propiedad, y da el ejemplo del usufructuario; la Constitución protege "
        "también la propiedad sobre bienes incorporales (art. 19 n.° 24). La A no, porque la "
        "ley reconoce derechos sobre ellas. La C no, porque los particulares pueden ser "
        "titulares. La D no, porque se reputan muebles o inmuebles según la cosa sobre que se "
        "ejercen o que se debe (art. 580).",
        f"{CC}, arts. 580 y 583; Constitución, art. 19 n.° 24; {UC}, IV, cap. II, 1.2.3",
    ),
    (
        "Cosas muebles e inmuebles",
        2,
        "Un tractor está permanentemente destinado al cultivo de un fundo. ¿Cómo lo califica "
        "el Código Civil?",
        [
            "Como mueble por anticipación.",
            "Como inmueble por adherencia.",
            "Como inmueble por destinación.",
            "Como mueble por naturaleza, sin excepción.",
        ],
        "C",
        "Es la C porque el art. 570 reputa inmuebles, aunque por su naturaleza no lo sean, "
        "las cosas permanentemente destinadas al uso, cultivo y beneficio de un inmueble, "
        "aunque puedan separarse sin detrimento; menciona expresamente los utensilios de "
        "labranza. La A no, porque los muebles por anticipación son productos de un inmueble "
        "o cosas accesorias a él que se reputan muebles para constituir un derecho sobre "
        "ellos a favor de otra persona que el dueño (art. 571). La B no, porque el tractor no "
        "está adherido al suelo (art. 568). La D no, porque la ley hace esta excepción.",
        f"{CC}, arts. 567, 568, 570 y 571; {UC}, IV, cap. II, 2",
    ),
    (
        "Cosas muebles e inmuebles",
        3,
        "Un acreedor tiene derecho a que su deudor le entregue un inmueble vendido. ¿Cómo se "
        "califica ese derecho personal?",
        [
            "Como mueble, porque todos los créditos son muebles.",
            "Como inmueble, porque los derechos se reputan muebles o inmuebles según lo sea la "
            "cosa en que han de ejercerse o que se debe.",
            "Ni mueble ni inmueble: los créditos no se clasifican.",
            "Como mueble, porque se trata de un hecho que se debe.",
        ],
        "B",
        "Es la B porque el art. 580 dispone que los derechos y acciones se reputan bienes "
        "muebles o inmuebles según lo sea la cosa en que han de ejercerse o que se debe, y da "
        "como ejemplo la acción del comprador para que se le entregue la finca comprada. La A "
        "no, porque la calificación depende de la cosa debida. La C no, porque el art. 580 sí "
        "los clasifica. La D no, porque aquí se debe una cosa, no un hecho; los hechos que se "
        "deben se reputan muebles (art. 581).",
        f"{CC}, arts. 580 y 581; {UC}, IV, cap. II, 2.2",
    ),
    (
        "Cosas consumibles, fungibles, singulares y universales",
        2,
        "¿Qué distingue a una cosa fungible de una consumible?",
        [
            "Son sinónimos en la doctrina.",
            "Fungible es la que tiene un mismo poder liberatorio que otras de su género (se "
            "puede reemplazar por otra igual); consumible es la que se destruye natural o "
            "civilmente por el primer uso.",
            "Fungible es la que se destruye con el primer uso; consumible, la que puede "
            "reemplazarse.",
            "Fungible es siempre un inmueble.",
        ],
        "B",
        "Es la B porque esa es la distinción doctrinaria; el art. 575 confunde ambas nociones, "
        "pero la doctrina las separa: el dinero, por ejemplo, es fungible y civilmente "
        "consumible, mientras que un libro de una misma edición es fungible y no consumible. "
        "La A no, porque la doctrina sí las distingue. La C no, porque invierte los conceptos. "
        "La D no, porque la fungibilidad es propia de cosas muebles.",
        f"{CC}, art. 575; {UC}, IV, cap. II, 3 y 4",
    ),
    (
        "Cosas consumibles, fungibles, singulares y universales",
        3,
        "¿Qué diferencia una universalidad de derecho de una universalidad de hecho?",
        [
            "La de derecho tiene activo y pasivo (como la herencia); la de hecho es un "
            "conjunto de bienes que conservan su individualidad, sin pasivo propio (como una "
            "biblioteca o un rebaño).",
            "La de hecho tiene activo y pasivo; la de derecho no.",
            "La de derecho solo comprende inmuebles.",
            "No hay diferencia: ambas son cosas singulares.",
        ],
        "A",
        "Es la A porque la universalidad de derecho (la herencia, el patrimonio) contiene "
        "elementos activos y pasivos y opera en ella la subrogación real; la de hecho es una "
        "pluralidad de cosas que se agrupan por un destino común, sin pasivo. La B no, porque "
        "invierte los conceptos. La C no, porque la herencia, por ejemplo, comprende muebles e "
        "inmuebles. La D no, porque ambas son cosas universales, no singulares.",
        f"{CC}, arts. 951 y 1317; {UC}, IV, cap. II, 5",
    ),
    (
        "Dominio: concepto, características y facultades",
        1,
        "¿Cómo define el art. 582 el dominio?",
        [
            "Como el derecho a usar una cosa ajena.",
            "Como el derecho real en una cosa corporal, para gozar y disponer de ella "
            "arbitrariamente; no siendo contra la ley o contra derecho ajeno.",
            "Como la tenencia de una cosa con ánimo de señor o dueño.",
            "Como el derecho personal a exigir la entrega de una cosa.",
        ],
        "B",
        "Es la B porque es la definición del art. 582. La A no, porque eso se parece al "
        "derecho de uso (art. 811), que es un derecho real limitado. La C no, porque esa es "
        "la definición de posesión (art. 700). La D no, porque eso es un crédito, no un "
        "derecho real.",
        f"{CC}, arts. 582 y 700; {UC}, IV, cap. III, 1",
    ),
    (
        "Dominio: concepto, características y facultades",
        2,
        "¿Cuál de las siguientes es una facultad del dueño que normalmente NO se transfiere "
        "al usufructuario?",
        [
            "El uso de la cosa.",
            "El goce de la cosa (percibir sus frutos).",
            "La disposición de la cosa (enajenarla o destruirla).",
            "La administración ordinaria de la cosa.",
        ],
        "C",
        "Es la C porque el usufructo confiere la facultad de gozar de una cosa con cargo de "
        "conservar su forma y sustancia y restituirla (art. 764): el nudo propietario "
        "conserva la disposición. La A no, porque el usufructuario usa la cosa. La B no, "
        "porque el usufructuario se hace dueño de los frutos. La D no, porque el "
        "usufructuario administra la cosa para gozarla.",
        f"{CC}, arts. 582 y 764; {UC}, IV, cap. III, 1.3",
    ),
    (
        "Copropiedad",
        2,
        "Tres hermanos son dueños en común de un departamento. Uno de ellos quiere poner "
        "término a la comunidad. ¿Puede hacerlo?",
        [
            "No, porque requiere la unanimidad de los comuneros.",
            "Sí, porque ninguno de los coasignatarios de una cosa universal o singular está "
            "obligado a permanecer en la indivisión; la partición puede pedirse siempre, salvo "
            "pacto de indivisión.",
            "Solo si han transcurrido diez años desde que se formó la comunidad.",
            "Solo si el juez considera que la indivisión es perjudicial.",
        ],
        "B",
        "Es la B porque el art. 1317 consagra el derecho a pedir la partición en cualquier "
        "tiempo; el pacto de indivisión no puede durar más de cinco años, aunque puede "
        "renovarse. La A no, porque basta la voluntad de uno. La C no, porque no hay plazo "
        "mínimo. La D no, porque el comunero no necesita justificar su petición.",
        f"{CC}, art. 1317; {UC}, IV, cap. III, 2.3",
    ),
    (
        "Copropiedad",
        3,
        "¿Cuál de estas es una causal de extinción de la comunidad según el art. 2312?",
        [
            "La muerte de uno de los comuneros.",
            "El arrendamiento de la cosa común a un tercero.",
            "La reunión de las cuotas de todos los comuneros en una sola persona.",
            "La inscripción de la cosa a nombre de todos los comuneros.",
        ],
        "C",
        "Es la C porque el art. 2312 señala que la comunidad termina por la reunión de las "
        "cuotas de todos los comuneros en una sola persona, por la destrucción de la cosa "
        "común y por la división del haber común. La A no, porque la cuota del comunero "
        "muerto pasa a sus herederos y la comunidad sigue. La B no, porque arrendar es un "
        "acto de administración. La D no, porque inscribir a nombre de todos confirma la "
        "comunidad.",
        f"{CC}, arts. 2304 y 2312; {UC}, IV, cap. III, 2.6",
    ),
    (
        "Modos de adquirir y tradición: requisitos",
        1,
        "En el sistema chileno, ¿qué se necesita para adquirir el dominio de una cosa que se "
        "compra?",
        [
            "Basta el contrato de compraventa.",
            "Un título (la compraventa) y un modo de adquirir (la tradición).",
            "Basta la tradición, sin título alguno.",
            "Basta el pago del precio.",
        ],
        "B",
        "Es la B porque Chile sigue el sistema del título y el modo: el contrato solo genera "
        "la obligación de transferir y el dominio se adquiere por la tradición (arts. 588, "
        "670 y 675). La A no, porque el contrato no transfiere el dominio por sí solo, a "
        "diferencia del sistema francés. La C no, porque la tradición requiere un título "
        "traslaticio de dominio (art. 675). La D no, porque el pago del precio es una "
        "obligación del comprador, no un modo de adquirir.",
        f"{CC}, arts. 588, 670 y 675; {UC}, IV, cap. III, 3.1",
    ),
    (
        "Modos de adquirir y tradición: requisitos",
        3,
        "Se hace la tradición de un inmueble en cumplimiento de una compraventa que luego se "
        "declara nula. ¿Qué efecto tiene la nulidad del título sobre la tradición?",
        [
            "Ninguno: la tradición es abstracta y transfiere el dominio igual.",
            "La tradición no transfiere el dominio, porque para que valga se requiere un "
            "título traslaticio de dominio válido.",
            "La tradición transfiere el dominio, pero el comprador debe pagar una multa.",
            "La tradición se convierte en donación.",
        ],
        "B",
        "Es la B porque el art. 675 exige para la validez de la tradición un título "
        "traslaticio de dominio, y agrega que se requiere además que el título sea válido "
        "respecto de la persona a quien se confiere: la tradición es causal en Chile. La A "
        "no, porque Chile no sigue el sistema de la tradición abstracta. La C no, porque la "
        "ley no prevé tal multa. La D no, porque no hay conversión en donación.",
        f"{CC}, art. 675; {UC}, IV, cap. III, 3.2.2.3",
    ),
    (
        "Efectos y especies de tradición",
        2,
        "Andrés vende y entrega un reloj que no era suyo. ¿Qué adquiere el comprador por "
        "esa tradición?",
        [
            "El dominio del reloj, porque actuó de buena fe.",
            "Nada, porque la tradición es nula.",
            "Los derechos transmisibles que tenía Andrés sobre el reloj y, además, la posesión, "
            "que le permite adquirir el dominio por prescripción.",
            "Solo la mera tenencia del reloj.",
        ],
        "C",
        "Es la C porque, si el tradente no es el verdadero dueño, no se adquieren por la "
        "tradición otros derechos que los transmisibles del mismo tradente sobre la cosa "
        "(art. 682), pero la tradición da al adquirente el derecho de ganar por prescripción "
        "el dominio (art. 683). La A no, porque nadie transfiere más derechos que los que "
        "tiene. La B no, porque la tradición no es nula: es inoponible al verdadero dueño. La "
        "D no, porque el adquirente entra en posesión, no en mera tenencia.",
        f"{CC}, arts. 682 y 683; {UC}, IV, cap. III, 3.2.3.2",
    ),
    (
        "Efectos y especies de tradición",
        2,
        "¿Cómo se efectúa la tradición del dominio de un inmueble?",
        [
            "Por la entrega de las llaves.",
            "Por la sola firma de la escritura pública de compraventa.",
            "Por la inscripción del título en el Registro del Conservador de Bienes Raíces.",
            "Por la ocupación material del inmueble durante un año.",
        ],
        "C",
        "Es la C porque el art. 686 dispone que la tradición del dominio de los bienes raíces "
        "se efectúa por la inscripción del título en el Registro del Conservador. La A no, "
        "porque la entrega de las llaves es una forma de tradición de los muebles (art. 684). "
        "La B no, porque la escritura es el título (solemnidad de la compraventa), no el modo. "
        "La D no, porque la ocupación material no es tradición.",
        f"{CC}, arts. 684 y 686; {UC}, IV, cap. III, 3.2.4.7",
    ),
    (
        "Posesión",
        1,
        "¿Qué es la posesión según el Código Civil?",
        [
            "El derecho real de dominio.",
            "La tenencia de una cosa determinada con ánimo de señor o dueño.",
            "La tenencia de una cosa en lugar o a nombre del dueño.",
            "Un derecho personal contra el dueño.",
        ],
        "B",
        "Es la B porque es la definición del art. 700: la posesión tiene un elemento material "
        "(corpus, la tenencia) y uno psicológico (animus, el ánimo de señor o dueño); el "
        "poseedor es reputado dueño mientras otra persona no justifica serlo. La A no, porque "
        "se puede poseer sin ser dueño y ser dueño sin poseer. La C no, porque esa es la mera "
        "tenencia (art. 714). La D no, porque la posesión es un hecho, no un crédito.",
        f"{CC}, arts. 700 y 714; {UC}, IV, cap. III, 3.3.1",
    ),
    (
        "Posesión",
        2,
        "¿Qué requisitos debe reunir la posesión regular?",
        [
            "Haber durado al menos diez años.",
            "Justo título y buena fe, y además tradición si el título es traslaticio de dominio.",
            "Que el poseedor sea dueño de la cosa.",
            "Que la posesión haya sido violenta o clandestina.",
        ],
        "B",
        "Es la B porque así la define el art. 702: procede de justo título y ha sido "
        "adquirida de buena fe, aunque la buena fe no subsista después; si el título es "
        "traslaticio de dominio, es también necesaria la tradición. La A no, porque el tiempo "
        "es un requisito de la prescripción, no de la posesión regular. La C no, porque el "
        "poseedor no necesita ser dueño. La D no, porque la violenta y la clandestina son "
        "posesiones viciosas (art. 709).",
        f"{CC}, arts. 702 y 709; {UC}, IV, cap. III, 3.3.1.4",
    ),
    (
        "Prescripción adquisitiva",
        2,
        "¿Cuáles son los plazos de la prescripción adquisitiva ordinaria y extraordinaria?",
        [
            "Ordinaria: 2 años para muebles y 5 para inmuebles; extraordinaria: 10 años.",
            "Ordinaria: 5 años para muebles y 10 para inmuebles; extraordinaria: 30 años.",
            "Ordinaria y extraordinaria: 10 años en todos los casos.",
            "Ordinaria: 1 año; extraordinaria: 5 años.",
        ],
        "A",
        "Es la A porque el art. 2508 fija la ordinaria en dos años para los muebles y cinco "
        "para los bienes raíces, y el art. 2511 fija la extraordinaria en diez años. La "
        "ordinaria requiere posesión regular; la extraordinaria se basta con la irregular. La "
        "B no, porque esos plazos no son los vigentes. La C no, porque la ordinaria es más "
        "breve. La D no, porque son plazos inventados.",
        f"{CC}, arts. 2507, 2508, 2510 y 2511; {UC}, IV, cap. III, 3.3.6",
    ),
    (
        "Prescripción adquisitiva",
        3,
        "Un menor de edad es dueño de un inmueble poseído por otro. ¿Qué efecto tiene la "
        "menor edad del dueño sobre la prescripción del poseedor?",
        [
            "Ninguno: ninguna prescripción se suspende.",
            "Suspende la prescripción ordinaria a favor del menor, pero no la extraordinaria.",
            "Suspende tanto la ordinaria como la extraordinaria.",
            "Interrumpe la prescripción y hace perder todo el tiempo transcurrido.",
        ],
        "B",
        "Es la B porque la prescripción ordinaria se suspende a favor de los menores y demás "
        "personas enumeradas en el art. 2509, mientras que la extraordinaria no se suspende a "
        "favor de ellos (art. 2511). La A no, porque la ordinaria sí se suspende. La C no, "
        "porque la extraordinaria no se suspende. La D no, porque la suspensión detiene el "
        "cómputo pero no borra el tiempo anterior, a diferencia de la interrupción.",
        f"{CC}, arts. 2509 y 2511; {UC}, IV, cap. III, 3.3.6",
    ),
    (
        "Usufructo",
        1,
        "Se constituye un usufructo sin fijar plazo a favor de una persona natural. ¿Cuánto dura?",
        [
            "Cinco años.",
            "Toda la vida del usufructuario.",
            "Treinta años.",
            "Hasta que el nudo propietario lo revoque.",
        ],
        "B",
        "Es la B porque el art. 770 dispone que, si no se fija tiempo alguno para su "
        "duración, el usufructo se entiende constituido por toda la vida del usufructuario; "
        "si el usufructuario es una corporación o fundación, no puede pasar de treinta años. "
        "La A no, porque no existe ese plazo supletorio. La C no, porque los treinta años son "
        "el máximo para personas jurídicas. La D no, porque el usufructo no es revocable a "
        "voluntad del nudo propietario.",
        f"{CC}, arts. 764 y 770; {UC}, IV, cap. III, 4.3.1.1",
    ),
    (
        "Usufructo",
        3,
        "Se constituye usufructo sobre una suma de dinero. ¿Cómo se denomina esta figura y "
        "qué debe restituir el usufructuario?",
        [
            "Usufructo propiamente tal; debe restituir los mismos billetes.",
            "Cuasiusufructo; el usufructuario se hace dueño del dinero y debe restituir otro "
            "tanto de igual cantidad y calidad, o su valor.",
            "Comodato; debe restituir los mismos billetes.",
            "Usufructo nulo, porque no puede recaer sobre cosas consumibles.",
        ],
        "B",
        "Es la B porque el art. 789 regula el usufructo sobre cosas fungibles o consumibles "
        "(cuasiusufructo): el usufructuario se hace dueño de ellas y queda obligado a "
        "restituir otras tantas del mismo género y calidad, o su valor. La A no, porque es "
        "imposible conservar la sustancia de una cosa que se consume. La C no, porque el "
        "comodato es un préstamo de uso de cosas no consumibles. La D no, porque la ley "
        "admite expresamente esta figura.",
        f"{CC}, arts. 764 y 789; {UC}, IV, cap. III, 4.3.1.1",
    ),
    (
        "Acción reivindicatoria y prestaciones mutuas",
        2,
        "¿Quién puede ejercer la acción reivindicatoria y contra quién?",
        [
            "El poseedor contra el dueño.",
            "El dueño de una cosa singular, de que no está en posesión, contra el actual poseedor.",
            "El mero tenedor contra el dueño.",
            "Cualquier acreedor contra cualquier tercero.",
        ],
        "B",
        "Es la B porque el art. 889 define la reivindicación como la acción que tiene el "
        "dueño de una cosa singular, de que no está en posesión, para que el poseedor de ella "
        "sea condenado a restituírsela; el art. 895 la dirige contra el actual poseedor. La A "
        "no, porque invierte las partes. La C no, porque el mero tenedor no es dueño. La D "
        "no, porque la acción es del dueño, no de cualquier acreedor.",
        f"{CC}, arts. 889, 893 y 895; {UC}, IV, cap. III, 5",
    ),
    (
        "Acción reivindicatoria y prestaciones mutuas",
        3,
        "Un poseedor vencido en un juicio reivindicatorio hizo en la cosa mejoras útiles. "
        "¿Tiene derecho a que se le abonen?",
        [
            "Sí, siempre, como las necesarias.",
            "Solo si era poseedor de buena fe a la época en que las hizo; el de mala fe solo "
            "puede llevarse los materiales si pueden separarse sin detrimento.",
            "No, nunca, porque las mejoras benefician al dueño.",
            "Solo si el dueño lo autoriza.",
        ],
        "B",
        "Es la B porque el art. 909 solo abona las mejoras útiles al poseedor de buena fe, y "
        "el art. 910 permite al de mala fe llevarse los materiales separables sin detrimento, "
        "salvo que el dueño prefiera pagarle su valor. Las necesarias, en cambio, se abonan a "
        "todo poseedor (art. 908). La A no, porque confunde las útiles con las necesarias. La "
        "C no, porque el poseedor de buena fe sí tiene derecho. La D no, porque el abono no "
        "depende de la autorización del dueño.",
        f"{CC}, arts. 904, 908, 909 y 910; {UC}, IV, cap. III, 5.5",
    ),
]
