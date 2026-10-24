// Temario del examen de grado de la Facultad de Derecho UC: cédulas vigentes desde el 1 de abril
// de 2021 (la de Derecho del Trabajo se actualizó el 2 de diciembre de 2025). Fuente oficial:
// https://derecho.uc.cl/carrera-y-programas/carrera-de-derecho/alumnos/examen-de-grado/ (pestaña
// «Cédulas»). Es un índice de materias: el detalle de cada cédula está en su PDF.

export type Chapter = { title: string; topics?: string[] };

export type Cedula = {
  number: number;
  name: string;
  kind: "obligatoria" | "electiva" | "suspendida";
  pdf?: string;
  chapters: Chapter[];
};

const PDF = "https://derecho.uc.cl/wp-content/uploads/2026/05/Cedula_";

export const TEMARIO_SOURCE =
  "https://derecho.uc.cl/carrera-y-programas/carrera-de-derecho/alumnos/examen-de-grado/";

export const CEDULAS: Cedula[] = [
  {
    number: 1,
    name: "Derecho Civil",
    kind: "obligatoria",
    pdf: `${PDF}Derecho_Civil_18.03.2021.pdf`,
    chapters: [
      {
        title: "Teoría de la ley",
        topics: ["Fuentes del Derecho", "La ley: definición, interpretación y efectos en el tiempo y el espacio", "Costumbre, doctrina y jurisprudencia"],
      },
      {
        title: "Teoría del acto jurídico",
        topics: [
          "Autonomía privada y el acto jurídico como categoría",
          "Clasificaciones de los actos jurídicos",
          "Requisitos: voluntad y sus vicios, objeto, causa, capacidad y formalidades",
          "Efectos e ineficacia: inexistencia y nulidad",
          "Simulación y representación",
        ],
      },
      { title: "Personas", topics: ["La persona natural y sus atributos", "Inicio y término de la persona", "La persona jurídica"] },
      {
        title: "Bienes",
        topics: ["Las cosas y su clasificación", "El dominio y la copropiedad", "Tradición, posesión y prescripción", "Usufructo y acción reivindicatoria"],
      },
      {
        title: "Obligaciones",
        topics: [
          "La obligación y su clasificación (naturales, solidarias, indivisibles, a plazo y condicionales)",
          "Efectos y modos de extinguir: pago, novación, compensación y prescripción",
          "Incumplimiento: cumplimiento forzado, resolución, indemnización y mora",
        ],
      },
      {
        title: "Fuentes de las obligaciones",
        topics: ["Responsabilidad extracontractual", "Teoría general del contrato", "Contratos en particular: promesa, compraventa, arrendamiento, mandato, transacción, mutuo y garantías"],
      },
      {
        title: "Derecho de familia",
        topics: ["Parentesco", "El matrimonio, su término y la compensación económica", "Regímenes patrimoniales del matrimonio", "Filiación y alimentos"],
      },
      {
        title: "Derecho sucesorio",
        topics: [
          "La sucesión por causa de muerte y el derecho real de herencia",
          "Incapacidades e indignidades",
          "Sucesión intestada y testada",
          "Asignaciones forzosas, partición y deudas hereditarias",
        ],
      },
    ],
  },
  {
    number: 2,
    name: "Derecho Procesal",
    kind: "obligatoria",
    pdf: `${PDF}Derecho_Procesal_18.03.2021.pdf`,
    chapters: [
      {
        title: "Instituciones procesales I",
        topics: ["El conflicto y sus formas de solución", "La jurisdicción", "El derecho a la tutela jurisdiccional y su contenido", "El proceso y el procedimiento"],
      },
      {
        title: "Instituciones procesales II",
        topics: ["Sujetos procesales", "Actos jurídicos procesales y su eficacia", "Teoría de la prueba", "Sistema recursivo y sistema cautelar"],
      },
      {
        title: "Procedimientos civiles I",
        topics: ["Medidas prejudiciales", "Juicio ordinario de mayor cuantía", "Suspensión y otras formas de terminación del procedimiento", "Incidentes", "Procedimiento sumario y arbitral"],
      },
      { title: "Procedimientos civiles II", topics: ["Procedimientos de ejecución", "Recursos"] },
      {
        title: "Procedimientos penales",
        topics: [
          "Estructura del proceso penal acusatorio chileno",
          "Acción penal y acción civil; control de garantías",
          "Sujetos procesales, salidas alternativas e investigación",
          "Medidas cautelares, etapa intermedia y juicio oral",
          "Recursos y procedimientos especiales",
        ],
      },
    ],
  },
  {
    number: 3,
    name: "Derecho Administrativo I",
    kind: "electiva",
    pdf: `${PDF}Derecho_Administrativo_1_18.03.2021.pdf`,
    chapters: [
      { title: "Introducción al Derecho Administrativo. Principio de juridicidad" },
      {
        title: "La organización administrativa del Estado",
        topics: ["La Ley 18.575 y los principios organizativos", "Administración centralizada y descentralizada", "Empresas del Estado"],
      },
      {
        title: "El actuar jurídico de la Administración",
        topics: ["Teoría del acto administrativo", "Procedimiento administrativo: la Ley 19.880"],
      },
    ],
  },
  {
    number: 4,
    name: "Derecho Administrativo II",
    kind: "electiva",
    pdf: `${PDF}Derecho_Administrativo_2_18.03.2021.pdf`,
    chapters: [
      { title: "La contratación administrativa", topics: ["El contrato administrativo", "Principales figuras contractuales"] },
      { title: "Régimen de dominio y concesiones", topics: ["Concesiones, permisos y licencias"] },
      { title: "Función pública", topics: ["Ingreso y principios", "Probidad administrativa", "Responsabilidad administrativa"] },
      { title: "Control de la Administración", topics: ["Control jurisdiccional", "Control administrativo"] },
    ],
  },
  {
    number: 5,
    name: "Derecho Canónico",
    kind: "electiva",
    pdf: `${PDF}Derecho_Canonico_18.03.2021.pdf`,
    chapters: [
      { title: "Dimensión jurídica de la Iglesia", topics: ["Naturaleza jurídica de la Iglesia", "Fieles: derechos y deberes"] },
      { title: "Función de santificar", topics: ["Bautismo", "Orden sagrado", "Matrimonio"] },
      { title: "Función de enseñar", topics: ["Magisterio", "Enseñanza religiosa en Chile"] },
      { title: "Función de regir", topics: ["Funciones legislativa, judicial y ejecutiva", "Estructura jerárquica de la Iglesia"] },
    ],
  },
  {
    number: 6,
    name: "Derecho Comercial I (Sociedades)",
    kind: "electiva",
    pdf: `${PDF}Derecho_Comercial_1_Sociedades_18.03.2021.pdf`,
    chapters: [
      { title: "La sociedad: concepto, naturaleza y personalidad jurídica" },
      { title: "Sociedades de personas", topics: ["Colectiva civil y comercial", "Responsabilidad limitada", "En comandita", "Cuentas en participación"] },
      { title: "La sociedad anónima", topics: ["Constitución y capital", "Acciones, directorio y juntas", "Transformación, fusión, división, disolución y liquidación"] },
      { title: "Sociedades por acciones y constitución simplificada" },
      { title: "Nulidad y saneamiento de sociedades" },
    ],
  },
  {
    number: 7,
    name: "Derecho Comercial II (Títulos de crédito)",
    kind: "electiva",
    pdf: `${PDF}Derecho_Comercial_2_Titulos_de_credito_18.03.2021.pdf`,
    chapters: [
      { title: "El dinero y los medios de pago" },
      { title: "Títulos de crédito", topics: ["Letra de cambio", "Pagaré", "Descuento y factoring"] },
      { title: "Contratos sobre dinero o crédito", topics: ["Operaciones de crédito de dinero", "Mutuo, apertura de crédito, depósito y cuenta corriente mercantil"] },
      { title: "Operaciones bancarias" },
      { title: "Contratos de garantía mercantiles", topics: ["Prenda mercantil y prendas especiales"] },
    ],
  },
  {
    number: 8,
    name: "Derecho Comercial III (Concursal)",
    kind: "electiva",
    pdf: `${PDF}Derecho_Comercial_3_Concursal_18.03.2021.pdf`,
    chapters: [
      { title: "Responsabilidad del comerciante individual" },
      { title: "Introducción y reglas generales del Derecho concursal" },
      { title: "Reorganización judicial y extrajudicial" },
      { title: "Liquidación de la empresa deudora y de la persona deudora" },
      { title: "Renegociación de la persona deudora" },
      { title: "Acciones revocatorias concursales" },
      { title: "Insolvencia transfronteriza" },
    ],
  },
  {
    number: 9,
    name: "Derecho Constitucional I (Derechos y garantías)",
    kind: "electiva",
    pdf: `${PDF}Derecho_Constitucional_1_-_Derechos_y_Garantias_18.03.2021.pdf`,
    chapters: [
      { title: "Bases de la institucionalidad" },
      { title: "Generalidades de los derechos fundamentales" },
      { title: "Bases del estatuto constitucional de la persona" },
      { title: "Protección de los derechos en la Constitución", topics: ["Los derechos del art. 19", "Acciones protectoras: protección y amparo"] },
    ],
  },
  {
    number: 10,
    name: "Derecho Constitucional II (Orgánico)",
    kind: "electiva",
    pdf: `${PDF}Derecho_Constitucional_2_-_Constitucional_Organico_18.03.2021.pdf`,
    chapters: [
      { title: "Fuentes del Derecho Constitucional" },
      { title: "Bases de la institucionalidad" },
      { title: "Función gubernativa", topics: ["Presidente de la República", "Ministros de Estado"] },
      { title: "Función legislativa", topics: ["Congreso Nacional", "La ley"] },
      { title: "Función judicial" },
      { title: "Contraloría, Tribunal Constitucional y Banco Central" },
      { title: "Reforma constitucional" },
    ],
  },
  {
    number: 11,
    name: "Historia del Derecho",
    kind: "electiva",
    pdf: `${PDF}Historia_del_Derecho_18.03.2021.pdf`,
    chapters: [
      { title: "El sustrato jurídico común de Occidente" },
      { title: "Difusión castellana de la tradición jurídica: el Derecho Indiano" },
      { title: "Independencia de Chile y Constitución de 1833" },
      { title: "La codificación en Chile desde 1855" },
      { title: "Cambios del ordenamiento jurídico y Constitución de 1925" },
      { title: "La crisis del Estado de Derecho en Chile" },
    ],
  },
  {
    number: 12,
    name: "Derecho Internacional Público",
    kind: "electiva",
    pdf: `${PDF}Derecho_Internacional_Publico_18.03.2021.pdf`,
    chapters: [
      { title: "Nociones generales y fuentes", topics: ["Tratados internacionales", "Derecho internacional y derecho chileno"] },
      { title: "Sujetos de derecho internacional", topics: ["El Estado", "Organizaciones internacionales", "La persona y los sistemas de derechos humanos"] },
      { title: "Hechos ilícitos, controversias y conflictos", topics: ["Responsabilidad internacional", "Solución pacífica de controversias", "Uso de la fuerza"] },
    ],
  },
  {
    number: 13,
    name: "Derecho Natural",
    kind: "electiva",
    pdf: `${PDF}Derecho_Natural_18.03.2021.pdf`,
    chapters: [
      { title: "Ética, orden moral y orden jurídico" },
      { title: "Fin último y acto humano" },
      { title: "Las virtudes: prudencia, fortaleza, templanza y justicia" },
      { title: "Ley y conciencia: ley eterna, natural y positiva" },
      { title: "Derecho natural: parte especial" },
    ],
  },
  {
    number: 14,
    name: "Derecho Penal",
    kind: "electiva",
    pdf: `${PDF}Derecho_Penal_18.03.2021.pdf`,
    chapters: [
      { title: "La ley penal: legalidad y ley penal en el tiempo" },
      { title: "La tipicidad", topics: ["Imputación objetiva y causalidad", "Dolo, error de tipo e imprudencia"] },
      { title: "La antijuridicidad", topics: ["Causas de justificación", "Legítima defensa y estado de necesidad"] },
      { title: "La culpabilidad", topics: ["Imputabilidad", "Error de prohibición", "Exigibilidad de otra conducta"] },
      { title: "Etapas del delito, autoría y participación" },
      { title: "Parte especial", topics: ["Homicidio simple", "Robo con violencia o intimidación", "Estafa", "Cohecho"] },
    ],
  },
  {
    number: 15,
    name: "Derecho Romano",
    kind: "electiva",
    pdf: `${PDF}Derecho_Romano_18.03.2021.pdf`,
    chapters: [
      { title: "Fuentes del Derecho romano y su evolución" },
      { title: "Personas" },
      { title: "Procedimiento y acciones" },
      { title: "Los bienes" },
      { title: "Las obligaciones y sus fuentes" },
      { title: "Las sucesiones" },
    ],
  },
  {
    number: 16,
    name: "Derecho del Trabajo",
    kind: "electiva",
    pdf: `${PDF}Derecho_del_Trabajo_02.12.2025.pdf`,
    chapters: [
      { title: "Bases y principios del Derecho del Trabajo" },
      {
        title: "Contrato de trabajo",
        topics: ["Elementos y tiempo de trabajo", "Remuneraciones y cotizaciones", "Subcontratación y servicios transitorios", "Suspensión y terminación", "Prescripción y caducidad"],
      },
      { title: "Sindicatos, negociación colectiva y huelga" },
    ],
  },
  {
    number: 17,
    name: "Derecho Tributario",
    kind: "electiva",
    pdf: `${PDF}Derecho_Tributario_18.03.2021.pdf`,
    chapters: [
      { title: "Introducción y parte general", topics: ["Norma general antielusión", "Principios constitucionales"] },
      { title: "Fuentes y la obligación tributaria" },
      { title: "El proceso tributario" },
      { title: "Ley sobre Impuesto a la Renta", topics: ["Primera categoría", "Impuestos al trabajo", "Impuesto adicional"] },
    ],
  },
  {
    number: 18,
    name: "Fundamentos del Derecho",
    kind: "electiva",
    pdf: `${PDF}Fundamentos_del_Derecho_18.03.2021.pdf`,
    chapters: [
      { title: "Naturaleza del conocimiento filosófico" },
      { title: "El hombre como sujeto de derecho: consideración antropológica" },
      { title: "El hombre como sujeto de derecho: consideración metafísica" },
      { title: "El hombre como sujeto de derecho: consideración teológica" },
      { title: "El hombre como ser personal y los fundamentos del derecho" },
    ],
  },
  { number: 19, name: "Derecho Internacional Privado", kind: "suspendida", chapters: [] },
];
