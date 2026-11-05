# Claude Shannon: information, noise and the limits of transmission

## Introduction

A sentence reaches a screen without a missing letter. The transfer has worked. The sentence may still be false, misunderstood or irrelevant to the person reading it. The difference between these outcomes seems obvious once stated, yet much of the modern world speaks about them as though they belonged to the same measure.

Claude Shannon made an extraordinary advance by treating one of these problems with unprecedented precision. A message must be selected, represented and transmitted through a channel subject to finite resources and disturbance. How much can cross it, and with what reliability? The message might be a love letter, a weather reading or a military command. What it means to a person need not enter the engineering calculation.

This deliberate boundary made the theory remarkably general. The problem for a reader now is to understand both the achievement and the limit that enabled it. **When a message arrives intact, what, exactly, has succeeded?**

## Shannon in five minutes

Claude Elwood Shannon (1916–2001) was an American mathematician and electrical engineer whose work helped establish the foundations of digital circuit theory and modern information theory. Born in Petoskey, Michigan, and raised in Gaylord, he studied mathematics and electrical engineering at the University of Michigan before moving to MIT.

Working with Vannevar Bush's Differential Analyzer, he saw a connection between switching circuits and Boolean algebra. His master's work, published as *A Symbolic Analysis of Relay and Switching Circuits* (1938), offered a rigorous way to analyze and design relay networks using logical operations. The history of computing has many contributors; this was a fundamental advance in the language of digital circuits, not the invention of the computer by one person.

Shannon joined Bell Laboratories in 1941, after graduate work and a research period in Princeton. In 1948, the two-part article *A Mathematical Theory of Communication* changed the treatment of information, noise and coding. He later pursued cryptography, chess, automata and playful mechanical inventions. Behind these apparently different interests lay a recurrent method: find the representation that makes a difficult problem tractable.

## From switching circuits to the structure of a problem

An electrical relay can be open or closed. A proposition in Boolean logic can be true or false. Shannon recognized that networks of switches could be described, simplified and constructed through logical relations. What had appeared to belong to separate practices—wiring and symbolic reasoning—could be treated within a shared formal structure.

This achievement helps explain the later communication theory. Shannon was not primarily offering a philosophy of machines. He sought descriptions precise enough to permit mathematical manipulation, and devices that could test whether an abstraction worked.

At Bell Labs the questions were urgent. Telephone networks, radio and telegraph systems had to contend with bandwidth, interference, power and cost. Harry Nyquist had investigated transmission rates and signal limits; Ralph Hartley had explored logarithmic measures of possible selections. Shannon extended these lines of inquiry by putting probability, source statistics and channel noise into a more general framework.

## The 1948 paper: a message among possible messages

In *A Mathematical Theory of Communication*, the engineering task concerns reproducing at one point a message selected at another, either exactly or to an acceptable approximation. A system cannot be designed only for the message that eventually travels through it. It must accommodate a range of possible messages, with statistical regularities that can be studied.

Shannon's conceptual diagram distinguishes an information source, a transmitter, a channel, a noise source, a receiver and a destination. The vocabulary applies to different physical media without pretending that their engineering details are identical.

The abstraction has a price, willingly paid: it is not necessary to establish the truth, beauty or importance of the words being carried. The choice of what the theory can measure is part of the scientific result.

## Bits, uncertainty and entropy

A binary digit is a symbol, 0 or 1. A bit as a unit of information measures an amount associated with selection under a probability model. When two possible outcomes are equally likely, learning which occurred resolves one bit of uncertainty. If one outcome is almost certain, the average uncertainty is smaller.

For an outcome with probability *p*, the self-information is conventionally written as *−log₂ p*. The quantity increases as an outcome becomes less probable. Its surprise is statistical, not psychological; an unlikely false statement may be informative in this technical sense without becoming more valuable or more true.

For a discrete random variable *X*, Shannon entropy is written *H(X) = −Σ p(x) log₂ p(x)*, where the sum runs over its possible outcomes. It measures average uncertainty for a specified distribution. A source whose next symbol is fully predictable has zero entropy; among a fixed number of alternatives, equal probabilities maximize it.

Entropy is connected mathematically and historically with statistical mechanics, yet the terms should not be transferred across theories without specifying the model. The bit likewise gives no warrant for declaring that matter consists of bits. Lucretius' atom and Shannon's unit answer different questions.

## Channels, noise and capacity

A communication channel may be modeled through the ways transmitted signals can give rise to received signals. Disturbances can change or obscure what arrives. In Shannon's framework, *noise* does not mean a lie, propaganda or meaningless speech. It refers to interference or uncertainty in the technical transmission.

*Channel capacity* expresses the highest reliable information rate under the specified channel model. For a discrete memoryless channel, its modern form is the maximum mutual information between the channel's input and output over permitted input distributions. Particular physical assumptions yield other, more specialized formulas.

Shannon's noisy-channel coding theorem establishes that, under its hypotheses, rates below capacity permit codes whose error probability can be made arbitrarily small with sufficiently long blocks. It does not promise zero error for a finite device, a cost-free solution or a single coding method. Above the relevant capacity, the same guarantee of arbitrarily reliable transmission at that rate is unavailable.

The striking result is a limit on what can be achieved, independent of the accidental design of one apparatus. Engineering must still find practical codes, latency, energy and complexity budgets within that boundary.

## Redundancy can be removed—and added

A predictable source contains statistical regularity. By exploiting it, a source code may represent information more economically. Lossless compression aims to reduce the expected number of symbols needed while permitting exact reconstruction. Entropy provides a fundamental benchmark under the stated assumptions.

A noisy channel poses a different problem. Here redundancy can be deliberately introduced so that corruption can be detected or sometimes corrected. A very simple demonstration repeats one binary symbol three times: transmit 111, receive 101 after a single flipped position, and recover 1 by majority vote. Such a toy code sacrifices transmission efficiency, corrects no more than one flip among those three symbols and has no special claim to optimality.

The same word, *redundancy*, thus names opposite engineering opportunities. Regularity in a source can be exploited to compress; additional structure in a channel code can protect. These are distinct operations, often used together.

## Compression, fidelity and what a reconstruction loses

Exact reconstruction is not always required. A voice recording or image can be represented using fewer resources when a specified amount of distortion is acceptable. Shannon's 1948 paper already considered fidelity criteria; later work developed the rate–distortion framework more systematically.

Lossless source coding, lossy coding and protection against channel errors answer three different questions. How compactly can a source be represented without changing it? What rate is possible when a specified difference is tolerable? How can a representation survive disturbances along the channel?

The definitions matter because a successful technical answer depends on what the system was asked to preserve. A faithful file transfer may still preserve a false assertion. A compressed image can remain intelligible while losing details that matter in another context.

## The meaning outside the calculation: Shannon and Weaver

Shannon explicitly bracketed semantic meaning from the engineering problem. This was a methodological decision, not a judgment that human meaning is unimportant.

In 1949, Warren Weaver introduced the volume *The Mathematical Theory of Communication*, which reprinted Shannon's work alongside Weaver's own discussion. Weaver distinguished technical accuracy, semantic interpretation and effectiveness: whether symbols arrive, what they mean and what consequences the received meaning has. The three-level formulation belongs to Weaver and should not be attributed to Shannon as an undivided joint invention.

The distinction is essential today. Recovering every character of a message cannot tell us whether its source is credible, whether the reader understands it or whether its claim deserves belief. Those questions require other forms of investigation.

## Secrecy, chess and automata

Shannon applied probabilistic reasoning to cryptography in *Communication Theory of Secrecy Systems* (1949), derived from earlier restricted wartime work. Perfect secrecy is a stringent condition: observing the ciphertext must reveal no information about which possible plaintext was sent, under the model. The one-time pad predates Shannon as a construction; his achievement was to formalize properties and requirements of secrecy.

His 1950 paper on computer chess treated a daunting search space as a problem of selection and tractable strategy. The electromechanical mouse Theseus explored and remembered a route through a maze. Such devices reveal a mind interested not merely in ideas, but in the mechanisms through which a structure becomes workable.

Shannon met Alan Turing during wartime work in 1943, but their achievements remain distinct: Turing's theory of computation and Shannon's treatment of switching, communication and coding are related without becoming one origin story. Shannon also joined the 1955 Dartmouth AI proposal and co-edited *Automata Studies* with John McCarthy in 1956. These are genuine historical connections, not proof that information theory is a complete theory of contemporary artificial intelligence.

## The Bandwagon: a scientist marks his own boundary

By the mid-1950s, information theory was attracting attention far beyond communications engineering. In *The Bandwagon* (1956), Shannon warned that the enthusiasm could encourage unsupported applications across unrelated fields. He did not forbid interdisciplinary inquiry; he asked that each application establish its own hypotheses and evidence.

The warning grows from the success of his own method. A formalism gains power by specifying what belongs to the problem. It loses precision when its vocabulary begins to stand for anything that sounds similar.

That caution also applies to the fashionable use of *entropy* as a synonym for chaos, *noise* as a synonym for misinformation and *information* as a synonym for knowledge. Such metaphors may have uses, but their conclusions do not follow from Shannon's theorems.

## The contemporary wound: transmission without understanding

An archive can store a document without corrupting a single character. A network can deliver an image in a moment. An automated system can generate a convincing answer. None of those achievements, on its own, establishes truth, judgment or understanding.

The problem is sharper than a general complaint about an excess of information. Technical performance at one level can be mistaken for success at another. When the symbols arrive, we may be tempted to believe that the matter has also been understood. Shannon helps identify the precise point at which that inference fails.

This is the last movement of the tenth triad. Lucretius asks what bodies are and how their effects reach perception; McLuhan examines how a medium reorganizes the human environment; Shannon measures the possibilities and limits of transmitting signals through a channel. The *simulacrum* is not a digital signal, McLuhan's *medium* is not Shannon's *channel*, and a bit is not an atom. Their distance is what makes the comparison productive.

We owe Shannon a rigorous account of the successful transmission. The decision about what the received message means remains ours.

## Primary texts and orientation

Primary works: Claude E. Shannon, *A Symbolic Analysis of Relay and Switching Circuits* (1938); *A Mathematical Theory of Communication*, *Bell System Technical Journal* 27 (1948), pp. 379–423 and 623–656; *Communication Theory of Secrecy Systems* (1949); *Programming a Computer for Playing Chess* (1950); *Prediction and Entropy of Printed English* (1951); *The Bandwagon* (1956); *Coding Theorems for a Discrete Source with a Fidelity Criterion* (1959). See also Warren Weaver's distinct introductory essay in *The Mathematical Theory of Communication* (1949).

For historical and technical orientation: Harry Nyquist and Ralph Hartley's 1928 work on communication; *Claude Elwood Shannon: Collected Papers*, edited by N. J. A. Sloane and Aaron D. Wyner; Thomas M. Cover and Joy A. Thomas, *Elements of Information Theory*; and biographical materials from the IEEE Information Theory Society and MIT. The critique of confusion between technical delivery and human comprehension, and the relation among the three authors, are original to Cerchi d'inchiostro. © Alessandro Gentili — Cerchi d'inchiostro. All rights reserved.
