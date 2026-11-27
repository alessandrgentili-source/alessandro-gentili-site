"""Exact EI06-B transformations of the four approved International guides."""
from hashlib import sha256
import re


SENECA = 'en/cerchi/guides/seneca-time-self-mastery-death/index.html'
SIMMEL = 'en/cerchi/guides/georg-simmel-money-metropolis-individuality/index.html'
NIETZSCHE = 'en/cerchi/guides/friedrich-nietzsche-nihilism-values-death-of-god/index.html'
CLAUSEWITZ = 'en/cerchi/guides/carl-von-clausewitz-war-politics-limits-of-force/index.html'

ATLAS_PATHS = {SENECA, NIETZSCHE}
HISTORICAL_BASES = {
    SIMMEL: "926d117841f685b125033cd3a0b02c211d7b6155",
    CLAUSEWITZ: "91eeaab213348182cbeb6a910c96806a01bf3203",
}

PINS = {
    SENECA: (
        "b88a9289d57d19b2d8d3dd1f166deeaf68ed03d5ea0b2ebb87f91e35e0e9d89c",
        "da0624c57f11fde7d213a20964e3dfcc4701c1efa9074b9301fc9e74cbacdb63",
    ),
    SIMMEL: (
        "74b785cda86dc9c01bd7beefcfc5ad3a48174f2939b63c9d4645faf4c436a813",
        "d64cd2009a43fdbd9a473f56fc5551cf8be17e51c25289fe16ad4ea106017a42",
    ),
    NIETZSCHE: (
        "ce612ac3ffed3abb06a3e8aa3c648ee0a3cba815baf796a5d57b3702776536cf",
        "09ab321bbfb0363a7d712683672655f375e3160a030fdfeb5ad5e709fd6045af",
    ),
    CLAUSEWITZ: (
        "329424dceb228e7f8be316384c400b98fac32cfe53e7988b4e66c7b097748d11",
        "b1c196a9a2aff0a272aad98dbf5cea92b3fa8a913e96946e8ca468d4ba979d80",
    ),
}

# Each fragment is bound to one section, with both literal HTML forms.
FRAGMENTS = {
    SENECA: (
        (
            'works',
            '<p>*<em>The </em>Moral Letters to Lucilius<em> (</em>Epistulae morales ad Lucilium<em>).</em>* A late collection of 124 surviving letters in twenty books. A literary-philosophical correspondence exploring time, virtue, friendship, mortality, wealth, freedom and the training of judgment. The personal tone should not be mistaken for unmediated autobiography.</p>',
            '<p><strong>The <em>Moral Letters to Lucilius</em> (<em>Epistulae morales ad Lucilium</em>).</strong> A late collection of 124 surviving letters in twenty books. A literary-philosophical correspondence exploring time, virtue, friendship, mortality, wealth, freedom and the training of judgment. The personal tone should not be mistaken for unmediated autobiography.</p>',
        ),
        (
            'works',
            '<p>*<em>On the Shortness of Life (</em>De brevitate vitae<em>).</em><em> An argument about the difference between years possessed and a life genuinely lived. It places the </em>occupati*, people absorbed in activities and obligations, under sharp examination.</p>',
            '<p><strong>On the Shortness of Life (<em>De brevitate vitae</em>).</strong> An argument about the difference between years possessed and a life genuinely lived. It places the <em>occupati</em>, people absorbed in activities and obligations, under sharp examination.</p>',
        ),
        (
            'works',
            '<p>*<em>On Anger (</em>De ira<em>).</em>* A sustained inquiry into destructive passion, the movement from impression to assent, and the effects of anger in personal life and in power.</p>',
            '<p><strong>On Anger (<em>De ira</em>).</strong> A sustained inquiry into destructive passion, the movement from impression to assent, and the effects of anger in personal life and in power.</p>',
        ),
        (
            'works',
            '<p>*<em>On Tranquillity of Mind (</em>De tranquillitate animi<em>).</em>* A response to the difficulty of living neither at peace with public commitment nor settled in withdrawal. It treats tranquillity as a demanding stability of judgment.</p>',
            '<p><strong>On Tranquillity of Mind (<em>De tranquillitate animi</em>).</strong> A response to the difficulty of living neither at peace with public commitment nor settled in withdrawal. It treats tranquillity as a demanding stability of judgment.</p>',
        ),
        (
            'works',
            '<p>*<em>On Clemency (</em>De clementia<em>).</em>* Addressed to Nero early in his reign. It studies the moral restraint appropriate to a ruler with extensive powers and belongs to the historical tradition of counsel to princes.</p>',
            '<p><strong>On Clemency (<em>De clementia</em>).</strong> Addressed to Nero early in his reign. It studies the moral restraint appropriate to a ruler with extensive powers and belongs to the historical tradition of counsel to princes.</p>',
        ),
        (
            'works',
            "<p>*<em>On the Happy Life (</em>De vita beata<em>).</em>* A defence of the Stoic account of happiness and virtue, including Seneca's response to criticism of his wealth.</p>",
            "<p><strong>On the Happy Life (<em>De vita beata</em>).</strong> A defence of the Stoic account of happiness and virtue, including Seneca's response to criticism of his wealth.</p>",
        ),
        (
            'works',
            '<p>*<em>On Leisure (</em>De otio<em>).</em>* An exploration of political participation, withdrawal and the possibility of serving a wider human community through philosophy. The surviving work is incomplete.</p>',
            '<p><strong>On Leisure (<em>De otio</em>).</strong> An exploration of political participation, withdrawal and the possibility of serving a wider human community through philosophy. The surviving work is incomplete.</p>',
        ),
        (
            'works',
            '<p>*<em>On Providence (</em>De providentia<em>).</em>* A discussion of suffering, fate and why adversity can occur to people striving to be good; its arguments belong to Stoic cosmology rather than modern theodicy.</p>',
            '<p><strong>On Providence (<em>De providentia</em>).</strong> A discussion of suffering, fate and why adversity can occur to people striving to be good; its arguments belong to Stoic cosmology rather than modern theodicy.</p>',
        ),
        (
            'works',
            "<p>*<em>On the Firmness of the Wise Person (</em>De constantia sapientis<em>).</em>* A study of what it means for a wise person's moral character to withstand insult or injury.</p>",
            "<p><strong>On the Firmness of the Wise Person (<em>De constantia sapientis</em>).</strong> A study of what it means for a wise person's moral character to withstand insult or injury.</p>",
        ),
        (
            'works',
            '<p>*<em>On Benefits (</em>De beneficiis<em>).</em>* A substantial examination of giving, receiving, gratitude, obligation and the moral relationships shaped through gifts.</p>',
            '<p><strong>On Benefits (<em>De beneficiis</em>).</strong> A substantial examination of giving, receiving, gratitude, obligation and the moral relationships shaped through gifts.</p>',
        ),
        (
            'works',
            "<p>*<em>The </em>Consolations<em>.</em>* Addresses associated with Marcia, Helvia and Polybius, each engaging loss or misfortune through distinct circumstances and rhetorical strategies. They expose both the care and the severity of Seneca's therapeutic prose.</p>",
            "<p><strong>The <em>Consolations</em>.</strong> Addresses associated with Marcia, Helvia and Polybius, each engaging loss or misfortune through distinct circumstances and rhetorical strategies. They expose both the care and the severity of Seneca's therapeutic prose.</p>",
        ),
        (
            'works',
            '<p>*<em>The </em>Natural Questions<em> (</em>Naturales quaestiones<em>).</em>* A late work on the physical world — including earthquakes, water, weather and celestial phenomena — repeatedly connecting investigation of nature with the scale of human judgment.</p>',
            '<p><strong>The <em>Natural Questions</em> (<em>Naturales quaestiones</em>).</strong> A late work on the physical world — including earthquakes, water, weather and celestial phenomena — repeatedly connecting investigation of nature with the scale of human judgment.</p>',
        ),
        (
            'concepts',
            "<p>*<em>Time (</em>tempus<em>).</em><em> The dimension of life that can be used or lost but never repaid. The first </em>Moral Letter* turns the reader's attention towards it as the condition of deliberate living.</p>",
            "<p><strong>Time (<em>tempus</em>).</strong> The dimension of life that can be used or lost but never repaid. The first <em>Moral Letter</em> turns the reader's attention towards it as the condition of deliberate living.</p>",
        ),
        (
            'concepts',
            "<p>*<em>Self-possession (</em>vindicare se sibi<em>).</em>* Seneca's legal-inflected expression for reclaiming oneself. The moral meaning depends on judgment rather than on a right to command all circumstances.</p>",
            "<p><strong>Self-possession (<em>vindicare se sibi</em>).</strong> Seneca's legal-inflected expression for reclaiming oneself. The moral meaning depends on judgment rather than on a right to command all circumstances.</p>",
        ),
        (
            'concepts',
            '<p>*<em>Occupation (</em>occupatio<em>).</em>* The state of being absorbed by business, ambition or distractions. For Seneca, full days can conceal a life with little inward freedom.</p>',
            '<p><strong>Occupation (<em>occupatio</em>).</strong> The state of being absorbed by business, ambition or distractions. For Seneca, full days can conceal a life with little inward freedom.</p>',
        ),
        (
            'concepts',
            '<p>*<em>Delay (</em>dilatio<em>).</em>* The habitual postponement of living until an imagined future moment when all conditions will be favourable.</p>',
            '<p><strong>Delay (<em>dilatio</em>).</strong> The habitual postponement of living until an imagined future moment when all conditions will be favourable.</p>',
        ),
        (
            'concepts',
            '<p>*<em>Moral progress (</em>profectus<em>).</em>* The movement of an imperfect person towards wiser judgment. The work of philosophy assumes that learners are neither perfectly wise nor irredeemably fixed.</p>',
            '<p><strong>Moral progress (<em>profectus</em>).</strong> The movement of an imperfect person towards wiser judgment. The work of philosophy assumes that learners are neither perfectly wise nor irredeemably fixed.</p>',
        ),
        (
            'concepts',
            '<p>*<em>Virtue (</em>virtus<em>).</em>* In Stoic ethics, the genuine moral good, expressed through sound and consistent rational judgment and conduct.</p>',
            '<p><strong>Virtue (<em>virtus</em>).</strong> In Stoic ethics, the genuine moral good, expressed through sound and consistent rational judgment and conduct.</p>',
        ),
        (
            'concepts',
            '<p>*<em>Reason (</em>ratio<em>).</em>* The human power of considering impressions and judgments within a Stoic conception of rational nature. It is more than calculation or administrative competence.</p>',
            '<p><strong>Reason (<em>ratio</em>).</strong> The human power of considering impressions and judgments within a Stoic conception of rational nature. It is more than calculation or administrative competence.</p>',
        ),
        (
            'concepts',
            "<p>*<em>Assent (</em>adsensio<em>).</em>* The mind's endorsement of an impression or judgment. Crucial to Seneca's analysis of passion, particularly anger.</p>",
            "<p><strong>Assent (<em>adsensio</em>).</strong> The mind's endorsement of an impression or judgment. Crucial to Seneca's analysis of passion, particularly anger.</p>",
        ),
        (
            'concepts',
            '<p>*<em>Anger (</em>ira<em>).</em>* A destructive passion oriented towards retaliation, understood as involving mistaken valuations and assent, with especially grave effects in those who wield power.</p>',
            '<p><strong>Anger (<em>ira</em>).</strong> A destructive passion oriented towards retaliation, understood as involving mistaken valuations and assent, with especially grave effects in those who wield power.</p>',
        ),
        (
            'concepts',
            "<p>*<em>Clemency (</em>clementia<em>).</em>* The considered restraint of a person empowered to punish. Its political value and institutional insufficiency are both visible in Seneca's writing to Nero.</p>",
            "<p><strong>Clemency (<em>clementia</em>).</strong> The considered restraint of a person empowered to punish. Its political value and institutional insufficiency are both visible in Seneca's writing to Nero.</p>",
        ),
        (
            'concepts',
            '<p>*<em>Tranquillity (</em>tranquillitas animi<em>).</em>* A steadiness of mind developed through careful judgment, not simply a comfortable mood or the absence of public obligations.</p>',
            '<p><strong>Tranquillity (<em>tranquillitas animi</em>).</strong> A steadiness of mind developed through careful judgment, not simply a comfortable mood or the absence of public obligations.</p>',
        ),
        (
            'concepts',
            '<p>*<em>Fortune (</em>fortuna<em>).</em>* The changing field of external circumstances: loss, influence, illness, prosperity and reversal. Stoic training asks what moral authority such events should have over a person.</p>',
            '<p><strong>Fortune (<em>fortuna</em>).</strong> The changing field of external circumstances: loss, influence, illness, prosperity and reversal. Stoic training asks what moral authority such events should have over a person.</p>',
        ),
        (
            'concepts',
            "<p>*<em>Nature (</em>natura<em>).</em>* The rationally ordered cosmos of Stoic philosophy, as well as the domain explored in Seneca's natural investigations. 'Living according to nature' has a philosophical content beyond enjoying a natural environment.</p>",
            "<p><strong>Nature (<em>natura</em>).</strong> The rationally ordered cosmos of Stoic philosophy, as well as the domain explored in Seneca's natural investigations. 'Living according to nature' has a philosophical content beyond enjoying a natural environment.</p>",
        ),
        (
            'concepts',
            '<p>*<em>Leisure (</em>otium<em>).</em>* Time withdrawn from ordinary public business that may be devoted to philosophy and meaningful service, without being reduced to idleness.</p>',
            '<p><strong>Leisure (<em>otium</em>).</strong> Time withdrawn from ordinary public business that may be devoted to philosophy and meaningful service, without being reduced to idleness.</p>',
        ),
        (
            'concepts',
            "<p>*<em>Public business (</em>negotium<em>).</em>* Professional, civic and political responsibilities, whose worth depends on circumstances and the uses of one's agency.</p>",
            "<p><strong>Public business (<em>negotium</em>).</strong> Professional, civic and political responsibilities, whose worth depends on circumstances and the uses of one's agency.</p>",
        ),
        (
            'concepts',
            '<p>*<em>Internal freedom (</em>libertas<em>).</em>* The moral independence of judgment from impulses and unstable external rewards. This must be distinguished from legal freedom and political rights.</p>',
            '<p><strong>Internal freedom (<em>libertas</em>).</strong> The moral independence of judgment from impulses and unstable external rewards. This must be distinguished from legal freedom and political rights.</p>',
        ),
        (
            'concepts',
            '<p>*<em>Enslavement (</em>servitus<em>).</em>* Both a concrete institution of Roman society and an image Seneca uses for dependence on passions. These meanings must be differentiated, especially when reading Letter 47.</p>',
            '<p><strong>Enslavement (<em>servitus</em>).</strong> Both a concrete institution of Roman society and an image Seneca uses for dependence on passions. These meanings must be differentiated, especially when reading Letter 47.</p>',
        ),
        (
            'concepts',
            "<p>*<em>Death (</em>mors<em>).</em>* A finite boundary whose contemplation can alter the way one values life, ambition and the future. The term requires ethical and historical care when applied to Seneca's final days.</p>",
            "<p><strong>Death (<em>mors</em>).</strong> A finite boundary whose contemplation can alter the way one values life, ambition and the future. The term requires ethical and historical care when applied to Seneca's final days.</p>",
        ),
        (
            'concepts',
            "<p>*<em>Providence (</em>providentia<em>) and fate (</em>fatum<em>).</em>* Concepts of rational cosmic order in Stoicism. They organize Seneca's questions about adversity and must not be confused with a guarantee that human events are pleasant or just.</p>",
            "<p><strong>Providence (<em>providentia</em>) and fate (<em>fatum</em>).</strong> Concepts of rational cosmic order in Stoicism. They organize Seneca's questions about adversity and must not be confused with a guarantee that human events are pleasant or just.</p>",
        ),
        (
            'curiosities',
            '<p>*<em>Is </em>Octavia<em> by Seneca?</em>* The work is transmitted with Senecan drama but is generally regarded as by another author. Its portrayal of Seneca cannot be treated as his own self-portrait.</p>',
            '<p><strong>Is <em>Octavia</em> by Seneca?</strong> The work is transmitted with Senecan drama but is generally regarded as by another author. Its portrayal of Seneca cannot be treated as his own self-portrait.</p>',
        ),
    ),
    SIMMEL: (
        (
            'the-works-a-map-for-reading',
            '<p>*<em>On Social Differentiation (</em>Über sociale Differenzierung<em>, 1890).</em>* An early systematic study of the organization of groups and the relation between social differentiation and individuality. Its account of overlapping memberships helps establish why a person can acquire a singular position through several partial affiliations.</p>',
            '<p><strong>On Social Differentiation (<em>Über sociale Differenzierung</em>, 1890).</strong> An early systematic study of the organization of groups and the relation between social differentiation and individuality. Its account of overlapping memberships helps establish why a person can acquire a singular position through several partial affiliations.</p>',
        ),
        (
            'the-works-a-map-for-reading',
            '<p>*<em>Introduction to Moral Science (</em>Einleitung in die Moralwissenschaft<em>, 1892–93).</em>* A substantial early project in ethical inquiry, informative for the changing intellectual route through which Simmel came to later concerns about value and life.</p>',
            '<p><strong>Introduction to Moral Science (<em>Einleitung in die Moralwissenschaft</em>, 1892–93).</strong> A substantial early project in ethical inquiry, informative for the changing intellectual route through which Simmel came to later concerns about value and life.</p>',
        ),
        (
            'the-works-a-map-for-reading',
            "<p>*<em>The Philosophy of Money (</em>Philosophie des Geldes<em>, 1900; revised 1907).</em>* The central book for exchange, distance, value, objective and subjective culture, personal independence, abstraction and the elevation of money from means towards apparent end. Its opening inquiry concerns value; its wider achievement is a philosophy of monetary modernity. It should not be mistaken for an economic textbook or a direct replacement for Marx's critique of political economy.</p>",
            "<p><strong>The Philosophy of Money (<em>Philosophie des Geldes</em>, 1900; revised 1907).</strong> The central book for exchange, distance, value, objective and subjective culture, personal independence, abstraction and the elevation of money from means towards apparent end. Its opening inquiry concerns value; its wider achievement is a philosophy of monetary modernity. It should not be mistaken for an economic textbook or a direct replacement for Marx's critique of political economy.</p>",
        ),
        (
            'the-works-a-map-for-reading',
            "<p>*<em>The Metropolis and Mental Life (</em>Die Großstädte und das Geistesleben<em>, 1903).</em><em> A compressed, unusually powerful account of metropolitan stimulation, reserve, punctuality, calculability, the </em>blasé* attitude and a distinctive urban freedom. Read the passages about Berlin's watches alongside the discussion of personal distance and objective culture.</p>",
            "<p><strong>The Metropolis and Mental Life (<em>Die Großstädte und das Geistesleben</em>, 1903).</strong> A compressed, unusually powerful account of metropolitan stimulation, reserve, punctuality, calculability, the <em>blasé</em> attitude and a distinctive urban freedom. Read the passages about Berlin's watches alongside the discussion of personal distance and objective culture.</p>",
        ),
        (
            'the-works-a-map-for-reading',
            '<p>*<em>Fashion (</em>Die Mode<em> and related treatments).</em>* An investigation of imitation and differentiation as intertwined social tendencies. Texts and editions associated with this theme appeared in different forms; the bibliography should not imply that one English anthology represents a single fixed original edition.</p>',
            '<p><strong>Fashion (<em>Die Mode</em> and related treatments).</strong> An investigation of imitation and differentiation as intertwined social tendencies. Texts and editions associated with this theme appeared in different forms; the bibliography should not imply that one English anthology represents a single fixed original edition.</p>',
        ),
        (
            'the-works-a-map-for-reading',
            '<p>*<em>Sociology: Inquiries into the Construction of Social Forms (</em>Soziologie<em>, 1908).</em><em> The major text for formal sociology, including the stranger, secrecy, conflict and forms of domination and association. Its title indicates an inquiry into </em>Vergesellschaftung*, the making of social relations, not a finished theory of a homogeneous thing called society.</p>',
            '<p><strong>Sociology: Inquiries into the Construction of Social Forms (<em>Soziologie</em>, 1908).</strong> The major text for formal sociology, including the stranger, secrecy, conflict and forms of domination and association. Its title indicates an inquiry into <em>Vergesellschaftung</em>, the making of social relations, not a finished theory of a homogeneous thing called society.</p>',
        ),
        (
            'the-works-a-map-for-reading',
            '<p>*<em>Philosophical Culture (</em>Philosophische Kultur<em>, 1911).</em>* Essays moving among social phenomena, philosophical reflection and cultural questions. Read in connection with the essay on the tragedy of culture, published in the early 1910s, to examine the changing relation between individual formation and increasingly autonomous cultural products.</p>',
            '<p><strong>Philosophical Culture (<em>Philosophische Kultur</em>, 1911).</strong> Essays moving among social phenomena, philosophical reflection and cultural questions. Read in connection with the essay on the tragedy of culture, published in the early 1910s, to examine the changing relation between individual formation and increasingly autonomous cultural products.</p>',
        ),
        (
            'the-works-a-map-for-reading',
            "<p>*<em>The Concept and Tragedy of Culture (</em>Der Begriff und die Tragödie der Kultur<em>, 1911).</em>* The particularly relevant essay on the gap between objective and subjective culture. The problem is structural: external creations become conditions for individual development and can outgrow the individual's capacity to integrate them.</p>",
            "<p><strong>The Concept and Tragedy of Culture (<em>Der Begriff und die Tragödie der Kultur</em>, 1911).</strong> The particularly relevant essay on the gap between objective and subjective culture. The problem is structural: external creations become conditions for individual development and can outgrow the individual's capacity to integrate them.</p>",
        ),
        (
            'the-works-a-map-for-reading',
            '<p>*<em>Sociability (</em>Die Geselligkeit<em>, early 1910s).</em>* A study of association in which being together becomes its own activity, with a form that requires tact and mutuality. Often read in later English collections, it merits attention beyond the image of conversation as mere leisure.</p>',
            '<p><strong>Sociability (<em>Die Geselligkeit</em>, early 1910s).</strong> A study of association in which being together becomes its own activity, with a form that requires tact and mutuality. Often read in later English collections, it merits attention beyond the image of conversation as mere leisure.</p>',
        ),
        (
            'the-works-a-map-for-reading',
            '<p>*<em>Fundamental Questions of Sociology (</em>Grundfragen der Soziologie<em>, 1917).</em><em> A concise later presentation of aspects of his sociological method and conceptual vocabulary. Especially useful after selections from the longer 1908 </em>Sociology*.</p>',
            '<p><strong>Fundamental Questions of Sociology (<em>Grundfragen der Soziologie</em>, 1917).</strong> A concise later presentation of aspects of his sociological method and conceptual vocabulary. Especially useful after selections from the longer 1908 <em>Sociology</em>.</p>',
        ),
        (
            'the-works-a-map-for-reading',
            '<p>*<em>The Conflict of Modern Culture (1918) and The View of Life (</em>Lebensanschauung<em>, 1918).</em>* Late reflections on the tension between life and its forms, and on philosophical questions that extend beyond the sociology of monetary exchange. Their late date should not lead us to read every earlier sociological essay as a preparatory chapter of a single finished metaphysical system.</p>',
            '<p><strong>The Conflict of Modern Culture (1918) and The View of Life (<em>Lebensanschauung</em>, 1918).</strong> Late reflections on the tension between life and its forms, and on philosophical questions that extend beyond the sociology of monetary exchange. Their late date should not lead us to read every earlier sociological essay as a preparatory chapter of a single finished metaphysical system.</p>',
        ),
        (
            'key-concepts',
            '<p>*<em>Reciprocal interaction (</em>Wechselwirkung<em>).</em>* Mutual effects through which individuals and groups influence one another; a basis for understanding society as ongoing relation.</p>',
            '<p><strong>Reciprocal interaction (<em>Wechselwirkung</em>).</strong> Mutual effects through which individuals and groups influence one another; a basis for understanding society as ongoing relation.</p>',
        ),
        (
            'key-concepts',
            '<p>*<em>Sociation (</em>Vergesellschaftung<em>).</em>* The process through which human purposes, desires and actions take recognizable social forms, such as conflict, cooperation or exchange.</p>',
            '<p><strong>Sociation (<em>Vergesellschaftung</em>).</strong> The process through which human purposes, desires and actions take recognizable social forms, such as conflict, cooperation or exchange.</p>',
        ),
        (
            'key-concepts',
            '<p>*<em>Metropolis (</em>Großstadt<em>).</em>* The large modern city as an environment of intense stimulation, highly differentiated functions and coordinated impersonal relations.</p>',
            '<p><strong>Metropolis (<em>Großstadt</em>).</strong> The large modern city as an environment of intense stimulation, highly differentiated functions and coordinated impersonal relations.</p>',
        ),
    ),
    NIETZSCHE: (
        (
            'misreadings',
            '<li>*<em>Is </em>The Will to Power<em> his final masterpiece?</em>* No. It is an editorial assemblage of posthumous notes.</li>',
            '<li><strong>Is <em>The Will to Power</em> his final masterpiece?</strong> No. It is an editorial assemblage of posthumous notes.</li>',
        ),
    ),
    CLAUSEWITZ: (
        (
            'an-original-cerchi-instrument-the-purpose-after-contact-test',
            '<figcaption>An editorial interpretation of *On War*, especially I.1, I.7 and VIII.6. The two views describe a conceptual relationship, not an actual campaign or a formula for predicting victory. Both remain available in print.</figcaption>',
            '<figcaption>An editorial interpretation of <em>On War</em>, especially I.1, I.7 and VIII.6. The two views describe a conceptual relationship, not an actual campaign or a formula for predicting victory. Both remain available in print.</figcaption>',
        ),
    ),
}


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def digest(data):
    return sha256(data).hexdigest()


def transform(path, data, *, reverse=False):
    """Check both complete documents and replace unique, section-bound fragments."""
    before, after = PINS[path]
    if reverse:
        before, after = after, before
    require(digest(data) == before, 'EI06-B input digest differs: ' + path)
    for section, old, new in FRAGMENTS[path]:
        if reverse:
            old, new = new, old
        article = re.findall(
            rb'<article\b[^>]*\bid="' + re.escape(section.encode()) + rb'"[^>]*>.*?</article>',
            data, re.S,
        )
        source = old.encode()
        require(len(article) == 1 and article[0].count(source) == data.count(source) == 1,
                'EI06-B fragment must be unique in #' + section)
        data = data.replace(source, new.encode(), 1)
    require(digest(data) == after, 'EI06-B output digest differs: ' + path)
    return data


def verify_revision(path, before, actual):
    require(actual == transform(path, before), 'EI06-B unapproved document: ' + path)


def test_revision(path, before, actual):
    require(transform(path, actual, reverse=True) == before, 'EI06-B revision is not reversible')
    fragments = FRAGMENTS[path]
    candidates = [actual + b'\n']
    for _, old, new in fragments:
        approved = new.encode()
        # Omission, a literal asterisk, different punctuation, and a different emphasis.
        candidates.extend(actual.replace(approved, alteration, 1) for alteration in (
            old.encode(),
            approved.replace(b'>', b'>*', 1),
            approved.replace(b'.</', b'!</', 1) if b'.</' in approved else approved.replace(b'.', b'!', 1),
            re.sub(rb'(.)</em>', rb'</em>\1', approved, count=1),
            re.sub(rb'(?<=>)[A-Z][a-z]+', b'Changed', approved, count=1),
            approved.replace(b'<em>', b'<i>', 1).replace(b'</em>', b'</i>', 1),
        ))
        if b'</strong>' in approved:
            moved = approved.replace(b'</strong> ', b' </strong>', 1)
            candidates.append(actual.replace(approved, moved, 1))
    if len(fragments) > 1:
        first, second = (f[2].encode() for f in fragments[:2])
        sentinel = b'<!-- EI06-B mutation -->'
        candidates.append(actual.replace(first, sentinel, 1).replace(second, first, 1).replace(sentinel, second, 1))
    if path != CLAUSEWITZ:
        fragment = fragments[0][2].encode()
        swapped = re.sub(rb'</?(?:em|strong)>',
                         lambda m: m[0].replace(b'strong', b'em') if b'strong' in m[0]
                         else m[0].replace(b'em', b'strong'), fragment)
        candidates.append(actual.replace(fragment, swapped, 1))
    if path == CLAUSEWITZ:
        candidates.extend(actual.replace(old, new, 1) for old, new in (
            (b'type="radio"', b'type="checkbox"'),
            (b'class="clausewitz-warning"', b'class="clausewitz-warning" hidden'),
        ))
    expected = 'EI06-B unapproved document: ' + path
    for candidate in candidates:
        require(candidate != actual, 'Ineffective EI06-B mutation: ' + path)
        try:
            verify_revision(path, before, candidate)
        except AssertionError as exc:
            require(str(exc) == expected, 'Unexpected EI06-B mutation rejection: ' + str(exc))
        else:
            raise AssertionError('EI06-B mutation accepted: ' + path)
    print(f'PASS EI06-B {path}: {len(fragments)} exact fragments, {len(candidates)} rejected mutations')
    return len(candidates)
