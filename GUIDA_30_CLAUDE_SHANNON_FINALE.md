# Claude Shannon — Informazione, rumore e limiti della trasmissione

## La misura dell’informazione e il confine tra comunicare, comprendere e conoscere

Ci sono svolte intellettuali che nascono aggiungendo qualcosa al mondo; quella di Claude Shannon prende forma, anzitutto, da una sottrazione.

Un messaggio può essere una dichiarazione d’amore, una quotazione di borsa, un ordine militare, una pagina di poesia, un errore, una menzogna. Per chi lo riceve, le differenze sono immense. Per il problema che Shannon decide di affrontare, possono essere temporaneamente messe tra parentesi. La domanda diventa un’altra: come rappresentare, codificare e trasmettere un messaggio attraverso un canale, con risorse finite e in presenza di rumore, stabilendo quantitativamente che cosa sia possibile ottenere?

Da questa delimitazione nasce una parte decisiva dell’ingegneria della comunicazione del Novecento. Sorgenti differenti possono essere descritte attraverso probabilità; segnali diversi possono essere confrontati mediante quantità d’informazione; ogni canale possiede limiti; la struttura statistica di una sorgente può essere sfruttata per rappresentarla con maggiore efficienza; la ridondanza può essere introdotta per proteggere la trasmissione dagli errori.

La forza di Shannon sta nel rigore con cui stabilisce che cosa la teoria misura e che cosa lascia fuori.

Oggi chiamiamo “informazione” quasi tutto: dati, notizie, conoscenze, documenti, immagini, risultati di ricerca, contenuti social, risposte generate da una macchina. Il significato tecnico reso misurabile da Shannon è molto più stretto: non garantisce la verità di un contenuto, non coincide con la conoscenza e non misura l’importanza di un messaggio per una vita umana.

Una civiltà può quindi diventare straordinariamente capace di trasmettere informazione e restare esposta a un problema differente: capire che cosa, fra ciò che circola, meriti di essere creduto, compreso, ricordato.

La precisione della teoria e il confine che la rende possibile sono inseparabili.

---

## Indice

1. Claude Shannon in breve
2. Perché Shannon conta
3. Il problema umano: che cosa scegliamo di lasciare fuori
4. Vita essenziale
5. La vita che illumina l’opera
6. Il contesto: quando comunicare diventa un problema matematico
7. Cerchi disciplinari
8. Opere e contributi principali
9. Prima rivoluzione: quando la logica entra nei circuiti
10. *A Mathematical Theory of Communication*
11. Il prezzo dell’astrazione
12. Che cosa significa “informazione”
13. Il bit: una misura, non una metafisica
14. Entropia: misurare l’incertezza
15. Canale, rumore e capacità
16. La ridondanza che salva il messaggio
17. Compressione, distorsione e correzione degli errori
18. Il significato messo tra parentesi
19. Shannon e Weaver
20. Shannon e Wiener
21. Shannon e Turing
22. Crittografia e segretezza
23. Scacchi, automi e problemi trattabili
24. La forma del pensiero di Shannon
25. Idee chiave
26. Concetti chiave
27. Costellazione
28. Eredità
29. Lucrezio, McLuhan, Shannon
30. Ferita contemporanea: la trasmissione senza comprensione
31. Limiti, tensioni e abusi
32. Curiosità che illuminano il metodo
33. Errori comuni
34. Glossario
35. Percorsi di lettura
36. Domande per orientarsi
37. Nodi da ricordare
38. FAQ
39. Fonti e copyright
40. Prosegui la lettura
41. Chiusura

---

## 1. Claude Shannon in breve

**Claude Elwood Shannon** nasce nel 1916 a Petoskey, nel Michigan, e muore nel 2001. Matematico, ingegnere e ricercatore, attraversa alcuni dei luoghi decisivi della scienza statunitense del Novecento: University of Michigan, MIT, Institute for Advanced Study di Princeton, Bell Laboratories.

Il suo primo risultato destinato a durare nasce dall’incontro fra algebra booleana e circuiti a relè. Mostra come le operazioni logiche possano essere usate sistematicamente per analizzare e progettare reti di commutazione: una connessione fondamentale per la teoria dei circuiti digitali.

Il centro della sua opera è l’articolo del 1948 *A Mathematical Theory of Communication*. Shannon costruisce una teoria generale della trasmissione dell’informazione attraverso canali, rendendo rigorosi concetti che diventeranno centrali nel lessico del digitale: informazione misurabile, bit, entropia, capacità del canale, codifica, ridondanza, rumore.

Il passaggio decisivo consiste nel separare il problema tecnico della comunicazione dal significato semantico del messaggio. La teoria vuole sapere quanto può essere trasmesso, con quale efficienza e con quale affidabilità. Verità, importanza, comprensibilità e valore appartengono ad altri livelli del problema.

Questa delimitazione rende possibile la formalizzazione.

Da qui nasce il paradosso contemporaneo che rende Shannon ancora necessario. Abbiamo costruito una civiltà capace di produrre, archiviare e trasmettere quantità enormi di informazione; quantità d’informazione, significato, conoscenza e verità restano però grandezze e problemi differenti.

---

## 2. Perché Shannon conta

Prima di Shannon, le telecomunicazioni disponevano già di una straordinaria ricchezza di dispositivi, tecniche e risultati matematici. Telegrafo, telefono e radio avevano creato problemi concreti di velocità, banda, distorsione, rumore, codifica. Harry Nyquist e Ralph Hartley avevano elaborato risultati essenziali sulla trasmissione e sulla misura logaritmica dell’informazione. George Boole aveva costruito nell’Ottocento un’algebra della logica. Norbert Wiener stava trattando comunicazione, filtraggio e previsione come problemi statistici.

Shannon porta questi fili entro una teoria di portata più generale.

L’originalità sta nel definire un oggetto abbastanza preciso da poter essere misurato. Restringere il problema consente di formalizzarlo; proprio quella restrizione produce risultati sorprendentemente generali.

Due risultati ne mostrano la portata.

Il primo riguarda la rappresentazione: una sorgente con una certa struttura statistica possiede un limite teorico alla compressione senza perdita. Se alcuni simboli o sequenze sono più prevedibili di altri, la rappresentazione può sfruttare quella regolarità.

Il secondo riguarda la trasmissione: un canale rumoroso possiede una capacità. Sotto quel limite esistono codifiche capaci, in senso asintotico, di rendere la probabilità d’errore arbitrariamente piccola; sopra il limite la stessa garanzia non è ottenibile.

Una parte decisiva delle infrastrutture digitali nasce dentro queste due domande: **come rappresentare con efficienza** e **come trasmettere con affidabilità**. Shannon rende formulabili limiti che ogni tecnologia concreta deve rispettare o cercare di avvicinare.

---

## 3. Il problema umano: che cosa scegliamo di lasciare fuori

Ogni misura comincia da una scelta: stabilire quali differenze contano per la domanda che stiamo ponendo.

Il problema umano emerge quando il successo di una misura nasconde quella scelta. Ciò che viene contato acquista allora un’evidenza superiore a ciò che resta fuori; una metrica nata per descrivere una parte del fenomeno può finire per rappresentarlo interamente.

Visualizzazioni, probabilità, punteggi, performance e flussi non sono falsi per il solo fatto di essere parziali. Diventano ingannevoli quando la parte misurata sostituisce l’oggetto che pretende soltanto di descrivere.

Shannon rende questa tensione particolarmente leggibile perché il suo ritaglio è dichiarato con precisione. Il problema tecnico della comunicazione viene isolato per poter essere trattato matematicamente. La validità del modello dipende anche dalla chiarezza del confine entro cui opera.

Cerchi d’inchiostro assume qui una lezione metodologica, non una filosofia universale: una formalizzazione responsabile deve conservare memoria di ciò che ha scelto di non misurare.

---

## 4. Vita essenziale

Claude Elwood Shannon nasce il 30 aprile 1916 a Petoskey, nel Michigan, e cresce a Gaylord. Fin da giovane mostra familiarità con apparecchi elettrici e meccanici; lavora anche come messaggero per Western Union.

Nel 1936 conclude alla University of Michigan una doppia formazione in matematica e ingegneria elettrica. La combinazione resterà un tratto riconoscibile della sua intelligenza scientifica: Shannon attraversa continuamente il confine fra teoria e costruzione.

Al MIT lavora come assistente sul **Differential Analyzer** di Vannevar Bush, un grande calcolatore analogico. I circuiti di controllo della macchina utilizzano relè elettromeccanici. Shannon riconosce che gli stati aperto/chiuso degli interruttori possono essere descritti attraverso l’algebra logica di George Boole. La tesi di master viene elaborata nel 1937 e pubblicata nel 1938 come *A Symbolic Analysis of Relay and Switching Circuits*, trasformando quell’intuizione in un metodo per l’analisi e la sintesi dei circuiti.

Nel 1940 consegue al MIT il dottorato in matematica con *An Algebra for Theoretical Genetics*, applicazione di strumenti algebrici alla genetica teorica.

Tra il 1940 e il 1941 è National Research Fellow all’Institute for Advanced Study di Princeton. Nel 1941 entra ai Bell Laboratories, dove durante la guerra lavora su sistemi di controllo, comunicazioni e crittografia. È in questo ambiente che maturano molti degli elementi destinati a convergere nella teoria dell’informazione.

Nel 1948 pubblica in due parti sul *Bell System Technical Journal* *A Mathematical Theory of Communication*. L’anno successivo esce *Communication Theory of Secrecy Systems*, sviluppo pubblico di un rapporto crittografico riservato preparato durante la guerra.

Dal 1956 torna al MIT, inizialmente come visiting professor; nel 1958 diventa Donner Professor of Science. Va in pensione nel 1978.

Muore il 24 febbraio 2001, a ottantaquattro anni.

---

## 5. La vita che illumina l’opera

La biografia di Shannon è interessante quando rende visibile il suo metodo.

Davanti al Differential Analyzer non si limita a comprendere come funziona una macchina. Cerca una struttura comune tra oggetti che appartengono a linguaggi diversi: interruttori elettrici e proposizioni logiche. Nel lavoro sulle telecomunicazioni compie un gesto affine: dietro mezzi differenti — telegrafo, telefono, radio, segnali discreti o continui — cerca una struttura abbastanza generale da rendere confrontabili i problemi.

Anche i suoi oggetti più giocosi hanno questo carattere. Il topo elettromeccanico **Theseus**, capace di percorrere un labirinto e memorizzare il cammino, le macchine per la giocoleria e gli esperimenti sugli scacchi mostrano la stessa inclinazione a trasformare un’idea in dispositivo e a sottoporre un’astrazione alla prova di una macchina. Il gioco diventa così un laboratorio in cui isolare una struttura.

Il suo intervento del 1952 sul pensiero creativo è coerente con questa postura. Shannon insiste su semplificazione, analogia, riformulazione, generalizzazione, scomposizione strutturale e inversione del problema. Sono strategie riconoscibili nelle opere maggiori: eliminare ciò che non serve, cambiare rappresentazione, cercare un livello più generale, invertire il punto di vista.

La conferenza va trattata per ciò che è: un dattiloscritto interno ai Bell Labs del 20 marzo 1952, non un articolo scientifico pubblicato. La bibliografia dei *Collected Papers* lo registra come *typescript* e specifica che non fu incluso nella raccolta; le trascrizioni circolate successivamente ne hanno reso accessibile il contenuto.

Ne emerge una costante: Shannon trova spesso la rappresentazione che rende il problema trattabile prima di cercarne la soluzione.

---

## 6. Il contesto: quando comunicare diventa un problema matematico

Il mondo in cui nasce la teoria di Shannon è già saturo di comunicazioni tecniche.

Il telegrafo aveva imposto il problema della codifica discreta. Il telefono aveva trasformato la voce in segnale elettrico continuo. La radio aveva moltiplicato distanza e interferenze. Le reti telefoniche dovevano usare in modo efficiente infrastrutture costose. Ogni sistema possedeva proprie tecniche, propri vincoli, proprio lessico.

Dentro i Bell Labs, Harry Nyquist aveva studiato la velocità di trasmissione e la relazione fra segnale, banda e interferenza tra simboli. Ralph Hartley aveva proposto nel 1928 una misura logaritmica della quantità d’informazione legata al numero delle possibili selezioni.

A questo si aggiungeva un’altra genealogia: la probabilità, la statistica, la meccanica statistica, il lavoro di Wiener sui processi stocastici, sul filtraggio e sulla previsione.

Shannon unifica senza cancellare le differenze. Un sistema di comunicazione può essere descritto in termini di sorgente, messaggio, trasmettitore, segnale, canale, rumore, ricevitore e destinazione. La natura fisica dei dispositivi conta per l’ingegneria concreta; la teoria cerca una struttura matematica comune.

Scelta fra possibilità, codifica, vincoli del canale e probabilità d’errore diventano così parti di un unico problema formalizzabile.

---

## 7. Cerchi disciplinari

### Matematica

Probabilità, logaritmi, processi stocastici ed entropia consentono di trattare quantitativamente sorgenti e canali.

### Ingegneria elettrica e telecomunicazioni

È il terreno originario della teoria: banda, segnali, rumore, potenza, codifica, trasmissione.

### Logica e circuiti

L’algebra booleana applicata ai relè mostra come operazioni astratte possano diventare architetture fisiche.

### Informatica

Shannon precede l’informatica come disciplina consolidata, ma il suo lavoro sui circuiti e sulla rappresentazione binaria entra nelle fondamenta concettuali del calcolo digitale.

### Crittografia

L’incertezza dell’avversario, la chiave e la segretezza possono essere trattate matematicamente. Shannon contribuisce a trasformare la crittografia moderna in un campo teorico.

### Teoria dei codici

La possibilità di rappresentare efficientemente le sorgenti e proteggere i messaggi dagli errori apre un territorio che verrà sviluppato da Hamming e da molte generazioni successive.

### Cibernetica e teoria dei sistemi

Shannon condivide con Wiener alcuni strumenti e problemi; feedback e controllo occupano però nella cibernetica un ruolo che non definisce il nucleo della teoria dell’informazione.

### Intelligenza artificiale, automi e problem solving

Scacchi, Theseus e teoria degli automi mostrano un interesse reale per memoria, scelta, ricerca e macchine. Shannon è inoltre tra i quattro firmatari della proposta del Dartmouth Summer Research Project on Artificial Intelligence del 1955 e co-curatore con John McCarthy di *Automata Studies* nel 1956. Il rapporto con la nascita storica dell’AI è quindi documentato, senza trasformare Shannon nel padre delle sue forme contemporanee.

### Filosofia dell’informazione

È soprattutto una storia successiva. Il successo della teoria rende inevitabile la domanda su che cosa “informazione” significhi fuori dal dominio ingegneristico. Proprio qui diventano necessari i confini stabiliti da Shannon.

---

## 8. Opere e contributi principali

### *A Symbolic Analysis of Relay and Switching Circuits* — 1938

Applica l’algebra booleana all’analisi e alla progettazione dei circuiti a relè. Il valore storico del lavoro consiste nell’aver reso sistematico il passaggio tra logica simbolica e reti di commutazione.

### *A Mathematical Theory of Communication* — 1948

È il centro dell’opera. Pubblicato in due parti sul *Bell System Technical Journal*, formalizza sorgenti, informazione, entropia, codifica, canali, rumore, capacità e limiti della trasmissione.

### *Communication in the Presence of Noise* — 1949

Sviluppa la rappresentazione geometrica dei segnali, il campionamento e la capacità di canali continui in presenza di rumore. Va letto nel contesto della storia che conduce al teorema oggi associato ai nomi di Nyquist e Shannon.

### *Communication Theory of Secrecy Systems* — 1949

Deriva da un rapporto riservato del periodo bellico. Applica strumenti probabilistici alla crittografia e formalizza, tra l’altro, la nozione di segretezza perfetta.

### *Programming a Computer for Playing Chess* — 1950

Affronta gli scacchi come problema di ricerca in uno spazio enorme di possibilità e discute strategie per renderlo trattabile. Il testo appartiene alla storia iniziale dei problemi che confluiranno nell’intelligenza artificiale, senza contenerne gli sviluppi successivi.

### *Prediction and Entropy of Printed English* — 1951

Studia la prevedibilità statistica dell’inglese scritto e il problema della ridondanza linguistica. Mostra quanto la teoria dell’informazione possa avvicinarsi al linguaggio senza diventare una teoria del significato.

### *Creative Thinking* — 1952

Dattiloscritto di una conferenza interna ai Bell Labs del 20 marzo 1952. È utile soprattutto per comprendere il metodo di Shannon: semplificare, cambiare prospettiva, scomporre e invertire. La sua natura documentaria richiede una cautela bibliografica maggiore rispetto agli articoli scientifici pubblicati.

### Proposta di Dartmouth — 1955

Shannon firma con John McCarthy, Marvin Minsky e Nathaniel Rochester la proposta del Dartmouth Summer Research Project on Artificial Intelligence. Il documento colloca Shannon dentro la formazione storica del campo, senza rendere la teoria dell’informazione una teoria dell’AI.

### *The Bandwagon* — 1956

In questo breve editoriale Shannon mette in guardia contro l’espansione indiscriminata della teoria dell’informazione fuori dal proprio dominio. Le applicazioni in altri campi, sostiene, richiedono ipotesi e verifica: non basta trasferire il vocabolario di informazione, entropia e ridondanza.

### *Automata Studies* — 1956

Volume curato da Shannon e John McCarthy, raccoglie lavori su automi, reti nervose, macchine di Turing e problemi di calcolo. Documenta un altro punto di contatto reale con il nascente campo delle macchine intelligenti.

### *Coding Theorems for a Discrete Source with a Fidelity Criterion* — 1959

Sviluppa in forma più sistematica il rapporto fra tasso di codifica e distorsione tollerabile. È uno dei testi fondativi della teoria rate–distortion e completa il quadro della codifica di sorgente quando la ricostruzione perfetta non è necessaria.

---

## 9. Prima rivoluzione: quando la logica entra nei circuiti

Prima della teoria dell’informazione, Shannon aveva già compiuto un passaggio decisivo.

Un relè può essere aperto o chiuso; una proposizione logica può assumere due valori. Shannon mostra che le regole dell’algebra booleana possono essere usate sistematicamente per descrivere reti di relè, verificarne le equivalenze, semplificarle e progettarle a partire da condizioni logiche desiderate.

Il contributo storico sta nella formalizzazione di un metodo di analisi e sintesi: una struttura logica può diventare una rete fisica di commutazione.

La nascita del computer digitale appartiene a una storia molto più ampia. Il lavoro di Shannon fornisce però un linguaggio teorico fondamentale per la progettazione dei circuiti logici.

È già visibile qui un tratto del suo pensiero: mettere in relazione domini differenti, identificarne una struttura comune e scegliere una rappresentazione che renda il problema manipolabile.

Il circuito può così essere letto come realizzazione fisica di una struttura logica. Metodologicamente, è lo stesso tipo di passaggio che nel 1948 permetterà di riportare tecnologie di comunicazione differenti a una struttura matematica comune.

---

## 10. *A Mathematical Theory of Communication*

L’articolo del 1948 parte da un problema apparentemente semplice: un messaggio viene scelto in un punto e deve essere ricostruito, esattamente o approssimativamente, in un altro.

La semplicità è ingannevole.

Per poter progettare un sistema, il messaggio effettivamente inviato non basta. Occorre considerare l’insieme dei messaggi possibili fra cui la sorgente avrebbe potuto scegliere e le probabilità con cui tali messaggi vengono prodotti.

Il modello generale distingue:

- **sorgente d’informazione**, che genera o seleziona il messaggio;
- **trasmettitore**, che converte il messaggio in un segnale adatto al canale;
- **canale**, cioè il mezzo tecnico attraverso cui il segnale passa;
- **sorgente di rumore**, che introduce perturbazioni;
- **ricevitore**, che ricostruisce il messaggio a partire dal segnale ricevuto;
- **destinazione**, a cui il messaggio è rivolto.

La teoria tratta sistemi discreti, continui e misti. Il problema comune riguarda la rappresentazione e la trasmissione sotto vincoli. Per le sorgenti continue, l’esatta ricostruzione richiederebbe in generale una quantità illimitata di bit; diventa allora necessario esplicitare un **criterio di fedeltà**, cioè quale distorsione della ricostruzione sia accettabile. Questo nucleo verrà sviluppato ulteriormente da Shannon nella teoria rate–distortion.

Qui entrano i concetti che renderanno celebre Shannon.

L’informazione viene collegata alla probabilità delle possibili selezioni. L’entropia misura l’incertezza media di una sorgente. La capacità stabilisce il massimo tasso d’informazione compatibile con un canale. I teoremi di codifica mostrano i limiti fondamentali della compressione e della trasmissione affidabile.

Ciò che colpisce ancora oggi non è soltanto la quantità dei risultati. È il livello al quale Shannon sceglie di porre la domanda.

Telegrafo, voce, immagini e dati diventano casi differenti di un problema comune.

---

## 11. Il prezzo dell’astrazione

L’universalità tecnica di Shannon nasce da una rinuncia controllata.

Per costruire una teoria comune a telegrafo, voce, immagini e dati bisogna ignorare differenze che, in altri contesti, restano decisive. Il formalismo considera struttura statistica, codice, canale e condizioni di ricezione; valore, verità e significato specifico del messaggio non entrano nel calcolo.

Questa esclusione è il contratto dell’astrazione shannoniana. Il modello guadagna generalità proprio perché dichiara il piano su cui opera.

Il prezzo appare quando quel contratto viene dimenticato. Se “informazione” diventa un nome indifferenziato per dati, significati, conoscenze, decisioni o forme di vita, la precisione tecnica del concetto non si trasferisce automaticamente ai nuovi domini.

La lettura proprietaria di Cerchi d’inchiostro sta qui: **un’astrazione resta feconda finché conserva memoria di ciò che ha escluso**.

---

## 12. Che cosa significa “informazione”

Nel linguaggio quotidiano, “informazione” suggerisce contenuto utile: una notizia, una conoscenza, qualcosa che ci rende più consapevoli.

In Shannon il termine assume un significato tecnico diverso.

Una sorgente produce simboli o messaggi secondo certe probabilità. Quanto maggiore è l’incertezza sulla prossima selezione, tanto maggiore è la quantità media d’informazione associata alla sorgente.

In notazione moderna, l’auto-informazione associata a un evento \(x\) di probabilità \(p(x)\) viene espressa come:

\[
I(x) = -\log_2 p(x)
\]

Un evento molto probabile porta poca auto-informazione perché era già atteso; un evento improbabile ne porta di più perché la sua osservazione riduce maggiormente l’incertezza. Questa “sorpresa” è probabilistica, non psicologica.

Se una sorgente genera sempre lo stesso simbolo, non c’è incertezza sulla selezione. Se invece due simboli sono equiprobabili, ogni scelta risolve un’alternativa.

Da qui segue una conseguenza importante: verità e quantità d’informazione appartengono a piani diversi. Un’affermazione falsa ma improbabile può avere alta auto-informazione rispetto alla distribuzione considerata; una verità ripetuta continuamente può aggiungerne pochissima.

La distinzione fra **informazione**, **significato**, **conoscenza** e **verità** non è un dettaglio terminologico: impedisce di chiedere alla misura shannoniana ciò che non è stata costruita per valutare.

---

## 13. Il bit: una misura, non una metafisica

Il bit è diventato una delle unità più familiari del nostro tempo.

La parola è una contrazione di *binary digit*, suggerita da John Tukey e adottata da Shannon nel 1948. Quando si usa il logaritmo in base 2, la quantità d’informazione viene misurata in bit.

Un bit corrisponde, nel caso elementare, alla quantità d’informazione risolta da una scelta fra due alternative equiprobabili.

Qui conviene distinguere due usi spesso sovrapposti. Una **binary digit** è una cifra 0 o 1 usata in una rappresentazione binaria; il **bit come unità d’informazione** misura una quantità. Una cifra binaria equiprobabile porta un bit d’informazione, mentre una sorgente binaria fortemente sbilanciata produce in media meno di un bit per simbolo.

La base 2 è naturale per molti sistemi digitali e rende trasparente il legame con stati come 0/1. La teoria, però, non sostiene che il mondo sia ontologicamente fatto di bit.

Circuiti, memoria, codifica e comunicazioni digitali possono essere progettati con rappresentazioni binarie robuste. Trasformare questa efficacia ingegneristica in una tesi sulla sostanza ultima della realtà significa uscire dal dominio dimostrato dalla teoria.

Per la stessa ragione, il bit non è l’equivalente moderno dell’atomo lucreziano. L’atomo appartiene a una teoria della costituzione della materia; il bit misura informazione e può partecipare a una rappresentazione.

La somiglianza fra “elementi minimi” non cancella la differenza ontologica.

---

## 14. Entropia: misurare l’incertezza

Per una sorgente discreta con possibili esiti \(x_i\) e probabilità \(p_i\), l’entropia di Shannon è espressa, usando la base 2, da:

\[
H(X) = -\sum_i p_i \log_2 p_i
\]

L’entropia misura l’incertezza media della sorgente e, nel modello, il valore atteso dell’informazione associata alle sue selezioni.

Se un esito è certo, l’entropia è minima. A parità di numero di alternative, raggiunge invece il massimo quando gli esiti sono equiprobabili. Per sorgenti con dipendenze temporali, ciò che conta in molti problemi di codifica è il **tasso di entropia**, che tiene conto anche della struttura fra simboli successivi.

Una sorgente regolare contiene prevedibilità sfruttabile; una sorgente meno prevedibile richiede, in media, più informazione per descrivere le sue selezioni.

Il termine “entropia” crea uno dei più resistenti equivoci nella ricezione di Shannon. La formula presenta una parentela matematica con l’entropia della meccanica statistica, ma le grandezze appartengono a quadri teorici differenti e non vanno identificate automaticamente.

Anche il celebre racconto secondo cui John von Neumann avrebbe suggerito il termine a Shannon va trattato come testimonianza retrospettiva, non come documento coevo. La versione più citata deriva dal resoconto pubblicato da Myron Tribus e Edward McIrvine nel 1971 di una conversazione con Shannon avvenuta anni dopo.

Per Shannon l’entropia è una misura definita su una distribuzione di possibilità. Usarla come sinonimo di disordine quotidiano, confusione politica o qualità di un testo richiede un passaggio metaforico ulteriore, che va dichiarato.

---

## 15. Canale, rumore e capacità

Il canale in Shannon è una struttura tecnica di trasmissione.

Può essere un filo, una banda di frequenze, un collegamento radio o qualunque sistema capace di portare un segnale dal trasmettitore al ricevitore. Il canale possiede vincoli: larghezza di banda, potenza, caratteristiche del rumore, probabilità di transizione fra simboli.

Il rumore introduce incertezza fra ciò che viene trasmesso e ciò che viene ricevuto. Nella teoria non coincide con falsità, propaganda o irrilevanza del contenuto: quelle sono estensioni metaforiche che appartengono ad altri livelli.

La nozione di **capacità del canale** stabilisce il massimo tasso compatibile con la trasmissione affidabile secondo il modello considerato.

Per un canale discreto senza memoria, una formulazione moderna è:

\[
C = \max_{p(x)} I(X;Y)
\]

dove \(I(X;Y)\) è l’informazione mutua fra ingresso e uscita e il massimo è preso sulle possibili distribuzioni d’ingresso. Nel 1948 Shannon scrive la stessa struttura in termini di entropia ed **equivocazione**; la notazione \(I(X;Y)\) è la forma oggi più comune.

Per un canale a banda limitata con rumore gaussiano bianco additivo, banda \(B\), potenza media del segnale \(S\) e potenza del rumore \(N\) **nella banda considerata**, la relazione comunemente chiamata formula di Shannon–Hartley è:

\[
C = B \log_2\left(1+\frac{S}{N}\right)
\]

Con \(B\) in hertz e logaritmo in base 2, \(C\) è espresso in bit al secondo. La formula riguarda questo specifico modello di canale e non sostituisce la definizione generale di capacità.

Nyquist aveva studiato i limiti imposti dalla banda alla velocità dei segnali; Hartley aveva collegato la quantità trasmessa al numero di selezioni distinguibili. Shannon incorpora il rumore e mostra che capacità e affidabilità possono essere trattate entro una teoria generale.

Il risultato decisivo è un confine quantitativo: sotto la capacità l’errore può essere reso arbitrariamente piccolo in senso asintotico mediante codici adeguati; sopra la capacità non si ottiene la stessa affidabilità arbitraria.

---

## 16. La ridondanza che salva il messaggio

“Ridondanza” sembra una parola negativa. Nel linguaggio comune suggerisce spreco, ripetizione, inefficienza.

In teoria dell’informazione la stessa parola compare in due funzioni che vanno tenute distinte.

Una **ridondanza della sorgente** nasce dalla prevedibilità statistica: alcune sequenze sono più probabili di altre. Questa struttura può essere sfruttata per rappresentare il messaggio usando, in media, meno risorse. È il principio che rende possibile la compressione senza perdita.

Una **ridondanza di codice**, invece, può essere aggiunta intenzionalmente quando il messaggio deve attraversare un canale rumoroso. Vincoli e simboli aggiuntivi aiutano il ricevitore a rilevare o correggere errori; non aumentano l’informazione prodotta dalla sorgente, ma aumentano la robustezza della rappresentazione trasmessa.

Da qui nasce uno dei paradossi più fertili dell’eredità shannoniana:

**l’efficienza della rappresentazione tende a togliere ridondanza; l’affidabilità della trasmissione può richiedere di aggiungerne.**

Una sorgente può essere compressa per evitare sprechi e il flusso risultante può poi essere protetto con un codice che reintroduce struttura per resistere agli errori. La parola è la stessa; la funzione nel sistema è diversa.

---

## 17. Compressione, distorsione e correzione degli errori

I teoremi di codifica di Shannon disegnano confini differenti a seconda del problema che vogliamo risolvere.

### Codifica della sorgente

Per una sorgente discreta e una ricostruzione senza perdita, la struttura statistica determina quanto sia possibile comprimere in media. L’entropia fornisce il limite fondamentale alla lunghezza media per simbolo, raggiungibile asintoticamente con blocchi sufficientemente lunghi sotto le ipotesi del modello.

Non ogni comunicazione, però, richiede una copia esatta.

Una voce telefonica, un’immagine o un segnale continuo possono tollerare una certa differenza fra originale e ricostruzione. Già nel 1948 Shannon formula il problema mediante criteri di fedeltà; nel 1959 sviluppa in modo più sistematico la relazione fra **tasso di codifica** e **distorsione ammessa**. La compressione con perdita chiede dunque quanta precisione possiamo sacrificare per ridurre le risorse necessarie.

### Codifica del canale

Un canale rumoroso pone un problema differente: proteggere la trasmissione dagli errori.

Nel 1948 Shannon mostra, con un argomento di esistenza basato su insiemi di codici, che sotto la capacità del canale si possono trovare codifiche per cui la frequenza o probabilità d’errore diventa arbitrariamente piccola al crescere della lunghezza dei blocchi. Il risultato è asintotico e non fornisce una ricetta universale per costruire codici efficienti; inoltre, sopra la capacità non è possibile mantenere la stessa garanzia di affidabilità arbitraria.

Una parte enorme della teoria dei codici successiva nasce dentro questo spazio: progettare schemi concretamente implementabili che si avvicinino ai limiti teorici con costi accettabili di complessità, ritardo ed energia.

Compressione senza perdita, compressione con distorsione controllata e protezione dagli errori rispondono quindi a tre domande diverse. La teoria stabilisce i limiti entro cui le tecnologie concrete devono operare.

---

## 18. Il significato messo tra parentesi

Nel saggio del 1948 Shannon formula una delle delimitazioni più famose della scienza del Novecento: gli aspetti semantici del messaggio non sono pertinenti al problema ingegneristico che sta formalizzando.

La frase è precisa. Shannon riconosce che i messaggi hanno significato; stabilisce poi che il sistema deve essere progettato rispetto all’insieme delle possibili selezioni, indipendentemente dal significato particolare del messaggio effettivamente scelto.

La sospensione della semantica rende il modello tecnicamente generale. Una poesia e una tabella meteorologica possono attraversare lo stesso canale; una frase vera e una falsa possono richiedere la stessa quantità di risorse.

Appena chiediamo se il destinatario abbia compreso, se l’affermazione corrisponda ai fatti, se la fonte sia affidabile o se il messaggio abbia valore, siamo entrati in problemi differenti da quello formalizzato da Shannon.

Il significato è quindi fuori dal modello per scelta metodologica, non per una tesi sulla sua irrilevanza nella comunicazione umana.

---

## 19. Shannon e Weaver: una distinzione necessaria

Nel 1949 l’articolo di Shannon viene ripubblicato in volume con un testo introduttivo di **Warren Weaver**. Il titolo passa da *A Mathematical Theory of Communication* a *The Mathematical Theory of Communication*: un volume composto da due testi distinti, che la ricezione successiva ha spesso fuso sotto l’etichetta “modello Shannon–Weaver”.

Weaver ha un ruolo decisivo nella diffusione interdisciplinare della teoria. Organizza il problema generale della comunicazione in tre livelli:

- problema **tecnico**: con quale accuratezza si trasmettono i simboli;
- problema **semantico**: con quale precisione i simboli trasmessi veicolano il significato desiderato;
- problema dell’**efficacia**: con quale successo il significato ricevuto produce l’effetto desiderato.

Questa tripartizione è di Weaver e non va attribuita indistintamente a Shannon.

Shannon è pienamente consapevole dell’esistenza del significato, ma costruisce la propria teoria sul problema tecnico. Weaver considera invece la possibilità che il quadro matematico abbia implicazioni più ampie e contribuisce a renderlo attraente per linguistica, psicologia e scienze sociali.

La fortuna interdisciplinare della teoria nasce anche da questa estensione. Distinguere i due autori permette di capire dove termina il formalismo shannoniano e dove comincia un programma più generale sulla comunicazione.

---

## 20. Shannon e Wiener: informazione non significa cibernetica

Nel 1948 escono quasi contemporaneamente *A Mathematical Theory of Communication* di Shannon e *Cybernetics* di Norbert Wiener.

La vicinanza storica ha favorito sovrapposizioni successive. I due campi condividono probabilità, statistica e problemi di comunicazione; Shannon riconosce l’importanza del lavoro di Wiener sul filtraggio e sulla previsione.

Gli oggetti centrali restano differenti. Shannon concentra la teoria su rappresentazione e trasmissione dell’informazione, limiti di sorgenti e canali, codifica e rumore. Wiener costruisce la cibernetica intorno a **comunicazione e controllo**, attribuendo al feedback un ruolo decisivo e allargando il quadro a macchine, organismi e sistemi.

La teoria dell’informazione diventa una risorsa per la cibernetica, senza coincidere con essa. “Informazione”, “feedback”, “controllo”, “decisione” e “apprendimento” appartengono a famiglie teoriche che si intersecano ma non sono sinonimi.

---

## 21. Shannon e Turing: due traiettorie che si incontrano

Nel 1943 Alan Turing trascorre un periodo negli Stati Uniti e frequenta i Bell Labs nel quadro delle attività belliche sulla crittografia e sulla comunicazione sicura. Qui incontra Shannon.

Entrambi lavorano su temi coperti da segreto, circostanza che limita ciò che possono condividere sui rispettivi progetti. Le testimonianze successive ricordano conversazioni su calcolatori, macchine e possibilità dell’intelligenza meccanica.

La convergenza è reale senza richiedere una leggenda fondativa. Turing formalizza la computazione e svilupperà lungo una traiettoria propria la questione delle macchine intelligenti; Shannon lavora su circuiti, comunicazione, informazione, crittografia, automi e problemi di ricerca.

Le loro strade mostrano due modi differenti di rendere trattabili problemi prima affidati all’intuizione: Turing attraverso la formalizzazione del calcolo, Shannon attraverso strutture logiche, probabilistiche e comunicative.

---

## 22. Crittografia e segretezza

La guerra porta Shannon dentro problemi di comunicazione sicura.

Nel 1949 pubblica *Communication Theory of Secrecy Systems*, basato su un rapporto confidenziale precedente. Il testo applica alla crittografia lo stesso tipo di astrazione probabilistica che caratterizza la teoria della comunicazione.

Un sistema di cifratura può essere studiato in termini di messaggi possibili, chiavi, crittogrammi e probabilità.

La nozione di **segretezza perfetta** stabilisce una condizione molto forte: osservare il testo cifrato non deve modificare le probabilità attribuite ai possibili messaggi originali.

Il one-time pad e il sistema di Vernam precedono Shannon come costruzioni crittografiche. Il contributo di Shannon consiste nel dare una formulazione teorica della segretezza perfetta. Nella costruzione standard del one-time pad la chiave deve essere davvero casuale, mantenuta segreta, usata una sola volta e almeno lunga quanto il messaggio; la teoria chiarisce perché la segretezza perfetta richieda un’incertezza della chiave adeguata a quella del messaggio.

La segretezza perfetta non risolve ogni problema della sicurezza. Autenticazione, integrità, gestione delle chiavi e sicurezza operativa richiedono proprietà ulteriori.

Anche qui la forza del metodo sta nel definire esattamente quale garanzia si vuole dimostrare.

---

## 23. Scacchi, automi e problemi trattabili

Nel 1950 Shannon pubblica *Programming a Computer for Playing Chess*.

Gli scacchi gli interessano perché rendono visibile un problema generale: lo spazio delle possibilità cresce troppo rapidamente perché una macchina possa esplorarlo integralmente con risorse finite. Bisogna selezionare, valutare posizioni, limitare la ricerca, costruire euristiche.

Nello stesso periodo costruisce **Theseus**, un topo elettromeccanico il cui apparato di controllo esplora un labirinto e conserva il percorso trovato. Nel linguaggio dell’epoca il dispositivo poteva essere presentato come una macchina capace di “imparare”; in termini più precisi, realizza memoria, ricerca e riutilizzo di una soluzione semplice.

Il rapporto di Shannon con l’intelligenza artificiale diventa più esplicito pochi anni dopo. Nel 1955 firma con John McCarthy, Marvin Minsky e Nathaniel Rochester la proposta del Dartmouth Summer Research Project on Artificial Intelligence; nel 1956 cura con McCarthy *Automata Studies*. Sono legami storici diretti con la formazione del campo.

Questo non rende la teoria dell’informazione una teoria dell’AI contemporanea. Mostra qualcosa di più preciso: Shannon partecipò all’ambiente in cui problemi di calcolo, memoria, automi, ricerca e comportamento delle macchine venivano organizzati come un nuovo territorio di ricerca.

Scacchi e labirinto rendono visibile la continuità fra teoria e costruzione: di fronte a un compito che sembra richiedere abilità intelligente, Shannon cerca la struttura che lo renda trattabile da una macchina.

---

## 24. La forma del pensiero di Shannon

Il metodo di Shannon emerge con maggiore chiarezza se lo si segue nei problemi concreti.

Davanti ai relè del Differential Analyzer cambia rappresentazione: una rete elettrica diventa una struttura logica che può essere manipolata algebricamente. Nella teoria dell’informazione compie un gesto affine su scala maggiore: separa trasmissione, significato e valore, descrive sorgenti e canali con strumenti probabilistici e stabilisce limiti prima di cercare una particolare macchina che li raggiunga.

La stessa postura riappare negli oggetti costruiti. Scacchi, labirinti e dispositivi meccanici servono a isolare memoria, ricerca, vincoli, regolarità temporali. L’astrazione non rimane sospesa sopra il mondo fisico: torna negli oggetti e ne verifica la tenuta.

Il dattiloscritto *Creative Thinking* rende esplicite alcune strategie che le opere già mostrano — semplificare, cambiare punto di vista, usare analogie, invertire il problema — ma non va trasformato in un manifesto sistematico. È una testimonianza sul modo di lavorare di uno scienziato che cercava la rappresentazione capace di rendere visibile la struttura essenziale del problema.

---

## 25. Idee chiave

### L’informazione può essere misurata senza misurare il significato

È il centro metodologico della teoria. La quantità d’informazione riguarda probabilità e possibilità, non il valore semantico.

### L’incertezza è parte della struttura dell’informazione

Una sorgente completamente prevedibile non produce nuova informazione statistica. La scelta acquista contenuto informativo perché esistono alternative.

### La comunicazione ha limiti fondamentali

Ogni canale possiede una capacità. Tecnologia e ingegneria possono avvicinarsi al limite; non possono abolirlo.

### Il rumore non rende impossibile l’affidabilità

Codici adeguati permettono, sotto la capacità e in senso asintotico, di rendere la probabilità d’errore arbitrariamente piccola.

### La ridondanza può avere funzioni opposte

La ridondanza della sorgente può essere sfruttata per comprimere; ridondanza aggiunta al codice può proteggere dagli errori.

### Un limite teorico non è una ricetta di progetto

I teoremi di Shannon dicono che cosa è possibile o impossibile nelle condizioni del modello. Costruire sistemi efficienti che si avvicinino a quei limiti resta un problema ingegneristico ulteriore.

---

## 26. Concetti chiave

### Informazione

Quantità legata alle probabilità delle possibili selezioni prodotte da una sorgente. Non coincide con significato, verità o conoscenza.

### Sorgente

Processo che produce simboli o messaggi secondo determinate regolarità statistiche.

### Messaggio

La sequenza o configurazione selezionata dalla sorgente e destinata alla trasmissione.

### Segnale

Forma fisica con cui il messaggio viene rappresentato per attraversare il canale.

### Bit

Unità d’informazione associata alla base logaritmica 2. Va distinta dalla semplice presenza di una cifra binaria: un simbolo 0/1 porta un bit soltanto nel caso equiprobabile.

### Entropia

Misura dell’incertezza media di una sorgente e della sua informazione media.

### Canale

Sistema fisico o astratto attraverso cui il segnale viene trasmesso.

### Rumore

Perturbazione che introduce incertezza fra ingresso e uscita del canale.

### Capacità del canale

Massimo tasso al quale l’informazione può essere trasmessa con affidabilità arbitrariamente elevata, date le caratteristiche del modello del canale.

### Codifica

Trasformazione del messaggio in una rappresentazione adatta a efficienza, trasmissione o protezione dagli errori.

### Distorsione

Misura della differenza ammessa fra sorgente e ricostruzione quando non è richiesta una copia esatta. Diventa centrale nei problemi di compressione con perdita e nei criteri di fedeltà.

### Ridondanza della sorgente

Prevedibilità statistica presente nei dati prodotti dalla sorgente e sfruttabile per una rappresentazione più efficiente.

### Ridondanza di codice

Struttura aggiunta intenzionalmente alla rappresentazione per rilevare o correggere errori durante trasmissione o memoria.

### Informazione mutua

Quantità che misura quanta incertezza su una variabile viene ridotta conoscendone un’altra; è centrale nella formulazione moderna della capacità di un canale discreto senza memoria.

### Segretezza perfetta

Condizione in cui l’osservazione del crittogramma non modifica l’informazione disponibile sul messaggio originale.

---

## 27. Costellazione

### Prima di Shannon — ciò che prepara il problema

**George Boole** fornisce l’algebra logica che Shannon collega ai circuiti di commutazione. La relazione è diretta sul piano formale, ma Boole non sta costruendo una teoria dei computer.

**Harry Nyquist** studia velocità di trasmissione, banda e segnali telegrafici. Prepara una parte essenziale dell’ingegneria matematica della comunicazione.

**Ralph Hartley** propone una misura logaritmica dell’informazione in relazione al numero delle possibili selezioni. Shannon estende questa linea introducendo probabilità, entropia, struttura statistica delle sorgenti e rumore.

**Vannevar Bush** offre a Shannon l’ambiente tecnico del Differential Analyzer e un modello di ricerca capace di attraversare matematica e ingegneria.

**Bell Laboratories** costituisce il laboratorio storico del problema: reti, voce, telegrafo, banda, rumore, costi e affidabilità.

### Contemporanei e interlocutori

**Warren Weaver** amplia la ricezione della teoria verso i problemi semantici e dell’efficacia. È un mediatore decisivo e va distinto da Shannon.

**Norbert Wiener** condivide il trattamento statistico della comunicazione e influenza Shannon, ma costruisce la cibernetica intorno a comunicazione, feedback e controllo.

**Alan Turing** lavora sulla computazione, la crittografia e le macchine. L’incontro del 1943 ai Bell Labs unisce due traiettorie senza fonderle.

**John von Neumann** appartiene allo stesso ambiente matematico e computazionale; la relazione storica è più ampia del celebre e incerto aneddoto sull’entropia.

**John Tukey** suggerisce il termine “bit”, che Shannon usa nel 1948.

**Richard Hamming** lavora negli stessi anni sul rilevamento e sulla correzione degli errori. I codici che portano il suo nome rendono concreta una delle grandi domande aperte dalla teoria: come costruire ridondanza utile contro gli errori.

**John McCarthy** incrocia Shannon sul terreno degli automi e della nascente intelligenza artificiale: insieme curano *Automata Studies*, e Shannon figura tra i promotori della proposta di Dartmouth.

### Dopo Shannon — ciò che cambia scala

**Teoria dei codici**: cerca codici implementabili che si avvicinino ai limiti dimostrati dalla teoria.

**Compressione dati**: utilizza la struttura statistica delle sorgenti per ridurre la rappresentazione necessaria, con o senza perdita secondo il problema.

**Telecomunicazioni digitali**: fanno della capacità, del rapporto segnale-rumore e della codifica problemi centrali di progetto.

**Archiviazione digitale**: tratta memoria e affidabilità come problemi di rappresentazione e correzione dell’errore.

**Crittografia moderna**: eredita da Shannon un modo informazionale di definire proprietà di sicurezza, pur sviluppandosi poi anche attraverso la complessità computazionale.

**Informazione algoritmica**: Kolmogorov, Solomonoff e Chaitin aprono una nozione differente, legata alla lunghezza delle descrizioni e alla complessità delle sequenze. Qui l’oggetto non è l’incertezza media di una sorgente probabilistica, ma la descrivibilità di singole sequenze o oggetti.

**Filosofia dell’informazione**: interroga statuto, significato e portata del concetto una volta uscito dal dominio originario.

### Fenomeni contemporanei leggibili attraverso Shannon

Streaming, reti mobili, comunicazioni satellitari, storage, compressione di immagini e audio, correzione degli errori, trasmissioni in fibra e sistemi wireless appartengono a una storia tecnica profondamente segnata dalla teoria dell’informazione.

Big data, piattaforme e intelligenza artificiale aprono invece un secondo livello di domanda: che cosa accade quando il termine “informazione” viene esteso fino a comprendere dati, linguaggio, conoscenza e decisione?

Shannon non fornisce una teoria già pronta del presente. Fornisce distinzioni che permettono di porre meglio il problema.

---

## 28. Eredità

L’eredità di Shannon attraversa più genealogie senza esaurirne nessuna.

La teoria dell’informazione stabilisce un linguaggio per misurare sorgenti, rappresentazioni, canali, rumore e limiti di trasmissione. Il lavoro sui circuiti collega algebra logica e reti di commutazione. La crittografia riceve una formulazione probabilistica della segretezza. La teoria dei codici trova un orizzonte di prestazioni entro cui cercare costruzioni concrete.

Compressione, telecomunicazioni digitali, storage affidabile e molte tecnologie di comunicazione ereditano direttamente questo quadro. Computer, Internet e intelligenza artificiale appartengono a storie più ampie, dentro le quali Shannon resta un nodo fondamentale.

La trasformazione decisiva può essere formulata con precisione: **l’informazione diventa una quantità ingegneristica**, dotata di unità, limiti e teoremi.

---

## 29. Lucrezio, McLuhan, Shannon

La triade **Lucrezio — McLuhan — Shannon** non racconta una genealogia della comunicazione. Costruisce tre domande autonome attorno a ciò che dal mondo raggiunge un soggetto, attraversa un mezzo e può essere trasmesso.

### Lucrezio

Nel *De rerum natura* il problema riguarda la materia, i corpi, il vuoto e le immagini sottili che si staccano dalle superfici e raggiungono i sensi. Il veicolo della percezione appartiene alla stessa ontologia materiale del mondo che descrive.

### McLuhan

Con McLuhan il centro si sposta verso i media come ambienti ed estensioni dei sensi. La forma del medium modifica scala, ritmo, percezione e relazioni; il mezzo non è un semplice condotto neutrale rispetto all’esperienza che rende possibile.

### Shannon

Shannon affronta un’altra domanda: quanta informazione può essere rappresentata e trasmessa attraverso un canale sottoposto a vincoli e rumore? Il canale viene caratterizzato attraverso proprietà tecniche — transizioni, banda, potenza, capacità — senza richiedere una teoria del significato o degli effetti culturali del medium.

Qui la distanza fra gli autori diventa produttiva.

**Il medium di McLuhan non è il channel di Shannon.**  
**Il message di McLuhan non coincide con l’information di Shannon.**  
**Il simulacrum di Lucrezio non è un segnale.**  
**L’atomo non conduce al bit.**

Il punto di maggiore tensione corre fra McLuhan e Shannon. McLuhan interroga la non-neutralità del mezzo rispetto all’ambiente umano; Shannon astrae dal significato e dagli effetti culturali del medium per misurare i vincoli della trasmissione. Le due prospettive non si confutano: selezionano proprietà differenti e rispondono a domande differenti.

Lucrezio mantiene aperto un piano ancora diverso: chiede che cosa siano i corpi e come il reale possa raggiungere i sensi.

**Materia, medium, informazione** non sono tre fasi della stessa storia. Sono tre livelli irriducibili che il presente tende facilmente a sovrapporre: costituzione del reale, ambiente della percezione, formalizzazione della trasmissione.

---

## 30. Ferita contemporanea: la trasmissione senza comprensione

Il mondo costruito dopo Shannon ha raggiunto un grado di affidabilità tecnica che per gran parte della storia sarebbe apparso quasi inconcepibile.

Testi, immagini, voce e video attraversano distanze immense in tempi minimi. Codici correggono errori; segnali deboli vengono ricostruiti; archivi vengono duplicati; reti trasportano quantità crescenti di dati.

Questa riuscita rende più visibile ciò che il problema tecnico non comprendeva.

**Una comunicazione può riuscire tecnicamente e fallire come comprensione.**

Un file può arrivare integro: questo dice che la trasmissione ha preservato i dati, non che conosciamo l’affidabilità della fonte. Una frase può essere riprodotta fedelmente e restare incompresa. Una proposizione può circolare senza essere vera. Una grande disponibilità di dati può non diventare conoscenza.

La ferita contemporanea non coincide con un generico “eccesso di informazione”. È un **errore di trasferimento**: **tendiamo a trasferire sul significato le prestazioni che abbiamo conquistato nella trasmissione**.

Velocità, disponibilità e accuratezza tecnica sono qualità reali, ma appartengono al livello per cui sono state misurate. Quando diventano, senza ulteriori prove, indizi di comprensione, verità o valore epistemico, il successo dell’infrastruttura viene scambiato per successo della conoscenza.

Weaver distingueva il problema tecnico da quello semantico e da quello dell’efficacia. La lettura contemporanea di Cerchi nasce nel divario fra questi piani: il primo può migliorare enormemente senza risolvere automaticamente gli altri.

Shannon non formulò una critica della società digitale. La sua teoria fornisce però il confine necessario per riconoscere l’errore: più informazione trasmissibile, da sola, non implica più conoscenza.

---

## 31. Limiti, tensioni e abusi

### Il limite semantico è intenzionale

La teoria di Shannon è costruita per il problema tecnico della comunicazione. Il significato resta fuori dal formalismo perché non è necessario a quel calcolo, non perché sia privo di importanza.

### Informazione e conoscenza appartengono a problemi diversi

Una quantità statistica non stabilisce che qualcuno abbia appreso qualcosa di vero, rilevante o utile.

### Entropia informativa e termodinamica richiedono distinzione

La parentela matematica e storica è reale; le grandezze appartengono però a quadri teorici differenti. Le metafore che le trasferiscono da un dominio all’altro devono esplicitare il passaggio.

### I teoremi di codifica non sono ricette di implementazione

Sapere che una prestazione è teoricamente possibile non equivale a possedere immediatamente un algoritmo o un codice pratico. Lunghezze finite, complessità, ritardi, energia e caratteristiche reali del canale restano problemi ingegneristici.

### Le estensioni interdisciplinari richiedono nuove prove

Nel 1956, in *The Bandwagon*, Shannon intervenne direttamente contro l’idea che il successo della teoria dell’informazione autorizzasse trasferimenti automatici verso psicologia, economia o altre scienze. Considerava possibili e promettenti alcune applicazioni, ma insisteva sul fatto che andassero fondate attraverso ipotesi e verifica empirica, non attraverso la sola trasposizione del vocabolario.

Questa cautela rafforza la lettura della “disciplina del confine”: la potenza di un concetto non elimina l’onere di ridefinirlo quando cambia dominio.

---

## 32. Curiosità che illuminano il metodo

### Theseus non è soltanto un giocattolo

Il topo elettromeccanico materializza un problema astratto: esplorare un labirinto, memorizzare una soluzione e riutilizzarla quando la configurazione viene riproposta.

### La giocoleria diventa un problema ingegneristico

Shannon studia e costruisce macchine capaci di eseguire movimenti di giocoleria. L’interesse non sta nella stranezza dell’hobby, ma nella possibilità di isolare regolarità temporali e meccaniche in un gesto apparentemente umano.

### Gli scacchi sono un laboratorio della complessità

Il problema consiste nel rendere trattabile uno spazio di possibilità troppo ampio per essere esplorato integralmente: selezionare, valutare e limitare la ricerca.

### La creatività può essere studiata come trasformazione del problema

Nel dattiloscritto del 1952 Shannon ritorna su semplificazione, analogia, inversione e cambiamento di rappresentazione. Le stesse strategie emergono, in forme diverse, nelle sue opere tecniche.

Le curiosità biografiche diventano così indizi di metodo: Shannon costruisce per capire e cambia rappresentazione per rendere il problema trattabile.

---

## 33. Errori comuni

### “Shannon ha inventato il bit”

La parola *bit* fu suggerita da John Tukey. Shannon la utilizzò nel 1948 e la rese centrale come unità della quantità d’informazione.

### “Un bit è semplicemente uno 0 o un 1”

Una cifra binaria è un simbolo di rappresentazione; il bit come unità misura una quantità d’informazione. Una sorgente binaria non equiprobabile produce in media meno di un bit per simbolo.

### “Shannon ha inventato il computer digitale”

Il suo lavoro sui circuiti a relè è fondamentale per la teoria dei circuiti logici, ma la nascita del computer ha una storia plurale.

### “Shannon ha inventato Internet”

La teoria dell’informazione fornisce principi fondamentali per le comunicazioni digitali. Internet nasce da architetture, protocolli, istituzioni e innovazioni successive.

### “Informazione significa conoscenza”

In Shannon è una quantità probabilistica. Una sequenza può essere altamente informativa senza essere vera o utile.

### “Un messaggio più sorprendente è più importante”

La sorpresa è statistica rispetto a una distribuzione di probabilità. Non è una misura del valore umano.

### “Entropia significa caos”

È una semplificazione inaffidabile. In Shannon misura l’incertezza media di una sorgente probabilistica.

### “Rumore significa disinformazione”

Il rumore shannoniano è una perturbazione del canale. La disinformazione coinvolge contenuto, intenzione, interpretazione e contesto sociale.

### “Ridondanza è sempre inefficienza”

La ridondanza della sorgente può essere sfruttata per comprimere; ridondanza aggiunta al codice può servire a rilevare e correggere errori.

### “Shannon spiega l’intelligenza artificiale”

Shannon partecipò realmente alla storia iniziale del campo — dagli scacchi e dagli automi alla proposta di Dartmouth e ad *Automata Studies*. La teoria dell’informazione, tuttavia, non coincide con una teoria generale dell’AI e non spiega da sola i sistemi contemporanei.

### “Un token di un modello linguistico è un bit”

Il token è un’unità di segmentazione di un sistema linguistico; il bit è un’unità di quantità d’informazione. In analisi probabilistiche si possono misurare grandezze come bit per token, ma token e bit restano oggetti differenti.

---

## 34. Glossario

**Algebra booleana** — sistema algebrico della logica basato su operazioni come AND, OR e NOT. Shannon ne mostra l’applicabilità sistematica ai circuiti di commutazione.

**Bit** — unità di quantità d’informazione quando si usa il logaritmo in base 2; non coincide automaticamente con una singola cifra binaria.

**Canale** — mezzo o sistema attraverso cui un segnale viene trasmesso.

**Capacità del canale** — massimo tasso d’informazione compatibile con trasmissione affidabile secondo il modello del canale.

**Codice** — regola che associa messaggi o simboli a rappresentazioni utilizzate per trasmissione o memoria.

**Codifica di canale** — aggiunta di struttura o ridondanza per rendere i dati resistenti agli errori.

**Codifica di sorgente** — rappresentazione efficiente della sorgente, tipicamente attraverso lo sfruttamento della sua prevedibilità statistica.

**Compressione lossless** — riduzione della rappresentazione necessaria mantenendo la possibilità di ricostruire esattamente i dati originali.

**Distorsione** — misura della differenza fra originale e ricostruzione accettata in un sistema che non richiede fedeltà perfetta.

**Entropia** — misura dell’incertezza media di una sorgente probabilistica.

**Errore** — differenza fra simbolo o messaggio trasmesso e ciò che viene ricostruito alla ricezione.

**Informazione** — nel senso shannoniano, quantità definita rispetto alle probabilità delle possibili selezioni.

**Informazione mutua** — misura della dipendenza informativa fra due variabili; indica quanto conoscere l’una riduca l’incertezza sull’altra.

**Messaggio** — elemento o sequenza selezionata dalla sorgente.

**Probabilità** — struttura matematica usata per descrivere l’incertezza delle selezioni.

**Ridondanza della sorgente** — prevedibilità statistica che può essere sfruttata per comprimere la rappresentazione.

**Ridondanza di codice** — struttura aggiunta intenzionalmente per rilevare o correggere errori.

**Rumore** — perturbazione del canale che altera la relazione fra segnale trasmesso e ricevuto.

**Segnale** — forma fisica o matematica usata per rappresentare il messaggio nel canale.

**Segretezza perfetta** — condizione in cui osservare il crittogramma non modifica le probabilità attribuite al messaggio originale.

**Sorgente** — processo che genera messaggi secondo certe probabilità.

**Trasmettitore** — componente che traduce il messaggio in un segnale adatto al canale.

---

## 35. Percorsi di lettura

### Percorso essenziale — capire Shannon senza matematica avanzata

1. Biografia essenziale
2. *A Mathematical Theory of Communication*
3. Informazione
4. Entropia
5. Canale, rumore e capacità
6. Il significato messo tra parentesi
7. Ferita contemporanea

Obiettivo: comprendere il gesto teorico prima delle formule.

### Percorso tecnico-concettuale — entrare nella teoria dell’informazione

1. Hartley e Nyquist
2. Entropia
3. Codifica della sorgente
4. Criterio di fedeltà e distorsione
5. Informazione mutua
6. Capacità del canale
7. Teorema di codifica per canali rumorosi
8. Compressione e correzione degli errori

Obiettivo: vedere come probabilità, rappresentazione e trasmissione diventano un unico campo.

### Percorso digitale — dalle commutazioni ai dati

1. Algebra booleana e relè
2. Bit
3. Codifica
4. Teoria dei codici
5. Compressione
6. Crittografia
7. Comunicazioni digitali

Obiettivo: comprendere perché Shannon è fondamentale per il digitale senza trasformarlo nel suo unico inventore.

### Percorso critico — informazione, significato, presente

1. Shannon e Weaver
2. Shannon e Wiener
3. Informazione versus conoscenza
4. Limiti della teoria
5. McLuhan e Shannon
6. Ferita contemporanea

Obiettivo: usare Shannon per distinguere ciò che i sistemi trasmettono da ciò che gli esseri umani comprendono.

---

## 36. Domande per orientarsi

1. Che cosa guadagna Shannon separando il problema tecnico dal significato?
2. Perché l’informazione viene collegata all’incertezza?
3. In che senso un evento improbabile può portare più informazione?
4. Perché un messaggio falso può essere informativo in senso shannoniano?
5. Che differenza c’è fra entropia e disordine?
6. Perché un canale possiede una capacità?
7. Come può una comunicazione essere affidabile nonostante il rumore?
8. Perché la ridondanza viene sia eliminata sia aggiunta?
9. Che cosa cambia quando accettiamo una certa distorsione nella ricostruzione?
10. Che cosa distingue Shannon da Weaver?
11. Perché la teoria dell’informazione non coincide con la cibernetica?
12. Che cosa distingue il *channel* di Shannon dal *medium* di McLuhan?
13. Che cosa rischiamo di perdere quando trasformiamo “informazione” in una metafora universale?

---

## 37. Nodi da ricordare

- Shannon rende l’informazione una quantità matematica legata a probabilità e scelta.
- La sua teoria riguarda anzitutto il problema tecnico della comunicazione.
- Il significato viene escluso metodologicamente, non negato.
- Il bit è un’unità di misura dell’informazione, non un atomo metafisico.
- L’entropia misura l’incertezza media di una sorgente.
- La capacità stabilisce un limite fondamentale del canale.
- Sotto la capacità, codici adeguati possono rendere l’errore arbitrariamente piccolo.
- La compressione senza perdita, la compressione con distorsione controllata e la protezione dagli errori rispondono a problemi differenti.
- La compressione tende a sfruttare e rimuovere ridondanza; la correzione degli errori può aggiungerne.
- Shannon e Weaver devono essere distinti.
- Shannon e Wiener condividono problemi, ma teoria dell’informazione e cibernetica non coincidono.
- Il contributo di Shannon al digitale è fondamentale senza equivalere all’invenzione di Internet, computer o AI.
- La sua lezione contemporanea più forte riguarda il confine fra informazione trasmissibile e comprensione.

---

## 38. FAQ

### Chi era Claude Shannon?

Claude Shannon è stato un matematico e ingegnere statunitense, nato nel 1916 e morto nel 2001. Ha fondato la teoria matematica dell’informazione e ha dato contributi fondamentali alla teoria dei circuiti logici, alla comunicazione digitale e alla crittografia.

### Che cos’è la teoria dell’informazione di Shannon?

È una teoria matematica che studia come quantificare, rappresentare e trasmettere informazione attraverso canali soggetti a vincoli e rumore. Introduce concetti come entropia, capacità del canale, codifica e ridondanza.

### Che cosa significa “informazione” per Shannon?

Indica una quantità legata alle probabilità delle possibili selezioni prodotte da una sorgente. Non coincide con il significato del messaggio, con la sua verità o con la conoscenza che può produrre.

### Shannon ha inventato il bit?

Shannon rese il bit centrale come unità della quantità d’informazione usando il logaritmo in base 2. Il termine *bit*, abbreviazione di *binary digit*, fu suggerito da John Tukey.

### Che cos’è l’entropia di Shannon?

È una misura dell’incertezza media di una sorgente probabilistica. È massima, a parità di alternative, quando gli esiti sono equiprobabili e diminuisce quando la sorgente diventa più prevedibile.

### L’entropia di Shannon è la stessa cosa dell’entropia termodinamica?

Le due formulazioni hanno una profonda parentela matematica e una storia concettuale intrecciata, ma appartengono a teorie differenti e non vanno identificate senza precisazioni.

### Che cos’è la capacità di un canale?

È il massimo tasso d’informazione al quale, secondo il modello del canale, è possibile trasmettere con probabilità d’errore arbitrariamente piccola usando codici appropriati.

### Perché Shannon esclude il significato?

Perché il suo obiettivo è formalizzare il problema tecnico della trasmissione. Il significato viene messo fuori dal modello perché non è necessario al calcolo di quantità come entropia, capacità ed errore; questo non equivale a negarne l’importanza nella comunicazione umana.

### Che differenza c’è tra Shannon e Weaver?

Shannon formula la teoria matematica del problema tecnico della comunicazione. Weaver, nell’introduzione al volume del 1949, distingue anche un livello semantico e uno dell’efficacia e contribuisce ad ampliare la ricezione interdisciplinare del lavoro. La comune etichetta “modello Shannon–Weaver” può quindi nascondere due contributi diversi.

### Un messaggio falso può avere molta informazione secondo Shannon?

Sì. La quantità d’informazione dipende dalla probabilità della selezione, non dalla verità semantica. Un messaggio falso e improbabile può quindi avere alta auto-informazione in senso tecnico.

### Che rapporto c’è tra Shannon e Internet?

La teoria dell’informazione fornisce principi fondamentali per comunicazioni, codifica, compressione e gestione del rumore, tutti decisivi per le reti digitali. Shannon non ha però inventato Internet e la sua teoria non descrive da sola la sua architettura.

### Che rapporto c’è tra Shannon e l’intelligenza artificiale?

Shannon lavorò su scacchi, automi e macchine e fu tra i firmatari della proposta di Dartmouth del 1955; nel 1956 curò con John McCarthy *Automata Studies*. Partecipò quindi alla formazione storica del campo, ma l’AI contemporanea deriva da sviluppi successivi e non può essere ridotta alla teoria dell’informazione.

### Claude AI prende il nome da Claude Shannon?

Secondo una ricostruzione del *New Yorker* del 2026 basata sulla cultura interna di Anthropic, il nome **Claude** è in parte un omaggio a Claude Shannon e in parte la scelta di un nome percepito come amichevole. Non risulta una dichiarazione istituzionale di Anthropic che presenti Shannon come unica origine del nome.

### Qual è la differenza tra Shannon e McLuhan?

Shannon studia le condizioni quantitative della trasmissione attraverso un canale. McLuhan studia come i media trasformano percezione, ambiente e relazioni. Il *channel* di Shannon e il *medium* di McLuhan appartengono a problemi differenti.

### Perché Shannon è ancora importante oggi?

Perché il mondo digitale continua a dipendere da codifica, capacità, compressione e correzione degli errori; e perché distinguere informazione, significato, conoscenza e verità è diventato ancora più urgente in una società satura di dati e messaggi.

---

## 39. Fonti e copyright

### Fonti primarie essenziali

- Claude E. Shannon, *A Symbolic Analysis of Relay and Switching Circuits*, *Transactions of the American Institute of Electrical Engineers*, vol. 57, n. 12, 1938, pp. 713–723.
- Claude E. Shannon, *A Mathematical Theory of Communication*, *Bell System Technical Journal*, vol. 27, 1948, pp. 379–423 e 623–656.
- Claude E. Shannon, *Communication in the Presence of Noise*, *Proceedings of the IRE*, vol. 37, n. 1, 1949, pp. 10–21.
- Claude E. Shannon, *Communication Theory of Secrecy Systems*, *Bell System Technical Journal*, vol. 28, 1949, pp. 656–715.
- Claude E. Shannon, *Programming a Computer for Playing Chess*, *Philosophical Magazine*, serie 7, vol. 41, n. 314, 1950, pp. 256–275.
- Claude E. Shannon, *Prediction and Entropy of Printed English*, *Bell System Technical Journal*, vol. 30, 1951, pp. 50–64.
- Claude E. Shannon, *Creative Thinking*, dattiloscritto Bell Laboratories, 20 marzo 1952, 10 pp.; registrato nella bibliografia dei *Collected Papers* come materiale non incluso nella raccolta.
- John McCarthy, Marvin L. Minsky, Nathaniel Rochester, Claude E. Shannon, *A Proposal for the Dartmouth Summer Research Project on Artificial Intelligence*, 31 agosto 1955.
- Claude E. Shannon, *The Bandwagon*, *IRE Transactions on Information Theory*, vol. IT-2, n. 1, 1956, p. 3.
- Claude E. Shannon, John McCarthy (a cura di), *Automata Studies*, Princeton University Press, 1956.
- Claude E. Shannon, *Coding Theorems for a Discrete Source with a Fidelity Criterion*, *IRE National Convention Record*, vol. 7, parte 4, 1959, pp. 142–163.
- Claude E. Shannon, Warren Weaver, *The Mathematical Theory of Communication*, University of Illinois Press, 1949. Le parti di Weaver e di Shannon vanno distinte.

### Precursori e contesto

- Harry Nyquist, *Certain Topics in Telegraph Transmission Theory*, *Transactions of the AIEE*, vol. 47, n. 2, 1928, pp. 617–644.
- Ralph V. L. Hartley, *Transmission of Information*, *Bell System Technical Journal*, vol. 7, n. 3, 1928, pp. 535–563.
- Norbert Wiener, *Cybernetics: Or Control and Communication in the Animal and the Machine*, 1948.
- Richard W. Hamming, *Error Detecting and Error Correcting Codes*, *Bell System Technical Journal*, 1950.

### Archivi e fonti istituzionali utili

- MIT Libraries e MIT News, materiali biografici, tesi e documenti su Shannon.
- Institute for Advanced Study, archivio dei membri.
- IEEE / Engineering and Technology History Wiki, storia della teoria dell’informazione e oral history.
- Computer History Museum, documenti sul computer chess e sulla storia del calcolo.
- Library of Congress, *Claude Elwood Shannon Papers*.

### Studi e raccolte

- N. J. A. Sloane, Aaron D. Wyner (a cura di), *Claude Elwood Shannon: Collected Papers*.
- Thomas M. Cover, Joy A. Thomas, *Elements of Information Theory*.
- Solomon W. Golomb, Elwyn R. Berlekamp, Thomas M. Cover, Robert G. Gallager, James L. Massey, Andrew J. Viterbi, *Claude Elwood Shannon (1916–2001)*, *Notices of the American Mathematical Society*, 2002.
- James Gleick, *The Information: A History, a Theory, a Flood*.
- Jimmy Soni, Rob Goodman, *A Mind at Play: How Claude Shannon Invented the Information Age*.
- Jon Gertner, *The Idea Factory: Bell Labs and the Great Age of American Innovation*.
- Gideon Lewis-Kraus, *What Is Claude? Anthropic Doesn’t Know, Either*, *The New Yorker*, 9 febbraio 2026, per la ricostruzione della *company lore* sull’origine del nome Claude.

### Cautela copyright

Le opere di Shannon e gran parte degli studi moderni non vanno trattati come testi liberamente riproducibili. Questa guida utilizza concetti, dati storici, formule standard e parafrasi originali. Le citazioni testuali, quando necessarie nella versione finale, dovranno restare brevi e puntualmente attribuite.

La presente guida è un contenuto originale di Alessandro Gentili per **Cerchi d’inchiostro**. La struttura, l’interpretazione, i testi, i percorsi di lettura e l’impianto editoriale sono protetti dal diritto d’autore. È possibile citare brevi passaggi o sintetizzare la guida per studio, critica, discussione e segnalazione, indicando autore, titolo del progetto e link alla pagina originale. La riproduzione integrale o sostanziale e il riuso commerciale, formativo, editoriale o in dataset richiedono autorizzazione scritta.

© Alessandro Gentili — Cerchi d’inchiostro. Tutti i diritti riservati.

---

## 40. Prosegui la lettura

### Tito Lucrezio Caro — Atomi, immagini e poesia della natura

Per tornare alla domanda più antica della triade: di che cosa è fatto il mondo, come i corpi raggiungono i sensi e perché comprendere la natura può liberarci dalla paura.

### Marshall McLuhan — Media, percezione e ambienti invisibili

Per passare dalla costituzione materiale del reale al problema dei media come ambienti che riorganizzano percezione, scala e relazioni.

Le due guide aprono i poli con cui Shannon entra in tensione. La sua domanda resta autonoma: che cosa può essere formalizzato, codificato e trasmesso entro i vincoli di un canale?

---

## 41. Chiusura

Claude Shannon ha dato alla parola “informazione” una precisione che la fortuna stessa del termine rischia continuamente di allargare.

La sua teoria mostra che una formalizzazione può essere straordinariamente generale senza pretendere di esaurire il fenomeno. Nel 1956 Shannon arrivò a mettere in guardia il proprio campo dall’idea che il vocabolario dell’informazione potesse essere trasferito altrove senza nuove ipotesi e nuove prove.

Oggi disponiamo di canali più capienti, archivi più vasti e macchine capaci di produrre e trasformare linguaggio su una scala che Shannon non conobbe. La distinzione fra ciò che un sistema può trasmettere e ciò che una persona può comprendere è diventata, se possibile, ancora più visibile.

Resta allora una domanda che appartiene a noi, non alla teoria del 1948:

**quando tutto può essere trasmesso, che cosa ci permette ancora di distinguere ciò che è arrivato da ciò che abbiamo davvero compreso?**
