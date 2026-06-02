const ALLOWED_PRODUCTION_ORIGIN = 'https://alessandro-gentili.it';
const LOCALHOST_ORIGIN_PATTERN = /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/;
const MIN_TEXT_CHARS = 600;
const MAX_TEXT_CHARS = 12000;
const OPENAI_RESPONSES_URL = 'https://api.openai.com/v1/responses';
const DEFAULT_OPENAI_MODEL = 'gpt-4.1-mini';
const REQUEST_TIMEOUT_MS = 45000;

const ENUMS = {
  text_type: ['essay', 'article', 'newsletter', 'website_page', 'long_post', 'white_paper'],
  audience: ['general', 'professional', 'cultural', 'corporate', 'international'],
  goal: ['clarify', 'persuade', 'position', 'argue', 'publish'],
  severity: ['standard', 'severe', 'very_severe']
};

const REPORT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: [
    'meta',
    'verdict',
    'scores',
    'strengths',
    'weaknesses',
    'revision_priorities',
    'final_recommendation',
    'method_note'
  ],
  properties: {
    meta: {
      type: 'object',
      additionalProperties: false,
      required: ['version', 'mode', 'text_type', 'audience', 'goal', 'severity', 'char_count', 'evaluation_limits', 'confidence'],
      properties: {
        version: { type: 'string', enum: ['0.2'] },
        mode: { type: 'string', enum: ['ai'] },
        text_type: { type: 'string', enum: ENUMS.text_type },
        audience: { type: 'string', enum: ENUMS.audience },
        goal: { type: 'string', enum: ENUMS.goal },
        severity: { type: 'string', enum: ENUMS.severity },
        char_count: { type: 'integer' },
        evaluation_limits: { type: 'array', items: { type: 'string' } },
        confidence: { type: 'number' }
      }
    },
    verdict: {
      type: 'object',
      additionalProperties: false,
      required: ['label', 'summary'],
      properties: {
        label: { type: 'string' },
        summary: { type: 'string' }
      }
    },
    scores: {
      type: 'object',
      additionalProperties: false,
      required: ['overall', 'thesis', 'structure', 'clarity', 'voice', 'density', 'readability', 'generic_ai_tone_risk'],
      properties: {
        overall: scoreSchema(),
        thesis: scoreSchema(),
        structure: scoreSchema(),
        clarity: scoreSchema(),
        voice: scoreSchema(),
        density: scoreSchema(),
        readability: scoreSchema(),
        generic_ai_tone_risk: scoreSchema()
      }
    },
    strengths: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['title', 'detail'],
        properties: {
          title: { type: 'string' },
          detail: { type: 'string' }
        }
      }
    },
    weaknesses: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['title', 'detail', 'severity'],
        properties: {
          title: { type: 'string' },
          detail: { type: 'string' },
          severity: { type: 'string', enum: ['low', 'medium', 'high'] }
        }
      }
    },
    revision_priorities: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['priority', 'action', 'reason'],
        properties: {
          priority: { type: 'integer', enum: [1, 2, 3] },
          action: { type: 'string' },
          reason: { type: 'string' }
        }
      }
    },
    final_recommendation: {
      type: 'object',
      additionalProperties: false,
      required: ['decision', 'summary', 'next_step'],
      properties: {
        decision: { type: 'string', enum: ['ready', 'revise_lightly', 'revise_substantially', 'not_ready'] },
        summary: { type: 'string' },
        next_step: { type: 'string' }
      }
    },
    method_note: {
      type: 'object',
      additionalProperties: false,
      required: ['summary'],
      properties: {
        summary: { type: 'string' }
      }
    }
  }
};

function scoreSchema() {
  return { type: 'integer' };
}

export default {
  async fetch(request, env) {
    const requestUrl = new URL(request.url);

    if (requestUrl.pathname !== '/analyze') {
      return jsonResponse({ ok: false, error: { code: 'NOT_FOUND', message: 'Endpoint non disponibile.' } }, 404, request, env);
    }

    if (request.method === 'OPTIONS') {
      return handleOptions(request, env);
    }

    if (request.method !== 'POST') {
      safeLog({ status: 405, code: 'METHOD_NOT_ALLOWED' });
      return jsonResponse(errorBody('METHOD_NOT_ALLOWED', 'Usa POST /analyze.'), 405, request, env, { Allow: 'POST, OPTIONS' });
    }

    const originCheck = getAllowedOrigin(request, env);
    if (!originCheck.allowed) {
      safeLog({ status: 403, code: 'ORIGIN_NOT_ALLOWED' });
      return jsonResponse(errorBody('ORIGIN_NOT_ALLOWED', 'Origin non consentito.'), 403, request, env);
    }

    const contentType = request.headers.get('content-type') || '';
    if (contentType.split(';')[0].trim().toLowerCase() !== 'application/json') {
      safeLog({ status: 400, code: 'INVALID_CONTENT_TYPE' });
      return jsonResponse(errorBody('INVALID_CONTENT_TYPE', 'Content-Type richiesto: application/json.'), 400, request, env);
    }

    let payload;
    try {
      payload = await request.json();
    } catch {
      safeLog({ status: 400, code: 'INVALID_PAYLOAD' });
      return jsonResponse(errorBody('INVALID_PAYLOAD', 'JSON non valido.'), 400, request, env);
    }

    const validation = validatePayload(payload);
    if (!validation.ok) {
      safeLog({ status: validation.status, code: validation.code, char_count: validation.charCount });
      return jsonResponse(errorBody(validation.code, validation.message), validation.status, request, env);
    }

    if (!env.OPENAI_API_KEY) {
      safeLog({ status: 502, code: 'MODEL_ERROR', char_count: validation.charCount });
      return jsonResponse(errorBody('MODEL_ERROR', 'Backend AI non configurato.'), 502, request, env);
    }

    try {
      const modelReport = await callOpenAI(validation.value, env);
      const report = normalizeReport(modelReport, validation.value);
      safeLog({ status: 200, char_count: validation.charCount });
      return jsonResponse({ ok: true, report }, 200, request, env);
    } catch (error) {
      const code = error && typeof error.code === 'string' ? error.code : 'MODEL_ERROR';
      const status = error && Number.isInteger(error.status) ? error.status : 502;
      safeLog({ status, code, char_count: validation.charCount });
      return jsonResponse(errorBody(code, publicErrorMessage(code)), status, request, env);
    }
  }
};

function getAllowedOrigin(request, env) {
  const origin = request.headers.get('Origin');
  if (origin === ALLOWED_PRODUCTION_ORIGIN) return { allowed: true, origin };
  if (env.ALLOW_LOCALHOST === 'true' && origin && LOCALHOST_ORIGIN_PATTERN.test(origin)) return { allowed: true, origin };
  return { allowed: false, origin: null };
}

function handleOptions(request, env) {
  const originCheck = getAllowedOrigin(request, env);
  if (!originCheck.allowed) {
    safeLog({ status: 403, code: 'ORIGIN_NOT_ALLOWED' });
    return jsonResponse(errorBody('ORIGIN_NOT_ALLOWED', 'Origin non consentito.'), 403, request, env);
  }

  return new Response(null, {
    status: 204,
    headers: corsHeaders(originCheck.origin, {
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400'
    })
  });
}

function validatePayload(payload) {
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
    return invalid('INVALID_PAYLOAD', 'Payload non valido.', 400);
  }

  const text = typeof payload.text === 'string' ? payload.text.trim() : '';
  const charCount = text.length;

  if (!text || typeof payload.text_type !== 'string' || typeof payload.audience !== 'string' || typeof payload.goal !== 'string' || typeof payload.severity !== 'string') {
    return invalid('INVALID_PAYLOAD', 'Campi richiesti: text, text_type, audience, goal, severity.', 400, charCount);
  }

  if (!ENUMS.text_type.includes(payload.text_type) || !ENUMS.audience.includes(payload.audience) || !ENUMS.goal.includes(payload.goal) || !ENUMS.severity.includes(payload.severity)) {
    return invalid('INVALID_PAYLOAD', 'Uno o più parametri non sono ammessi.', 400, charCount);
  }

  if (charCount < MIN_TEXT_CHARS) {
    return invalid('TEXT_TOO_SHORT', `Il testo deve contenere almeno ${MIN_TEXT_CHARS} caratteri.`, 400, charCount);
  }

  if (charCount > MAX_TEXT_CHARS) {
    return invalid('TEXT_TOO_LONG', `Il testo non può superare ${MAX_TEXT_CHARS} caratteri.`, 413, charCount);
  }

  return {
    ok: true,
    charCount,
    value: {
      text,
      text_type: payload.text_type,
      audience: payload.audience,
      goal: payload.goal,
      severity: payload.severity,
      char_count: charCount
    }
  };
}

function invalid(code, message, status, charCount = 0) {
  return { ok: false, code, message, status, charCount };
}

async function callOpenAI(input, env) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(OPENAI_RESPONSES_URL, {
      method: 'POST',
      signal: controller.signal,
      headers: {
        Authorization: `Bearer ${env.OPENAI_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: env.OPENAI_MODEL || DEFAULT_OPENAI_MODEL,
        input: [
          { role: 'system', content: buildSystemPrompt() },
          { role: 'user', content: buildOperationalPrompt(input) }
        ],
        text: {
          format: {
            type: 'json_schema',
            name: 'lente_editoriale_report_v02',
            strict: true,
            schema: REPORT_SCHEMA
          }
        },
        max_output_tokens: 2200
      })
    });

    if (response.status === 429) throw modelError('RATE_LIMITED', 429);
    if (!response.ok) throw modelError('MODEL_ERROR', response.status >= 500 ? 502 : 502);

    const data = await response.json();
    const text = extractOutputText(data);
    if (!text) throw modelError('MODEL_JSON_INVALID', 502);

    try {
      return JSON.parse(text);
    } catch {
      throw modelError('MODEL_JSON_INVALID', 502);
    }
  } catch (error) {
    if (error && error.name === 'AbortError') throw modelError('MODEL_ERROR', 504);
    if (error && error.code) throw error;
    throw modelError('MODEL_ERROR', 502);
  } finally {
    clearTimeout(timeout);
  }
}

function buildSystemPrompt() {
  return [
    'Sei Lente Editoriale v0.2, un revisore editoriale severo, prudente e non sostitutivo di un editor umano.',
    'Valuta il testo senza riscriverlo integralmente e senza produrre markdown.',
    'Non promettere rilevazione AI, plagio check, fact checking esaustivo o verifica delle fonti.',
    'Restituisci esclusivamente JSON valido conforme allo schema fornito.',
    'Adatta il giudizio a tipo di testo, pubblico, obiettivo e severità.',
    'La metrica generic_ai_tone_risk è inversa: 0 significa rischio basso, 100 rischio alto.',
    'Dichiara sempre i limiti della valutazione in evaluation_limits e method_note.',
    'Non includere nel report citazioni lunghe o porzioni estese del testo inviato.'
  ].join(' ');
}

function buildOperationalPrompt(input) {
  return JSON.stringify({
    task: 'Genera un referto editoriale severo in italiano. Valuta tesi, struttura, chiarezza, voce, densità, leggibilità e rischio di tono generico/AI-like senza riscrivere il testo.',
    constraints: {
      version: '0.2',
      mode: 'ai',
      exact_strengths: 3,
      exact_weaknesses: 3,
      exact_revision_priorities: 3,
      scores_range: '0-100 integers',
      confidence_range: '0-1 number',
      no_markdown: true,
      no_plagiarism_check: true,
      no_ai_detection_claim: true,
      no_full_rewrite: true
    },
    input: {
      text_type: input.text_type,
      audience: input.audience,
      goal: input.goal,
      severity: input.severity,
      char_count: input.char_count,
      text: input.text
    }
  });
}

function extractOutputText(data) {
  if (typeof data.output_text === 'string') return data.output_text;
  if (!Array.isArray(data.output)) return '';

  for (const item of data.output) {
    if (!Array.isArray(item.content)) continue;
    for (const content of item.content) {
      if (content.type === 'output_text' && typeof content.text === 'string') return content.text;
      if (typeof content.text === 'string') return content.text;
    }
  }

  return '';
}

function normalizeReport(report, input) {
  if (!report || typeof report !== 'object') throw modelError('MODEL_JSON_INVALID', 502);

  return {
    meta: {
      version: '0.2',
      mode: 'ai',
      text_type: input.text_type,
      audience: input.audience,
      goal: input.goal,
      severity: input.severity,
      char_count: input.char_count,
      evaluation_limits: normalizeStringArray(report.meta?.evaluation_limits, 1, 4, ['Valutazione editoriale automatica non sostitutiva di un editor umano.']),
      confidence: clampNumber(report.meta?.confidence, 0, 1)
    },
    verdict: {
      label: normalizeString(report.verdict?.label, 'Referto editoriale generato'),
      summary: normalizeString(report.verdict?.summary, 'Il testo richiede una revisione editoriale mirata.')
    },
    scores: normalizeScores(report.scores),
    strengths: normalizeObjectList(report.strengths, 3, (item) => ({
      title: normalizeString(item?.title, 'Punto forte'),
      detail: normalizeString(item?.detail, 'Elemento utile da preservare nella revisione.')
    })),
    weaknesses: normalizeObjectList(report.weaknesses, 3, (item) => ({
      title: normalizeString(item?.title, 'Criticità'),
      detail: normalizeString(item?.detail, 'Aspetto da chiarire o rafforzare.'),
      severity: ['low', 'medium', 'high'].includes(item?.severity) ? item.severity : 'medium'
    })),
    revision_priorities: normalizeObjectList(report.revision_priorities, 3, (item, index) => ({
      priority: index + 1,
      action: normalizeString(item?.action, 'Rivedere una priorità editoriale.'),
      reason: normalizeString(item?.reason, 'Serve ad aumentare leggibilità ed efficacia del testo.')
    })),
    final_recommendation: {
      decision: ['ready', 'revise_lightly', 'revise_substantially', 'not_ready'].includes(report.final_recommendation?.decision)
        ? report.final_recommendation.decision
        : 'revise_substantially',
      summary: normalizeString(report.final_recommendation?.summary, 'Procedere con una revisione prima della pubblicazione.'),
      next_step: normalizeString(report.final_recommendation?.next_step, 'Definire una priorità di revisione e intervenire sul testo.')
    },
    method_note: {
      summary: normalizeString(report.method_note?.summary, 'Analisi automatica limitata al testo fornito e ai parametri selezionati; non include verifica fonti, plagio check o AI detection.')
    }
  };
}

function normalizeScores(scores = {}) {
  return {
    overall: clampInteger(scores.overall, 0, 100),
    thesis: clampInteger(scores.thesis, 0, 100),
    structure: clampInteger(scores.structure, 0, 100),
    clarity: clampInteger(scores.clarity, 0, 100),
    voice: clampInteger(scores.voice, 0, 100),
    density: clampInteger(scores.density, 0, 100),
    readability: clampInteger(scores.readability, 0, 100),
    generic_ai_tone_risk: clampInteger(scores.generic_ai_tone_risk, 0, 100)
  };
}

function normalizeObjectList(list, size, mapper) {
  const source = Array.isArray(list) ? list.slice(0, size) : [];
  while (source.length < size) source.push({});
  return source.map(mapper);
}

function normalizeStringArray(list, min, max, fallback) {
  const values = Array.isArray(list) ? list.filter((item) => typeof item === 'string' && item.trim()).map((item) => item.trim()).slice(0, max) : [];
  while (values.length < min) values.push(fallback[values.length] || fallback[0]);
  return values;
}

function normalizeString(value, fallback) {
  return typeof value === 'string' && value.trim() ? value.trim() : fallback;
}

function clampInteger(value, min, max) {
  return Math.round(clampNumber(value, min, max));
}

function clampNumber(value, min, max) {
  const number = Number(value);
  if (!Number.isFinite(number)) return min;
  return Math.min(Math.max(number, min), max);
}

function modelError(code, status) {
  const error = new Error(code);
  error.code = code;
  error.status = status;
  return error;
}

function publicErrorMessage(code) {
  const messages = {
    MODEL_ERROR: 'Il modello non ha restituito un risultato utilizzabile.',
    MODEL_JSON_INVALID: 'Il modello ha restituito JSON non valido.',
    RATE_LIMITED: 'Troppe richieste in questo momento. Riprova più tardi.'
  };
  return messages[code] || 'Errore backend.';
}

function errorBody(code, message) {
  return { ok: false, error: { code, message } };
}

function jsonResponse(body, status, request, env, headers = {}) {
  const originCheck = getAllowedOrigin(request, env);
  return new Response(JSON.stringify(body), {
    status,
    headers: corsHeaders(originCheck.allowed ? originCheck.origin : null, {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      ...headers
    })
  });
}

function corsHeaders(origin, headers = {}) {
  const baseHeaders = { ...headers };
  if (origin) {
    baseHeaders['Access-Control-Allow-Origin'] = origin;
    baseHeaders.Vary = 'Origin';
  }
  return baseHeaders;
}

function safeLog(metadata) {
  console.log(JSON.stringify(metadata));
}
