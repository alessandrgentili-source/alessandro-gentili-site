"""Exact transformations approved in CERCHI_EI08_CANDIDATO_STRUTTURALE.md."""
from hashlib import sha256
import json
import re
import subprocess

import cerchi_ei09 as ei09


BASELINE = 'c39f098de8fc6b1f4cf301d8b8acc612b9a2ddd3'
CANDIDATE_SHA256 = '1f0d8c055878ef969934fcfdd8f0911f0f3c40c6df4506583364c9f1818eefd8'

PINS = {
    'cerchi/guide/daniel-kahneman-giudizio-bias-decisione-sotto-incertezza/index.html': (
        'a5ed5f81d913f149d583f8a7335b40498e1896c21da5e188756b73261f77b6b3',
        '6f07be87735c16947e5bae19b4c08dfbd580ad378074959d2610a2becc398250',
    ),
    'cerchi/guide/epicuro-desiderio-paura-liberta-prima-della-scelta/index.html': (
        'fef7db27620b922c7aaea6febe12c1486336f622f9b0740950f77afcf3fa6bb6',
        '38a2ae67bfb1e73f27ff3e356b9451f78d53e36513872b332daf1a3a3e5dba95',
    ),
    'cerchi/guide/freud-inconscio-desiderio-civilta/index.html': (
        '70cfc3c0477d9a53696b116942c7755454626ddf703cc0dccc22d5dc0664eeea',
        '2672484e0837c2e53b4e34da4f35791505686333bd857c7c7e4e2b6b3f3e6f76',
    ),
    'cerchi/guide/gramsci-egemonia-cultura-senso-comune/index.html': (
        'ef8e27450f20348623e818efaa29eab0bc8816ddc344fa61d30eed16c410b9cf',
        'e8ed70c1e5002aebe04d20c59dedb78884dc4af1effc644e7c479d4b26537872',
    ),
    'cerchi/guide/hobbes-paura-sovranita-ordine-politico/index.html': (
        '600a17f61db85f4c1bf170b90bec012e88740b91cd951b4231302713aa1b1cdc',
        '6d953513557c71cf216bbdcfbdfff0b87f2f28aa9110fd943bdd6e85ab5b1ecf',
    ),
    'cerchi/guide/lucrezio-atomi-immagini-poesia-della-natura/index.html': (
        'f464a81549dc52c9bb856a6c46f738d76300727e9af7bc0fa3d72a44a07502eb',
        '26d9d5b923d9a8aceacbe7c1a039dfb326d2e19d04c056d810aa06c29b594582',
    ),
    'cerchi/guide/weber-razionalizzazione-potere-disincanto/index.html': (
        '211ba0ab4ecbb1233aa954279d539eb4f35985c04f9c5928a988878745ccd6e6',
        'c5a195b74c89bba17a16d5eca6322a4f20a233b104759fc303178ffc45edfb0c',
    ),
}

# Original and approved fragments, in application order.
PATCHES = {
    'cerchi/guide/daniel-kahneman-giudizio-bias-decisione-sotto-incertezza/index.html': (
        (
            'EI05-012 r. 663',
            '<h4 id="kahneman-ha-dimostrato-che-l-essere-umano-e-irrazionale">«Kahneman ha dimostrato che l’essere umano è irrazionale»</h4>',
            '<h3 class="ei08-h4-style" id="kahneman-ha-dimostrato-che-l-essere-umano-e-irrazionale">«Kahneman ha dimostrato che l’essere umano è irrazionale»</h3>',
        ),
        (
            'EI05-012 r. 665',
            '<h4 id="le-euristiche-sono-errori">«Le euristiche sono errori»</h4>',
            '<h3 class="ei08-h4-style" id="le-euristiche-sono-errori">«Le euristiche sono errori»</h3>',
        ),
        (
            'EI05-012 r. 667',
            '<h4 id="sistema-1-e-emotivo-sistema-2-razionale-sono-due-parti-del-cervello">«Sistema 1 è emotivo, Sistema 2 razionale: sono due parti del cervello»</h4>',
            '<h3 class="ei08-h4-style" id="sistema-1-e-emotivo-sistema-2-razionale-sono-due-parti-del-cervello">«Sistema 1 è emotivo, Sistema 2 razionale: sono due parti del cervello»</h3>',
        ),
        (
            'EI05-012 r. 669',
            '<h4 id="kahneman-ha-inventato-la-behavioral-economics">«Kahneman ha inventato la behavioral economics»</h4>',
            '<h3 class="ei08-h4-style" id="kahneman-ha-inventato-la-behavioral-economics">«Kahneman ha inventato la behavioral economics»</h3>',
        ),
        (
            'EI05-012 r. 671',
            '<h4 id="kahneman-ha-scoperto-tutti-i-bias-cognitivi">«Kahneman ha scoperto tutti i bias cognitivi»</h4>',
            '<h3 class="ei08-h4-style" id="kahneman-ha-scoperto-tutti-i-bias-cognitivi">«Kahneman ha scoperto tutti i bias cognitivi»</h3>',
        ),
        (
            'EI05-012 r. 673',
            '<h4 id="perdere-fa-sempre-esattamente-il-doppio-male-di-quanto-faccia-piacere-guadagnare">«Perdere fa sempre esattamente il doppio male di quanto faccia piacere guadagnare»</h4>',
            '<h3 class="ei08-h4-style" id="perdere-fa-sempre-esattamente-il-doppio-male-di-quanto-faccia-piacere-guadagnare">«Perdere fa sempre esattamente il doppio male di quanto faccia piacere guadagnare»</h3>',
        ),
        (
            'EI05-012 r. 675',
            '<h4 id="framing-significa-manipolazione">«Framing significa manipolazione»</h4>',
            '<h3 class="ei08-h4-style" id="framing-significa-manipolazione">«Framing significa manipolazione»</h3>',
        ),
        (
            'EI05-012 r. 677',
            '<h4 id="thinking-fast-and-slow-e-l-origine-delle-teorie-di-kahneman">«<em>Thinking, Fast and Slow</em> è l’origine delle teorie di Kahneman»</h4>',
            '<h3 class="ei08-h4-style" id="thinking-fast-and-slow-e-l-origine-delle-teorie-di-kahneman">«<em>Thinking, Fast and Slow</em> è l’origine delle teorie di Kahneman»</h3>',
        ),
        (
            'EI05-012 r. 679',
            '<h4 id="se-conosco-i-bias-smetto-di-averli">«Se conosco i bias, smetto di averli»</h4>',
            '<h3 class="ei08-h4-style" id="se-conosco-i-bias-smetto-di-averli">«Se conosco i bias, smetto di averli»</h3>',
        ),
        (
            'CSS locale approvato',
            '</head>',
            (
                '<style>\n'
                '.guide-page-main .guide-section h3.ei08-h4-style {\n'
                '  font: inherit;\n'
                '  font-weight: bolder;\n'
                '  margin: 1.33em 0;\n'
                '  letter-spacing: inherit;\n'
                '  text-wrap: inherit;\n'
                '  color: inherit;\n'
                '}\n'
                '</style>\n'
                '</head>'
            ),
        ),
    ),
    'cerchi/guide/epicuro-desiderio-paura-liberta-prima-della-scelta/index.html': (
        (
            'EI05-011 r. 742',
            '<h4>Epicuro predicava il piacere sfrenato</h4>',
            '<h3 class="ei08-h4-style">Epicuro predicava il piacere sfrenato</h3>',
        ),
        (
            'EI05-011 r. 744',
            '<h4>Epicuro rifiutava ogni dolore</h4>',
            '<h3 class="ei08-h4-style">Epicuro rifiutava ogni dolore</h3>',
        ),
        (
            'EI05-011 r. 746',
            '<h4>Epicuro era semplicemente ateo</h4>',
            '<h3 class="ei08-h4-style">Epicuro era semplicemente ateo</h3>',
        ),
        (
            'EI05-011 r. 748',
            '<h4>Atarassia significa non provare emozioni</h4>',
            '<h3 class="ei08-h4-style">Atarassia significa non provare emozioni</h3>',
        ),
        (
            'EI05-011 r. 750',
            '<h4>Il Giardino era un rifugio individualista</h4>',
            '<h3 class="ei08-h4-style">Il Giardino era un rifugio individualista</h3>',
        ),
        (
            'EI05-011 r. 752',
            '<h4>Epicuro invitava semplicemente ad abbandonare la politica</h4>',
            '<h3 class="ei08-h4-style">Epicuro invitava semplicemente ad abbandonare la politica</h3>',
        ),
        (
            'EI05-011 r. 754',
            '<h4>Il clinamen dimostra il libero arbitrio</h4>',
            '<h3 class="ei08-h4-style">Il clinamen dimostra il libero arbitrio</h3>',
        ),
        (
            'EI05-011 r. 756',
            '<h4>Epicuro aveva anticipato la fisica atomica moderna</h4>',
            '<h3 class="ei08-h4-style">Epicuro aveva anticipato la fisica atomica moderna</h3>',
        ),
        (
            'EI05-011 r. 758',
            '<h4>L’epicureismo coincide con il minimalismo contemporaneo</h4>',
            '<h3 class="ei08-h4-style">L’epicureismo coincide con il minimalismo contemporaneo</h3>',
        ),
        (
            'EI05-011 r. 760',
            '<h4>Epicuro aveva previsto consumismo, social network o algoritmi</h4>',
            '<h3 class="ei08-h4-style">Epicuro aveva previsto consumismo, social network o algoritmi</h3>',
        ),
        (
            'CSS locale approvato',
            '</head>',
            (
                '<style>\n'
                '.guide-page-main .guide-section h3.ei08-h4-style {\n'
                '  font: inherit;\n'
                '  font-weight: bolder;\n'
                '  margin: 1.33em 0;\n'
                '  letter-spacing: inherit;\n'
                '  text-wrap: inherit;\n'
                '  color: inherit;\n'
                '}\n'
                '</style>\n'
                '</head>'
            ),
        ),
    ),
    'cerchi/guide/freud-inconscio-desiderio-civilta/index.html': (
        (
            'EI05-023 FAQPage',
            (
                '<script type="application/ld+json">\n'
                '{\n'
                '  "@context": "https://schema.org",\n'
                '  "@type": "FAQPage",\n'
                '  "mainEntity": [\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Freud è ancora attuale?",\n'
                '      "acceptedAnswer": {"@type": "Answer", "text": "Sì, se non lo si trasforma in una formula rigida: resta decisiva la domanda sulla trasparenza dell’uomo a sé stesso."}\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Che cosa significa inconscio in Freud?",\n'
                '      "acceptedAnswer": {"@type": "Answer", "text": "L’inconscio è una dimensione attiva della vita psichica: agisce, ritorna, si maschera e si esprime in forme indirette."}\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Che cos’è la rimozione in Freud?",\n'
                '      "acceptedAnswer": {"@type": "Answer", "text": "La rimozione è un meccanismo inconsapevole che esclude dalla coscienza contenuti dolorosi, incompatibili o perturbanti."}\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Freud pensava davvero che tutto dipendesse dal sesso?",\n'
                '      "acceptedAnswer": {"@type": "Answer", "text": "No: la sessualità è centrale, ma indica una dimensione ampia della vita pulsionale, non una spiegazione riduttiva di ogni gesto umano."}\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Che cosa sono Io, Es e Super-Io?",\n'
                '      "acceptedAnswer": {"@type": "Answer", "text": "Sono tre istanze della seconda topica freudiana: Es come polo pulsionale, Io come mediazione, Super-Io come interiorizzazione di norme, ideali e divieti."}\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Che cosa significa narcisismo in Freud?",\n'
                '      "acceptedAnswer": {"@type": "Answer", "text": "Il narcisismo riguarda il modo in cui la libido può investire l’Io e non va ridotto a vanità, insulto morale o diagnosi rapida."}\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Che rapporto c’è tra Freud e la civiltà?",\n'
                '      "acceptedAnswer": {"@type": "Answer", "text": "Per Freud la civiltà protegge l’uomo, ma richiede rinunce, limiti, divieti e forme di sublimazione che non eliminano il conflitto."}\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Freud serve per capire la politica?",\n'
                '      "acceptedAnswer": {"@type": "Answer", "text": "Freud non è un teorico politico in senso stretto, ma aiuta a leggere identificazione, massa, autorità, paura e bisogno di protezione."}\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Perché Freud è importante per capire il presente?",\n'
                '      "acceptedAnswer": {"@type": "Answer", "text": "Perché il presente parla molto dell’io, ma non sempre lo comprende: Freud aiuta a distinguere raccontarsi e conoscersi."}\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Qual è il legame tra Freud, Gramsci e Hobbes?",\n'
                '      "acceptedAnswer": {"@type": "Answer", "text": "Freud, Gramsci e Hobbes mostrano tre profondità dell’obbedienza: uomo abitato, uomo formato e uomo contenuto."}\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Perché Freud viene spesso banalizzato?",\n'
                '      "acceptedAnswer": {"@type": "Answer", "text": "Perché parole come inconscio, rimozione, trauma, narcisismo e lapsus sono entrate nel linguaggio comune perdendo precisione."}\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Come va letto Freud dentro Cerchi d’inchiostro?",\n'
                '      "acceptedAnswer": {"@type": "Answer", "text": "Freud va letto come autore della frattura interna: mostra un uomo abitato da desideri, paure, difese, colpe, pulsioni e rimozioni."}\n'
                '    }\n'
                '  ]\n'
                '}\n'
                '  </script>'
            ),
            (
                '<script type="application/ld+json">\n'
                '{\n'
                '  "@context": "https://schema.org",\n'
                '  "@type": "FAQPage",\n'
                '  "mainEntity": [\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Freud è ancora attuale?",\n'
                '      "acceptedAnswer": {\n'
                '        "@type": "Answer",\n'
                '        "text": "Sì, Freud è ancora attuale se non lo si trasforma in una formula rigida.\\n\\nNon tutto il suo pensiero può essere assunto oggi come definitivo. Molte sue ipotesi sono state discusse, corrette, trasformate o criticate dalla psicoanalisi successiva, dalla psicologia contemporanea, dalle neuroscienze e dalle scienze umane. Ma la domanda che Freud ha aperto resta decisiva: l’uomo è davvero trasparente a sé stesso?\\n\\nFreud è attuale perché aiuta a leggere il desiderio, la rimozione, la colpa, il disagio, la massa e il bisogno di protezione dentro la civiltà contemporanea, senza pretendere di spiegare tutto."\n'
                '      }\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Che cosa significa inconscio in Freud?",\n'
                '      "acceptedAnswer": {\n'
                '        "@type": "Answer",\n'
                '        "text": "In Freud, l’inconscio non è un semplice deposito di ricordi nascosti.\\n\\nÈ una dimensione attiva della vita psichica: agisce, ritorna, si maschera, si esprime in forme indirette. Può lasciare tracce nei sogni, nei sintomi, nei lapsus, negli atti mancati, nelle ripetizioni, nelle fantasie. Se lo si immagina come archivio, bisogna intenderlo come un archivio vivo: non conserva soltanto, ma continua a lavorare."\n'
                '      }\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Che cos’è la rimozione in Freud?",\n'
                '      "acceptedAnswer": {\n'
                '        "@type": "Answer",\n'
                '        "text": "La rimozione è un meccanismo inconsapevole attraverso cui contenuti dolorosi, incompatibili o perturbanti vengono esclusi dalla coscienza.\\n\\nNon è una cancellazione volontaria e non è una semplice dimenticanza. Può avere una funzione protettiva, perché impedisce alla mente di essere travolta da ciò che non riesce a sostenere. Ma ciò che viene rimosso non sparisce: può tornare in forma indiretta, attraverso sintomi, sogni, atti mancati, ripetizioni o angosce."\n'
                '      }\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Freud pensava davvero che tutto dipendesse dal sesso?",\n'
                '      "acceptedAnswer": {\n'
                '        "@type": "Answer",\n'
                '        "text": "No: Freud non pensava che tutto dipendesse dal sesso nel senso riduttivo e comune della parola.\\n\\nLa sessualità è centrale in Freud, ma riguarda una dimensione più ampia della vita pulsionale: corpo, piacere, desiderio, sviluppo, fantasie, legami, divieti, identificazioni, colpa, rapporto con l’altro e con la legge.\\n\\nRidurre Freud a “tutto è sesso” significa non capire il suo problema."\n'
                '      }\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Che cosa sono Io, Es e Super-Io?",\n'
                '      "acceptedAnswer": {\n'
                '        "@type": "Answer",\n'
                '        "text": "Io, Es e Super-Io sono tre istanze della seconda topica freudiana, ma non vanno ridotte allo schema “istinto, ragione, morale”.\\n\\nL’Es indica il polo pulsionale, l’Io la funzione di mediazione, il Super-Io l’interiorizzazione di norme, ideali, divieti e giudizio. Il punto decisivo è che l’Io non è padrone assoluto della vita psichica: deve mediare tra spinte interne, realtà esterna, richieste morali e immagini interiorizzate dell’autorità."\n'
                '      }\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Che cosa significa narcisismo in Freud?",\n'
                '      "acceptedAnswer": {\n'
                '        "@type": "Answer",\n'
                '        "text": "Il narcisismo, in Freud, non significa semplicemente vanità o culto dell’immagine.\\n\\nRiguarda il modo in cui la libido può investire l’Io: il soggetto può diventare oggetto d’amore per sé stesso. Freud distingue un narcisismo primario e un narcisismo secondario. Per questo il concetto non va usato come insulto morale o diagnosi rapida del presente. Il rapporto con sé può essere fragile, difensivo, idealizzato, ma partecipa anche alla costruzione dell’autostima e dell’immagine di sé."\n'
                '      }\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Che rapporto c’è tra Freud e la civiltà?",\n'
                '      "acceptedAnswer": {\n'
                '        "@type": "Answer",\n'
                '        "text": "Per Freud, la civiltà protegge l’uomo ma gli chiede un prezzo psichico.\\n\\nVivere insieme significa rinunciare a una parte della soddisfazione pulsionale, accettare limiti, norme, divieti, differimenti, forme di sublimazione. La civiltà rende possibile la convivenza, ma non elimina il conflitto. Lo sposta, lo interiorizza, lo trasforma in tensione, colpa, disagio."\n'
                '      }\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Freud serve per capire la politica?",\n'
                '      "acceptedAnswer": {\n'
                '        "@type": "Answer",\n'
                '        "text": "Freud non è un teorico politico in senso stretto, ma aiuta a leggere alcune radici psichiche dell’obbedienza.\\n\\nÈ utile per capire una parte profonda della politica: identificazione, massa, capo, bisogno di protezione, autorità interiorizzata, paura, aggressività, desiderio di appartenenza.\\n\\nLa politica non è fatta solo di programmi, interessi e istituzioni. È fatta anche di affetti, immagini, paure, fantasie di ordine, nemici, promesse di sicurezza."\n'
                '      }\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Perché Freud è importante per capire il presente?",\n'
                '      "acceptedAnswer": {\n'
                '        "@type": "Answer",\n'
                '        "text": "Perché il presente parla moltissimo dell’io, ma non sempre lo comprende.\\n\\nViviamo in una società di esposizione, identità, profili, narrazioni personali, benessere, linguaggio psicologico, performance e autenticità. Freud aiuta a dubitare dell’equivalenza tra raccontarsi e conoscersi.\\n\\nIl presente mostra molto, ma può rimuovere proprio attraverso l’eccesso di visibilità. Il soggetto può nascondersi anche mentre si espone."\n'
                '      }\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Qual è il legame tra Freud, Gramsci e Hobbes?",\n'
                '      "acceptedAnswer": {\n'
                '        "@type": "Answer",\n'
                '        "text": "Freud, Gramsci e Hobbes permettono di leggere tre profondità dell’obbedienza.\\n\\nFreud mostra l’uomo abitato: desiderio, inconscio, rimozione, colpa, identificazione.\\nGramsci mostra l’uomo formato: cultura, scuola, lingua, senso comune, egemonia.\\nHobbes mostra l’uomo contenuto: paura, ordine, sovranità, protezione dal caos.\\n\\nLa triade non dice che tutto sia psicologia, cultura o politica. Dice che l’obbedienza è stratificata: nasce dentro il soggetto, prende forma nella cultura e si organizza nella sovranità."\n'
                '      }\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Perché Freud viene spesso banalizzato?",\n'
                '      "acceptedAnswer": {\n'
                '        "@type": "Answer",\n'
                '        "text": "Perché alcune sue parole sono diventate lingua comune: inconscio, rimozione, trauma, narcisismo, complesso, lapsus, desiderio.\\n\\nQuando un autore entra nel linguaggio quotidiano, guadagna diffusione ma perde precisione. Freud è diventato così famoso da essere spesso ridotto a caricatura: sogni, sesso, divano, madre, lapsus.\\n\\nLeggerlo seriamente significa recuperare la complessità dei suoi concetti senza trasformarli in gergo clinico per pochi specialisti."\n'
                '      }\n'
                '    },\n'
                '    {\n'
                '      "@type": "Question",\n'
                '      "name": "Come va letto Freud dentro Cerchi d’inchiostro?",\n'
                '      "acceptedAnswer": {\n'
                '        "@type": "Answer",\n'
                '        "text": "Freud va letto come autore della frattura interna.\\n\\nNon come icona pop, non come santino della psicoanalisi, non come diagnosi universale del presente. Freud serve perché mostra che l’uomo non è una superficie compatta: è abitato da desideri, paure, difese, colpe, immagini, pulsioni, parole e rimozioni che non controlla fino in fondo.\\n\\nDentro Cerchi d’inchiostro, Freud aiuta a vedere una ferita del presente: una società può raccontarsi moltissimo e conoscersi pochissimo."\n'
                '      }\n'
                '    }\n'
                '  ]\n'
                '}\n'
                '  </script>'
            ),
        ),
    ),
    'cerchi/guide/gramsci-egemonia-cultura-senso-comune/index.html': (
        (
            'EI05-021 kicker',
            '<p class="kicker">Indice</p><h2>Indice della guida</h2><nav class="guide-toc" aria-label="Indice della guida Antonio Gramsci">',
            '<h2>Indice della guida</h2><nav class="guide-toc" aria-label="Indice della guida Antonio Gramsci">',
        ),
    ),
    'cerchi/guide/hobbes-paura-sovranita-ordine-politico/index.html': (
        (
            'EI05-022 kicker',
            (
                '    <p class="kicker">Indice</p>\n'
                '    <h2>Indice della guida</h2>\n'
                '    <nav class="guide-toc" aria-label="Indice della guida Thomas Hobbes">'
            ),
            (
                '    <h2>Indice della guida</h2>\n'
                '    <nav class="guide-toc" aria-label="Indice della guida Thomas Hobbes">'
            ),
        ),
    ),
    'cerchi/guide/lucrezio-atomi-immagini-poesia-della-natura/index.html': (
        (
            'EI05-013 r. 507',
            '<h4 id="le-lettere-e-gli-elementi">Le lettere e gli elementi</h4>',
            '<h3 class="ei08-h4-style" id="le-lettere-e-gli-elementi">Le lettere e gli elementi</h3>',
        ),
        (
            'EI05-014 r. 589',
            '<h4 id="tutte-le-sensazioni-sono-vere">Tutte le sensazioni sono vere?</h4>',
            '<h3 class="ei08-h4-style" id="tutte-le-sensazioni-sono-vere">Tutte le sensazioni sono vere?</h3>',
        ),
        (
            'EI05-014 r. 597',
            '<h4 id="i-simulacra-non-sono-i-media">I <em>simulacra</em> non sono i media</h4>',
            '<h3 class="ei08-h4-style" id="i-simulacra-non-sono-i-media">I <em>simulacra</em> non sono i media</h3>',
        ),
        (
            'EI05-015 r. 619',
            '<h4 id="attraversare-i-confini-del-mondo">Attraversare i confini del mondo</h4>',
            '<h3 class="ei08-h4-style" id="attraversare-i-confini-del-mondo">Attraversare i confini del mondo</h3>',
        ),
        (
            'EI05-015 r. 626',
            '<h4 id="il-miele-e-il-paziente">Il miele e il paziente</h4>',
            '<h3 class="ei08-h4-style" id="il-miele-e-il-paziente">Il miele e il paziente</h3>',
        ),
        (
            'EI05-015 r. 636',
            '<h4 id="le-lettere-fanno-cio-che-spiegano">Le lettere fanno ciò che spiegano</h4>',
            '<h3 class="ei08-h4-style" id="le-lettere-fanno-cio-che-spiegano">Le lettere fanno ciò che spiegano</h3>',
        ),
        (
            'EI05-015 r. 642',
            '<h4 id="una-lingua-che-deve-ancora-esistere">Una lingua che deve ancora esistere</h4>',
            '<h3 class="ei08-h4-style" id="una-lingua-che-deve-ancora-esistere">Una lingua che deve ancora esistere</h3>',
        ),
        (
            'EI05-016 r. 706',
            '<h4 id="1-la-fisica-e-una-terapia-della-paura">1. La fisica è una terapia della paura</h4>',
            '<h3 class="ei08-h4-style" id="1-la-fisica-e-una-terapia-della-paura">1. La fisica è una terapia della paura</h3>',
        ),
        (
            'EI05-016 r. 708',
            '<h4 id="2-il-reale-eccede-cio-che-vediamo">2. Il reale eccede ciò che vediamo</h4>',
            '<h3 class="ei08-h4-style" id="2-il-reale-eccede-cio-che-vediamo">2. Il reale eccede ciò che vediamo</h3>',
        ),
        (
            'EI05-016 r. 710',
            '<h4 id="3-la-natura-non-ha-l-uomo-come-destinatario">3. La natura non ha l’uomo come destinatario</h4>',
            '<h3 class="ei08-h4-style" id="3-la-natura-non-ha-l-uomo-come-destinatario">3. La natura non ha l’uomo come destinatario</h3>',
        ),
        (
            'EI05-016 r. 712',
            '<h4 id="4-l-uomo-appartiene-alla-materia">4. L’uomo appartiene alla materia</h4>',
            '<h3 class="ei08-h4-style" id="4-l-uomo-appartiene-alla-materia">4. L’uomo appartiene alla materia</h3>',
        ),
        (
            'EI05-016 r. 714',
            '<h4 id="5-percepire-e-giudicare-sono-operazioni-differenti">5. Percepire e giudicare sono operazioni differenti</h4>',
            '<h3 class="ei08-h4-style" id="5-percepire-e-giudicare-sono-operazioni-differenti">5. Percepire e giudicare sono operazioni differenti</h3>',
        ),
        (
            'EI05-016 r. 716',
            '<h4 id="6-la-civilta-e-un-processo">6. La civiltà è un processo</h4>',
            '<h3 class="ei08-h4-style" id="6-la-civilta-e-un-processo">6. La civiltà è un processo</h3>',
        ),
        (
            'EI05-016 r. 718',
            '<h4 id="7-il-progresso-e-ambivalente">7. Il progresso è ambivalente</h4>',
            '<h3 class="ei08-h4-style" id="7-il-progresso-e-ambivalente">7. Il progresso è ambivalente</h3>',
        ),
        (
            'EI05-016 r. 720',
            '<h4 id="8-la-forma-poetica-partecipa-alla-conoscenza">8. La forma poetica partecipa alla conoscenza</h4>',
            '<h3 class="ei08-h4-style" id="8-la-forma-poetica-partecipa-alla-conoscenza">8. La forma poetica partecipa alla conoscenza</h3>',
        ),
        (
            'EI05-017 r. 849',
            '<h4 id="una-biografia-quasi-irrecuperabile">Una biografia quasi irrecuperabile</h4>',
            '<h3 class="ei08-h4-style" id="una-biografia-quasi-irrecuperabile">Una biografia quasi irrecuperabile</h3>',
        ),
        (
            'EI05-017 r. 851',
            '<h4 id="una-fedelta-che-complica-l-idea-di-originalita">Una fedeltà che complica l’idea di originalità</h4>',
            '<h3 class="ei08-h4-style" id="una-fedelta-che-complica-l-idea-di-originalita">Una fedeltà che complica l’idea di originalità</h3>',
        ),
        (
            'EI05-017 r. 853',
            '<h4 id="il-clinamen-resta-controverso">Il <em>clinamen</em> resta controverso</h4>',
            '<h3 class="ei08-h4-style" id="il-clinamen-resta-controverso">Il <em>clinamen</em> resta controverso</h3>',
        ),
        (
            'EI05-017 r. 855',
            '<h4 id="l-atomismo-antico-non-e-la-fisica-moderna">L’atomismo antico non è la fisica moderna</h4>',
            '<h3 class="ei08-h4-style" id="l-atomismo-antico-non-e-la-fisica-moderna">L’atomismo antico non è la fisica moderna</h3>',
        ),
        (
            'EI05-017 r. 857',
            '<h4 id="la-teoria-della-percezione-e-storicamente-superata">La teoria della percezione è storicamente superata</h4>',
            '<h3 class="ei08-h4-style" id="la-teoria-della-percezione-e-storicamente-superata">La teoria della percezione è storicamente superata</h3>',
        ),
        (
            'EI05-017 r. 859',
            '<h4 id="venere-resiste-a-una-soluzione-unica">Venere resiste a una soluzione unica</h4>',
            '<h3 class="ei08-h4-style" id="venere-resiste-a-una-soluzione-unica">Venere resiste a una soluzione unica</h3>',
        ),
        (
            'EI05-017 r. 861',
            '<h4 id="il-materialismo-non-coincide-automaticamente-con-l-ateismo-moderno">Il materialismo non coincide automaticamente con l’ateismo moderno</h4>',
            '<h3 class="ei08-h4-style" id="il-materialismo-non-coincide-automaticamente-con-l-ateismo-moderno">Il materialismo non coincide automaticamente con l’ateismo moderno</h3>',
        ),
        (
            'EI05-017 r. 863',
            '<h4 id="il-poema-sembra-completo-ma-probabilmente-non-definitivamente-revisionato">Il poema sembra completo, ma probabilmente non definitivamente revisionato</h4>',
            '<h3 class="ei08-h4-style" id="il-poema-sembra-completo-ma-probabilmente-non-definitivamente-revisionato">Il poema sembra completo, ma probabilmente non definitivamente revisionato</h3>',
        ),
        (
            'EI05-018 r. 868',
            '<h4 id="una-sola-frase-di-cicerone-ha-generato-secoli-di-discussione">Una sola frase di Cicerone ha generato secoli di discussione</h4>',
            '<h3 class="ei08-h4-style" id="una-sola-frase-di-cicerone-ha-generato-secoli-di-discussione">Una sola frase di Cicerone ha generato secoli di discussione</h3>',
        ),
        (
            'EI05-018 r. 870',
            '<h4 id="il-manifesto-del-miele-compare-due-volte">Il manifesto del miele compare due volte</h4>',
            '<h3 class="ei08-h4-style" id="il-manifesto-del-miele-compare-due-volte">Il manifesto del miele compare due volte</h3>',
        ),
        (
            'EI05-018 r. 872',
            '<h4 id="machiavelli-copio-lucrezio">Machiavelli copiò Lucrezio</h4>',
            '<h3 class="ei08-h4-style" id="machiavelli-copio-lucrezio">Machiavelli copiò Lucrezio</h3>',
        ),
        (
            'EI05-018 r. 874',
            '<h4 id="la-prima-grande-traduzione-italiana-dovette-aspettare">La prima grande traduzione italiana dovette aspettare</h4>',
            '<h3 class="ei08-h4-style" id="la-prima-grande-traduzione-italiana-dovette-aspettare">La prima grande traduzione italiana dovette aspettare</h3>',
        ),
        (
            'EI05-018 r. 876',
            '<h4 id="la-peste-finale-viene-da-tucidide">La peste finale viene da Tucidide</h4>',
            '<h3 class="ei08-h4-style" id="la-peste-finale-viene-da-tucidide">La peste finale viene da Tucidide</h3>',
        ),
        (
            'EI05-018 r. 878',
            '<h4 id="elementa-significa-anche-lettere"><em>Elementa</em> significa anche lettere</h4>',
            '<h3 class="ei08-h4-style" id="elementa-significa-anche-lettere"><em>Elementa</em> significa anche lettere</h3>',
        ),
        (
            'EI05-019 r. 883',
            '<h4 id="la-polvere-nel-raggio-di-sole-e-il-moto-browniano">“La polvere nel raggio di sole è il moto browniano”</h4>',
            '<h3 class="ei08-h4-style" id="la-polvere-nel-raggio-di-sole-e-il-moto-browniano">“La polvere nel raggio di sole è il moto browniano”</h3>',
        ),
        (
            'EI05-019 r. 885',
            '<h4 id="lucrezio-ha-anticipato-la-fisica-moderna">“Lucrezio ha anticipato la fisica moderna”</h4>',
            '<h3 class="ei08-h4-style" id="lucrezio-ha-anticipato-la-fisica-moderna">“Lucrezio ha anticipato la fisica moderna”</h3>',
        ),
        (
            'EI05-019 r. 887',
            '<h4 id="il-clinamen-anticipa-la-meccanica-quantistica">“Il <em>clinamen</em> anticipa la meccanica quantistica”</h4>',
            '<h3 class="ei08-h4-style" id="il-clinamen-anticipa-la-meccanica-quantistica">“Il <em>clinamen</em> anticipa la meccanica quantistica”</h3>',
        ),
        (
            'EI05-019 r. 889',
            '<h4 id="il-clinamen-dimostra-il-libero-arbitrio">“Il <em>clinamen</em> dimostra il libero arbitrio”</h4>',
            '<h3 class="ei08-h4-style" id="il-clinamen-dimostra-il-libero-arbitrio">“Il <em>clinamen</em> dimostra il libero arbitrio”</h3>',
        ),
        (
            'EI05-019 r. 891',
            '<h4 id="i-simulacra-sono-i-social-media-dell-antichita">“I <em>simulacra</em> sono i social media dell’antichità”</h4>',
            '<h3 class="ei08-h4-style" id="i-simulacra-sono-i-social-media-dell-antichita">“I <em>simulacra</em> sono i social media dell’antichità”</h3>',
        ),
        (
            'EI05-019 r. 893',
            '<h4 id="lucrezio-era-semplicemente-ateo">“Lucrezio era semplicemente ateo”</h4>',
            '<h3 class="ei08-h4-style" id="lucrezio-era-semplicemente-ateo">“Lucrezio era semplicemente ateo”</h3>',
        ),
        (
            'EI05-019 r. 895',
            '<h4 id="lucrezio-copia-epicuro">“Lucrezio copia Epicuro”</h4>',
            '<h3 class="ei08-h4-style" id="lucrezio-copia-epicuro">“Lucrezio copia Epicuro”</h3>',
        ),
        (
            'EI05-019 r. 897',
            '<h4 id="la-poesia-e-soltanto-miele-sulla-filosofia">“La poesia è soltanto miele sulla filosofia”</h4>',
            '<h3 class="ei08-h4-style" id="la-poesia-e-soltanto-miele-sulla-filosofia">“La poesia è soltanto miele sulla filosofia”</h3>',
        ),
        (
            'EI05-019 r. 899',
            '<h4 id="poggio-bracciolini-ha-salvato-un-testo-completamente-scomparso">“Poggio Bracciolini ha salvato un testo completamente scomparso”</h4>',
            '<h3 class="ei08-h4-style" id="poggio-bracciolini-ha-salvato-un-testo-completamente-scomparso">“Poggio Bracciolini ha salvato un testo completamente scomparso”</h3>',
        ),
        (
            'EI05-019 r. 901',
            '<h4 id="lucrezio-ha-creato-la-modernita">“Lucrezio ha creato la modernità”</h4>',
            '<h3 class="ei08-h4-style" id="lucrezio-ha-creato-la-modernita">“Lucrezio ha creato la modernità”</h3>',
        ),
        (
            'CSS locale approvato',
            '</head>',
            (
                '<style>\n'
                '.lucretius-guide .atlas-reading.complete-body > .guide-section h3.ei08-h4-style {\n'
                '  font: 600 1.05rem/1.5 system-ui, sans-serif;\n'
                '  margin: 1.8rem 0 .6rem;\n'
                '  letter-spacing: inherit;\n'
                '  text-wrap: inherit;\n'
                '  color: var(--complete-ink);\n'
                '}\n'
                '</style>\n'
                '</head>'
            ),
        ),
    ),
    'cerchi/guide/weber-razionalizzazione-potere-disincanto/index.html': (
        (
            'EI05-020 kicker',
            (
                '  <p class="kicker">Indice</p>\n'
                '  <h2>Indice della guida</h2>\n'
                '  <nav class="guide-toc" aria-label="Indice della guida Max Weber">'
            ),
            (
                '  <h2>Indice della guida</h2>\n'
                '  <nav class="guide-toc" aria-label="Indice della guida Max Weber">'
            ),
        ),
    ),
}

ATLAS_PATHS = {
    'cerchi/guide/epicuro-desiderio-paura-liberta-prima-della-scelta/index.html',
    'cerchi/guide/lucrezio-atomi-immagini-poesia-della-natura/index.html',
    'cerchi/guide/weber-razionalizzazione-potere-disincanto/index.html',
}


def require(condition, message):
    if not condition:
        raise AssertionError(f'EI08: {message}')


def apply(path, document, *, reverse=False):
    changes = reversed(PATCHES[path]) if reverse else PATCHES[path]
    for label, original, approved in changes:
        old, new = (approved, original) if reverse else (original, approved)
        old, new = old.encode(), new.encode()
        require(document.count(old) == 1, f'nonunique fragment {label}: {path}')
        document = document.replace(old, new, 1)
    return document


def restore(path, revised):
    original, approved = PINS[path]
    require(sha256(revised).hexdigest() == approved, f'wrong result SHA-256: {path}')
    before = apply(path, revised, reverse=True)
    require(sha256(before).hexdigest() == original, f'wrong preimage SHA-256: {path}')
    require(apply(path, before) == revised, f'integral reconstruction failed: {path}')
    return before


def historical_bytes(root, path):
    """Reconstruct a nominated preimage only after checking the exact release bytes."""
    document = ei09.historical_bytes(root, path)
    return restore(path, document) if path in PINS else document


def faq_mutations(fragment):
    schema = json.loads(fragment[fragment.index('>') + 1:fragment.rindex('</script>')])
    pairs = schema['mainEntity']
    first = pairs[0]['acceptedAnswer']['text']
    head = '<script type="application/ld+json">\n'
    tail = '\n  </script>'
    for label, replacement in (
        ('abbreviated answer', first.split('\n\n')[0]),
        ('answer punctuation', first.replace('Sì,', 'Sì', 1)),
        ('missing paragraph break', first.replace('\n\n', ' ', 1)),
    ):
        require(first != replacement, f'inactive mutation: {label}')
        pairs[0]['acceptedAnswer']['text'] = replacement
        yield label, head + json.dumps(schema, ensure_ascii=False, indent=2) + tail
    pairs[0]['acceptedAnswer']['text'] = first
    pairs[0], pairs[1] = pairs[1], pairs[0]
    yield 'reordered FAQ pair', head + json.dumps(schema, ensure_ascii=False, indent=2) + tail


def test_revision(path, before, revised):
    mutations = {'rollback': before, 'out-of-scope byte': revised + b'\n'}
    for label, original, approved in PATCHES[path]:
        approved_bytes = approved.encode()
        mutations[label + ' reverted'] = revised.replace(approved_bytes, original.encode(), 1)
        if ' r. ' in label:
            mutations[label + ' lost class'] = revised.replace(
                approved_bytes, approved_bytes.replace(b' class="ei08-h4-style"', b'', 1), 1)
        elif label.endswith(' kicker'):
            mutations[label + ' lost heading'] = revised.replace(
                approved_bytes, approved_bytes.replace(b'<h2>Indice della guida</h2>', b'', 1), 1)
            mutations[label + ' lost accessible name'] = revised.replace(
                approved_bytes, re.sub(rb' aria-label="[^"]+"', b'', approved_bytes), 1)
            mutations[label + ' changed anchor'] = re.sub(
                rb'(<nav class="guide-toc"[^>]*>\s*<a href="#)[^"]+',
                rb'\g<1>changed-anchor', revised, count=1)
        elif label.endswith(' FAQPage'):
            for change, schema in faq_mutations(approved):
                mutations[change] = revised.replace(approved_bytes, schema.encode(), 1)
            mutations['changed visible FAQ'] = revised.replace(
                b'<h3>1. Freud ', b'<h3>1. Altered Freud ', 1)
            mutations['changed Article schema'] = revised.replace(
                b'"@type": "Article"', b'"@type": "WebPage"', 1)
            mutations['changed BreadcrumbList schema'] = revised.replace(
                b'"@type":"BreadcrumbList"', b'"@type":"Other"', 1)

    if '/lucrezio-' in path:
        for anchor in ('il-progresso-ambivalente', 'lucrezio-era-ateo'):
            pattern = rb'<h4 id="' + anchor.encode() + rb'">.*?</h4>'
            mutations['promoted valid H4 ' + anchor] = re.sub(
                pattern, lambda m: m[0].replace(b'h4', b'h3'), revised, count=1)

    for label, candidate in mutations.items():
        require(candidate != revised, f'inactive mutation {label}: {path}')
        try:
            restore(path, candidate)
        except AssertionError:
            continue
        raise AssertionError(f'EI08: mutation accepted {label}: {path}')

    label, _, approved = PATCHES[path][0]
    fragment = approved.encode()
    for invalid in (b'', fragment * 2):
        candidate = revised.replace(fragment, invalid, 1)
        try:
            apply(path, candidate, reverse=True)
        except AssertionError as error:
            require(str(error) == f'EI08: nonunique fragment {label}: {path}',
                    f'unexpected uniqueness rejection: {path}')
        else:
            raise AssertionError(f'EI08: nonunique fragment accepted: {path}')
    return len(mutations) + 2


def verify_release(root, self_test=False):
    require(PATCHES.keys() == PINS.keys() and len(PINS) == 7
            and sum(map(len, PATCHES.values())) == 65, 'unexpected scope')
    tests = 0
    for path in PINS:
        revised = ei09.historical_bytes(root, path)
        before = subprocess.check_output(['git', 'show', f'{BASELINE}:{path}'], cwd=root)
        require(restore(path, revised) == before, f'preimage differs from frozen main: {path}')
        if self_test:
            tests += test_revision(path, before, revised)
    print(f'PASS EI08: 58 headings, 3 local styles, 3 kickers, 1 FAQPage, 7 exact inversions; {tests} negative regressions')
