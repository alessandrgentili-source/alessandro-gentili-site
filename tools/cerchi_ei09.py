"""Exact transformations approved in CERCHI_EI09_CANDIDATO_EDITORIALE_v2_APPROVATO.md."""
from hashlib import sha256
import subprocess


BASELINE = 'fccf27b5cd6d220e8550133b967cb636af644372'
CANDIDATE_SHA256 = 'd665c599dc55566cd52e87ce940ef1200cb197d7af8f9a66b0a8a8c9896117ce'

PINS = {
    'cerchi/guide/adam-smith-scambio-simpatia-ricchezza/index.html': (
        'b72afdf4e2a0dabd7f385507a327462cd097625bf1bbcd70ed2aef4d709f1f08',
        'dacb440a8074fa6e5923641b8a686c186db6a39461d13d50f7ca6e41f5e7ebfa',
    ),
    'cerchi/guide/adriano-olivetti-la-comunita-e-il-potere/index.html': (
        '193a1febd02c578872df42ae442167f6cfa73821c8c203c0b1bfc1dcd0cd27c7',
        '84e987a874169f9507ff00320756000b609bafa08d177d50cd6d5b013863b30d',
    ),
    'cerchi/guide/alexis-de-tocqueville-democrazia-opinione-liberta/index.html': (
        '971b6cc85ffb5033945fea35e5186dccd9699b727f6ab60856a0d0b791a852e3',
        '59046a82364c20490f3726617242077c3518c2e0f8baae610821e3ab4c03a209',
    ),
    'cerchi/guide/aristotele-forma-fine-realta/index.html': (
        'a0aab6b83ed2b7326f4c14285ef05bd3c8d2348fab0b7eee1f7fc94024420012',
        '2b96a3c39c8cf7d6f344db5fe9991cad2ea199e750623e01df0036b016609f0a',
    ),
    'cerchi/guide/cicerone-repubblica-legge-parola-civile/index.html': (
        '83b6318792558e5ae87e777141fb924b416deb6448f6fd0638b113d82e202ce5',
        '8750f398740383a2c59a7d1258158f1a68051e3842f13d67688d60013313a500',
    ),
    'cerchi/guide/claude-shannon-informazione-rumore-limiti-della-trasmissione/index.html': (
        '60ed95f9b08ce8196f519a11d95b6a314395423a0b828e9cf2afe628e17e8011',
        'a1a78862b82c82885b58eaa1402c4a7e9847e11fec2dde2119d0f2ca62210d35',
    ),
    'cerchi/guide/edgar-morin-la-conoscenza-e-i-suoi-punti-ciechi/index.html': (
        'a0a3a312bb69c39668ebb7f114f8ce9de5a76fff6c5c4ddd50206a3323e75e57',
        '25ca1927d8cd2eaf48201adf27fdc6671e6c60718d2754f6686cf66bbc0841fb',
    ),
    'cerchi/guide/gabriel-tarde-imitazione-credenza-desiderio/index.html': (
        '2493133d809a57a0ff32d00d713eda7f5261fbbae502310356464f3e020b1d4a',
        '5e4ef4635523f3d5f25a2e8b4c945a34399e85c9d9af84a72850d69ea5f0f19a',
    ),
    'cerchi/guide/gaetano-mosca-classe-politica-organizzazione-governo-reale/index.html': (
        '170edb6450e5055bc522384a5d60a6ea5fc3ab0f8c5796346674214ebd1d0e0d',
        'b4da45f264ca0d9ce961c3c4dc3d8737e8da7e2c73d088cb19763ae0a38384e5',
    ),
    'cerchi/guide/hobbes-paura-sovranita-ordine-politico/index.html': (
        '6d953513557c71cf216bbdcfbdfff0b87f2f28aa9110fd943bdd6e85ab5b1ecf',
        '8094b784dcdc97c3e9eb73461818a1640b73bc21b93665f67154c012af9705ea',
    ),
    'cerchi/guide/machiavelli-vita-opere-pensiero-politico/index.html': (
        '74e0d59eda7c809c36b7de67ea42d987855d050f78276f3d8d00140c85ec0c1c',
        '5c033ad49be906c18490329b80d15c015c04a8cf75a753d9a34d7724be3ccdda',
    ),
    'cerchi/guide/marx-vita-opere-pensiero/index.html': (
        '2e536f659a08de848941cadadbb7280925242346f55bd03b17eeb21c526475d3',
        '6a208a685a59efc20a7085fbcac9bd31f45b12fd68c6ea29771433818dfa04db',
    ),
    'cerchi/guide/nicolas-de-condorcet-istruzione-progresso-decisione/index.html': (
        '418c8da4ce820cc19e273df30a4cfd808fe10f89756bc449ab9726581e5b5e52',
        '4b3674a38b6fb86b37dbe84062ef7ec1da498f0de19971efbaff31e5d4db70fc',
    ),
    'cerchi/guide/nietzsche-vita-opere-pensiero/index.html': (
        '5f4b5deca63411bb928c0dbb0e13147ca137407bca40de3bad7ee2a50e774c87',
        '6c3485244f5af129c2a05a6751a9120608fb6b724cfb394c793204d7adffc837',
    ),
    'cerchi/guide/polibio-costituzione-potenza-decadenza/index.html': (
        '782bf22f344feb73a782707e7c384de7ec59ffa6dfa8d2b3867b036a53fde866',
        '869620abd0ae118d69b14e2489a6c6a5000ed7364c724e53c5019116b31dd18a',
    ),
    'cerchi/guide/seneca-dominio-tempo-morte/index.html': (
        'f075e2da8a1541797c59ed07e7ad116414d333c52ddf8b2a8b8a4e120cbd56e0',
        '175c43bba9dc4c0cd58e87579edd34734bcd5aa458de06ffb809c7d726d390eb',
    ),
    'cerchi/guide/simmel-denaro-metropoli-individualita/index.html': (
        '49d62680785813346051c3afdc6a0191f340633f090342f14a905e1ea5ea5163',
        'b443349d42124e5624995ed2c23c55f6faef25767877f18026d7ea5f1a99f652',
    ),
    'cerchi/guide/vilfredo-pareto-elite-residui-circolazione/index.html': (
        'b2180af9428e5b5ee0235970e22ecfa47e13dd4c0769b30a39c049b40484f6ec',
        '3c9804b4ba9f7247f2830161d6e7fe61ea6ede74c83938da350251eb203b828f',
    ),
    'en/cerchi/guides/adriano-olivetti-community-power/index.html': (
        'ce0ad0dddad328223f7b1550d12a0e86bc1756b5021137ad8edd70f2083eab3a',
        '74f67647b58632ca887a59d366751da596c8babb83d2185bf53f5442e328bee5',
    ),
    'en/cerchi/guides/claude-shannon-information-noise-limits-of-transmission/index.html': (
        'ea4af2cd0549ced4f2da3e6e8d225d0a235ae76404ebf94a0707b16ce0d24811',
        '115fc551398269ae972bac7e936ead3d7a3acfb60185429a5ec2cf9657c71eee',
    ),
    'en/cerchi/guides/edgar-morin-knowledge-and-its-blind-spots/index.html': (
        '324f14f75407540129e2c90c3564a41d30732d1c1fa62f93f34f985365e3f817',
        '007db7f5d05b97d1f742e84d20fcfb6c5c47c7d4db3a4d011af72ff7cc31faf8',
    ),
    'en/cerchi/guides/georg-simmel-money-metropolis-individuality/index.html': (
        'd64cd2009a43fdbd9a473f56fc5551cf8be17e51c25289fe16ad4ea106017a42',
        '5769cf93f7959d86bc4ecb18f17fb87cfe62ba0be2c87f2fb048773dec16fa78',
    ),
    'en/cerchi/guides/michel-foucault-life-under-examination/index.html': (
        '20ff96c1405c94659e39626e54b7bb7145b50f64204524ef48fc498e1842d71f',
        '19f3df72f47d049dc653af2b6282befe93f8b2a7d5ee9ffbab5c9e93aad08b51',
    ),
    'en/cerchi/guides/polybius-constitution-power-decline/index.html': (
        'b73ad6022f25f4b62241c2c8874c49a67437007ee6934e6ccb9166cfd6af4af2',
        '14b98055010613e461e58081ed95fa93694d452dce4abf83418d39ca926e0736',
    ),
}

# Literal preimages and approved replacements, in application order.
PATCHES = {
    'cerchi/guide/adam-smith-scambio-simpatia-ricchezza/index.html': (
        (
            'R01-19 r. 668',
            '<h3>Risorse autorevoli non invasive</h3>',
            '<h3>Risorse di consultazione</h3>',
        ),
    ),
    'cerchi/guide/adriano-olivetti-la-comunita-e-il-potere/index.html': (
        (
            'EI05-048 r. 403',
            '<p>L&#x27;opera va letta nel confronto politico della prima Repubblica. La formula di una democrazia senza partiti implica difficoltà concrete: come organizzare il dissenso, le alternative di governo e la competizione tra programmi? La scheda dell&#x27;edizione curata da Cadeddu per Rubbettino documenta la pubblicazione del 1949; il testo originale non è stato letto integralmente per questa revisione.</p>',
            '<p>L&#x27;opera va letta nel confronto politico della prima Repubblica. La formula di una democrazia senza partiti implica difficoltà concrete: come organizzare il dissenso, le alternative di governo e la competizione tra programmi? La scheda dell&#x27;edizione curata da Cadeddu per Rubbettino documenta la pubblicazione del 1949; il testo originale non è stato letto integralmente.</p>',
        ),
        (
            'EI05-048 r. 409',
            '<p>L&#x27;insieme affronta industria, istituzioni, cultura e finalità della convivenza. Questa revisione ne ha verificato l&#x27;identificazione bibliografica, non il testo integrale.</p>',
            '<p>L&#x27;insieme affronta industria, istituzioni, cultura e finalità della convivenza. È stata verificata l&#x27;identificazione bibliografica. Il testo integrale non è stato esaminato.</p>',
        ),
        (
            'EI05-048 r. 488',
            '<p>La monografia di Stefano Musso costituisce il principale riferimento specialistico. In questa revisione sono state consultate la scheda accademica del volume e una ricostruzione dell&#x27;Associazione Archivio Storico Olivetti che ne riprende i risultati; i verbali originali e il volume integrale restano da esaminare nell&#x27;eventuale audit documentale.</p>',
            '<p>La monografia di Stefano Musso costituisce il principale riferimento specialistico. Sono state consultate la scheda accademica del volume e una ricostruzione dell&#x27;Associazione Archivio Storico Olivetti che ne riprende i risultati. I verbali originali e il volume integrale non sono stati esaminati.</p>',
        ),
        (
            'EI05-050 r. 863',
            '<li>Valerio Ochetto, <em>Adriano Olivetti. La biografia</em>. <strong>Opera identificata attraverso bibliografie specialistiche, non letta per questa bozza.</strong></li>',
            '<li>Valerio Ochetto, <em>Adriano Olivetti. La biografia</em>. <strong>Opera identificata attraverso bibliografie specialistiche. Il testo non è stato consultato per la guida.</strong></li>',
        ),
    ),
    'cerchi/guide/alexis-de-tocqueville-democrazia-opinione-liberta/index.html': (
        (
            'R01-20 r. 890',
            '<h3>Risorse autorevoli non invasive</h3>',
            '<h3>Risorse di consultazione</h3>',
        ),
    ),
    'cerchi/guide/aristotele-forma-fine-realta/index.html': (
        (
            'R01-10 r. 579',
            '<p>Queste categorie vanno lette dentro il loro contesto storico. Il termine “democrazia” in Aristotele non coincide immediatamente con l’ideale costituzionale contemporaneo. La guida deve evitare sovrapposizioni frettolose.</p>',
            '<p>Queste categorie vanno lette dentro il loro contesto storico. Il termine “democrazia” in Aristotele non coincide immediatamente con l’ideale costituzionale contemporaneo.</p>',
        ),
        (
            'R01-10 r. 684',
            '<p>Può avere piattaforme senza comunità, informazione senza conoscenza, competenze senza carattere. Tre coppie bastano. Oltre, il pensiero diventa elenco.</p>',
            '<p>Può avere piattaforme senza comunità, informazione senza conoscenza, competenze senza carattere.</p>',
        ),
        (
            'R01-21 r. 919',
            '<h3>Risorse autorevoli non invasive</h3>',
            '<h3>Risorse per approfondire</h3>',
        ),
    ),
    'cerchi/guide/cicerone-repubblica-legge-parola-civile/index.html': (
        (
            'R01-12 r. 898',
            '<li><strong>Enciclopedia Treccani, Stanford Encyclopedia of Philosophy e Internet Encyclopedia of Philosophy</strong>, risorse di orientamento da nominare senza trasformare la guida in una pagina di link esterni.</li>',
            '<li><strong>Enciclopedia Treccani, Stanford Encyclopedia of Philosophy e Internet Encyclopedia of Philosophy</strong>, risorse di orientamento.</li>',
        ),
        (
            'R01-22 r. 891',
            '<h3>Risorse autorevoli non invasive</h3>',
            '<h3>Risorse di consultazione</h3>',
        ),
    ),
    'cerchi/guide/claude-shannon-informazione-rumore-limiti-della-trasmissione/index.html': (
        (
            'EI05-046 / R01-18 r. 900',
            '<p>Le opere di Shannon e gran parte degli studi moderni non vanno trattati come testi liberamente riproducibili. Questa guida utilizza concetti, dati storici, formule standard e parafrasi originali. Le citazioni testuali, quando necessarie nella versione finale, dovranno restare brevi e puntualmente attribuite.</p>',
            '<p>Le opere di Shannon e gran parte degli studi moderni non vanno trattati come testi liberamente riproducibili. Questa guida utilizza concetti, dati storici, formule standard e parafrasi originali. Le citazioni testuali, quando necessarie, devono restare brevi e puntualmente attribuite.</p>',
        ),
    ),
    'cerchi/guide/edgar-morin-la-conoscenza-e-i-suoi-punti-ciechi/index.html': (
        (
            'EI05-026 r. 523',
            '<p><strong>Studi critici e interpretativi.</strong> Carlos Reynoso, <em>Modelos o metáforas: Crítica del paradigma de la complejidad de Edgar Morin</em> (Buenos Aires, Sb Editorial, 2009); Edgar Morin, «Restricted Complexity, General Complexity», intervento al convegno di Cerisy (2005), pubblicato in <em>Worldviews, Science and Us</em> (World Scientific, 2007); Robert K. Merton, «The Unanticipated Consequences of Purposive Social Action», <em>American Sociological Review</em>, 1(6), 1936, pp. 894–904; Bernard Paillard, «Plozévet et l’affaire Morin», <em>Becedia</em>, 2022; Charles Forsdick, «Plonger dans un milieu réel: Edgar Morin in the field», 1997; Enio A. Blay e José Roberto C. Piqueira, «The Emergence of Edgar Morin’s Complex Thinking», <em>Anais da Academia Brasileira de Ciências</em>, 96(4), 2024, DOI 10.1590/0001-3765202420231112; Robert Delorme, «Deep Complexity and the problem of criticality in Morin’s and Le Moigne’s accounts of complexity», <em>Journal of Public Governance</em>, fasc. 19(1), riferito al 2012, pubblicato nel 2013, pp. 85–108; Salvatore Roberto Arpaia, «Edgar Morin e l’epistemologia dell’incompletezza», <em>Studi sulla Formazione</em>, 24(2), 2021, pp. 31–36, DOI 10.13128/ssf-13346; Laurent Dobuzinskis, «Where Is Morin’s Road to Complexity Going?», <em>World Futures</em>, 60(5–6), 2004, pp. 433–455, DOI 10.1080/02604020490471830.</p>',
            (
                '<p><strong>Studi critici e interpretativi.</strong></p>\n'
                '<ul>\n'
                '<li>Carlos Reynoso, <em>Modelos o metáforas: Crítica del paradigma de la complejidad de Edgar Morin</em> (Buenos Aires, Sb Editorial, 2009);</li>\n'
                '<li>Edgar Morin, «Restricted Complexity, General Complexity», intervento al convegno di Cerisy (2005), pubblicato in <em>Worldviews, Science and Us</em> (World Scientific, 2007);</li>\n'
                '<li>Robert K. Merton, «The Unanticipated Consequences of Purposive Social Action», <em>American Sociological Review</em>, 1(6), 1936, pp. 894–904;</li>\n'
                '<li>Bernard Paillard, «Plozévet et l’affaire Morin», <em>Becedia</em>, 2022;</li>\n'
                '<li>Charles Forsdick, «Plonger dans un milieu réel: Edgar Morin in the field», 1997;</li>\n'
                '<li>Enio A. Blay e José Roberto C. Piqueira, «The Emergence of Edgar Morin’s Complex Thinking», <em>Anais da Academia Brasileira de Ciências</em>, 96(4), 2024, DOI 10.1590/0001-3765202420231112;</li>\n'
                '<li>Robert Delorme, «Deep Complexity and the problem of criticality in Morin’s and Le Moigne’s accounts of complexity», <em>Journal of Public Governance</em>, fasc. 19(1), riferito al 2012, pubblicato nel 2013, pp. 85–108;</li>\n'
                '<li>Salvatore Roberto Arpaia, «Edgar Morin e l’epistemologia dell’incompletezza», <em>Studi sulla Formazione</em>, 24(2), 2021, pp. 31–36, DOI 10.13128/ssf-13346;</li>\n'
                '<li>Laurent Dobuzinskis, «Where Is Morin’s Road to Complexity Going?», <em>World Futures</em>, 60(5–6), 2004, pp. 433–455, DOI 10.1080/02604020490471830.</li>\n'
                '</ul>'
            ),
        ),
    ),
    'cerchi/guide/gabriel-tarde-imitazione-credenza-desiderio/index.html': (
        (
            'EI05-024 r. 462',
            (
                '</article>\n'
                '  </article>\n'
                '  <article class="item guide-section" id="tarde-e-durkheim">'
            ),
            (
                '</article>\n'
                '  <article class="item guide-section" id="tarde-e-durkheim">'
            ),
        ),
    ),
    'cerchi/guide/gaetano-mosca-classe-politica-organizzazione-governo-reale/index.html': (
        (
            'R01-23 r. 726',
            '<h3>Risorse autorevoli non invasive</h3>',
            '<h3>Risorse di consultazione</h3>',
        ),
    ),
    'cerchi/guide/hobbes-paura-sovranita-ordine-politico/index.html': (
        (
            'EI05-058 / R01-29 r. 212',
            '<a href="#fonti-verificate">23. Fonti verificate e letture da controllare</a>',
            '<a href="#fonti-verificate">23. Fonti verificate e orientamento critico</a>',
        ),
        (
            'EI05-058 / R01-29 r. 620',
            '<h2>Fonti verificate e letture da controllare</h2>',
            '<h2>Fonti verificate e orientamento critico</h2>',
        ),
        (
            'EI05-058 / R01-29 r. 630',
            '<h3>Letture critiche prioritarie</h3>',
            '<h3>Riferimenti critici da verificare</h3>',
        ),
    ),
    'cerchi/guide/machiavelli-vita-opere-pensiero-politico/index.html': (
        (
            'R01-30 r. 103',
            '<p>L’opera di Machiavelli è in pubblico dominio. Questa guida è un’opera editoriale originale protetta. Sono consentite citazioni brevi con attribuzione ad Alessandro Gentili, riferimento a Cerchi d’inchiostro e link alla pagina originale. La riproduzione sostanziale o il riuso commerciale, formativo, editoriale o in dataset non sono consentiti senza autorizzazione scritta.</p><p>© Alessandro Gentili — Cerchi d’inchiostro. Tutti i diritti riservati.</p>',
            '<p>© Alessandro Gentili — Cerchi d’inchiostro. Tutti i diritti riservati.</p>',
        ),
    ),
    'cerchi/guide/marx-vita-opere-pensiero/index.html': (
        (
            'R01-13 r. 97',
            '<p>Confondere Marx, comunismo, marxismo, leninismo, stalinismo, socialdemocrazia, teoria critica e movimenti operai significa rinunciare alla precisione. Una guida seria deve tenere insieme il legame storico e la distinzione concettuale.</p>',
            '<p>Confondere Marx, comunismo, marxismo, leninismo, stalinismo, socialdemocrazia, teoria critica e movimenti operai significa rinunciare alla precisione. Il legame storico fra queste esperienze e questi concetti va letto insieme alle loro differenze.</p>',
        ),
        (
            'R01-24 r. 104',
            '<h3>Risorse autorevoli non invasive</h3>',
            '<h3>Risorse di consultazione</h3>',
        ),
    ),
    'cerchi/guide/nicolas-de-condorcet-istruzione-progresso-decisione/index.html': (
        (
            'R01-25 r. 872',
            '<h3>Risorse autorevoli non invasive</h3>',
            '<h3>Risorse di consultazione</h3>',
        ),
    ),
    'cerchi/guide/nietzsche-vita-opere-pensiero/index.html': (
        (
            'R01-11 r. 128',
            '<p>Torino è l’ultima scena della vita lucida di Nietzsche. L’episodio del cavallo è diventato quasi mitico: il filosofo che avrebbe abbracciato un cavallo maltrattato prima di crollare. Va raccontato, se lo si racconta, con prudenza. La sua forza simbolica è enorme, ma una guida seria non deve trasformare Nietzsche in personaggio da romanzo terminale.</p>',
            '<p>Torino è l’ultima scena della vita lucida di Nietzsche. L’episodio del cavallo è diventato quasi mitico: il filosofo che avrebbe abbracciato un cavallo maltrattato prima di crollare. La sua forza simbolica è enorme. La cautela sull’attendibilità dell’episodio aiuta a distinguere la figura storica dal personaggio che l’aneddoto ha contribuito a creare.</p>',
        ),
        (
            'R01-11 r. 140',
            '<p>Byung-Chul Han non è un interprete classico di Nietzsche come Heidegger, Deleuze o Foucault. È però una lente contemporanea utile per leggere società della prestazione, stanchezza, auto-sfruttamento, positività obbligatoria. Va usato così: non come fonte primaria su Nietzsche, ma come ponte verso la ferita contemporanea.</p>',
            '<p>Byung-Chul Han non è un interprete classico di Nietzsche come Heidegger, Deleuze o Foucault. È però una lente contemporanea utile per leggere società della prestazione, stanchezza, auto-sfruttamento, positività obbligatoria. La sua lettura offre un ponte verso la ferita contemporanea. Le fonti primarie su Nietzsche appartengono a un altro piano.</p>',
        ),
        (
            'R01-26 r. 150',
            '<h3>Risorse autorevoli non invasive</h3>',
            '<h3>Risorse di consultazione</h3>',
        ),
    ),
    'cerchi/guide/polibio-costituzione-potenza-decadenza/index.html': (
        (
            'R01-14 r. 330',
            '<p>La vicinanza agli Scipioni spiega l’accesso privilegiato alle istituzioni romane, ma pone un problema critico. Polibio conosce Roma attraverso una parte della sua aristocrazia. Il suo sguardo è informato e insieme situato. La guida deve conservare entrambe le dimensioni: l’eccezionale qualità dell’osservazione e la possibilità che la prospettiva senatoria influenzi ciò che viene reso visibile.</p>',
            '<p>La vicinanza agli Scipioni spiega l’accesso privilegiato alle istituzioni romane, ma pone un problema critico. Polibio conosce Roma attraverso una parte della sua aristocrazia. Il suo sguardo è informato e insieme situato. La prospettiva senatoria può influenzare ciò che emerge anche in un’osservazione di qualità eccezionale.</p>',
        ),
        (
            'R01-14 r. 616',
            '<p>La nozione di oclocrazia può essere usata per delegittimare il conflitto popolare. Polibio distingue la democrazia corretta dalla degenerazione, ma il suo linguaggio resta legato a una cultura politica gerarchica. La guida deve applicare la stessa severità alla tirannide e all’oligarchia, evitando che soltanto i molti vengano descritti come pericolo.</p>',
            '<p>La nozione di oclocrazia può essere usata per delegittimare il conflitto popolare. Polibio distingue la democrazia corretta dalla degenerazione, ma il suo linguaggio resta legato a una cultura politica gerarchica. La stessa severità vale per la tirannide e l’oligarchia. Il pericolo di degenerazione riguarda anche il potere di uno e quello di pochi.</p>',
        ),
    ),
    'cerchi/guide/seneca-dominio-tempo-morte/index.html': (
        (
            'EI05-061 r. 350',
            '<p>È uno dei testi centrali per questa guida. Seneca vi sostiene che la vita non è breve in senso puramente quantitativo. Diventa breve quando viene dissipata. Il problema non è solo quanto tempo abbiamo, ma a chi e a che cosa lo consegniamo.</p>',
            '<p>Seneca vi sostiene che la vita non è breve in senso puramente quantitativo. Diventa breve quando viene dissipata. Il problema non è solo quanto tempo abbiamo, ma a chi e a che cosa lo consegniamo.</p>',
        ),
        (
            'EI05-062 r. 367',
            '<p>Per questa guida è importante perché collega la morale individuale alla forma dei rapporti sociali. Il beneficio può costruire comunità, ma può anche diventare favore, vincolo, gerarchia, obbligazione: un punto decisivo per leggere Seneca nel rapporto tra etica, potere e dipendenza.</p>',
            '<p>Il <em>De beneficiis</em> collega la morale individuale alla forma dei rapporti sociali. Il beneficio può costruire comunità, ma può anche diventare favore, vincolo, gerarchia, obbligazione: un punto decisivo per leggere Seneca nel rapporto tra etica, potere e dipendenza.</p>',
        ),
        (
            'EI05-063 r. 379',
            '<p>Il corpus tragico senecano presenta questioni di attribuzione e di destinazione che vanno ricordate con prudenza: alcune tragedie sono discusse dagli studiosi, e resta aperto il problema del loro rapporto con la scena, la recitazione e la lettura colta. Per questa guida, il punto decisivo è il loro valore come controcampo morale: la passione quando non trova più misura.</p>',
            '<p>Il corpus tragico senecano presenta questioni di attribuzione e di destinazione che vanno ricordate con prudenza: alcune tragedie sono discusse dagli studiosi, e resta aperto il problema del loro rapporto con la scena, la recitazione e la lettura colta. Le tragedie mostrano il controcampo morale della passione quando non trova più misura.</p>',
        ),
        (
            'R01-06 r. 271',
            '<p>Il quarto motivo è il rapporto con il potere. Seneca è anche un filosofo dello studio e dell’interiorità, ma la sua opera resta inseparabile dalla vicinanza al comando imperiale. Questo lo rende scomodo: il suo pensiero sulla virtù convive con ricchezza, influenza politica, compromessi e contraddizioni. Proprio qui la guida deve leggerlo con maggiore serietà. Non per assolverlo in anticipo, non per liquidarlo come incoerente, ma per comprendere che la filosofia morale diventa più difficile quando entra nella corte, negli apparati, nelle relazioni di forza.</p>',
            '<p>Il quarto motivo è il rapporto con il potere. Seneca è anche un filosofo dello studio e dell’interiorità, ma la sua opera resta inseparabile dalla vicinanza al comando imperiale. Questo lo rende scomodo: il suo pensiero sulla virtù convive con ricchezza, influenza politica, compromessi e contraddizioni. La filosofia morale diventa più difficile quando entra nella corte, negli apparati, nelle relazioni di forza. Per comprendere Seneca occorre misurare insieme il peso della virtù che professava e quello delle circostanze in cui agiva.</p>',
        ),
        (
            'R01-06 r. 482',
            '<p>Già nel mondo antico gli venne rimproverata la distanza tra la sua filosofia del distacco e l’entità dei suoi beni. Il problema è reale e non va aggirato. Una guida seria deve affrontarlo senza trasformarlo né in assoluzione automatica né in condanna sbrigativa.</p>',
            '<p>Già nel mondo antico gli venne rimproverata la distanza tra la sua filosofia del distacco e l’entità dei suoi beni. Il problema è reale e non va aggirato. La distanza fra il pensiero e i beni richiede un giudizio che tenga conto delle circostanze.</p>',
        ),
        (
            'R01-06 r. 754',
            '<p>La ricchezza, la posizione politica e la vicinanza a Nerone aprono problemi reali. La grandezza della guida sta nel tenere insieme pensiero e contraddizione, senza trasformare Seneca in figura pura né in bersaglio sbrigativo.</p>',
            '<p>La ricchezza, la posizione politica e la vicinanza a Nerone aprono problemi reali. Pensiero e contraddizione appartengono alla stessa figura storica e chiedono di essere giudicati insieme.</p>',
        ),
    ),
    'cerchi/guide/simmel-denaro-metropoli-individualita/index.html': (
        (
            'R01-27 r. 756',
            '<h3>Risorse autorevoli non invasive</h3>',
            '<h3>Risorse di consultazione</h3>',
        ),
    ),
    'cerchi/guide/vilfredo-pareto-elite-residui-circolazione/index.html': (
        (
            'R01-28 r. 768',
            '<h3>Risorse autorevoli non invasive</h3>',
            '<h3>Risorse di consultazione</h3>',
        ),
    ),
    'en/cerchi/guides/adriano-olivetti-community-power/index.html': (
        (
            'EI05-049 r. 400',
            '<p>The work must be read within the political confrontations of the early Republic. The formula of a democracy without parties carries concrete difficulties: how to organise dissent, alternatives of government and competition between programmes? The record of the edition edited by Cadeddu for Rubbettino documents the 1949 publication; the original text has not been read in full for this revision.</p>',
            '<p>The work must be read within the political confrontations of the early Republic. The formula of a democracy without parties carries concrete difficulties: how to organise dissent, alternatives of government and competition between programmes? The record of the edition edited by Cadeddu for Rubbettino documents the 1949 publication; the original text was not read in full.</p>',
        ),
        (
            'EI05-049 r. 406',
            '<p>The whole addresses industry, institutions, culture and the purposes of living together. This revision has verified its bibliographic identification, not its full text.</p>',
            '<p>The whole addresses industry, institutions, culture and the purposes of living together. The bibliographic identification was verified. The full text was not examined.</p>',
        ),
        (
            'EI05-049 r. 527',
            '<p>Stefano Musso’s monograph is the principal specialist reference. For this revision the academic record of the volume was consulted, together with a reconstruction by the Associazione Archivio Storico Olivetti that draws on his findings; the original minutes and the full volume remain to be examined in any eventual documentary audit.</p>',
            '<p>Stefano Musso’s monograph is the principal specialist reference. The academic record of the volume was consulted, together with a reconstruction by the Associazione Archivio Storico Olivetti that draws on his findings. The original minutes and the full volume were not examined.</p>',
        ),
        (
            'EI05-051 r. 966',
            '<li>Valerio Ochetto, <em>Adriano Olivetti. La biografia</em>. <strong>Work identified through specialist bibliographies, not read for this draft.</strong></li>',
            '<li>Valerio Ochetto, <em>Adriano Olivetti. La biografia</em>. <strong>Work identified through specialist bibliographies. The text was not consulted for this guide.</strong></li>',
        ),
        (
            'EI05-053 r. 454',
            '<p><em>A documentary summary of section 8. Order of presentation follows the master, not chronology. The nature of each document and the degree to which it was consulted are kept distinct: no text is presented as read in full when the source does not say so.</em></p>',
            '<p><em>A documentary summary of section 8. The documents appear in the order used in section 8. That order is not chronological. The nature of each document and the degree to which it was consulted are kept distinct: no text is presented as read in full when the source does not say so.</em></p>',
        ),
        (
            'EI05-053 r. 568',
            '<p><em>Sources and limits: sections 15 and 16, cross-checked against Limits and contradictions (section 30). The diagram rests on the reconstructions cited in the master; the original Statute, the minutes and the full monograph were not consulted directly. The “boundary of participation” is an editorial category of Cerchi d’inchiostro. Consultation and limited deliberation are not equivalent to full co-determination.</em></p>',
            '<p><em>Sources and limits: sections 15 and 16, cross-checked against Limits and contradictions (section 30). The diagram draws on the reconstructions cited in the guide. The original Statute, the minutes and the full monograph were not consulted directly. The “boundary of participation” is an editorial category of Cerchi d’inchiostro. Consultation and limited deliberation are not equivalent to full co-determination.</em></p>',
        ),
    ),
    'en/cerchi/guides/claude-shannon-information-noise-limits-of-transmission/index.html': (
        (
            'EI05-047 r. 792',
            '<p data-source-block="454">Shannon&#x27;s works and much of modern scholarship must not be treated as freely reproducible texts. This guide uses concepts, historical data, standard formulas, and original paraphrases. Direct quotations, where needed in the final version, must remain brief and precisely attributed.</p>',
            '<p data-source-block="454">Shannon&#x27;s works and much of modern scholarship must not be treated as freely reproducible texts. This guide uses concepts, historical data, standard formulas, and original paraphrases. Direct quotations, where needed, must remain brief and precisely attributed.</p>',
        ),
    ),
    'en/cerchi/guides/edgar-morin-knowledge-and-its-blind-spots/index.html': (
        (
            'EI05-027 r. 504',
            '<p><strong>Critical and interpretive scholarship.</strong> Carlos Reynoso, <em>Modelos o metáforas: Crítica del paradigma de la complejidad de Edgar Morin</em> (Buenos Aires, Sb Editorial, 2009); Edgar Morin, “Restricted Complexity, General Complexity”, presented at the Cerisy conference (2005) and published in <em>Worldviews, Science and Us</em> (World Scientific, 2007); Robert K. Merton, “The Unanticipated Consequences of Purposive Social Action”, <em>American Sociological Review</em>, 1(6), 1936, pp. 894–904; Bernard Paillard, “Plozévet et l’affaire Morin”, <em>Becedia</em>, 16 August 2022; André Burguière, <em>Bretons de Plozévet</em> (Paris, Flammarion, 1975); Charles Forsdick, “Plonger dans un milieu réel: Edgar Morin in the field”, 1997; Enio A. Blay and José Roberto C. Piqueira, “The Emergence of Edgar Morin’s Complex Thinking”, <em>Anais da Academia Brasileira de Ciências</em>, 96(4), 2024, DOI 10.1590/0001-3765202420231112; Robert Delorme, “Deep Complexity and the problem of criticality in Morin’s and Le Moigne’s accounts of complexity”, <em>Journal of Public Governance</em>, vol. 19(1), dated 2012 and published in 2013, pp. 85–108; Salvatore Roberto Arpaia, “Edgar Morin e l’epistemologia dell’incompletezza”, <em>Studi sulla Formazione</em>, 24(2), 2021, pp. 31–36, DOI 10.13128/ssf-13346; Laurent Dobuzinskis, “Where Is Morin’s Road to Complexity Going?”, <em>World Futures</em>, 60(5–6), 2004, pp. 433–455, DOI 10.1080/02604020490471830.</p>',
            (
                '<p><strong>Critical and interpretive scholarship.</strong></p>\n'
                '<ul>\n'
                '<li>Carlos Reynoso, <em>Modelos o metáforas: Crítica del paradigma de la complejidad de Edgar Morin</em> (Buenos Aires, Sb Editorial, 2009);</li>\n'
                '<li>Edgar Morin, “Restricted Complexity, General Complexity”, presented at the Cerisy conference (2005) and published in <em>Worldviews, Science and Us</em> (World Scientific, 2007);</li>\n'
                '<li>Robert K. Merton, “The Unanticipated Consequences of Purposive Social Action”, <em>American Sociological Review</em>, 1(6), 1936, pp. 894–904;</li>\n'
                '<li>Bernard Paillard, “Plozévet et l’affaire Morin”, <em>Becedia</em>, 16 August 2022;</li>\n'
                '<li>André Burguière, <em>Bretons de Plozévet</em> (Paris, Flammarion, 1975);</li>\n'
                '<li>Charles Forsdick, “Plonger dans un milieu réel: Edgar Morin in the field”, 1997;</li>\n'
                '<li>Enio A. Blay and José Roberto C. Piqueira, “The Emergence of Edgar Morin’s Complex Thinking”, <em>Anais da Academia Brasileira de Ciências</em>, 96(4), 2024, DOI 10.1590/0001-3765202420231112;</li>\n'
                '<li>Robert Delorme, “Deep Complexity and the problem of criticality in Morin’s and Le Moigne’s accounts of complexity”, <em>Journal of Public Governance</em>, vol. 19(1), dated 2012 and published in 2013, pp. 85–108;</li>\n'
                '<li>Salvatore Roberto Arpaia, “Edgar Morin e l’epistemologia dell’incompletezza”, <em>Studi sulla Formazione</em>, 24(2), 2021, pp. 31–36, DOI 10.13128/ssf-13346;</li>\n'
                '<li>Laurent Dobuzinskis, “Where Is Morin’s Road to Complexity Going?”, <em>World Futures</em>, 60(5–6), 2004, pp. 433–455, DOI 10.1080/02604020490471830.</li>\n'
                '</ul>'
            ),
        ),
    ),
    'en/cerchi/guides/georg-simmel-money-metropolis-individuality/index.html': (
        (
            'EI05-025 r. 321',
            "<p>We should remember what the apparently warmer arrangement could demand. The village where everyone knows one's name also knows whom one is supposed to marry, what profession one may enter and whose approval will count. A gift may produce a debt without a clear end. A favour can bind a person to a patron whose generosity is never wholly free. Monetary mediation loosens such dependence. Its abstractness enables contact and cooperation beyond a narrow circle, and it gives an individual the possibility of changing a place in the world without asking the entire community for permission. Simmel's account of money therefore cannot be translated into a complaint that commerce destroys authentic relations. Money can increase the number of people with whom one may interact. It may extend choice and permit reserve. The individual can purchase a service without surrendering the details of a private life. Where contracts and law work fairly, this impersonality can also limit arbitrary discretion. These are historically substantial achievements, though their distribution is never equal.</p>",
            (
                "<p>We should remember what the apparently warmer arrangement could demand. The village where everyone knows one's name also knows whom one is supposed to marry, what profession one may enter and whose approval will count. A gift may produce a debt without a clear end. A favour can bind a person to a patron whose generosity is never wholly free.</p>\n"
                "<p>Monetary mediation loosens such dependence. Its abstractness enables contact and cooperation beyond a narrow circle, and it gives an individual the possibility of changing a place in the world without asking the entire community for permission. Simmel's account of money therefore cannot be translated into a complaint that commerce destroys authentic relations. Money can increase the number of people with whom one may interact. It may extend choice and permit reserve. The individual can purchase a service without surrendering the details of a private life. Where contracts and law work fairly, this impersonality can also limit arbitrary discretion. These are historically substantial achievements, though their distribution is never equal.</p>"
            ),
        ),
        (
            'EI05-025 r. 367',
            "<p>Simmel examined this distance through the relation between <strong>objective culture</strong> and <strong>subjective culture</strong>, and most explicitly in his essay on the concept and tragedy of culture, published in 1911. Objective culture consists of works, knowledge, institutions, techniques and organized forms that acquire an existence beyond those who produced them. Subjective culture concerns the individual's development through appropriating and transforming such material. Culture, in the fuller sense, involves the movement from a living person through external forms and back into the formation of a living person. That movement can fail because of the very success of its first part. Collective creations grow in volume, complexity and specialization. A scientific field becomes impossible to master in its entirety. A technology demands training in an ever narrower range of functions. Institutions establish rules and categories that shape what users are able to do. The individual's capacity to assimilate the available world does not expand at an equivalent pace. The products of life acquire their own momentum.</p>",
            (
                "<p>Simmel examined this distance through the relation between <strong>objective culture</strong> and <strong>subjective culture</strong>, and most explicitly in his essay on the concept and tragedy of culture, published in 1911. Objective culture consists of works, knowledge, institutions, techniques and organized forms that acquire an existence beyond those who produced them. Subjective culture concerns the individual's development through appropriating and transforming such material. Culture, in the fuller sense, involves the movement from a living person through external forms and back into the formation of a living person.</p>\n"
                "<p>That movement can fail because of the very success of its first part. Collective creations grow in volume, complexity and specialization. A scientific field becomes impossible to master in its entirety. A technology demands training in an ever narrower range of functions. Institutions establish rules and categories that shape what users are able to do. The individual's capacity to assimilate the available world does not expand at an equivalent pace. The products of life acquire their own momentum.</p>"
            ),
        ),
        (
            'EI05-057 r. 446',
            '<p><strong>Fashion (<em>Die Mode</em> and related treatments).</strong> An investigation of imitation and differentiation as intertwined social tendencies. Texts and editions associated with this theme appeared in different forms; the bibliography should not imply that one English anthology represents a single fixed original edition.</p>',
            '<p><strong>Fashion (<em>Die Mode</em> and related treatments).</strong> An investigation of imitation and differentiation as intertwined social tendencies. Texts and editions associated with this theme appeared in different forms. No single English anthology should be taken to represent a fixed original edition.</p>',
        ),
    ),
    'en/cerchi/guides/michel-foucault-life-under-examination/index.html': (
        (
            'EI05-064 r. 620',
            '<p><a href="https://alessandro-gentili.it/cerchi/guide/nietzsche-vita-opere-pensiero/">Guide 05 — Nietzsche</a> introduces Foucault&#x27;s genealogical debt and makes it possible to compare the origins of values with the history of institutions.</p>',
            '<p><a href="https://alessandro-gentili.it/en/cerchi/guides/friedrich-nietzsche-nihilism-values-death-of-god/">Guide 05 — Nietzsche</a> introduces Foucault&#x27;s genealogical debt and makes it possible to compare the origins of values with the history of institutions.</p>',
        ),
        (
            'EI05-064 r. 480',
            '<p><strong>Nietzsche</strong> is a decisive interlocutor for genealogy. In <em>On the Genealogy of Morality</em>, guilt and punishment have histories that unsettle explanations constructed after the fact. Foucault brings that suspicion of necessary origins into the archives of institutional practice. <a href="https://alessandro-gentili.it/cerchi/guide/nietzsche-vita-opere-pensiero/">Guide 05 to Nietzsche</a> helps distinguish a philosophical debt from a difference in method.</p>',
            '<p><strong>Nietzsche</strong> is a decisive interlocutor for genealogy. In <em>On the Genealogy of Morality</em>, guilt and punishment have histories that unsettle explanations constructed after the fact. Foucault brings that suspicion of necessary origins into the archives of institutional practice. <a href="https://alessandro-gentili.it/en/cerchi/guides/friedrich-nietzsche-nihilism-values-death-of-god/">Guide 05 to Nietzsche</a> helps distinguish a philosophical debt from a difference in method.</p>',
        ),
    ),
    'en/cerchi/guides/polybius-constitution-power-decline/index.html': (
        (
            'EI05-055 r. 563',
            "<p><strong>Checked primary passages and scholarly discussion.</strong> The textual comparison for this draft used the accessible English renderings of <em>Histories</em> Books III, VI and XII hosted by the University of Chicago's LacusCurtius collection, together with the <em>Oxford Classical Dictionary</em> and the scholarly study “Learning from Experience: Polybius and the Progress of Rome” in <em>The Classical Quarterly</em>. John Thornton's “La costituzione mista in Polibio” was consulted for the historical and conceptual framework of Book VI. These are targeted checks; their use is not presented as complete reading of the forty-book primary work or the full scholarly literature.</p>",
            "<p><strong>Checked primary passages and scholarly discussion.</strong> The textual comparison used the accessible English renderings of <em>Histories</em> Books III, VI and XII hosted by the University of Chicago's LacusCurtius collection, together with the <em>Oxford Classical Dictionary</em> and the scholarly study “Learning from Experience: Polybius and the Progress of Rome” in <em>The Classical Quarterly</em>. John Thornton's “La costituzione mista in Polibio” was consulted for the historical and conceptual framework of Book VI. These are targeted checks; their use is not presented as complete reading of the forty-book primary work or the full scholarly literature.</p>",
        ),
    ),
}

def require(condition, message):
    if not condition:
        raise AssertionError(f'EI09: {message}')


def apply(path, document, *, reverse=False):
    patches = reversed(PATCHES[path]) if reverse else PATCHES[path]
    for label, original, approved in patches:
        old, new = (approved, original) if reverse else (original, approved)
        old, new = old.encode(), new.encode()
        require(document.count(old) == 1, f'nonunique fragment {label}: {path}')
        document = document.replace(old, new, 1)
    return document


def restore(path, revised):
    before_pin, after_pin = PINS[path]
    require(sha256(revised).hexdigest() == after_pin, f'wrong result SHA-256: {path}')
    previous = apply(path, revised, reverse=True)
    require(sha256(previous).hexdigest() == before_pin, f'wrong preimage SHA-256: {path}')
    require(apply(path, previous) == revised, f'integral reconstruction failed: {path}')
    return previous


def historical_bytes(root, path):
    """Read a historical preimage only after proving the nominated release exactly."""
    document = (root / path).read_bytes()
    return restore(path, document) if path in PINS else document


def historical_ref(path, document):
    """A Git base may precede EI09 or already contain its exact approved output."""
    if path in PINS and sha256(document).hexdigest() == PINS[path][1]:
        return restore(path, document)
    return document


def test_revision(path, before, revised):
    candidates = {'rollback': before, 'outside scope': revised + b'\n'}
    for label, original, approved in PATCHES[path]:
        fragment = approved.encode()
        candidates[label + ' reverted'] = revised.replace(fragment, original.encode(), 1)
        candidates[label + ' missing'] = revised.replace(fragment, b'', 1)
        candidates[label + ' duplicated'] = revised.replace(fragment, fragment + fragment, 1)
        if 'EI05-064 ' in label:
            candidates[label + ' wrong link language'] = revised.replace(
                fragment, fragment.replace(b'/en/cerchi/guides/', b'/cerchi/guide/'), 1)
    for label, candidate in candidates.items():
        require(candidate != revised, f'inactive negative fixture {label}: {path}')
        try:
            restore(path, candidate)
        except AssertionError:
            continue
        raise AssertionError(f'EI09: accepted {label}: {path}')

    label, _, approved = PATCHES[path][0]
    fragment = approved.encode()
    for invalid in (b'', fragment * 2):
        changed = revised.replace(fragment, invalid, 1)
        try:
            apply(path, changed, reverse=True)
        except AssertionError as error:
            require(str(error) == f'EI09: nonunique fragment {label}: {path}',
                    f'unexpected rejection for uniqueness: {path}')
        else:
            raise AssertionError(f'EI09: accepted nonunique fragment: {path}')
    return len(candidates) + 2


def verify_release(root, self_test=False):
    require(PINS.keys() == PATCHES.keys() and len(PINS) == 24
            and sum(map(len, PATCHES.values())) == 49, 'unexpected approved scope')
    tests = 0
    for path in PINS:
        revised = (root / path).read_bytes()
        before = subprocess.check_output(['git', 'show', f'{BASELINE}:{path}'], cwd=root)
        require(restore(path, revised) == before, f'preimage differs from frozen main: {path}')
        if self_test:
            tests += test_revision(path, before, revised)
    print(f'PASS EI09: 49 edits, 24 exact inversions; {tests} negative regressions')
