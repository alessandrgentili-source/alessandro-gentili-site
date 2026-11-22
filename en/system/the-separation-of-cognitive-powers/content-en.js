'use strict';

const titles = [
  'The Separation of Cognitive Powers',
  'Five questions for the work of tomorrow',
  'It all began with a poem',
  'Quality takes more than a claim',
  'Knowledge takes shape',
  'From need to system',
  'Separate the cognitive powers',
  'Starting tomorrow, a better process'
];
const source = {
  essay: 'https://alessandro-gentili.it/saggi/saggio-20-il-futuro-degli-altri.html',
  triadIT: 'https://alessandro-gentili.it/cerchi/triadi/#decima-triade',
  triadEN: 'https://alessandro-gentili.it/en/cerchi/triads/#triad-10',
  privacy: 'https://www.garanteprivacy.it/web/guest/home/principi-fondamentali-del-trattamento',
  law: 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679'
};
const questions = [
  ['The need', 'Start with a real difficulty.', 'A summary that is hard to check is a well-defined problem to work on.'],
  ['The knowledge', 'Choose what to rely on.', 'Use public or authorised documents, original sources and the expertise to interpret them.'],
  ['The process', 'Make the steps repeatable.', 'Define inputs, proposal, checks and approval before asking for an answer.'],
  ['The responsibility', 'Name the roles.', 'Who prepares the draft? Who checks the sources? Who can authorise its use?'],
  ['The learning', 'Measure the whole job.', 'Consider quality, corrections and total time, including the cost of verification.']
];
const story = [
  '<strong>Voice gives direction.</strong> Before the text comes a question and a point of view you can answer for.',
  '<strong>Research provides support.</strong> Consult works and documents and distinguish the source from its interpretation.',
  '<strong>Revision puts the work to the test.</strong> Check claims, quotations, coherence and register.',
  '<strong>Publication brings responsibility.</strong> The author decides what to make public and which references to provide.'
];
const editorial = [
  'Look for repeated phrases, an impersonal tone and overconfident claims.',
  'Open the original document. Every important claim should be verifiable.',
  'Keep, revise or remove the wording, and explain the reason for the editorial choice.'
];
const principles = [
  ['Data minimisation', 'Use relevant data and limit it to what the purpose requires.'],
  ['Accuracy', 'Check that the data is accurate and, where necessary, up to date.'],
  ['Storage limitation', 'Relate the retention period to the purpose and consider the applicable provisions.']
];
const method = [
  ['Thinking', 'What outcome do we really need?', 'One page for a colleague that distinguishes data minimisation, accuracy and storage limitation.', 'The intended reader, the need and the success criterion.'],
  ['Planning', 'Which sources should we use, and within what limits?', 'Select the Italian Data Protection Authority’s guidance. Record the URL and date and check which tools are permitted.', 'The source, scope of use and people involved.'],
  ['System', 'How can we make the work repeatable?', 'Prepare a brief and a record of checks, and define the reviewer’s role.', 'Permitted inputs, instructions, review and approval.'],
  ['Execution', 'Where does drafting end and checking begin?', 'AI can propose three definitions. A person compares them with the original document.', 'Claim → source → verification outcome.'],
  ['Evaluation', 'Is the process useful?', 'Assess accuracy, omissions, corrections and total time, including the review.', 'Criteria to measure. No outcomes established yet.'],
  ['Evolution', 'What changes in the next trial?', 'Revise the brief or the checks. If the process proves of little use, change the approach or stop.', 'A fresh decision about the original need.']
];
const powerBodies = [
  '<span class="mini">01 / Proposal</span><h3>It sounds precise.<br>Is it reliable?</h3><p>A numerical deadline and a reference to a regulation can make a false claim sound plausible.</p><button class="action" data-power-next>Check against the source <span>→</span></button>',
  '<span class="mini">02 / Check · Art. 5(1)(e)</span><h3>Retention depends<br>on the purpose.</h3><p>The regulation sets no universal 30-day deadline. The proposal is unsupported.</p><button class="action" data-power-next>Go to the decision <span>→</span></button>',
  '<span class="mini">03 / Professional decision · Exercise</span><h3>Verification informs.<br>A person decides.</h3><p>Choose how to handle the unsupported claim.</p><div class="decision-buttons"><button data-decision="correct" aria-pressed="false">Correct</button><button data-decision="reject" aria-pressed="false">Reject</button></div><p class="decision-feedback" role="status"></p>'
];
const copy = {
  detail: 'Further reading',
  announce: n => `Scene ${n} of 8.`,
  makeExplicit: 'MAKE EXPLICIT',
  animationsOff: 'Animations disabled',
  animationsOn: 'Animations enabled, subject to system preferences',
  index: 'Eight scenes',
  indexKicker: 'Index · Choose a scene',
  corrected: 'Illustrative outcome: revise the claim, then submit the new version for verification and approval.',
  rejected: 'Illustrative outcome: remove the claim and record why it was rejected.'
};
function triadBody() {
  return `<p class="notice">Original excerpts from both publications, retrieved on 9 November 2026. The original wording is preserved and formatted here for reading. This is an excerpt from each site edition.</p>
  <div class="triad-switch" aria-label="Triad edition"><button data-language="it" lang="it" aria-pressed="false">Italiano</button><button data-language="en" lang="en" aria-pressed="true">English</button></div>
  <div class="triad-source" data-language-panel="it" lang="it" hidden>${CONTENT.triadIT}</div><div class="triad-source" data-language-panel="en" lang="en">${CONTENT.triadEN}</div>
  <div class="source-row">${external(source.triadIT, 'Original Italian publication')}${external(source.triadEN, 'Original English publication')}</div>
  <p class="source-meta">The six guide links open online pages when selected. Publication establishes that the project exists. Its educational benefit remains to be established.</p>`;
}
const details = {
  essay: ['Essay 20 · The Future of Others', () => `<img class="local-proof" src="assets/saggio-20-cover.webp" alt="Original cover of Essay 20: The Future of Others">
  <p><b>Observable fact:</b> the essay was published on 29 October 2026 with the full text, publication details, related author studies, references and a note in English.</p>
  <p>The cover comes from the original page. It provides no evidence of time savings, generative output or the method’s effectiveness.</p>
  ${external(source.essay, 'Open the published essay (in Italian)')}
  <p class="source-meta">Source consulted on 9 November 2026. The note on AI use mentioned in earlier materials could not be found on the page and is therefore not attributed to the essay.</p>`, 'Demonstrate · Public artefact'],
  privacy: ['Three principles, three checks', () => `<p class="notice">Teaching paraphrases of three selected principles from Article 5 of the GDPR.</p>
  <div class="source-row"><h3>Quantity → Data minimisation</h3><p>Limit the data to what is relevant and necessary for the purpose.</p></div>
  <div class="source-row"><h3>Accuracy → Accuracy principle</h3><p>Check that the data is accurate and, where necessary, up to date.</p></div>
  <div class="source-row"><h3>Duration → Storage limitation</h3><p>Retention is tied to the purposes of processing. For a specific case, consider the applicable rules and any exceptions.</p></div>
  ${external(source.privacy, 'Italian Data Protection Authority · Processing principles (in Italian)')}${external(source.law, 'EUR-Lex · Legal text')}
  <p class="source-meta">The Authority’s guidance was consulted on 9 November 2026. The fact that data is public gives no automatic permission to use it in any tool. Purpose, authorisations and organisational rules still apply.</p>`, 'Verify · Italian Data Protection Authority'],
  law: ['The 30-day rule does not hold up', () => `<p class="notice">The “30 days” claim was invented for the exercise. It does not represent an observed response from an AI system.</p>
  <h3>Regulation (EU) 2016/679<br>Article 5(1)(e)</h3>
  <blockquote class="notice">“for no longer than is necessary for the purposes for which the personal data are processed”</blockquote>
  <p class="source-meta">Short extract from Article 5(1)(e). The indexed EUR-Lex text was checked on 9 November 2026 for the original presentation. The linked English text provides the full context.</p>
  <p>The retention period is tied to the purposes of processing. The provision also allows longer retention for certain purposes, subject to adequate safeguards. It sets no universal 30-day deadline.</p>
  <p>This teaching paraphrase does not determine a retention period for an operational case.</p>
  ${external(source.law, 'Read the original regulation')}${external(source.privacy, 'Read the Authority’s summary (in Italian)')}
  <p class="source-meta">EUR-Lex may request a browser check. The teaching example is available offline. Opening the original text requires a connection.</p>
  <h3>Record of the check in this exercise</h3><p><b>Source:</b> Art. 5(1)(e).<br><b>Outcome:</b> the proposed universal rule is unsupported.<br><b>Decision:</b> correct or reject it.<br><b>Responsibility:</b> identify the qualified professional in your own context.</p>`, 'Verify · Legal source'],
  triad: ['Matter, medium and information', triadBody, 'Demonstrate · Circles of Ink'],
  github: ['GitHub Traffic', () => `<img class="github-dialog-image" src="assets/github-traffic-2026-11-09.png" width="1672" height="941" alt="GitHub Traffic for the alessandro-gentili-site repository: 2,851 clones and 589 unique cloners in the last 14 days. Two original charts, with a tooltip on 6 November showing 1,148 clones.">
  <p class="source-meta">GitHub Traffic · alessandro-gentili-site repository · Recorded on 9 November 2026.</p><p class="source-meta">Repository clones and website visits are different measures. Clone counts alone establish neither economic value nor professional impact.</p>`, 'Observe · Evidence supplied by the author'],
  paola: ['Paola — prototype', () => `<img class="paola-dialog-image" src="assets/paola-accesso-2026-10-15.png" width="1440" height="900" alt="Paola prototype sign-in screen documented on 15 October 2026. The sign-in fields are empty.">
  <p class="paola-dialog-caption">Paola prototype · Sign-in screen documented on 15 October 2026</p>`, 'Demonstrate · Original screenshot']
};
const introduction = ['How to read this presentation', `<p><b>Explore:</b> select questions, stages or concepts and apply them to a case.</p><p><b>Verify:</b> compare claims with original sources.</p><p><b>Demonstrate:</b> look at actual publications and source materials.</p>
<div class="notice"><b>Facts:</b> observable publications and attributed accounts.<br><b>Hypotheses:</b> benefits and criteria still to be measured.<br><b>Decisions:</b> choices reported in the author’s materials.</div>
<p>The presentation and local excerpts work offline. Links marked “online” require a connection.</p>`];
const help = ['Presentation controls', `<p><b>← / → or Page Up / Down</b> · change scene<br><b>Home / End</b> · first / last scene<br><b>E</b> · sources and further reading<br><b>F</b> · full screen<br><b>S</b> · turn off animations<br><b>Esc</b> · close the panel and return focus to the control that opened it</p>
<p>Tab and Shift+Tab move focus. Enter or Space activates a button. The navigation arrows leave text fields unaffected.</p>
<p><a href="reading.html" target="_blank" rel="noopener">Accessible reading version</a> · <a href="worksheet.html" target="_blank" rel="noopener">Fillable, printable worksheet</a> · <a href="preview.html" target="_blank" rel="noopener">Preview all eight scenes</a></p><p class="notice">Essential content is available offline. Opening online sources is optional.</p>`, 'Help'];
const fullscreenFallback = ['Full screen unavailable', '<p>The browser did not allow full screen. Use the presentation or full-screen command in the browser menu.</p>'];
