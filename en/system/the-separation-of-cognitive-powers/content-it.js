'use strict';
const titles = ['La separazione dei poteri cognitivi','Cinque domande per il lavoro di domani','Tutto è cominciato con una poesia','La qualità non si autodichiara','La conoscenza prende forma','Dal bisogno al sistema','Separare i poteri cognitivi','Da domani, un processo migliore'];
const source = {
  essay:'https://alessandro-gentili.it/saggi/saggio-20-il-futuro-degli-altri.html',
  triadIT:'https://alessandro-gentili.it/cerchi/triadi/#decima-triade',
  triadEN:'https://alessandro-gentili.it/en/cerchi/triads/#triad-10',
  privacy:'https://www.garanteprivacy.it/web/guest/home/principi-fondamentali-del-trattamento',
  law:'https://eur-lex.europa.eu/eli/reg/2016/679/oj/ita'
};
const questions = [
 ['Il bisogno','Partire da un attrito reale.','Una sintesi difficile da controllare è un problema circoscritto su cui lavorare.'],
 ['La conoscenza','Scegliere su che cosa fondarsi.','Documenti pubblici o autorizzati, fonti originarie e competenze per interpretarli.'],
 ['Il processo','Rendere i passaggi ripetibili.','Definire input, proposta, riscontri e approvazione prima di chiedere una risposta.'],
 ['La responsabilità','Dare un nome ai ruoli.','Chi prepara la bozza? Chi controlla le fonti? Chi può autorizzarne l’uso?'],
 ['L’apprendimento','Misurare tutto il lavoro.','Considerare qualità, correzioni e tempo totale, compreso il costo della verifica.']
];
const story = [
 '<strong>La voce orienta.</strong> Prima del testo, una domanda e un punto di vista di cui rispondere.',
 '<strong>La ricerca sostiene.</strong> Aprire opere e documenti; distinguere il riferimento dall’interpretazione.',
 '<strong>La revisione mette alla prova.</strong> Confrontare affermazioni, citazioni, coerenza e registro.',
 '<strong>La pubblicazione impegna.</strong> L’autore decide che cosa rendere pubblico e con quali riferimenti.'
];
const editorial = [
 'Individuare formule ripetute, tono impersonale e affermazioni troppo sicure.',
 'Aprire il documento originale. Ogni affermazione importante deve poter essere riscontrata.',
 'Conservare, correggere o eliminare una formulazione, motivando la scelta autoriale.'
];
const principles = [
 ['Minimizzazione','Usare dati pertinenti e limitati a quanto serve alla finalità.'],
 ['Esattezza','Controllare correttezza e, quando necessario, aggiornamento dei dati.'],
 ['Limitazione della conservazione','Collegare la durata alla finalità, considerando le disposizioni applicabili.']
];
const method = [
 ['Pensiero','Quale risultato serve davvero?','Una pagina che distingua minimizzazione, esattezza e conservazione per un collega.','Destinatario, bisogno e criterio di riuscita.'],
 ['Pianificazione','Su quali fonti e con quali vincoli?','Scegliere la scheda del Garante. Annotare URL e data; verificare gli strumenti consentiti.','Fonte, perimetro d’uso e persone coinvolte.'],
 ['Sistema','Come rendere ripetibile il lavoro?','Preparare una consegna, un registro dei riscontri e il ruolo del revisore.','Input ammessi, istruzioni, controllo e approvazione.'],
 ['Esecuzione','Dove finisce la bozza e inizia il controllo?','L’IA può proporre tre definizioni. Una persona le confronta con il documento originale.','Affermazione → fonte → esito della verifica.'],
 ['Valutazione','Il processo produce utilità?','Valutare correttezza, omissioni, correzioni e tempo totale, incluso il controllo.','Criteri da misurare. Nessun risultato già acquisito.'],
 ['Evoluzione','Che cosa cambia alla prossima prova?','Correggere la consegna o i controlli. Se l’utilità non emerge, cambiare approccio o fermarsi.','Una nuova decisione sul bisogno iniziale.']
];
const powerBodies = [
 '<span class="mini">01 / Proposta</span><h3>Suona precisa.<br>È attendibile?</h3><p>Un termine numerico e un riferimento normativo possono rendere plausibile una frase falsa.</p><button class="action" data-power-next>Confronta con la fonte <span>→</span></button>',
 '<span class="mini">02 / Riscontro · art. 5(1)(e)</span><h3>La durata dipende<br>dalle finalità.</h3><p>La norma non stabilisce un termine universale di 30 giorni. La proposta non è supportata.</p><button class="action" data-power-next>Passa alla decisione <span>→</span></button>',
 '<span class="mini">03 / Decisione professionale · esercizio</span><h3>La verifica informa.<br>La persona decide.</h3><p>Scegli come trattare la frase non supportata.</p><div class="decision-buttons"><button data-decision="correct" aria-pressed="false">Correggere</button><button data-decision="reject" aria-pressed="false">Respingere</button></div><p class="decision-feedback" role="status"></p>'
 ];
const copy = {
 detail: 'Approfondimento',
 announce: n => `Scena ${n} di 8.`,
 makeExplicit: 'DA RENDERE ESPLICITO',
 animationsOff: 'Animazioni disabilitate',
 animationsOn: 'Animazioni abilitate, salvo preferenze del sistema',
 index: 'Otto scene',
 indexKicker: 'Indice · seleziona una scena',
 corrected: 'Esito illustrativo: correggere, poi sottoporre la nuova versione a verifica e approvazione.',
 rejected: 'Esito illustrativo: escludere la frase e registrare il motivo del rifiuto.'
};
const privacyBody = () => `<p class="notice">Parafrasi didattiche dei principi dell’art. 5. Tre controlli selezionati, non l’intero quadro GDPR.</p><div class="source-row"><h3>Quantità → minimizzazione</h3><p>Limitare i dati a quelli pertinenti e necessari allo scopo.</p></div><div class="source-row"><h3>Correttezza → esattezza</h3><p>Verificare che i dati siano corretti e aggiornati quando necessario.</p></div><div class="source-row"><h3>Durata → conservazione</h3><p>La conservazione è legata alle finalità; il caso concreto richiede di considerare le norme applicabili e le eventuali eccezioni.</p></div>${external(source.privacy,'Garante · principi del trattamento')}${external(source.law,'EUR-Lex · testo normativo')}<p class="source-meta">Scheda del Garante consultata il 9 novembre 2026. I dati pubblici non sono automaticamente utilizzabili in qualunque strumento: valgono finalità, autorizzazioni e regole dell’organizzazione.</p>`;
const lawBody = () => `<p class="notice">La frase dei “30 giorni” è inventata per l’esercizio. Non rappresenta una risposta realmente prodotta da un sistema di IA.</p><h3>Regolamento (UE) 2016/679<br>Art. 5, par. 1, lett. e)</h3><blockquote class="notice">«per un arco di tempo non superiore al conseguimento delle finalità per le quali sono trattati»</blockquote><p class="source-meta">Breve estratto dell’art. 5(1)(e); testo indicizzato EUR-Lex riscontrato il 9 novembre 2026. Il contesto completo è nel collegamento originale.</p><p>La durata della conservazione è collegata alle finalità del trattamento. La disposizione considera inoltre alcuni scopi di conservazione più lunga con garanzie adeguate. Non stabilisce un termine universale di 30 giorni.</p><p>Questa è una parafrasi didattica: non determina un periodo di conservazione per un caso operativo.</p>${external(source.law,'Consulta la norma originale')}${external(source.privacy,'Consulta la sintesi del Garante')}<p class="source-meta">EUR-Lex può richiedere una verifica nel browser. Il riscontro didattico resta leggibile offline; l’apertura del testo originale richiede Internet.</p><h3>Traccia del riscontro nell’esercizio</h3><p><b>Fonte:</b> art. 5(1)(e).<br><b>Esito:</b> la regola universale proposta non è supportata.<br><b>Decisione da assumere:</b> correggere o respingere.<br><b>Responsabile:</b> professionista competente da identificare nel proprio contesto.</p>`;
function triadBody(){
 return `<p class="notice">Estratti autentici delle due pubblicazioni, acquisiti il 9 novembre 2026. Testi invariati; impaginazione locale per la consultazione. Non è una replica del sito.</p><div class="triad-switch" aria-label="Edizione della triade"><button data-language="it" lang="it" aria-pressed="true">Italiano</button><button data-language="en" lang="en" aria-pressed="false">English</button></div><div class="triad-source" data-language-panel="it" lang="it">${CONTENT.triadIT}</div><div class="triad-source" data-language-panel="en" lang="en" hidden>${CONTENT.triadEN}</div><div class="source-row">${external(source.triadIT,'Pubblicazione originale IT')}${external(source.triadEN,'Pubblicazione originale EN')}</div><p class="source-meta">I collegamenti alle sei guide aprono pagine online su azione esplicita. La pubblicazione prova l’esistenza del prodotto, non il suo beneficio pedagogico.</p>`;
}
const details = {
 essay: ['Saggio 20 · Il futuro degli altri', () => `<img class="local-proof" src="assets/saggio-20-cover.webp" alt="Copertina originale del Saggio 20"><p><b>Fatto osservabile:</b> pubblicazione del 29 ottobre 2026, testo integrale, coordinate editoriali, studi, riferimenti ed English note.</p><p>La copertina proviene dalla pagina originale. Non documenta risparmi di tempo, esiti generativi o efficacia del metodo.</p>${external(source.essay,'Apri il saggio pubblicato')}<p class="source-meta">Fonte consultata il 9 novembre 2026. Nella pagina corrente non è stata individuata la nota sull’uso dell’IA menzionata nei materiali precedenti; non viene attribuita al saggio.</p>`, 'Dimostrare · artefatto pubblico'],
 privacy: ['Tre princìpi, tre controlli', privacyBody, 'Verificare · Garante Privacy'],
 law: ['La regola dei 30 giorni non regge', lawBody, 'Verificare · fonte normativa'],
 triad: ['Materia, medium e informazione', triadBody, 'Dimostrare · Cerchi d’inchiostro'],
 github: ['GitHub Traffic', () => '<img class="github-dialog-image" src="assets/github-traffic-2026-11-09.png" width="1672" height="941" alt="GitHub Traffic, repository alessandro-gentili-site: 2.851 cloni e 589 clonatori unici negli ultimi 14 giorni. Due grafici originali; tooltip sul 6 novembre con 1.148 cloni."><p class="source-meta">GitHub Traffic · Repository alessandro-gentili-site · Rilevazione del 9 novembre 2026.</p><p class="source-meta">I cloni del repository non equivalgono alle visite del sito e non dimostrano, da soli, valore economico o impatto professionale.</p>', 'Osservare · evidenza fornita dall’autore'],
 paola: ['Paola — prototipo', () => '<img class="paola-dialog-image" src="assets/paola-accesso-2026-10-15.png" width="1440" height="900" alt="Paola — prototipo, schermata di accesso documentata il 15 ottobre 2026. Campi di accesso vuoti."><p class="paola-dialog-caption">Paola — prototipo, schermata di accesso documentata il 15 ottobre 2026</p>', 'Dimostrare · schermata autentica'],
};
const introduction = ['Come leggere questa presentazione','<p><b>Esplorare:</b> selezionare domande, fasi o concetti per applicarli a un caso.</p><p><b>Verificare:</b> confrontare affermazioni e fonti originali.</p><p><b>Dimostrare:</b> osservare pubblicazioni e materiali autentici.</p><div class="notice"><b>Fatti:</b> pubblicazioni osservabili e resoconti attribuiti.<br><b>Ipotesi:</b> benefici e criteri ancora da misurare.<br><b>Decisioni:</b> scelte riportate nei materiali dell’autore.</div><p>La presentazione principale e gli estratti locali funzionano offline. I link contrassegnati “online” richiedono una connessione.</p>'];
const help = ['Comandi della presentazione',`<p><b>← / → oppure Page Up / Down</b> · cambia scena<br><b>Home / End</b> · prima / ultima scena<br><b>E</b> · fonti e approfondimenti<br><b>F</b> · schermo intero<br><b>S</b> · modalità senza animazioni<br><b>Esc</b> · chiude l’approfondimento; il focus torna al comando di origine</p><p>Tab e Maiusc+Tab spostano il focus; Invio o Spazio attivano i pulsanti. Le frecce di navigazione non operano nei campi di scrittura.</p><p><a href="lettura.html" target="_blank" rel="noopener">Versione lettura accessibile</a> · <a href="scheda.html" target="_blank" rel="noopener">Scheda compilabile e stampabile</a> · <a href="anteprima.html" target="_blank" rel="noopener">Anteprima delle otto scene</a></p><p class="notice">Tutto il contenuto essenziale è locale. Le aperture online sono facoltative.</p>`,'Guida all’uso'];
const fullscreenFallback = ['Schermo intero non disponibile','<p>Il browser non ha consentito lo schermo intero. Usa il comando di presentazione o schermo intero nel menu del browser.</p>'];
