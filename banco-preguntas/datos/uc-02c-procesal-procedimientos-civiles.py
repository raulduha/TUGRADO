"""Cédula UC de Derecho Procesal, partes III y IV (Procedimientos civiles I y II)."""

JURISDICCION = "Chile"
PROGRAMA = "Cédulas UC (licenciatura, vigentes desde 2021)"
CEDULA = "Cédula 2: Derecho Procesal (15-03-2021)"
MATERIA = "Derecho Procesal"

COT = "Código Orgánico de Tribunales"
CPC = "Código de Procedimiento Civil"
UC = "Cédula UC Derecho Procesal"

PREGUNTAS = [
    # ------------------------------------------- III cap. I: medidas prejudiciales
    (
        "Medidas prejudiciales",
        2,
        "¿Qué finalidad tienen las medidas prejudiciales preparatorias?",
        [
            "Asegurar el resultado de la acción mediante el embargo de bienes.",
            "Preparar la entrada al juicio: obtener del futuro demandado antecedentes que el "
            "demandante necesita para demandar (por ejemplo, la exhibición de la cosa que será "
            "objeto de la acción o el reconocimiento de firma).",
            "Reemplazar la demanda.",
            "Ejecutar una sentencia extranjera.",
        ],
        "B",
        "Es la B porque las preparatorias (art. 273 CPC) buscan que el futuro demandante "
        "obtenga información para entrar al juicio: declaración jurada sobre la capacidad o "
        "calidad del demandado, exhibición de la cosa, de sentencias, testamentos o libros "
        "de contabilidad, reconocimiento de firma, entre otras. La A no, porque eso es propio "
        "de las prejudiciales precautorias. La C no, porque no reemplazan la demanda. La D "
        "no, porque la ejecución de sentencias extranjeras requiere exequátur.",
        f"{CPC}, arts. 273 y 288; {UC}, III, cap. I, 1",
    ),
    (
        "Medidas prejudiciales",
        3,
        "Se decreta una medida precautoria como prejudicial. ¿Qué carga tiene el solicitante y "
        "qué pasa si no la cumple?",
        [
            "Ninguna: la medida es indefinida.",
            "Debe presentar la demanda dentro de diez días (ampliables hasta treinta por motivos "
            "fundados) y pedir que se mantenga la medida; si no lo hace, la medida queda sin "
            "efecto de pleno derecho y responde de los perjuicios, presumiéndose dolo.",
            "Debe pagar una multa al Fisco.",
            "Debe obtener la confirmación de la Corte de Apelaciones.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 280 CPC; para decretarlas, el art. 279 exige "
        "además motivos graves y calificados, determinar el monto de los bienes y rendir "
        "fianza u otra garantía. La A no, porque la ley les fija un plazo. La C no, porque la "
        "sanción no es una multa. La D no, porque no requieren confirmación.",
        f"{CPC}, arts. 279 y 280; {UC}, III, cap. I, 3",
    ),
    # ------------------------------- III cap. II: juicio ordinario de mayor cuantía
    (
        "Demanda y emplazamiento",
        1,
        "¿Cuál de estos es un requisito de la demanda según el art. 254 CPC?",
        [
            "Acompañar la prueba testimonial.",
            "La exposición clara de los hechos y fundamentos de derecho en que se apoya, y la "
            "enunciación precisa y clara de las peticiones que se someten al fallo del tribunal.",
            "Que el demandado la firme.",
            "Que conste en escritura pública.",
        ],
        "B",
        "Es la B porque el art. 254 CPC exige, además de los requisitos comunes a todo "
        "escrito, la designación del tribunal, la individualización del demandante y del "
        "demandado, la exposición de los hechos y fundamentos de derecho y las peticiones "
        "concretas. La A no, porque la prueba se rinde después. La C no, porque el demandado "
        "no firma la demanda. La D no, porque no requiere escritura pública.",
        f"{CPC}, arts. 254 y 256; {UC}, III, cap. II, 2.1",
    ),
    (
        "Demanda y emplazamiento",
        2,
        "Un demandado es notificado personalmente en la misma comuna en que funciona el "
        "tribunal. ¿De qué plazo dispone para contestar la demanda en el juicio ordinario?",
        [
            "De 3 días.",
            "De 15 días.",
            "De 30 días.",
            "De 6 meses.",
        ],
        "B",
        "Es la B porque el art. 258 CPC fija el término de emplazamiento en quince días si el "
        "demandado es notificado en la comuna donde funciona el tribunal; se aumenta en tres "
        "días si lo es dentro del territorio jurisdiccional pero fuera de esa comuna, y según "
        "la tabla de emplazamiento si lo es fuera del territorio (art. 259). La A no, porque "
        "tres días es el traslado de los incidentes. La C no, porque no es el plazo legal "
        "base. La D no, porque seis meses es el plazo del abandono del procedimiento.",
        f"{CPC}, arts. 258 y 259; {UC}, III, cap. II, 2.2",
    ),
    (
        "Excepciones dilatorias y perentorias",
        2,
        "¿Qué caracteriza a las excepciones dilatorias en el juicio ordinario?",
        [
            "Atacan el fondo de la acción y se fallan en la sentencia definitiva.",
            "Se refieren a la corrección del procedimiento sin afectar el fondo de la acción, y "
            "deben oponerse todas en un mismo escrito y dentro del término de emplazamiento.",
            "Solo pueden oponerse en segunda instancia.",
            "Las resuelve la Corte Suprema.",
        ],
        "B",
        "Es la B porque así lo establecen los arts. 303 y 305 CPC; entre ellas están la "
        "incompetencia, la falta de capacidad o de personería, la litis pendencia, la "
        "ineptitud del libelo y el beneficio de excusión. La A no, porque eso describe las "
        "perentorias. La C no, porque se oponen al inicio del juicio. La D no, porque las "
        "resuelve el tribunal de la causa como incidente previo.",
        f"{CPC}, arts. 303 y 305; {UC}, III, cap. II, 2.3.3.1",
    ),
    (
        "Excepciones dilatorias y perentorias",
        3,
        "¿Cuáles excepciones perentorias pueden oponerse en cualquier estado de la causa, aunque "
        "no se hayan opuesto al contestar (excepciones anómalas)?",
        [
            "Todas las excepciones perentorias, sin límite de tiempo.",
            "La prescripción, la cosa juzgada, la transacción y el pago efectivo de la deuda "
            "cuando se funde en un antecedente escrito; deben alegarse por escrito antes de la "
            "citación para oír sentencia en primera instancia o de la vista de la causa en "
            "segunda.",
            "Solo la incompetencia del tribunal.",
            "Solo la nulidad del contrato.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 310 CPC; si se oponen antes de la recepción a "
        "prueba se tramitan como incidente, y si se oponen después el tribunal no deja de "
        "recibirlas pero las resuelve en la sentencia definitiva. La A no, porque la regla "
        "general es oponerlas al contestar. La C no, porque la incompetencia es dilatoria. La "
        "D no, porque la nulidad no está en la enumeración.",
        f"{CPC}, art. 310; {UC}, III, cap. II, 2.3.3.2.2",
    ),
    (
        "Reconvención, réplica y dúplica",
        2,
        "¿Qué es la reconvención?",
        [
            "La respuesta del demandante a la contestación.",
            "La demanda que el demandado deduce contra el demandante en el mismo juicio, al "
            "contestar.",
            "Un recurso contra la sentencia definitiva.",
            "La citación a oír sentencia.",
        ],
        "B",
        "Es la B porque la reconvención es una contrademanda que el demandado formula en el "
        "escrito de contestación (art. 314 CPC); el tribunal debe tener competencia para "
        "conocer de ella estimada como demanda y debe estar sujeta a la misma clase de "
        "procedimiento (art. 315). La A no, porque esa es la réplica. La C no, porque no es "
        "un recurso. La D no, porque la citación a oír sentencia es un trámite posterior.",
        f"{CPC}, arts. 314 a 317; {UC}, III, cap. II, 2.3.4",
    ),
    (
        "Reconvención, réplica y dúplica",
        2,
        "¿De qué plazo disponen las partes para presentar la réplica y la dúplica en el juicio "
        "ordinario?",
        [
            "De 3 días cada una.",
            "De 6 días cada una.",
            "De 15 días cada una.",
            "No hay plazo legal.",
        ],
        "B",
        "Es la B porque el art. 311 CPC concede seis días para replicar y seis días para "
        "duplicar. En la réplica y la dúplica las partes pueden ampliar, adicionar o "
        "modificar sus acciones y excepciones, sin alterar las principales (art. 312). La A "
        "no, porque tres días es el traslado de los incidentes. La C no, porque quince días "
        "es el plazo base de contestación. La D no, porque la ley fija el plazo.",
        f"{CPC}, arts. 311 y 312; {UC}, III, cap. II, 2.4",
    ),
    (
        "Conciliación y recepción de la causa a prueba",
        2,
        "¿Qué hechos fija el tribunal en la resolución que recibe la causa a prueba?",
        [
            "Todos los hechos que las partes mencionaron, sin excepción.",
            "Los hechos sustanciales, pertinentes y controvertidos sobre los cuales debe recaer "
            "la prueba.",
            "Solo los hechos que el juez considera verdaderos.",
            "Los hechos que figuran en el auto acordado de la Corte Suprema.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 318 CPC. Contra esa resolución procede "
        "reposición dentro de tercero día y apelación en subsidio, en el solo efecto "
        "devolutivo (art. 319). La A no, porque se excluyen los no controvertidos o "
        "impertinentes. La C no, porque el juez no anticipa su convicción. La D no, porque "
        "los hechos dependen de cada juicio.",
        f"{CPC}, arts. 318 y 319; {UC}, III, cap. II, 4.1",
    ),
    (
        "Conciliación y recepción de la causa a prueba",
        3,
        "En un juicio civil en que es admisible la transacción, agotados los escritos de "
        "discusión, el juez omite llamar a las partes a conciliación. ¿Qué consecuencia "
        "puede tener esa omisión?",
        [
            "Ninguna: la conciliación es facultativa.",
            "Es la omisión de un trámite esencial, que puede fundar un recurso de casación en "
            "la forma contra la sentencia de primera instancia.",
            "El juicio se transforma en sumario.",
            "El demandado gana automáticamente.",
        ],
        "B",
        "Es la B porque el art. 262 CPC obliga al juez a llamar a conciliación en todo juicio "
        "civil en que sea admisible la transacción (salvo las excepciones legales), y el "
        "art. 795 n.° 2 considera el llamado a conciliación como trámite esencial en primera "
        "instancia, cuya falta es causal de casación en la forma (art. 768 n.° 9). La A no, "
        "porque el llamado es obligatorio. La C no, porque no cambia el procedimiento. La D "
        "no, porque no tiene ese efecto.",
        f"{CPC}, arts. 262, 768 n.° 9 y 795 n.° 2; {UC}, III, cap. II, 3",
    ),
    (
        "Términos probatorios",
        1,
        "¿Cuánto dura el término probatorio ordinario en el juicio ordinario de mayor cuantía?",
        [
            "5 días.",
            "10 días.",
            "20 días.",
            "60 días.",
        ],
        "C",
        "Es la C porque el art. 328 CPC fija el término probatorio ordinario en veinte días. "
        "Es común para las partes (art. 327). La A no, porque cinco días es el plazo para "
        "presentar la lista de testigos (art. 320). La B no, porque diez días es el plazo de "
        "observaciones a la prueba (art. 430). La D no, porque sesenta días es el plazo para "
        "dictar la sentencia definitiva (art. 162).",
        f"{CPC}, arts. 327 y 328; {UC}, III, cap. II, 4.2.1",
    ),
    (
        "Términos probatorios",
        2,
        "Una parte necesita rendir prueba en el extranjero. ¿Qué término probatorio debe pedir?",
        [
            "El ordinario.",
            "El extraordinario, que procede para rendir prueba fuera del territorio "
            "jurisdiccional del tribunal o fuera de la República.",
            "El especial.",
            "Ninguno: la prueba en el extranjero no se admite.",
        ],
        "B",
        "Es la B porque el término extraordinario (art. 329 CPC) se concede para rendir "
        "prueba fuera del territorio del tribunal o fuera de Chile. La A no, porque el "
        "ordinario no basta para esos casos. La C no, porque el especial procede cuando "
        "durante el probatorio ocurren entorpecimientos que impiden rendir la prueba (art. "
        "339). La D no, porque la ley sí la admite.",
        f"{CPC}, arts. 329 y 339; {UC}, III, cap. II, 4.2.2",
    ),
    (
        "Prueba documental",
        2,
        "Se acompaña en juicio un instrumento privado emanado de la contraparte y esta no "
        "alega su falsedad o falta de integridad. ¿Qué ocurre?",
        [
            "Carece de todo valor.",
            "Se tiene por reconocido si no se objeta dentro de los seis días siguientes a su "
            "presentación, y adquiere el valor de escritura pública respecto de quienes lo "
            "suscribieron.",
            "Debe ser ratificado por un notario.",
            "Solo vale si la Corte lo aprueba.",
        ],
        "B",
        "Es la B porque el art. 346 n.° 3 CPC establece ese reconocimiento tácito, y el art. "
        "1702 del Código Civil da al instrumento privado reconocido el valor de escritura "
        "pública respecto de quienes aparecen o se reputan haberlo suscrito. La A no, porque "
        "sí tiene valor. La C no, porque no se requiere notario. La D no, porque no hay tal "
        "exigencia.",
        f"{CPC}, art. 346; Código Civil, art. 1702; {UC}, III, cap. II, 4.3.1",
    ),
    (
        "Prueba documental",
        2,
        "¿Qué valor probatorio tiene un instrumento público según el Código Civil?",
        [
            "Ninguno, salvo que se ratifique con testigos.",
            "Hace plena fe en cuanto al hecho de haberse otorgado y su fecha, pero no en cuanto "
            "a la verdad de las declaraciones que en él hayan hecho los interesados, en lo cual "
            "solo hace plena fe contra los declarantes.",
            "Hace plena fe respecto de todo su contenido frente a todos.",
            "Solo vale como principio de prueba por escrito.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 1700 del Código Civil. La A no, porque tiene "
        "valor propio. La C no, porque la ley distingue entre el otorgamiento y la verdad de "
        "las declaraciones. La D no, porque es plena prueba en lo indicado.",
        f"Código Civil, art. 1700; {CPC}, art. 342; {UC}, III, cap. II, 4.3.1.6",
    ),
    (
        "Prueba testimonial",
        2,
        "¿Qué valor puede tener, según el art. 384 CPC, la declaración de dos testigos?",
        [
            "Ninguno, si no son parientes de la parte.",
            "La de dos o más testigos contestes en el hecho y en sus circunstancias esenciales, "
            "sin tacha, legalmente examinados y que den razón de sus dichos, puede constituir "
            "plena prueba cuando no haya sido desvirtuada por otra prueba en contrario.",
            "Siempre es plena prueba.",
            "Solo vale como presunción judicial.",
        ],
        "B",
        "Es la B porque esa es la regla del art. 384 n.° 2 CPC; el testimonio de un solo "
        "testigo imparcial y verídico constituye una presunción judicial (n.° 1). La A no, "
        "porque el parentesco más bien puede inhabilitar. La C no, porque la ley exige varios "
        "requisitos. La D no, porque bajo esas condiciones puede ser plena prueba.",
        f"{CPC}, art. 384; {UC}, III, cap. II, 4.3.2.5",
    ),
    (
        "Prueba testimonial",
        3,
        "Un niño de 12 años presenció un hecho. ¿Puede declarar como testigo en un juicio civil?",
        [
            "Sí, con el mismo valor que un adulto.",
            "Es inhábil, pero el tribunal puede aceptar su declaración sin previo juramento y "
            "estimarla como base para una presunción judicial, cuando tenga discernimiento "
            "suficiente.",
            "No puede declarar bajo ninguna circunstancia.",
            "Solo puede declarar si sus padres lo autorizan por escritura pública.",
        ],
        "B",
        "Es la B porque el art. 357 n.° 1 CPC declara inhábiles a los menores de catorce años, "
        "pero permite aceptar sus declaraciones sin juramento como base de una presunción "
        "judicial si tienen discernimiento suficiente. La A no, porque su testimonio no tiene "
        "el valor del art. 384. La C no, porque la ley admite esa excepción. La D no, porque "
        "no existe ese requisito.",
        f"{CPC}, art. 357; {UC}, III, cap. II, 4.3.2.2",
    ),
    (
        "Confesión",
        2,
        "Citado a absolver posiciones, el litigante no comparece a la segunda citación. ¿Qué "
        "puede pedir la contraparte?",
        [
            "Que se le condene por desacato.",
            "Que se le dé por confeso de todos los hechos que estén categóricamente afirmados en "
            "el escrito en que se pidió su declaración (confesión tácita o ficta).",
            "Que se le multe y se cite por tercera vez.",
            "Nada: la confesión es voluntaria.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 394 CPC, que también se aplica si comparece y "
        "se niega a declarar o da respuestas evasivas. La A no, porque la consecuencia es "
        "procesal, no penal. La C no, porque basta la segunda citación. La D no, porque la "
        "ley impone esa consecuencia.",
        f"{CPC}, art. 394; {UC}, III, cap. II, 4.3.3",
    ),
    (
        "Confesión",
        3,
        "¿Qué valor tiene la confesión judicial expresa sobre hechos personales del confesante?",
        [
            "Ninguno, si no se ratifica con testigos.",
            "Produce plena prueba contra el confesante, sin perjuicio de las excepciones legales.",
            "Solo vale como presunción judicial.",
            "Vale solo si se presta ante notario.",
        ],
        "B",
        "Es la B porque los arts. 1713 del Código Civil y 399 CPC dan a la confesión judicial "
        "el valor de plena prueba contra el confesante. Por regla general es indivisible, "
        "salvo las excepciones del art. 401 CPC. La A no, porque no necesita ratificación. La "
        "C no, porque es plena prueba. La D no, porque la confesión judicial se presta ante "
        "el tribunal.",
        f"Código Civil, art. 1713; {CPC}, arts. 399 y 401; {UC}, III, cap. II, 4.3.3.4",
    ),
    (
        "Peritos, inspección personal y presunciones",
        2,
        "¿Cómo aprecia el tribunal la fuerza probatoria del informe de peritos?",
        [
            "Como plena prueba, siempre.",
            "Considerando la competencia de los peritos, la uniformidad o disconformidad de sus "
            "opiniones, los principios científicos en que se apoyan y la concordancia con las "
            "reglas de la lógica y los demás antecedentes: conforme a las reglas de la sana "
            "crítica.",
            "No tiene valor si las partes lo objetan.",
            "Solo como presunción judicial de un solo hecho.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 425 CPC: es uno de los pocos medios que el "
        "Código de Procedimiento Civil manda apreciar según la sana crítica. La A no, porque "
        "no es plena prueba legal. La C no, porque la objeción no lo priva de valor por sí "
        "sola. La D no, porque la ley no lo limita así.",
        f"{CPC}, art. 425; {UC}, III, cap. II, 4.3.5",
    ),
    (
        "Peritos, inspección personal y presunciones",
        3,
        "¿Puede una sola presunción judicial constituir plena prueba según el art. 426 CPC?",
        [
            "No, nunca: se requieren al menos tres.",
            "Sí, cuando a juicio del tribunal tenga caracteres de gravedad y precisión "
            "suficientes para formar su convencimiento.",
            "Sí, pero solo si la acepta la contraparte.",
            "Solo en materia penal.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 426 inc. 2 CPC; en general, las presunciones "
        "judiciales deben ser graves, precisas y concordantes (art. 1712 del Código Civil). "
        "La A no, porque la ley admite una sola en esas condiciones. La C no, porque no "
        "depende de la aceptación de la contraparte. La D no, porque la regla es del "
        "procedimiento civil.",
        f"{CPC}, art. 426; Código Civil, art. 1712; {UC}, III, cap. II, 4.3.6",
    ),
    (
        "Citación a oír sentencia y medidas para mejor resolver",
        2,
        "¿Qué efecto tiene la citación para oír sentencia en el juicio ordinario?",
        [
            "Abre un nuevo término probatorio.",
            "Desde que se notifica, no se admiten escritos ni pruebas de ninguna clase, salvo "
            "las excepciones legales (como las medidas para mejor resolver).",
            "Suspende el juicio por seis meses.",
            "Obliga a las partes a una nueva conciliación.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 433 CPC; la citación se dicta vencido el plazo "
        "de diez días para formular observaciones a la prueba (arts. 430 y 432). La A no, "
        "porque cierra la etapa de prueba. La C no, porque no suspende el juicio. La D no, "
        "porque no obliga a conciliar nuevamente.",
        f"{CPC}, arts. 430, 432 y 433; {UC}, III, cap. II, 5 y 6",
    ),
    (
        "Citación a oír sentencia y medidas para mejor resolver",
        3,
        "¿Qué caracteriza a las medidas para mejor resolver?",
        [
            "Las piden las partes en cualquier momento del juicio.",
            "Las decreta el tribunal de oficio, solo dentro del plazo para dictar sentencia, "
            "entre las que enumera la ley, y deben cumplirse dentro de veinte días; vencido ese "
            "plazo, se tienen por no decretadas.",
            "Permiten al juez abrir un nuevo período de discusión.",
            "Solo existen en segunda instancia.",
        ],
        "B",
        "Es la B porque así lo establece el art. 159 CPC; entre ellas están la agregación de "
        "documentos, la confesión judicial, la inspección personal, el informe de peritos y "
        "la comparecencia de testigos que ya declararon para aclarar sus dichos. La A no, "
        "porque las decreta el tribunal de oficio. La C no, porque no reabren la discusión. "
        "La D no, porque proceden también en primera instancia.",
        f"{CPC}, art. 159; {UC}, III, cap. II, 7",
    ),
    # --------------------------- III caps. III a VI: terminación, incidentes, sumario y arbitral
    (
        "Abandono y desistimiento",
        2,
        "¿Cuándo procede el abandono del procedimiento según el art. 152 CPC?",
        [
            "Cuando el juez no dicta sentencia en 60 días.",
            "Cuando todas las partes que figuran en el juicio han cesado en su prosecución "
            "durante seis meses, contados desde la fecha de la última resolución recaída en "
            "alguna gestión útil para dar curso progresivo a los autos.",
            "Cuando el demandante muere.",
            "Cuando el demandado no contesta la demanda.",
        ],
        "B",
        "Es la B porque esa es la regla del art. 152 CPC; el abandono se alega como incidente "
        "por el demandado, y se entiende renunciado si este realiza cualquier gestión que no "
        "tenga por objeto alegarlo (art. 155). La A no, porque la demora del juez no produce "
        "abandono. La C no, porque la muerte de una parte tiene otras reglas. La D no, porque "
        "la falta de contestación da lugar a la rebeldía.",
        f"{CPC}, arts. 152, 153 y 155; {UC}, III, cap. IV, 9",
    ),
    (
        "Abandono y desistimiento",
        3,
        "¿Qué efecto tiene la sentencia que acepta el desistimiento de la demanda?",
        [
            "Ninguno: el demandante puede volver a demandar al día siguiente lo mismo.",
            "Extingue las acciones a que se refiere, con relación a las partes litigantes y a "
            "todas las personas a quienes habría afectado la sentencia del juicio.",
            "Solo suspende el juicio por seis meses.",
            "Obliga al demandado a pagar lo demandado.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 150 CPC: produce cosa juzgada. Distinto es el "
        "retiro de la demanda antes de que sea notificada, que no tiene ese efecto (art. "
        "148). La A no, porque las acciones se extinguen. La C no, porque no es una "
        "suspensión. La D no, porque el desistimiento favorece al demandado.",
        f"{CPC}, arts. 148 y 150; {UC}, III, cap. III y cap. IV, 8",
    ),
    (
        "Incidentes y acumulación de autos",
        2,
        "¿Qué es un incidente según el art. 82 CPC?",
        [
            "La demanda principal.",
            "Toda cuestión accesoria de un juicio que requiera pronunciamiento especial con "
            "audiencia de las partes.",
            "La sentencia definitiva.",
            "Un recurso extraordinario.",
        ],
        "B",
        "Es la B porque es la definición del art. 82 CPC; en los incidentes ordinarios se "
        "confiere traslado por tres días (art. 89). La A no, porque el incidente es accesorio "
        "a la cuestión principal. La C no, porque la sentencia definitiva resuelve el asunto "
        "principal. La D no, porque no es un recurso.",
        f"{CPC}, arts. 82 y 89; {UC}, III, cap. IV, 1 y 3",
    ),
    (
        "Incidentes y acumulación de autos",
        3,
        "¿Qué efecto produce la acumulación de autos cuando los juicios están en distinto "
        "estado de tramitación?",
        [
            "Se anula el juicio menos avanzado.",
            "Se suspende el curso del juicio más avanzado hasta que el otro llegue al mismo "
            "estado, para que ambos terminen por una misma sentencia.",
            "Se fallan por separado igual.",
            "El juicio más antiguo se archiva.",
        ],
        "B",
        "Es la B porque la acumulación busca mantener la continencia o unidad de la causa "
        "(art. 92 CPC) y el art. 97 suspende el juicio más adelantado hasta que el otro "
        "llegue al mismo estado; además, los juicios deben estar sometidos a una misma clase "
        "de procedimiento y en instancias análogas (art. 95). La A no, porque no se anula "
        "nada. La C no, porque terminan por una misma sentencia. La D no, porque no se "
        "archiva.",
        f"{CPC}, arts. 92, 95 y 97; {UC}, III, cap. IV, 6",
    ),
    (
        "Procedimiento sumario y procedimiento arbitral",
        2,
        "¿Cuándo se aplica el procedimiento sumario como regla general según el art. 680 CPC?",
        [
            "Cuando la cuantía es inferior a 10 UTM.",
            "En defecto de otra regla especial, cuando la acción deducida requiera, por su "
            "naturaleza, tramitación rápida para que sea eficaz.",
            "Cuando lo piden ambas partes en una escritura pública.",
            "Solo en materia penal.",
        ],
        "B",
        "Es la B porque esa es la regla general del art. 680 inc. 1 CPC, que además enumera "
        "casos especiales en que se aplica. Su estructura es concentrada: la demanda se "
        "contesta en un comparendo y no hay réplica ni dúplica. La A no, porque no depende de "
        "esa cuantía. La C no, porque no se elige por escritura pública. La D no, porque es "
        "un procedimiento civil.",
        f"{CPC}, arts. 680 y 683; {UC}, III, cap. V",
    ),
    (
        "Procedimiento sumario y procedimiento arbitral",
        3,
        "¿Qué reglas de procedimiento debe seguir un árbitro arbitrador?",
        [
            "Siempre las del juicio ordinario de mayor cuantía.",
            "Las que las partes hayan expresado en el acto constitutivo del compromiso; si nada "
            "han dicho, debe oír a las partes y fallar obedeciendo a lo que su prudencia y la "
            "equidad le dicten.",
            "Las del Código Procesal Penal.",
            "Las que fije la Corte Suprema en cada caso.",
        ],
        "B",
        "Es la B porque así lo disponen los arts. 637 y 640 CPC; el árbitro de derecho, en "
        "cambio, tramita conforme a las reglas de los jueces ordinarios según la naturaleza "
        "de la acción (art. 628). La A no, porque esa regla es para el árbitro de derecho. La "
        "C no, porque es un procedimiento civil. La D no, porque las reglas las fijan las "
        "partes o la ley.",
        f"{CPC}, arts. 628, 637 y 640; {UC}, III, cap. VI",
    ),
    # --------------------------------------- IV cap. I: procedimientos de ejecución
    (
        "Juicio ejecutivo: títulos y requisitos",
        2,
        "¿Cuál de estos documentos es un título ejecutivo según el art. 434 CPC?",
        [
            "Un correo electrónico en que el deudor reconoce la deuda.",
            "La copia autorizada de una escritura pública.",
            "Una factura sin aceptar.",
            "La declaración jurada del acreedor.",
        ],
        "B",
        "Es la B porque el art. 434 CPC enumera, entre otros, la sentencia firme, la copia "
        "autorizada de escritura pública, el acta de avenimiento, el instrumento privado "
        "reconocido judicialmente o mandado tener por reconocido, la confesión judicial y "
        "los títulos de crédito protestados en las condiciones legales. La A no, porque no "
        "está en la enumeración y requeriría una gestión preparatoria. La C no, porque la "
        "factura necesita cumplir requisitos de una ley especial. La D no, porque nadie puede "
        "crearse un título a sí mismo.",
        f"{CPC}, art. 434; {UC}, IV, cap. I, 1.1.1",
    ),
    (
        "Juicio ejecutivo: títulos y requisitos",
        3,
        "Además de constar en un título ejecutivo, ¿qué requisitos debe cumplir la obligación "
        "para que proceda la acción ejecutiva?",
        [
            "Que conste en escritura pública y supere 100 UTM.",
            "Que sea líquida, actualmente exigible y que la acción ejecutiva no esté prescrita "
            "(prescribe en tres años).",
            "Que el deudor acepte ser demandado.",
            "Que haya sido declarada por un juez penal.",
        ],
        "B",
        "Es la B porque esos son los requisitos de los arts. 437, 438 y 442 CPC; la acción "
        "ejecutiva prescribe en tres años y, convertida en ordinaria, dura otros dos (art. "
        "2515 del Código Civil). La A no, porque no se exige escritura pública ni una cuantía "
        "mínima. La C no, porque no depende de la voluntad del deudor. La D no, porque no "
        "requiere declaración penal.",
        f"{CPC}, arts. 437, 438 y 442; Código Civil, art. 2515; {UC}, IV, cap. I, 1.1",
    ),
    (
        "Juicio ejecutivo: mandamiento, excepciones y tercerías",
        2,
        "¿Qué contiene el mandamiento de ejecución y embargo?",
        [
            "La sentencia definitiva del juicio.",
            "La orden de requerir de pago al deudor y, si no paga en el acto, de embargarle "
            "bienes suficientes para cubrir la deuda.",
            "La citación a una audiencia de conciliación.",
            "La orden de arresto del deudor.",
        ],
        "B",
        "Es la B porque así lo establece el art. 443 CPC; el requerimiento de pago debe "
        "hacerse, en principio, personalmente al deudor. La A no, porque la sentencia se "
        "dicta después de las excepciones. La C no, porque no hay conciliación obligatoria en "
        "el juicio ejecutivo. La D no, porque no existe prisión por deudas civiles.",
        f"{CPC}, art. 443; {UC}, IV, cap. I, 1.2.3",
    ),
    (
        "Juicio ejecutivo: mandamiento, excepciones y tercerías",
        3,
        "¿Cuál de estas afirmaciones sobre las excepciones del ejecutado es correcta?",
        [
            "Puede oponer cualquier defensa, sin límite.",
            "Solo puede oponer las excepciones que enumera taxativamente el art. 464 CPC (entre "
            "ellas el pago de la deuda, la prescripción, la falsedad del título y la falta de "
            "requisitos para que tenga fuerza ejecutiva).",
            "No puede oponer excepciones: debe pagar.",
            "Solo puede alegar la incompetencia del tribunal.",
        ],
        "B",
        "Es la B porque las excepciones del juicio ejecutivo son taxativas (art. 464 CPC) y "
        "deben oponerse dentro del plazo legal desde el requerimiento (cuatro días si se le "
        "requiere en la comuna asiento del tribunal, art. 459). La A no, porque la "
        "enumeración es cerrada. La C no, porque la ley le permite defenderse. La D no, "
        "porque la incompetencia es solo una de ellas.",
        f"{CPC}, arts. 459 y 464; {UC}, IV, cap. I, 1.3",
    ),
    (
        "Cumplimiento incidental y exequátur",
        2,
        "Se pide la ejecución de una sentencia ante el mismo tribunal que la dictó, dentro del "
        "año siguiente a que se hizo exigible. ¿Qué procedimiento se aplica?",
        [
            "El juicio ordinario.",
            "El cumplimiento incidental, en el cual las excepciones del ejecutado deben basarse "
            "en antecedentes escritos y en hechos posteriores a la sentencia.",
            "El exequátur ante la Corte Suprema.",
            "El procedimiento sumario.",
        ],
        "B",
        "Es la B porque esas son las condiciones del cumplimiento incidental (arts. 231 y 233 "
        "CPC), y el art. 234 limita las excepciones a las que enumera (pago, remisión, "
        "novación, transacción, entre otras), fundadas en antecedentes escritos y en hechos "
        "acaecidos con posterioridad a la sentencia. La A no, porque no es necesario un nuevo "
        "juicio declarativo. La C no, porque el exequátur es para sentencias extranjeras. La "
        "D no, porque no se aplica el sumario.",
        f"{CPC}, arts. 231, 233 y 234; {UC}, IV, cap. I, 2",
    ),
    (
        "Cumplimiento incidental y exequátur",
        2,
        "¿Qué tribunal concede el exequátur para cumplir en Chile una sentencia extranjera?",
        [
            "El juez de letras del domicilio del deudor.",
            "La Corte Suprema.",
            "El Ministerio de Relaciones Exteriores.",
            "La Corte de Apelaciones de Santiago.",
        ],
        "B",
        "Es la B porque los arts. 247 y 248 CPC entregan a la Corte Suprema la autorización "
        "para cumplir resoluciones pronunciadas en el extranjero; entre los requisitos del "
        "art. 245 están que no contengan nada contrario a las leyes de la República, que no "
        "se opongan a la jurisdicción nacional, que la parte contra quien se invoca haya "
        "sido debidamente notificada y que estén ejecutoriadas. La A no, porque el juez de "
        "letras interviene después, en la ejecución. La C no, porque no es un órgano "
        "jurisdiccional. La D no, porque la competencia es de la Corte Suprema.",
        f"{CPC}, arts. 242 a 251; {UC}, IV, cap. I, 3",
    ),
    # --------------------------------------------------- IV cap. II: recursos
    (
        "Aclaración y reposición",
        2,
        "¿Contra qué resoluciones procede el recurso de reposición y en qué plazo, como regla "
        "general?",
        [
            "Contra sentencias definitivas, dentro de 10 días.",
            "Contra autos y decretos, dentro de cinco días.",
            "Contra cualquier resolución, en cualquier tiempo.",
            "Solo contra resoluciones de la Corte Suprema.",
        ],
        "B",
        "Es la B porque el art. 181 CPC permite pedir reposición de los autos y decretos "
        "dentro de cinco días; la resolución que recibe la causa a prueba admite reposición "
        "dentro de tercero día (art. 319). La A no, porque la sentencia definitiva no es "
        "reponible por regla general. La C no, porque la ley distingue resoluciones y "
        "plazos. La D no, porque procede ante cualquier tribunal.",
        f"{CPC}, arts. 181 y 319; {UC}, IV, cap. II, 2",
    ),
    (
        "Aclaración y reposición",
        3,
        "¿Para qué sirve la solicitud de aclaración, rectificación o enmienda?",
        [
            "Para cambiar el sentido de lo resuelto.",
            "Para aclarar los puntos oscuros o dudosos, salvar las omisiones y rectificar los "
            "errores de copia, de referencia o de cálculos numéricos que aparezcan de "
            "manifiesto en la sentencia.",
            "Para pedir una nueva prueba.",
            "Para que conozca un tribunal superior.",
        ],
        "B",
        "Es la B porque esa es la excepción al desasimiento que permite el art. 182 CPC. La A "
        "no, porque no puede alterar lo decidido. La C no, porque no reabre la prueba. La D "
        "no, porque la conoce el mismo tribunal que dictó la sentencia.",
        f"{CPC}, art. 182; {UC}, IV, cap. II, 1",
    ),
    (
        "Recurso de apelación y recurso de hecho",
        2,
        "¿En qué plazo debe apelarse de una sentencia definitiva en materia civil?",
        [
            "Dentro de 3 días.",
            "Dentro de 5 días.",
            "Dentro de 10 días.",
            "Dentro de 30 días.",
        ],
        "C",
        "Es la C porque el art. 189 CPC fija en cinco días el plazo general de la apelación, "
        "y en diez días cuando se trata de sentencias definitivas, contados desde la "
        "notificación; el escrito debe contener los fundamentos de hecho y de derecho y las "
        "peticiones concretas. La A no, porque tres días es el plazo de otros trámites. La B "
        "no, porque cinco días es el plazo general, no el de la sentencia definitiva. La D "
        "no, porque no es un plazo legal de apelación.",
        f"{CPC}, arts. 186 y 189; {UC}, IV, cap. II, 3",
    ),
    (
        "Recurso de apelación y recurso de hecho",
        3,
        "El juez de primera instancia declara inadmisible una apelación que debió concederse. "
        "¿Qué puede hacer el apelante?",
        [
            "Interponer recurso de casación en el fondo.",
            "Interponer recurso de hecho ante el tribunal superior, dentro de cinco días.",
            "Esperar la sentencia definitiva.",
            "Interponer recurso de revisión.",
        ],
        "B",
        "Es la B porque el recurso de hecho (art. 203 CPC) procede cuando el inferior deniega "
        "una apelación que debió concederse, la concede siendo improcedente o la otorga en "
        "un efecto que no corresponde. La A no, porque la casación no es la vía. La C no, "
        "porque el plazo para recurrir de hecho correría igual. La D no, porque la revisión "
        "procede contra sentencias firmes por causales específicas.",
        f"{CPC}, arts. 196 y 203; {UC}, IV, cap. II, 4",
    ),
    (
        "Recurso de casación en la forma",
        2,
        "¿Qué exige el art. 769 CPC para que sea admisible el recurso de casación en la forma, "
        "como regla general?",
        [
            "Que la causa supere cierta cuantía.",
            "Que quien lo entabla haya reclamado del vicio, ejerciendo oportunamente y en todos "
            "sus grados los recursos establecidos por la ley (preparación del recurso).",
            "Que lo patrocinen dos abogados.",
            "Que la otra parte esté de acuerdo.",
        ],
        "B",
        "Es la B porque esa es la preparación del recurso del art. 769 CPC, con excepciones "
        "(por ejemplo, cuando el vicio nace en la misma sentencia). El recurso se interpone "
        "dentro de quince días desde la notificación (art. 770). La A no, porque no depende "
        "de la cuantía. La C no, porque no exige dos abogados. La D no, porque no requiere "
        "acuerdo de la contraparte.",
        f"{CPC}, arts. 768, 769 y 770; {UC}, IV, cap. II, 5.1",
    ),
    (
        "Recurso de casación en la forma",
        3,
        "La sentencia otorga al demandante más de lo que pidió en su demanda. ¿Qué causal de "
        "casación en la forma configura?",
        [
            "La de haber sido dada por tribunal incompetente.",
            "La ultra petita: haber sido dada otorgando más de lo pedido por las partes, o "
            "extendiéndose a puntos no sometidos a la decisión del tribunal.",
            "La de faltar el emplazamiento.",
            "La de ser contraria a otra pasada en autoridad de cosa juzgada.",
        ],
        "B",
        "Es la B porque esa es la causal del art. 768 n.° 4 CPC. La A no, porque esa es la "
        "causal n.° 1. La C no, porque la falta de emplazamiento es un trámite esencial "
        "(causal n.° 9). La D no, porque esa es la causal n.° 6.",
        f"{CPC}, art. 768; {UC}, IV, cap. II, 5.1.3",
    ),
    (
        "Recurso de casación en el fondo",
        2,
        "¿Contra qué resoluciones procede el recurso de casación en el fondo y qué tribunal lo "
        "conoce?",
        [
            "Contra cualquier resolución de primera instancia; lo conoce la Corte de Apelaciones.",
            "Contra sentencias definitivas inapelables e interlocutorias inapelables que ponen "
            "término al juicio o hacen imposible su continuación, dictadas por Cortes de "
            "Apelaciones o tribunales arbitrales de segunda instancia, con infracción de ley "
            "que haya influido sustancialmente en lo dispositivo; lo conoce la Corte Suprema.",
            "Solo contra decretos; lo conoce el mismo juez.",
            "Contra sentencias penales; lo conoce el tribunal oral.",
        ],
        "B",
        "Es la B porque así lo establece el art. 767 CPC; el recurso se interpone dentro de "
        "quince días y debe expresar en qué consisten los errores de derecho y de qué modo "
        "influyen sustancialmente en lo dispositivo (art. 772). La A no, porque no procede "
        "contra resoluciones de primera instancia en general. La C no, porque los decretos no "
        "son casables. La D no, porque en materia penal existe el recurso de nulidad.",
        f"{CPC}, arts. 767 y 772; {UC}, IV, cap. II, 5.2",
    ),
    (
        "Recurso de casación en el fondo",
        3,
        "La Corte Suprema acoge un recurso de casación en el fondo. ¿Qué hace a continuación?",
        [
            "Devuelve el expediente para que se repita el juicio desde la demanda.",
            "Dicta, acto continuo y sin nueva vista, pero separadamente, la sentencia que crea "
            "conforme a la ley y al mérito de los hechos tal como se han dado por establecidos "
            "en el fallo recurrido (sentencia de reemplazo).",
            "Ordena una nueva prueba.",
            "Remite los antecedentes al Ministerio Público.",
        ],
        "B",
        "Es la B porque así lo dispone el art. 785 CPC; la Corte no revisa los hechos, salvo "
        "infracción de las leyes reguladoras de la prueba. La A no, porque no se repite el "
        "juicio. La C no, porque no hay nueva prueba. La D no, porque no hay intervención "
        "del Ministerio Público.",
        f"{CPC}, art. 785; {UC}, IV, cap. II, 5.2.6",
    ),
    (
        "Recurso de queja y recurso de revisión",
        2,
        "¿Cuál es el único objeto del recurso de queja según el art. 545 COT?",
        [
            "Revisar cualquier sentencia que la parte considere injusta.",
            "Corregir las faltas o abusos graves cometidos en la dictación de resoluciones de "
            "carácter jurisdiccional, y solo procede contra sentencias definitivas o "
            "interlocutorias que pongan fin al juicio o hagan imposible su continuación y que "
            "no sean susceptibles de recurso alguno.",
            "Reclamar contra un decreto de mero trámite.",
            "Pedir la aclaración de una sentencia.",
        ],
        "B",
        "Es la B porque así lo define el art. 545 COT; se interpone dentro de cinco días "
        "desde la notificación (art. 548). La A no, porque no es una tercera instancia. La C "
        "no, porque no procede contra decretos. La D no, porque la aclaración es otra "
        "solicitud.",
        f"{COT}, arts. 545 y 548; {UC}, IV, cap. II, 6",
    ),
    (
        "Recurso de queja y recurso de revisión",
        3,
        "Una sentencia firme se fundó en documentos que después fueron declarados falsos por "
        "otra sentencia firme. ¿Qué puede hacer la parte afectada y en qué plazo?",
        [
            "Apelar dentro de cinco días.",
            "Interponer recurso (acción) de revisión ante la Corte Suprema, dentro del plazo de "
            "un año contado desde la fecha de la última notificación de la sentencia "
            "impugnada.",
            "Pedir la nulidad procesal dentro de cinco días.",
            "Nada: la cosa juzgada es absoluta.",
        ],
        "B",
        "Es la B porque el art. 810 CPC permite a la Corte Suprema rever una sentencia firme, "
        "entre otros casos, si se fundó en documentos declarados falsos por otra sentencia "
        "firme, y el art. 811 fija el plazo de un año. La A no, porque la sentencia ya está "
        "firme. La C no, porque la nulidad procesal no procede contra la cosa juzgada. La D "
        "no, porque la revisión es justamente la excepción.",
        f"{CPC}, arts. 810 y 811; {UC}, IV, cap. II, 7",
    ),
]
