"""Exact editorial revisions approved in CERCHI_EI07_CANDIDATO_EDITORIALE_v2.md."""
from hashlib import sha256
import re
import subprocess


BASELINE = '28de776022cd8f99e52f79699cde3e4d9f7fdf51'
CANDIDATE_SHA256 = '020187e1d1379b88c58a9a659f67454f638c8d565a2c4f20dff1de2186e0d04d'

PINS = {
    'cerchi/guide/aristide-merloni-impresa-lavoro-destino-luoghi/index.html': (
        '00d64933a2b934e3708b2216922db2db4bbf50d0ec2baaca32fef307ddfe6b2c',
        'ae9f6bd94ac8b072d4df7dc2c4d41161bbb3d140a9a252e4edff0c0a451c4d0c',
    ),
    'cerchi/guide/carl-schmitt-decisione-eccezione-ordine-politico/index.html': (
        'a9cc117cf665071978fd8e33f294c4aefac515eecca9b984436ee68f03fd1f86',
        '47e5dbbbce3f1e99cb989316d7e67a62a61e0a1de476591b618211d4f32717c1',
    ),
    'cerchi/guide/cesare-beccaria-limite-diritto-punire/index.html': (
        'c9a38a0f2d0b3de927652727c0e582cf13019feaa1f859975598b431191aeb56',
        '412d02860fa4da4dc94313d9f68c5dcfd6695fa9178c6e64d75de7d3b12f3313',
    ),
    'cerchi/guide/edgar-morin-la-conoscenza-e-i-suoi-punti-ciechi/index.html': (
        '95585ed7d977430901f241b3128e4af8d537e5abbca05f157168fcdeca74bc8e',
        'a0a3a312bb69c39668ebb7f114f8ce9de5a76fff6c5c4ddd50206a3323e75e57',
    ),
    'cerchi/guide/enrico-mattei-energia-impresa-pubblica-autonomia/index.html': (
        '747b8eba46dec5b375dcaa304f674e3c6a1e5333af28e258c361a4f420381716',
        'f22b9f1fd2770df988f5a87a81e3ffbf6428f329d52b9eed9ba07e2cd16bb4c4',
    ),
    'cerchi/guide/michel-foucault-la-vita-sotto-esame/index.html': (
        '88c4059967a3b0adfd70d09d3d480986a1dcef1d2af1bb3ad92333fddced7c63',
        '8ba2835df01ad1e5169e5dde773976ab429faae889d52302f8c6e83e4f16cd43',
    ),
    'cerchi/guide/polibio-costituzione-potenza-decadenza/index.html': (
        '199db91e95e30444781cae53cb9028d808c206f5f299fa1518e1c5dda1ca453b',
        '782bf22f344feb73a782707e7c384de7ec59ffa6dfa8d2b3867b036a53fde866',
    ),
    'cerchi/guide/sofocle-legge-colpa-limite-citta/index.html': (
        'b640730c713e71e693c187f8184387e3e6fdc3c255bd8f1f5dd0d9ff9ee28479',
        'ea8c1144a916b44ca66c8bd1c964bcb2cd9986a80456116de79a9a9326419991',
    ),
    'en/cerchi/guides/adriano-olivetti-community-power/index.html': (
        '46df2f82e11301a2966c0bf16f7fa3375d1ef5c552fac10b48a1e75b7fb49072',
        'ce0ad0dddad328223f7b1550d12a0e86bc1756b5021137ad8edd70f2083eab3a',
    ),
    'en/cerchi/guides/aristide-merloni-enterprise-fate-of-places/index.html': (
        '94bdf956e2cd0d28c19f764655dc892eef4f4adc1e66f63c639528c9a8ad59f0',
        '4f4a469432bb239b389ee96adb3cee8e43fcb4836156f20257b08e7715b0b8ea',
    ),
    'en/cerchi/guides/edgar-morin-knowledge-and-its-blind-spots/index.html': (
        'b8cced9f25370ebd3911c5ab6a61581b1261f0aa905172fb9ef33ff3779b04ce',
        '324f14f75407540129e2c90c3564a41d30732d1c1fa62f93f34f985365e3f817',
    ),
    'en/cerchi/guides/enrico-mattei-energy-public-enterprise-autonomy/index.html': (
        'f8268380837ed45c071873085b9268bc8b864f0882877cbb8d5240f538670689',
        '90c853ea3b7d974b7fb46cd3e31772d00a88bffd4010231936611972868c3171',
    ),
    'en/cerchi/guides/sophocles-law-guilt-limits-city/index.html': (
        '2840adf4939f0758df1222bb87567a4029f31c838cb7d1c2f7a138487463b745',
        '5f6b565475546e0d363aae61ea42d3277cc78a899a074dee95783af61fdbe7d7',
    ),
}

# Every replacement is bound to its original article.
FRAGMENTS = {
    'cerchi/guide/aristide-merloni-impresa-lavoro-destino-luoghi/index.html': (
        (
            'prosegui-la-lettura',
            '<p><strong>Adriano Olivetti — Impresa, comunità e progetto politico.</strong> Il nodo successivo della dodicesima triade, da sviluppare e collegare dopo la pubblicazione.</p>',
            '<p><strong><a href="https://alessandro-gentili.it/cerchi/guide/adriano-olivetti-la-comunita-e-il-potere/">Adriano Olivetti</a> — Impresa, comunità e progetto politico.</strong> È il nodo successivo della dodicesima triade.</p>',
        ),
    ),
    'cerchi/guide/carl-schmitt-decisione-eccezione-ordine-politico/index.html': (
        (
            'percorsi-di-lettura',
            "<p><strong>Verso Clausewitz.</strong> <em>Il concetto del politico</em> e <em>Teoria del partigiano</em> preparano il problema dell'inimicizia, lasciando alla futura guida militare il compito di spiegare la condotta della guerra.</p>",
            '<p><strong>Verso Clausewitz.</strong> <em>Il concetto del politico</em> e <em>Teoria del partigiano</em> preparano il problema dell\'inimicizia, mentre la guida a <a href="https://alessandro-gentili.it/cerchi/guide/carl-von-clausewitz-guerra-politica-limiti-della-forza/">Carl von Clausewitz</a> affronta la condotta della guerra nel suo rapporto con la politica.</p>',
        ),
    ),
    'cerchi/guide/cesare-beccaria-limite-diritto-punire/index.html': (
        (
            'percorsi-di-lettura',
            '<p>Metti Beccaria accanto a <strong>Hobbes</strong> per il problema della sicurezza e dell&#x27;autorità; a <strong>Manzoni</strong> per la prova, l&#x27;errore e la responsabilità dei giudici. <strong>Sofocle</strong> e <strong>Foucault</strong> appartengono alla Triade 14 in preparazione: i confronti qui proposti non rinviano a pagine già pubblicate.</p>',
            '<p>Metti Beccaria accanto a <strong>Hobbes</strong> per il problema della sicurezza e dell&#x27;autorità; a <strong>Manzoni</strong> per la prova, l&#x27;errore e la responsabilità dei giudici. <strong>Sofocle</strong> e <strong>Foucault</strong> appartengono alla Triade 14 — Legge, colpa, punizione.</p>',
        ),
        (
            'prosegui-la-lettura',
            '<p><strong>Triade 14 — Sofocle, Michel Foucault, Cesare Beccaria.</strong> Questo è un percorso editoriale in preparazione. I testi delle guide 40 e 41 non vengono presentati come pagine pubblicate, né si creano collegamenti a URL ipotetiche.</p>',
            '<p>La <strong>Triade 14 — Legge, colpa, punizione</strong> accosta il giudizio tragico di <a href="https://alessandro-gentili.it/cerchi/guide/sofocle-legge-colpa-limite-citta/">Sofocle</a>, le pratiche disciplinari studiate da <a href="https://alessandro-gentili.it/cerchi/guide/michel-foucault-la-vita-sotto-esame/">Michel Foucault</a> e la riflessione di Beccaria sui limiti del diritto di punire.</p>',
        ),
        (
            'prosegui-la-lettura',
            '<p><strong>Alessandro Manzoni — Lingua, storia e responsabilità.</strong> La guida pubblicata a Manzoni affronta anche <em>Storia della colonna infame</em>. Il confronto conduce dal problema delle prove e della tortura alla responsabilità di chi decide quando una città è dominata dalla paura. Pagina attualmente pubblica: <code>/cerchi/guide/alessandro-manzoni-lingua-storia-responsabilita/</code>.</p>',
            '<p><strong><a href="https://alessandro-gentili.it/cerchi/guide/alessandro-manzoni-lingua-storia-responsabilita/">Alessandro Manzoni</a> — Lingua, storia e responsabilità.</strong> La guida a Manzoni affronta anche <em>Storia della colonna infame</em>. Il confronto conduce dal problema delle prove e della tortura alla responsabilità di chi decide quando una città è dominata dalla paura.</p>',
        ),
        (
            'prosegui-la-lettura',
            '<p><strong>Thomas Hobbes — Paura, sovranità e ordine politico.</strong> La guida già presente nel corpus permette di tornare alla ragione per cui gli uomini affidano potere a una sovranità, e a quanto spazio rimanga per i limiti della coercizione.</p>',
            '<p><strong><a href="https://alessandro-gentili.it/cerchi/guide/hobbes-paura-sovranita-ordine-politico/">Thomas Hobbes</a> — Paura, sovranità e ordine politico.</strong> La guida permette di tornare alla ragione per cui gli uomini affidano potere a una sovranità, e a quanto spazio rimanga per i limiti della coercizione.</p>',
        ),
    ),
    'cerchi/guide/edgar-morin-la-conoscenza-e-i-suoi-punti-ciechi/index.html': (
        (
            'prosegui-la-lettura',
            '<p>La tredicesima triade proseguirà, quando le rispettive guide saranno pubblicate, con Rachel Carson e John Maynard Keynes. Qui i loro nomi indicano un percorso editoriale in costruzione, non collegamenti a pagine già disponibili.</p>',
            '<p>La tredicesima triade prosegue con <a href="https://alessandro-gentili.it/cerchi/guide/rachel-carson-la-vita-dopo-l-intervento/">Rachel Carson</a> e <a href="https://alessandro-gentili.it/cerchi/guide/john-maynard-keynes-economia-futuro-incerto/">John Maynard Keynes</a>.</p>',
        ),
    ),
    'cerchi/guide/enrico-mattei-energia-impresa-pubblica-autonomia/index.html': (
        (
            'prosegui-la-lettura',
            '<p>Le future guide ad Aristide Merloni e Adriano Olivetti, quando saranno pubblicate, permetteranno di completare il percorso della dodicesima triade <em>Stato, impresa e comunità</em>.</p>',
            '<p>Le guide ad <a href="https://alessandro-gentili.it/cerchi/guide/aristide-merloni-impresa-lavoro-destino-luoghi/">Aristide Merloni</a> e <a href="https://alessandro-gentili.it/cerchi/guide/adriano-olivetti-la-comunita-e-il-potere/">Adriano Olivetti</a> completano il percorso della dodicesima triade <em>Stato, impresa e comunità</em>.</p>',
        ),
    ),
    'cerchi/guide/michel-foucault-la-vita-sotto-esame/index.html': (
        (
            'prosegui-la-lettura',
            '<p>Nella <strong>Triade 14 — Legge, colpa, punizione</strong>, Sofocle apre la questione del giudizio tragico; Foucault indaga i modi in cui le istituzioni rendono conoscibili e governabili gli individui; Beccaria interroga le ragioni e i limiti della punizione. I collegamenti alle Guide 40 e 42 saranno introdotti solo quando le relative pagine saranno effettivamente pubblicate.</p>',
            '<p>Nella <strong>Triade 14 — Legge, colpa, punizione</strong>, <a href="https://alessandro-gentili.it/cerchi/guide/sofocle-legge-colpa-limite-citta/">Sofocle</a> apre la questione del giudizio tragico; Foucault indaga i modi in cui le istituzioni rendono conoscibili e governabili gli individui; <a href="https://alessandro-gentili.it/cerchi/guide/cesare-beccaria-limite-diritto-punire/">Beccaria</a> interroga le ragioni e i limiti della punizione.</p>',
        ),
        (
            'fonti-edizioni-e-copyright',
            '<p>La presente guida è un contenuto originale di Alessandro Gentili per Cerchi d&#x27;inchiostro. La struttura, l&#x27;interpretazione, i testi, i percorsi di lettura e l&#x27;impianto editoriale sono protetti dal diritto d&#x27;autore. È possibile citare brevi passaggi o sintetizzare la guida per studio, critica, discussione e segnalazione, indicando autore, titolo del progetto e link alla pagina originale, quando pubblicata. La riproduzione integrale o sostanziale e il riuso commerciale, formativo, editoriale o in dataset richiedono autorizzazione scritta.</p>',
            '<p>La presente guida è un contenuto originale di Alessandro Gentili per Cerchi d&#x27;inchiostro. La struttura, l&#x27;interpretazione, i testi, i percorsi di lettura e l&#x27;impianto editoriale sono protetti dal diritto d&#x27;autore. È possibile citare brevi passaggi o sintetizzare la guida per studio, critica, discussione e segnalazione, indicando autore, titolo del progetto e link alla pagina originale. La riproduzione integrale o sostanziale e il riuso commerciale, formativo, editoriale o in dataset richiedono autorizzazione scritta.</p>',
        ),
    ),
    'cerchi/guide/polibio-costituzione-potenza-decadenza/index.html': (
        (
            'prosegui-la-lettura',
            '<p><strong>Prossima guida: Gaetano Mosca — classe politica, organizzazione e governo reale.</strong></p>',
            '<p><strong>Prossima guida: <a href="https://alessandro-gentili.it/cerchi/guide/gaetano-mosca-classe-politica-organizzazione-governo-reale/">Gaetano Mosca</a> — classe politica, organizzazione e governo reale.</strong></p>',
        ),
    ),
    'cerchi/guide/sofocle-legge-colpa-limite-citta/index.html': (
        (
            'prosegui-la-lettura',
            '<p>Michel Foucault consentirà di interrogare le pratiche istituzionali attraverso cui la modernità osserva, classifica e corregge.</p>',
            '<p><a href="https://alessandro-gentili.it/cerchi/guide/michel-foucault-la-vita-sotto-esame/">Michel Foucault</a> consentirà di interrogare le pratiche istituzionali attraverso cui la modernità osserva, classifica e corregge.</p>',
        ),
        (
            'prosegui-la-lettura',
            '<p>Cesare Beccaria porterà il confronto verso la giustificazione e i limiti del diritto di punire.</p>',
            '<p><a href="https://alessandro-gentili.it/cerchi/guide/cesare-beccaria-limite-diritto-punire/">Cesare Beccaria</a> porterà il confronto verso la giustificazione e i limiti del diritto di punire.</p>',
        ),
        (
            'costellazione',
            '<p><strong>Michel Foucault — La verità distribuita fra le testimonianze.</strong> In <em>La verità e le forme giuridiche</em> Foucault interpreta l&#x27;inchiesta di <em>Edipo re</em> come composizione progressiva di frammenti di verità: l&#x27;oracolo, il sovrano, il messaggero, il pastore. Il testimone di condizione inferiore può portare una parola capace di rovesciare la sicurezza del re. Questo è un rapporto testuale reale con la futura Guida 41; l&#x27;indagine storica sulle pratiche giuridiche di Foucault rimane distinta dalla struttura religiosa della tragedia.</p>',
            '<p><strong>Michel Foucault — La verità distribuita fra le testimonianze.</strong> In <em>La verità e le forme giuridiche</em> Foucault interpreta l&#x27;inchiesta di <em>Edipo re</em> come composizione progressiva di frammenti di verità: l&#x27;oracolo, il sovrano, il messaggero, il pastore. Il testimone di condizione inferiore può portare una parola capace di rovesciare la sicurezza del re. La <a href="https://alessandro-gentili.it/cerchi/guide/michel-foucault-la-vita-sotto-esame/">guida a Michel Foucault</a> riprende questa lettura. L&#x27;indagine storica sulle pratiche giuridiche di Foucault rimane distinta dalla struttura religiosa della tragedia.</p>',
        ),
        (
            'costellazione',
            '<p><strong>Manzoni — Quando l&#x27;accusa diventa procedura.</strong> La <em>Storia della colonna infame</em> permette un raccordo più specifico delle generiche affinità fra potere e sofferenza: il processo, il sospetto e l&#x27;errore del giudizio diventano storia documentata. Il contesto è quello delle istituzioni moderne; il ponte verso Beccaria appartiene alla storia familiare e intellettuale di Manzoni, nipote di Beccaria, e dovrà essere sviluppato nella terza guida della triade.</p>',
            '<p><strong>Manzoni — Quando l&#x27;accusa diventa procedura.</strong> La <em>Storia della colonna infame</em> permette un raccordo più specifico delle generiche affinità fra potere e sofferenza: il processo, il sospetto e l&#x27;errore del giudizio diventano storia documentata. Il contesto è quello delle istituzioni moderne; il ponte verso Beccaria appartiene alla storia familiare e intellettuale di Manzoni, nipote di Beccaria. La <a href="https://alessandro-gentili.it/cerchi/guide/cesare-beccaria-limite-diritto-punire/">terza guida della triade, dedicata a Cesare Beccaria</a>, riprende questo nesso.</p>',
        ),
    ),
    'en/cerchi/guides/adriano-olivetti-community-power/index.html': (
        (
            'continue-reading',
            '<p><strong><a href="/cerchi/guide/enrico-mattei-energia-impresa-pubblica-autonomia/">Enrico Mattei — Energy, Public Enterprise and Autonomy</a> (Italian edition).</strong> The history of ENI introduces the question of the State’s industrial capacity and its responsibility for the use of strategic resources. Infrastructure and international negotiations show how development depends on material means and powers that can actually be exercised.</p>',
            '<p><strong><a href="https://alessandro-gentili.it/en/cerchi/guides/enrico-mattei-energy-public-enterprise-autonomy/">Enrico Mattei — Energy, Public Enterprise and Autonomy</a>.</strong> The history of ENI introduces the question of the State’s industrial capacity and its responsibility for the use of strategic resources. Infrastructure and international negotiations show how development depends on material means and powers that can actually be exercised.</p>',
        ),
        (
            'continue-reading',
            '<p><strong><a href="/cerchi/guide/aristide-merloni-impresa-lavoro-destino-luoghi/">Aristide Merloni — Enterprise and the Fate of Places</a> (Italian edition).</strong> Manufacturing in inland Marche illuminates the meeting of skill, work and territory. The distribution of factories and the way the business was organised raise the question of how long local economic capabilities can endure.</p>',
            '<p><strong><a href="https://alessandro-gentili.it/en/cerchi/guides/aristide-merloni-enterprise-fate-of-places/">Aristide Merloni — Enterprise and the Fate of Places</a>.</strong> Manufacturing in inland Marche illuminates the meeting of skill, work and territory. The distribution of factories and the way the business was organised raise the question of how long local economic capabilities can endure.</p>',
        ),
    ),
    'en/cerchi/guides/aristide-merloni-enterprise-fate-of-places/index.html': (
        (
            'continue-reading',
            '<p><strong><a href="/cerchi/guide/enrico-mattei-energia-impresa-pubblica-autonomia/">Enrico Mattei</a> — The state, energy and national autonomy.</strong> The preceding guide in the twelfth triad, available in Italian on the author&#x27;s website.</p>',
            '<p><strong><a href="https://alessandro-gentili.it/en/cerchi/guides/enrico-mattei-energy-public-enterprise-autonomy/">Enrico Mattei</a> — The state, energy and national autonomy.</strong> The preceding guide in the twelfth triad.</p>',
        ),
        (
            'continue-reading',
            '<p><strong><a href="/cerchi/guide/adriano-olivetti-la-comunita-e-il-potere/">Adriano Olivetti</a> — Enterprise, community and political thought.</strong> The following guide in the twelfth triad, also available in Italian. No English edition is implied to be live.</p>',
            '<p><strong><a href="https://alessandro-gentili.it/en/cerchi/guides/adriano-olivetti-community-power/">Adriano Olivetti</a> — Enterprise, community and political thought.</strong> The following guide in the twelfth triad.</p>',
        ),
    ),
    'en/cerchi/guides/edgar-morin-knowledge-and-its-blind-spots/index.html': (
        (
            'continue-reading',
            '<p>Triad 13 will continue, when the relevant guides have been published, with Rachel Carson and John Maynard Keynes. For now, their names indicate an editorial path under construction, not links to pages already available.</p>',
            '<p>Triad 13 continues with <a href="https://alessandro-gentili.it/en/cerchi/guides/rachel-carson-life-after-the-intervention/">Rachel Carson</a> and <a href="https://alessandro-gentili.it/en/cerchi/guides/john-maynard-keynes-economy-of-an-uncertain-future/">John Maynard Keynes</a>.</p>',
        ),
    ),
    'en/cerchi/guides/enrico-mattei-energy-public-enterprise-autonomy/index.html': (
        (
            'continue-reading',
            '<p>For the companion perspectives, see the published Italian guides to <a href="https://alessandro-gentili.it/cerchi/guide/aristide-merloni-impresa-lavoro-destino-luoghi/">Aristide Merloni</a> and <a href="https://alessandro-gentili.it/cerchi/guide/adriano-olivetti-la-comunita-e-il-potere/">Adriano Olivetti</a>, which complete the twelfth triad, <em>State · Enterprise · Community</em>.</p>',
            '<p>For the companion perspectives, see the published guides to <a href="https://alessandro-gentili.it/en/cerchi/guides/aristide-merloni-enterprise-fate-of-places/">Aristide Merloni</a> and <a href="https://alessandro-gentili.it/en/cerchi/guides/adriano-olivetti-community-power/">Adriano Olivetti</a>, which complete the twelfth triad, <em>State · Enterprise · Community</em>.</p>',
        ),
    ),
    'en/cerchi/guides/sophocles-law-guilt-limits-city/index.html': (
        (
            'constellation',
            '<p><strong>Michel Foucault — Truth distributed among witnesses.</strong> In <em>Truth and Juridical Forms</em>, Foucault reads the inquiry in <em>Oedipus the King</em> as the progressive assembly of fragments of truth: oracle, ruler, messenger, and shepherd. A low-status witness can speak a truth that overturns a king&#x27;s confidence. This is a genuine textual link to the forthcoming Guide 41; Foucault&#x27;s historical inquiry into legal practices remains distinct from the play&#x27;s religious order.</p>',
            '<p><strong>Michel Foucault — Truth distributed among witnesses.</strong> In <em>Truth and Juridical Forms</em>, Foucault reads the inquiry in <em>Oedipus the King</em> as the progressive assembly of fragments of truth: oracle, ruler, messenger, and shepherd. A low-status witness can speak a truth that overturns a king&#x27;s confidence. The <a href="https://alessandro-gentili.it/en/cerchi/guides/michel-foucault-life-under-examination/">guide to Michel Foucault</a> takes up this reading. Foucault&#x27;s historical inquiry into legal practices remains distinct from the play&#x27;s religious order.</p>',
        ),
        (
            'constellation',
            '<p><strong>Manzoni — When accusation becomes procedure.</strong> <em>The History of the Infamous Column</em> (<em>Storia della colonna infame</em>) offers a more precise connection than a general affinity between power and suffering: trial, suspicion, and failures of judgement become documented history. The setting is that of early modern institutions. The connection with Beccaria belongs to Manzoni&#x27;s familial and intellectual history—he was Beccaria&#x27;s grandson—and will be developed in the third guide of the triad.</p>',
            '<p><strong>Manzoni — When accusation becomes procedure.</strong> <em>The History of the Infamous Column</em> (<em>Storia della colonna infame</em>) offers a more precise connection than a general affinity between power and suffering: trial, suspicion, and failures of judgement become documented history. The setting is that of early modern institutions. The connection with Beccaria belongs to Manzoni&#x27;s familial and intellectual history—he was Beccaria&#x27;s grandson. The <a href="https://alessandro-gentili.it/en/cerchi/guides/cesare-beccaria-limits-right-to-punish/">third guide of the triad, on Cesare Beccaria</a>, takes up that connection.</p>',
        ),
    ),
}

def require(condition, message):
    if not condition:
        raise AssertionError(f'EI07: {message}')


def replace_paragraphs(path, document, reverse=False):
    fragments = reversed(FRAGMENTS[path]) if reverse else FRAGMENTS[path]
    for section, before, after in fragments:
        old, new = (after.encode(), before.encode()) if reverse else (before.encode(), after.encode())
        articles = re.findall(
            rb'<article\b[^>]*\bid="' + re.escape(section.encode()) + rb'"[^>]*>.*?</article>',
            document, re.S,
        )
        require(len(articles) == 1 and articles[0].count(old) == 1,
                f'paragraph missing or repeated in {path}#{section}')
        require(document.count(old) == 1 and document.count(new) == 0,
                f'paragraph substitution is not unique in {path}#{section}')
        document = document.replace(old, new, 1)
    return document


def restore(path, revised):
    before_pin, after_pin = PINS[path]
    require(sha256(revised).hexdigest() == after_pin, f'wrong result SHA-256: {path}')
    before = replace_paragraphs(path, revised, reverse=True)
    require(sha256(before).hexdigest() == before_pin, f'wrong preimage SHA-256: {path}')
    require(replace_paragraphs(path, before) == revised, f'integral reconstruction failed: {path}')
    return before


def historical_bytes(root, path):
    """Give a historical gate the original bytes after proving the exact revision."""
    document = (root / path).read_bytes()
    pins = PINS.get(path)
    if pins is None or sha256(document).hexdigest() == pins[0]:
        return document
    return restore(path, document)


def test_revision(path, before, revised):
    _, original, approved = FRAGMENTS[path][0]
    original, approved = original.encode(), approved.encode()
    candidates = {
        'rollback': before,
        'partial rollback': revised.replace(approved, original, 1),
        'duplicate paragraph': revised.replace(approved, approved * 2, 1),
        'deleted paragraph': revised.replace(approved, b'', 1),
        'edited paragraph': revised.replace(approved, approved.replace(b'<p>', b'<p>Altered ', 1), 1),
        'trailing change': revised + b'\n',
        'changed metadata': revised.replace(b'<title>', b'<title>Altered ', 1),
        'stripped json-ld type': revised.replace(b'application/ld+json', b'application/json', 1),
    }
    if match := re.search(rb'href="https://alessandro-gentili\.it/(en/)?cerchi/(?:guide|guides)/', approved):
        wrong = (b'href="https://alessandro-gentili.it/cerchi/guide/' if match[1]
                 else b'href="https://alessandro-gentili.it/en/cerchi/guides/')
        candidates['wrong language link'] = revised.replace(approved, approved.replace(match[0], wrong, 1), 1)
    for label, candidate in candidates.items():
        require(candidate != revised, f'inactive negative fixture {label}: {path}')
        try:
            restore(path, candidate)
        except AssertionError:
            continue
        raise AssertionError(f'EI07: accepted {label}: {path}')
    return len(candidates)


def verify_release(root, self_test=False):
    require(PINS.keys() == FRAGMENTS.keys() and len(PINS) == 13
            and sum(map(len, FRAGMENTS.values())) == 23, 'unexpected scope')
    tests = 0
    for path in PINS:
        approved = (root / path).read_bytes()
        historical = subprocess.check_output(['git', 'show', f'{BASELINE}:{path}'], cwd=root)
        require(restore(path, approved) == historical, f'reconstruction differs from frozen main: {path}')
        if self_test:
            tests += test_revision(path, historical, approved)
    print(f'PASS EI07: 23 paragraphs in 13 guides, full reconstruction; {tests} negative regressions')
