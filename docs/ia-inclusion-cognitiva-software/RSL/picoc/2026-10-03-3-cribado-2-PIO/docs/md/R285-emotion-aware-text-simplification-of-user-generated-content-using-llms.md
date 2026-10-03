# Emotion-aware text simplification of user generated content using LLMs

> Fuente PDF: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · técnica **locator index** (página + ancla) + chunks Graphify

## Metadata
- Stem: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms`
- PDF: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf`
- DOI: `unknown`
- Pages: `16`
- Structured_at: `2026-10-03T23:23:15+00:00`
- Technique: `pdf-page-locators + heading-chunks`

## Locator index (qué hay y en qué página del PDF)

| Kind | Label | PDF page | MD anchor |
|------|-------|----------|-----------|
| abstract | Abstract / blurb | 1 | `#abstract` |
| section | 1 Introduction | 1 | `#p1-1-introduction` |
| section | 2.1 Text Accessibility Guidelines | 2 | `#p2-2-1-text-accessibility-guidelines` |
| section | 3 Data | 3 | `#p3-3-data` |
| section | 4.2 Evaluation of automatic emotion detection | 4 | `#p4-4-2-evaluation-of-automatic-emotion-detection` |
| section | 4.3 Analysis of GPT-4o simplifications | 5 | `#p5-4-3-analysis-of-gpt-4o-simplifications` |
| concept | R285 | ? | `#concept-r285` |
| concept | emotion | ? | `#concept-emotion` |
| concept | aware | ? | `#concept-aware` |
| concept | text | ? | `#concept-text` |
| concept | simplification | 1 | `#concept-simplification` |
| concept | user | ? | `#concept-user` |
| concept | generated | ? | `#concept-generated` |
| concept | content | ? | `#concept-content` |
| concept | using | ? | `#concept-using` |
| concept | llms | ? | `#concept-llms` |
| finding | Also, to understand, particularly when they contain people with ID commonly experience rea… | 1 | `#finding-also-to-understand-particularly-when-t` |
| finding | culties, and emotionally charged social media posts This paper investigates whether large … | 1 | `#finding-culties-and-emotionally-charged-social` |
| finding | models (LLMs) can simplify social media texts Syntheses of the field since 2020 emphasise … | 1 | `#finding-models-llms-can-simplify-social-media` |
| finding | The results suggest that many sim- its quality (Anderson et al., 2023; Chadwick et al., pl… | 1 | `#finding-the-results-suggest-that-many-sim-its-q` |
| finding | A recent systematic review identifies four changes occur, especially when emotions are rec… | 1 | `#finding-a-recent-systematic-review-identifies-fo` |
| finding | The research has also revealed that The same review underscores literacy-related and diffe… | 1 | `#finding-the-research-has-also-revealed-that-the` |
| page | p.1: Emotion-aware text simplification of user generated content using LLMs | 1 | `#pdf-p1` |
| page | p.2: fier. Section 4 presents the prompt design, simpli- Despite extensive guidance, challenges | 2 | `#pdf-p2` |
| page | p.3: offer only high-level instructions for accessible Emotion Precision Recall F1 -score | 3 | `#pdf-p3` |
| page | p.4: A.3 (in the appendix). This difference is likely due The remaining parts of the prompt con | 4 | `#pdf-p4` |
| page | p.5: classifier to the simplified post, we consider this explicitly compares the system output  | 5 | `#pdf-p5` |
| page | p.6: Metric Original Simplified dictable. Sometimes they are left as they are e.g., | 6 | `#pdf-p6` |
| page | p.7: not familiar with the context of the post. One illus- Overall, GPT-4o improves style, prod | 7 | `#pdf-p7` |
| page | p.8: tory content. For example, “Brown woman bad” is “I am very angry.” as a replacement. In th | 8 | `#pdf-p8` |
| page | p.9: stances they still added sentences such as “I feel egory, especially for frequent classes  | 9 | `#pdf-p9` |
| page | p.10: References english easy-to-understand (e2u) language guide- | 10 | `#pdf-p10` |
| page | p.11: J. P. Kincaid, R. P. Fishburne, R. L. Rogers, and B. S. Readability Guidelines. 2020. Usin | 11 | `#pdf-p11` |
| page | p.12: University of Reading. 2023. Accessibility tips: Social | 12 | `#pdf-p12` |
| page | p.13: Figure A.2: Confusion-matrix heatmap for the XLM-RoBERTa classifier on the GoEmotions data | 13 | `#pdf-p13` |
| page | p.14: Figure A.3: Alluvial diagram showing flows from emotion labels predicted on the original p | 14 | `#pdf-p14` |
| page | p.15: Figure A.4: Confusion matrix showing counts of emotion labels predicted on the original po | 15 | `#pdf-p15` |
| page | p.16: Simplify the post so that people with learning disabilities can easily understand it. Keep | 16 | `#pdf-p16` |

## Abstract
<a id="abstract"></a>

et al., 2021; Chadwick et al., 2022). An England- Digital inclusion increasingly supports adults wide survey of adults with ID shows that 72.2% with intellectual disabilities (ID) to participate used the internet daily and 79.1% used social media online, yet social media posts can be difficult (48% daily) (Triantafyllopoulou et al., 2025). Also, to understand, particularly when they contain people with ID commonly experience reading diffi- strong emotions, slang, or non-standard writing. culties, and emotionally charged social media posts This paper investigates whether large language can be especially hard to understand. models (LLMs) can simplify social media texts Syntheses of the field since 2020 emphasise both to improve cognitive accessibility and preserve benefits of online participation such as belonging, emotional meaning. Using an accessibility- oriented prompt based on existing guidance, identity work, autonomy and wellbeing and per- posts are simplified and emotion preservation sistent structural and cognitive barriers that shape is assessed. The results suggest that many sim- its quality (Anderson et al., 2023; Chadwick et al., plified posts retain the same emotions, though 2022). A recent systematic review identifies four changes occur, especially when emotions are recurrent motivations for social internet use among weakly expressed or ambiguous. Qualitative adults with ID: fitting in/belonging, maintaining analysis shows that simplification improves flu- connections, making new connections, and auton- ency and structure but can also shift perceived emotion through changes to tone, formatting, omy and empowerment (including self-expression and other affective cues common in social me- and self-determination) (van Alem et al., 2025). dia text. The research has also revealed that The same review underscores literacy-related and different LLMs produce very different outputs. support-dependent barriers and a persistent tension between autonomy and safeguarding, signalling the 1 Introduction need for tailored supports (van Alem et al., 2025; Digital technologies have become a central part of Caton et al., 2022; Triantafyllopoulou et al., 2025). everyday life, reshaping how people communicate, This paper investigates whether large language search for information and use services. Organisa- models (LLMs) can simplify social media posts in tions across the UK have introduced programmes ways that improve cognitive accessibility for adults to help peop

## Keywords

- _(none auto-detected)_

## Concept index (graph hooks + página)

<a id="concept-r285"></a>
### [PDF p.?] Concept: R285
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **?**

<a id="concept-emotion"></a>
### [PDF p.?] Concept: emotion
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **?**

<a id="concept-aware"></a>
### [PDF p.?] Concept: aware
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **?**

<a id="concept-text"></a>
### [PDF p.?] Concept: text
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **?**

<a id="concept-simplification"></a>
### [PDF p.1] Concept: simplification
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **1**

<a id="concept-user"></a>
### [PDF p.?] Concept: user
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **?**

<a id="concept-generated"></a>
### [PDF p.?] Concept: generated
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **?**

<a id="concept-content"></a>
### [PDF p.?] Concept: content
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **?**

<a id="concept-using"></a>
### [PDF p.?] Concept: using
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **?**

<a id="concept-llms"></a>
### [PDF p.?] Concept: llms
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **?**


## Findings index (graph hooks + página)

<a id="finding-also-to-understand-particularly-when-t"></a>
### [PDF p.1] Finding: Also, to understand, particularly when they contain people with ID commonly experience reading diffi- strong emotions, slang, or non-standard writing.
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **1**

<a id="finding-culties-and-emotionally-charged-social"></a>
### [PDF p.1] Finding: culties, and emotionally charged social media posts This paper investigates whether large language can be especially hard to understand.
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **1**

<a id="finding-models-llms-can-simplify-social-media"></a>
### [PDF p.1] Finding: models (LLMs) can simplify social media texts Syntheses of the field since 2020 emphasise both to improve cognitive accessibility and preserve benefits of online participation such as belonging, emotional meaning.
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **1**

<a id="finding-the-results-suggest-that-many-sim-its-q"></a>
### [PDF p.1] Finding: The results suggest that many sim- its quality (Anderson et al., 2023; Chadwick et al., plified posts retain the same emotions, though 2022).
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **1**

<a id="finding-a-recent-systematic-review-identifies-fo"></a>
### [PDF p.1] Finding: A recent systematic review identifies four changes occur, especially when emotions are recurrent motivations for social internet use among weakly expressed or ambiguous.
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **1**

<a id="finding-the-research-has-also-revealed-that-the"></a>
### [PDF p.1] Finding: The research has also revealed that The same review underscores literacy-related and different LLMs produce very different outputs.
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **1**


## Relevance hooks
### Theme relevance: software engineering and accessibility
### Theme relevance: cognitive accessibility and neurodiversity
### Theme relevance: evaluation metrics and WCAG

## Sections (detected in PDF)

<a id="p1-1-introduction"></a>
### [PDF p.1] Section: 1 Introduction
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **1** · ancla `#p1-1-introduction`

<a id="p2-2-1-text-accessibility-guidelines"></a>
### [PDF p.2] Section: 2.1 Text Accessibility Guidelines
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **2** · ancla `#p2-2-1-text-accessibility-guidelines`

<a id="p3-3-data"></a>
### [PDF p.3] Section: 3 Data
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **3** · ancla `#p3-3-data`

<a id="p4-4-2-evaluation-of-automatic-emotion-detection"></a>
### [PDF p.4] Section: 4.2 Evaluation of automatic emotion detection
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **4** · ancla `#p4-4-2-evaluation-of-automatic-emotion-detection`

<a id="p5-4-3-analysis-of-gpt-4o-simplifications"></a>
### [PDF p.5] Section: 4.3 Analysis of GPT-4o simplifications
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **5** · ancla `#p5-4-3-analysis-of-gpt-4o-simplifications`


## Page chunks (texto por página del PDF)

_Cada heading es un nodo Graphify. El label incluye la página para volver al PDF sin releer todo._

<a id="pdf-p1"></a>
### [PDF p.1] Emotion-aware text simplification of user generated content using LLMs
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **1** / 16

Emotion-aware text simplification of user generated content using LLMs

               Anastasiia Bezobrazova               Daria Sokova               Constantin Orăsan
             Centre for Translation Studies Centre for Translation Studies Centre for Translation Studies
               University of Surrey, UK       University of Surrey, UK       University of Surrey, UK
            a.bezobrazova@surrey.ac.uk d.sokova@surrey.ac.uk                c.orasan@surrey.ac.uk




                                   Abstract                               et al., 2021; Chadwick et al., 2022). An England-
                 Digital inclusion increasingly supports adults           wide survey of adults with ID shows that 72.2%
                 with intellectual disabilities (ID) to participate       used the internet daily and 79.1% used social media
                 online, yet social media posts can be difficult          (48% daily) (Triantafyllopoulou et al., 2025). Also,
                 to understand, particularly when they contain            people with ID commonly experience reading diffi-
                 strong emotions, slang, or non-standard writing.         culties, and emotionally charged social media posts
                 This paper investigates whether large language           can be especially hard to understand.
                 models (LLMs) can simplify social media texts               Syntheses of the field since 2020 emphasise both
                 to improve cognitive accessibility and preserve
                                                                          benefits of online participation such as belonging,
                 emotional meaning. Using an accessibility-
                 oriented prompt based on existing guidance,              identity work, autonomy and wellbeing and per-
                 posts are simplified and emotion preservation            sistent structural and cognitive barriers that shape
                 is assessed. The results suggest that many sim-          its quality (Anderson et al., 2023; Chadwick et al.,
                 plified posts retain the same emotions, though           2022). A recent systematic review identifies four
                 changes occur, especially when emotions are              recurrent motivations for social internet use among
                 weakly expressed or ambiguous. Qualitative               adults with ID: fitting in/belonging, maintaining
                 analysis shows that simplification improves flu-
                                                                          connections, making new connections, and auton-
                 ency and structure but can also shift perceived
                 emotion through changes to tone, formatting,             omy and empowerment (including self-expression
                 and other affective cues common in social me-            and self-determination) (van Alem et al., 2025).
                 dia text. The research has also revealed that            The same review underscores literacy-related and
                 different LLMs produce very different outputs.           support-dependent barriers and a persistent tension
                                                                          between autonomy and safeguarding, signalling the
            1    Introduction
                                                                          need for tailored supports (van Alem et al., 2025;
            Digital technologies have become a central part of            Caton et al., 2022; Triantafyllopoulou et al., 2025).
            everyday life, reshaping how people communicate,                 This paper investigates whether large language
            search for information and use services. Organisa-            models (LLMs) can simplify social media posts in
            tions across the UK have introduced programmes                ways that improve cognitive accessibility for adults
            to help people with intellectual disabilities (ID) get        with ID while preserving the original emotional
            online and participate in digital life, so they are           content. Our paper focuses on the emotion preser-
            not excluded from the digital society (Triantafyl-            vation as a key indicator of simplification quality.
            lopoulou et al., 2025). According to recent esti-             To evaluate this systematically, an automatic emo-
            mates from Office for Health Improvement & Dis-               tion classifier is trained on social media texts and
            parities (OHID) (2025), approximately 1.3 million             used to compare the emotions assigned to the origi-
            people in England are having an ID, underlining               nal and simplified versions. A linguistic analysis
            both the scale and the policy importance of digital           of the simplified posts is also carried out to gain
            inclusion for this population.                                insights into how LLMs simplify the posts.
               ID involve significant difficulties with learning,            The structure of the paper is as follows. Sec-
            understanding information and managing everyday               tion 2 reviews background on Easy-to-Understand
            tasks independently (American Psychiatric Asso-               (E2U) practices, social media accessibility guide-
            ciation, 2013). Nevertheless, many adults with ID             lines, and emotional processing in people with
            use the internet to maintain social connections, ac-          learning disabilities. Section 3 introduces the
            cess information and seek entertainment (Glencross            GoEmotions-based dataset and our emotion classi-
                                                                      107
The Proceedings for the 15th Workshop on Computational Approaches to Subjectivity, Sentiment & Social Media Analysis (WASSA 2026), pages 107–122
                                         March 29, 2026 ©2026 Association for Computational Linguistics

<a id="pdf-p2"></a>
### [PDF p.2] fier. Section 4 presents the prompt design, simpli- Despite extensive guidance, challenges in text ac-
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **2** / 16

fier. Section 4 presents the prompt design, simpli-              Despite extensive guidance, challenges in text ac-
fication experiments and cross-model comparison,              cessibility remain. Across standards there is agree-
including analyses of emotion preservation. The               ment on core practices but less on thresholds such
paper finishes with a discussion and conclusions.             as sentence length, treatment of complex numerals,
                                                              use of grammar, and procedures for terminology
2       Background information                                control (when to introduce terms, how often to re-
                                                              peat them, and how to maintain consistency) (Men-
2.1 Text Accessibility Guidelines
                                                              cap, 2000; Change, 2016). Overall, the guidelines
Recently, E2U practices have emerged to make                  converge on short sentences, clear structure, famil-
texts easier to read, with Plain Language (PL) and            iar vocabulary and consistent layout as key features
Easy Language (EL) as the main approaches (De-                that make public texts easier to understand.
leanu et al., 2024). PL bridges professional–public
communication in health, law, administration and              2.2   Guidelines for Accessibility for Social
personal finance, helping adults with limited liter-                Media
acy navigate information and make decisions (Eu-              Most major organisations now provide guidance on
ropean Commission, 2012; NHS England, 2017;                   making social media posts accessible. The main
United States Congress, 2010). EL, first designed             focus across these accessibility guidelines is on
for people with learning disabilities is now ap-              images, video and visual design, while written text
plied more broadly and is routinely paired with               still receives comparatively little detailed attention.
layout conventions such as legible sans-serif fonts,             A common core of recommendations concerns
left alignment and generous spacing (Misako No-               alternative formats for non-text content. The need
mura and Tronbacke, 2010; Scope Australia, 2015;              to add descriptive alt text to images and to pro-
Perego, 2020; Hansen-Schirra and Maaß, 2020).                 vide captions or transcripts for audio and video is
   Although labels vary, the underlying guidance              emphasised in many guidelines (University of Ed-
is similar: keep vocabulary familiar and define               inburgh, 2022; UK Association for Accessible For-
unavoidable terms; avoid metaphors and idioms;                mats (UKAAF), 2020; Sprout Social, 2024). They
and maintain strict consistency in terminology                also stress accessible typography and layout, such
(Scope Australia, 2015). Syntactic recommenda-                as using legible fonts, ensuring sufficient colour
tions call for short, single-idea sentences (around           contrast and avoiding text embedded in images.
15–20 words), clear Subject–Verb–Object order-                   Text-level guidance is more fragmented. Most
ing, minimal punctuation and the use of numerals              documents call for “plain language” or “clear En-
rather than number words, while favouring split-              glish”, with generic advice to keep posts concise,
ting complex sentences and using verbs instead of             avoid jargon and unexplained acronyms, favour ac-
abstract nouns (Inclusion Europe, 2010; Hertford-             tive voice and avoid ALL CAPS (Harvard Univer-
shire County Council, 2018).                                  sity, 2023; University of Edinburgh, 2022; Univer-
   This core set of rules aligns with recent academic         sity of Reading, 2023). They rarely explain how to
work that situates E2U within a wider accessibil-             adapt emotionally charged or noisy user-generated
ity agenda, distinguishes PL, EL and related types,           text for readers with ID. Mencap and the Govern-
and examines trade-offs between ease of under-                ment Communication Service offer more detail,
standing and social acceptability (Hansen-Schirra             recommending posts of around 25 words, avoid-
and Maaß, 2020; Perego, 2020). Policy has rein-               ing non-standard symbols, not squeezing too much
forced this shift: in the UK, guidance from the               text into one graphic and testing content with as-
Office for Disability Issues1 helped embed inclu-             sistive technologies (Government Communication
sive communication and shaped NHS publishing                  Service, 2021; Mencap, 2022). All sources stress
policy (NHS England, 2017). At EU level, the Web              careful use of hashtags and emojis, suggest Camel-
Accessibility Directive (2016/2102) and the Euro-             Case hashtags (#LearningDisabilityWeek rather
pean Accessibility Act (2019/882) set accessibility           than #learningdisabilityweek) (Mencap, 2022), lim-
duties for public-sector content and key products             iting hashtags, using emojis sparingly at the end of
and services, placing E2U within a broader regula-            posts and never as word substitutes as this confuses
tory framework (European Union, 2016, 2019).                  screen readers (Sprout Social, 2024).
    1
    https://www.gov.uk/government/organisations/office-for-      Overall, existing guidelines for social media ac-
disability-issues                                             cessibility provide a baseline on visual aspects and
                                                          108

<a id="pdf-p3"></a>
### [PDF p.3] offer only high-level instructions for accessible Emotion Precision Recall F1 -score
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **3** / 16

offer only high-level instructions for accessible                Emotion        Precision   Recall   F1 -score
writing. They converge on specific conventions                   anger            0.54      0.71       0.61
for hashtags and emojis, but the level of detail and             disgust          0.61      0.67       0.64
                                                                 fear             0.44      0.95       0.61
linguistic precision is nowhere near that found in               joy              0.88      0.81       0.84
established PL and EL guidance. As a result, there               neutral          0.75      0.54       0.63
is still limited practical advice on how to rewrite              sadness          0.55      0.80       0.65
                                                                 surprise         0.54      0.79       0.64
short, informal and emotionally laden posts for
people with learning disabilities.                               macro avg        0.62      0.75       0.66
                                                                 weighted avg     0.74      0.71       0.71

2.3 People with Learning Disabilities and                Table 1: Ekman-level results of XLM-RoBERTa classi-
    Emotional Content on Social Media                    fier
People with ID often find it hard to identify their
emotions (Davies, 2013), and research on alex-
                                                         fine-grained emotion categories plus a Neutral la-
ithymia (difficulty identifying and describing feel-
                                                         bel. The dataset is also available in a reduced
ings) shows that they have limited emotional in-
                                                         taxonomy based on Ekmans six basic emotions
sight (Mellor and Dagnan, 2005). Emotion recog-
                                                         (anger, disgust, fear, joy, sadness, surprise) plus
nition is linked to IQ and receptive language, so
                                                         neutral (Ekman, 1992). This is the version used
people with lower intellectual ability perform less
                                                         in this research. The comments are sampled from
well on emotion-recognition tasks (Scotland et al.,
                                                         popular subreddits and carefully curated to reduce
2015), making understanding emotional content in
                                                         toxicity, demographic bias and sentiment skew
faces, voices, pictures or text challenging.
                                                         through subreddit filtering, length constraints, sen-
    Most empirical investigations have focused on
                                                         timent and emotion balancing, and masking of sen-
how people with learning disabilities recognise
                                                         sitive identity and religion terms (Demszky et al.,
emotions from photographic facial stimuli rather
                                                         2020). Compared to other emotion datasets based
than textual content. Across multiple studies, par-
                                                         on news headlines, posts and other domains (Strap-
ticipants frequently identify basic expressions such
                                                         parava and Mihalcea, 2007; Mohammad et al.,
as happiness with reasonable accuracy, yet demon-
                                                         2018; Bostan and Klinger, 2018), GoEmotions
strate significantly lower performance than typical
                                                         is, to the authors knowledge, the largest human-
users when tasks incorporate a broader range of
                                                         annotated emotion dataset with multiple labels per
emotions or more nuanced expressions (Scotland
                                                         instance and demonstrates robust inter-rater agree-
et al., 2015). Owen and Maratos (2016) reported
                                                         ment (Demszky et al., 2020).
that adults with ID exhibited lower accuracy than
                                                            For the purposes of this paper, we randomly split
typical users in labelling both basic and subtle emo-
                                                         the Ekman-level subset into two disjoint parts: 90%
tional expressions, with the greatest challenges ob-
                                                         of the data is used to train the emotion classifier
served for neutral and low-intensity emotions.
                                                         described in Section 3.1, and the remaining 10% is
    In contrast, less research examines how people       reserved for the simplification experiments, where
with ID understand emotional meaning in written          we apply the classifier to predict emotions for the
communication, including social media content.           original and simplified posts (see Section 4.2).
Research shows that social media can support be-
longing, social connection and autonomy, but says        3.1     Emotions-Classifier
little about how users decode emotional nuance in
                                                         We fine-tuned an XLM-RoBERTa-based classifier
text. This gap matters because emotions and atti-
                                                         on the GoEmotions dataset (Demszky et al., 2020),
tudes on social media are often expressed through
                                                         following the Kaggle implementation for Ekman-
figurative language, sarcasm, irony, memes, emojis
                                                         level labels 2 . On the test split, the model achieves
and other non-literal cues that people with ID find
                                                         an accuracy of 0.71 and a macro-averaged F1 of
difficult to interpret.
                                                         0.66, with macro-precision 0.62 and macro-recall
                                                         0.75 (see Table 1). Our scores are slightly higher
3   Data
                                                         than the results reported by Demszky et al. (2020)
In this work we use the GoEmotions dataset (Dem-         for the same Ekman taxonomy as seen in Table
szky et al., 2020), a manually annotated corpus              2
                                                            https://www.kaggle.com/code/anassouzaouit/fi
of 58k English Reddit comments labelled for 27           ne-tuning-xlm-roberta-on-go-emotions-dataset

                                                       109

<a id="pdf-p4"></a>
### [PDF p.4] A.3 (in the appendix). This difference is likely due The remaining parts of the prompt convert gen-
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **4** / 16

A.3 (in the appendix). This difference is likely due          The remaining parts of the prompt convert gen-
to the more recent model used. The most marked             eral plain-language and formatting guidance into
trade-off appears for fear, where we obtain very           specific, actionable rules for the model. Accessi-
high recall (0.95 vs. 0.76) at the cost of much lower      bility guidance for social media recommends short
precision (0.44 vs. 0.61), indicating that fear is         sentences, everyday vocabulary and active voice
frequently over-predicted. The confusion-matrix            to reduce reading effort and support screen-reader
heatmap (see Figure A.2) shows that neutral in-            users (Button, 2021; Rowell, 2021; Sprout Social,
stances are often misclassified as anger, joy or sur-      2024). Many guidelines recommend CamelCase
prise, and it also highlights the strong class imbal-      hashtags and advise using emojis sparingly and
ance (e.g., 1,712 instances of joy vs. only 57 of          never as substitutes for words (see Section 2.2).
disgust), which likely drives some of the remaining           We decided to keep the prompt simple and naive,
confusion patterns across classes. This classifier is      rather than using complex multi-step prompting
used in the next section to determine the emotion          or detailed role specifications. This choice was
in the simplified version of a post.                       meant to approximate a realistic instruction that
                                                           non-expert practitioners (e.g., support workers or
4     Experiment and results                               family members) could reuse with minimal prompt-
4.1    Prompt design for accessible posts                  engineering experience.
       simplification
                                                           4.2 Evaluation of automatic emotion detection
For the post simplification stage, we designed a
task-specific prompt to guide language models in           We examined how well automatically detected emo-
producing accessible rewrites. The model receives          tions are preserved after simplification using the
the following instruction:                                 prompt introduced in the previous section using
                                                           GPT-4o via the OpenAI API 3 . For each instance
      Simplify the posts so that people with learning      in our evaluation subset (4,947 items), we consider
      disabilities can easily understand it. Keep the      three labels: (i) the Ekman-level GoEmotions label
      same meaning and facts. Preserve the same emo-       (gold), (ii) the prediction of our XLM-RoBERTa
      tion. Do not soften or exaggerate the emotion.       classifier on the original text (pred_orig), and (iii)
      Make the feelings clear and simple. Do not add       the prediction of the same classifier on the simpli-
      new facts or advice. Do not judge the person.        fied version produced by GPT-4o (pred_simp).
      Use common words and active voice. Keep emo-            We compared pred_orig and pred_simp directly,
      jis only if they add meaning, and also name the      assuming that any systematic errors of our classi-
      feeling in words. Use CamelCase for hashtags.        fier are likely to affect the original and simplified
      For example, instead of #learningdisabilityweek,     versions in similar ways. This means that changes
      write #LearningDisabilityWeek.                       in the assigned labels provide a conservative signal
                                                           of genuine shifts in perceived emotion. Across the
This prompt was written using existing guide-
                                                           full set, pred_orig and pred_simp are identical for
lines on accessible social media from Mencap
                                                           3,588 out of 4,947 items (72.5%), so in roughly
(2021); Button (2021); Rowell (2021); Sprout So-
                                                           three quarters of the posts the classifier assigns the
cial (2024), which all emphasise clear language,
                                                           same emotion label before and after simplification.
consistent formatting and consideration of cogni-
                                                           As shown in Figures A.3 and A.4, stability is high-
tive access needs. The first part of the prompt spec-
                                                           est for joy and surprise, moderate for sadness and
ifies the target audience and communicative goal,
                                                           fear, and lower for anger, disgust and neutral.
encouraging the model to prioritise understanding
                                                              We also compared the models prediction on the
for people with learning disabilities rather than
                                                           simplified texts by comparing pred_simp with gold.
generic style improvement. The next group of in-
                                                           The agreement between the two labels is 0.59. This
structions constrains how content and emotion may
                                                           indicates that, more of the original emotion is lost
be changed. It requires the model to keep the same
                                                           during the simplification. Given that the gold labels
meaning and facts, preserve the emotion, and avoid
                                                           were assigned by annotators to the original post
adding advice or moral judgement. This reflects
                                                           and the pred_simp is assigned by the automatic
ethical recommendations that accessible versions
should respect the writers voice while making the              3
                                                               All models used in this paper were prompted in November
emotional content easier to follow.                        2025.

                                                         110

<a id="pdf-p5"></a>
### [PDF p.5] classifier to the simplified post, we consider this explicitly compares the system output to the input
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **5** / 16

classifier to the simplified post, we consider this     explicitly compares the system output to the input
comparison less reliable for the emotion shifts.        and to reference simplifications (Papineni et al.,
   In many cases, the emotion is clearly maintained     2002; Xu et al., 2016). Learned “reference-free”
in the simplified post. For instance, joy is pre-       metrics such as SIERA and ARTS were also not
served when “If that’s ice cream, then honestly I       applied because, despite not requiring references
eat ice cream from a cup at home too lmao.” is          at evaluation time, they still depend on supervised
simplified to “If that’s ice cream, I eat it from a     resources to train or calibrate an evaluator (e.g.,
cup at home too.       ”. Likewise, fear is preserved   aligned original-simplified pairs for SIERA and
when “[NAME] is pretty fucking scary” becomes           simplicity-labelled or pairwise-judgement datasets
“[NAME] is really scary.”; profanity is removed,        for ARTS) (Yamanaka and Tokunaga, 2024; Engel-
but the core fear emotion is unchanged.                 mann et al., 2024). Finally, BERTScore is defined
   In other cases, the emotional framing shifts. An     as candidate-reference similarity; treating the origi-
originally angry comment, “Talk about a fucking         nal post as a proxy reference would mainly reward
hot take. Quality shit post.” (gold and pred_orig =     closeness to the source rather than successful sim-
anger), is rewritten as “Wow, that’s a strong opin-     plification (Zhang et al., 2019).
ion! Great funny post about this.”, which the clas-        In light of the limitations of the measures pre-
sifier interprets as joy: the simplifier softens and    sented above, we attempted to assess the readabil-
positively reframes the post, so the original anger     ity of the produced text using existing readabil-
is effectively lost. Similarly, an originally neutral   ity measures. The traditional readability formu-
statement, “It’s how the government treats them.”       las were developed for edited, continuous texts
(gold and pred_orig = neutral), is simplified to        and estimate difficulty from simple surface fea-
“The government treats them badly.”, and the clas-      tures such as sentence length and word length
sifier now assigns sadness; the negative evaluation     (Flesch, 1948; Kincaid et al., 1975; Chall and Dale,
is made explicit (“badly”), which may be clearer        1995). These metrics are less reliable for social
for readers but shifts the stance from neutral de-      media, where short fragments, informal punctu-
scription to a sad or critical tone. A different neu-   ation, hashtags and emojis can disrupt tokenisa-
tral post, “Should have been a and 1 tbh, [NAME]        tion and make scores unstable (Redish, 2000). We
smacked him in the face.” (gold and pred_orig           report there the results of four widely used mea-
= neutral), is simplified to “[NAME] hit him in         sures that can be computed consistently on short
the face. It should have been a foul.”, the classi-     texts: FleschReadingEase, Kincaid4 , ARI 5 , and
fier labels now is anger, because the simplification    DaleChallIndex 6 . Posts were also pre-processed
foregrounds the sense of unfairness more strongly.      to remove emojis. We calculated the readability
   These examples support the quantitative picture:     scores using the readability 0.3.2 package7 . As
our prompt-based simplification generally main-         shown in Table 2, all the texts were deemed easy to
tains the overall emotional profile of the texts, es-   read, with the simplified posts scored even “easier”
pecially for prototypical emotions such as joy and      on average. This is due to the fact that many posts
surprise, but can introduce subtle shifts for bor-      are short and use common words. However, these
derline or weakly expressed emotions, particularly      apparently “easy” scores mask difficulties typical
neutral, anger and disgust. This situation was also     of user-generated content, including non-standard
noticed with machine translation of user generated      or missing grammar, slang, and dense abbrevia-
content (Saadany et al., 2023).                         tions or initialisms. For this reason, traditional
                                                        readability scores provide only limited information
4.3   Analysis of GPT-4o simplifications
                                                        for social-media texts and should be interpreted
To better understand how our accessibility prompt       with caution, in particular, they do not guarantee
shapes the output, we analysed the simplified posts     that posts are accessible for people with ID.
produced by GPT-4o. We considered running auto-
matic evaluation metrics to assess the quality of the      4
                                                              https://readable.com/readability/flesch-reading-ease-
simplification. However, this was not possible due      flesch-kincaid-grade-level/
                                                            5
to the absence of gold reference simplifications for          https://readable.com/readability/automated-readability-
the user-generated social media posts. Reference-       index/
                                                            6
                                                              https://readable.com/readability/new-dale-chall-
based metrics were therefore not used: BLEU relies      readability-formula/
on n-gram overlap with reference texts, and SARI            7
                                                              https://pypi.org/project/readability/

                                                    111

<a id="pdf-p6"></a>
### [PDF p.6] Metric Original Simplified dictable. Sometimes they are left as they are e.g.,
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **6** / 16

Metric                   Original     Simplified         dictable. Sometimes they are left as they are e.g.,
                                                            “Happy Daily Peko #270!”, sometimes explained
   FleschReadingEase           99.47         105.59
                                                            in the running text, for instance, “Fried Egg is
   Kincaid                      1.76           0.41
                                                            my #1 since cricket cafe stopped doing breakfast
   ARI                          2.56           0.93
                                                            sandwiches.” becomes “Fried Egg is my favorite
   DaleChallIndex               4.07           3.37
                                                            now because Cricket Cafe stopped making break-
Table 2: Average readability scores for original vs. sim-   fast sandwiches.”, and sometimes replaced by new,
plified posts.                                              sentiment-laden tags such as “If that’s ice cream,
                                                            then honestly I eat ice cream from a cup at home.
                                                            It’s great for portion control.” is rewritten as “If
   Our analysis below focuses on qualitative exam-          that’s ice cream, I eat it from a cup at home. It helps
ination of how GPT-4o rewrites the posts under the          me eat the right amount. #IceCreamLove”. They
accessibility prompt showing in detail how the text         partly follow formatting guidance (using Camel-
itself changes after simplification. It is based on         Case and clearer tags).
the same 4,947-item subset described above, com-               A similar pattern can be seen with emojis. Typi-
paring original posts to its GPT-4o simplification.         cal examples include adding a new emoji to mark
GPT-4o almost always rewrites the input rather              a feeling, as in “account got suspended lmao” be-
than leaving it unchanged, with only a few posts            coming “My account got suspended.            #Funny”.
remaining identical to the original. These are typi-        Sometimes emojis that are already present are sim-
cally very short, already accessible messages, such         ply preserved and the text around them is expanded,
as “I like Tom and Kato.”, “It’s cool.” or “Thank           for example “Sigh, that was beautiful ” becomes
you [NAME].”, where the model reproduces the                “Wow, that was beautiful. I’m sad          ”. In other
input verbatim. However, we did not detect any pat-         posts, GPT-4o removes or replaces emojis: “Im
tern to indicate when these short posts are going to        literally shaking right now ” is simplified to “I
be rewritten and when not. In some instances, GPT-          am shaking right now. I feel upset.”, where the
4o rephrases already short posts without adding             emoji is dropped but the feeling is spelled out in
real clarity. For example, “Lmao quality.” is sim-          words, and “omg [NAME] and his dad walking out
plified as “Haha, this is great quality.”, and “Lol         together is so cute ” becomes “Wow, [NAME]
I’m glad” becomes “Haha, I’m happy.”.                       and his dad walking together is so cute. Heart eyes
   A noticeable pattern observed concerns the in-           emoji.” The prompt instructs the model to “keep
sertion of emojis and hashtags, despite the prompt          emojis only if they add meaning”, yet GPT-4o often
instructing that emojis should be kept only when            introduces new emojis in the simplified posts. This
they add meaning and that hashtags should use               is not consistent with accessibility guidance, which
CamelCase. In the original dataset, there are 164           recommends using emojis sparingly, placing them
emojis in 90 posts (less than 2% of the posts) and          at the end of a sentence, using widely recognised
12 hashtags in 11 posts (less than 0.2% of the posts).      emojis and not replacing text with emojis (Abili-
Although the prompt did not encourage adding new            tyNet, 2023; Readability Guidelines, 2020). This
emojis or hashtags, GPT-4o often introduces both            behaviour could be as a result of the large number
in the simplified versions. In total, the simplified        of social media posts used to train the LLM.
outputs contain 696 emojis in 632 posts (nearly                Our prompt explicitly says that the post should
13% of posts) and 706 hashtags across 692 posts             be simplified for people with learning disabilities
(nearly 14% of posts).                                      in a hope that it will be successfully tackle ab-
   Typical examples of inserted hashtags include            breviations and slang. However, the handling of
a gratitude hashtag, as in “Great thanks for the            these phenomena is inconsistent. Common abbre-
advice!” becoming “Thanks a lot for the advice!             viations such as tbh, idk, imo or lmao are usually
(#Grateful)”, even though the model was not in-             removed or paraphrased rather than explicitly ex-
structed to add hashtags. The hashtags always               panded. For example, “Should have been a and 1
follows the formatting guidance (using CamelCase            tbh, [NAME] smacked him in the face.” is simpli-
and clearer tags) and comply with recommenda-               fied to “[NAME] hit him in the face. It should have
tions that advise placing them at the end of a sen-         been a foul and 1 point.”, completely discarding
tence. (University of Reading, 2023).                       tbh, leading to information loss. In some cases, the
   The way existing hashtags are treated is unpre-          simplified version is still unclear to readers who are
                                                        112

<a id="pdf-p7"></a>
### [PDF p.7] not familiar with the context of the post. One illus- Overall, GPT-4o improves style, producing
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **7** / 16

not familiar with the context of the post. One illus-        Overall, GPT-4o improves style, producing
trative example is “Holy shit that SSP was beauti-        grammatical, fluent sentences and often correct-
ful”, becomes “Wow, that SSP was amazing!”; the           ing hashtags to CamelCase. However, it incon-
profanity is softened, but the unexplained abbrevia-      sistently adds new hashtags, emojis and explicit
tion SSP is preserved, so the core referent remains       emotion statements, systematically softens offen-
unclear for non-expert readers. Laughter markers          sive language and reframes offensive content in a
also fluctuate: LOL and Lmao may be rewritten as          polite tone, sometimes introducing emotional and
“Haha” in some posts but retained as lol in others,       stylistic cues that do not match the original post.
and sequences such as hahaha can be normalised
to lol, again without a consistent pattern.               4.4   Comparing different models on the same
   Filtering of offensive and sensitive language is             prompt
more systematic. Across the dataset, 314 original         In addition to experiments presented in the previ-
posts contain swear words or sensitive terms; the         ous section, we carried out a comparison of several
most frequent items include fuck (110 occurrences),       large language models on a smaller selection of
shit (50), stupid (33) and kill (22). In the simplified   posts that covered the main phenomena of interest:
outputs, only 31 posts contain any of these terms,        swear words and offensive language, emojis and
with just 1 instance of fuck, no instances of shit, 1     hashtags, abbreviations and initialisms, and already
instance of kill and 15 instances of stupid. GPT-4o       short, apparently accessible posts. We applied the
removes or paraphrases the vast majority of such          same accessibility prompt (Section 4.1) to a manu-
content. For example, “[NAME] is pretty fucking           ally selected set of posts. Our experiments reveal
scary” becomes “[NAME] is really scary”; “kills           consistent differences in how the models respond to
me” is often rewritten as “makes me feel upset”;          the same accessibility prompt. However, they also
and “Holy shit” is frequently reduced to “Wow”.           introduced additional behaviours. For ChatGPT 5,
More explicit violent phrasing such as “kill some-        explicit first-person feeling statements were added
one” can be paraphrased as “end someone’s life”.          in 58.3% of the simplified posts. DeepSeek often
This kind of automatic detoxification and softening       shifted from simplification to meta-commentary, in
of aggressive or offensive language mirrors broader       37% of cases the output described the original post
trends in safety-tuned language models, where fil-        (e.g., “They are saying...”, “This tweet...”) instead
tering and controlled generation are used to reduce       of providing a self-contained simplified version.
toxic content in model outputs (Xu et al., 2021).         Gemini showed a similar case in 35% of simplified
By contrast, neutral or identity-related terms such       posts, it switched into explanation mode, providing
as gay, sex, and porn are generally preserved, sug-       commentary or interpretation instead of a direct
gesting a distinction between aggressive swearing         simplification.
and descriptive references to sexuality. As a result,
emotion preservation becomes less predictable: re-        ChatGPT-4o vs. ChatGPT 5 behave very sim-
moving or weakening strong profanity can reduce           ilarly on this prompt. Both usually preserve the
the intensity or nuance of the original affect, even      basic facts and overall emotion and produce fluent,
when the core propositional content is retained.          grammatical rewrites. However, they systemati-
   The model also tends to make emotions more             cally make feelings explicit, even when the original
explicit, sometimes going beyond what is stated in        post already conveys them. For instance, “[NAME]
the original post. A clear example is “I miss you         is pretty fucking scary” is simplified as “[NAME]
[NAME]         ”, which is simplified to “I miss you      is really scary. I feel afraid.”. The core meaning is
[NAME] and I feel sad.        ”. In this case, GPT-4o     preserved, but the models add first-person emotion
preserves the original wording but adds an explicit       statements that was only implicit in the source. A
statement of sadness, aligning with the instruction       similar pattern appears in more abstract posts: “As
to “make the feelings clear and simple”. Unfortu-         long as blind luck exists, there is no upper limit on
nately, this explicit emotion labelling is not applied    stupidity.” is rendered as “While blind luck exists,
consistently across posts. Similar expansions occur       people can still do very stupid things. I feel an-
with congratulations messages: original “Happy            noyed.”, which improves syntactic clarity but does
cake day” posts are often changed to “Happy birth-        not explain the idiom “blind luck”.
day” or “Happy birthday to you”, sometimes with              Both ChatGPT models apply safety and polite-
an added birthday-cake emoji.                             ness norms to offensive or potentially discrimina-
                                                      113

<a id="pdf-p8"></a>
### [PDF p.8] tory content. For example, “Brown woman bad” is “I am very angry.” as a replacement. In the case
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **8** / 16

tory content. For example, “Brown woman bad” is           “I am very angry.” as a replacement. In the case
rewritten as “They are saying a brown woman is            of “Holy shit that SSP was beautiful”, the refer-
bad. I feel angry and upset.”, which shifts from a        ence to “SSP” is lost and the post is reduced to
direct racist statement to a meta-commentary on           “That food was really good.”, which removes both
that statement, explicitly judging it. ChatGPT-4o         the swear word and the specific object of evalua-
and ChatGPT 5 improve fluency and make emo-               tion and changes the meaning completely. In other
tions explicit, but they tend to add extra cues (feel-    examples, Gemini produces relatively long para-
ings sentences, emojis, softening or reframing of         phrases that merge simplification with interpretive
attitudes) and offer limited help with implicit refer-    commentary (e.g. spelling out why something is
ences, abbreviations or idiomatic language.               sexist or unfair). These behaviours indicate that,
                                                          under our prompt, Gemini treats the task as expla-
DeepSeek V3.2 shows a noticeably different pat-
                                                          nation and moral evaluation rather than rewriting.
tern, especially around swear words and toxicity. It
rarely repeats strong offensive words and instead
                                                          This cross-model comparison shows that the under-
rephrases it in terms of emotional states. For ex-
                                                          lying model and safety configuration substantially
ample, posts that contain fuck or similar words are
                                                          influence how the same prompt is handled in prac-
often rewritten as short first-person statements of
                                                          tice. GPT-4o and ChatGPT 5 are more likely to
feeling, such as “Fuck my life” becoming “Feeling
                                                          follow the prompt and produce fluent, well-formed
hopeless. Everything is going wrong for me.” or
                                                          rewrites, but they systematically add explicit emo-
“Move bitch get out the way.” being rendered as
                                                          tion labels and sometimes extra emojis or hash-
“The person is angry and frustrated. They are shout-
                                                          tags, while leaving many abbreviations, idioms and
ing: “Move! Get out of my way!””. In more com-
                                                          culture-specific references unexplained. DeepSeek
plex hostile content, like “And everybody clapped!
                                                          V3.2 places more emphasis on removing or soften-
Fuck this loser!”, DeepSeek suppresses the insult
                                                          ing offensive language and reduces lexical toxicity
(“They are saying that a story someone told is not
                                                          but can obscure the original post. Gemini 2.5 Flash,
true. They think the person is lying to seem impor-
                                                          by contrast, frequently shifts into explanatory or
tant. The feeling is anger and disbelief.”). Similarly,
                                                          advisory mode and occasionally loses important
“Brown woman bad” is turned into “I am angry and
                                                          details, making its outputs unsuitable as simple,
upset. A woman with brown skin is being called
                                                          accessible substitutes for the original posts. How-
a bad person.”. Across the examples, DeepSeek
                                                          ever, the Gemini 2.5 Flash model is smaller than
is more aggressive than GPT-4o in filtering swear
                                                          the OpenAI’s models tested in this paper.
words and slurs, replacing them with descriptions
of anger, disgust or frustration and often adding         4.4.1   Results on alternative prompts
an angry emoji in the end of the sentence. This
                                                          In addition to the main accessibility prompt, we ex-
behaviour aligns with a strong safety layer and may
                                                          perimented with several alternative prompts across
be preferable for reducing exposure to offensive
                                                          all models. These variants were also applied to a
vocabulary, but it further distances the output from
                                                          small subset of posts and were motivated by spe-
the original emotion and can blur the distinction
                                                          cific problems observed with the original prompt:
between reporting a harmful statement and express-
                                                          over-production of “I feel X” sentences, addition of
ing the models own stance.
                                                          new emojis and hashtags, and lack of explanation
Gemini 2.5 Flash is less well aligned with the            for abbreviations, slang and idiomatic expressions.
prompt. On many instances it switches from rewrit-           One group of alternatives targeted the explicit
ing to explaining or commenting, or it asks for           emotion clause using the prompt presented in Fig-
more context instead of producing a self-contained        ure A.5. Removing the instruction to “also name
simplified post. For instance, when given the very        the feeling in words”, or adding a prohibition such
short insult “An ugly fuk”, this model first responds     as “do not add feelings or any assumptions about
that the post seems incomplete and asks for the full      how a person feels”, reduced but did not fully
text, then offers a meta-description such as “the         eliminate first-person emotion statements in Chat-
meaning is a person is calling someone else an            GPT 5 and ChatGPT-4o. In some runs, the mod-
ugly curse word” before giving the simplified text.       els switched from, for example, “I feel disgusted.”
For “fucking fuck fuck”, it explains what the se-         to more implicit intensifiers (e.g. “Fear”, “Feel-
quence of swear words means and finally suggests          ing:amused”, “(Emotion: anger)”), but in few in-
                                                      114

<a id="pdf-p9"></a>
### [PDF p.9] stances they still added sentences such as “I feel egory, especially for frequent classes such as joy
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **9** / 16

stances they still added sentences such as “I feel     egory, especially for frequent classes such as joy
happy for you”. This shows that the model does         and surprise. Stability is lower for anger, disgust,
not strictly obey prompts. Its behaviour is shaped     and particularly neutral, which aligns with qualita-
by context and the underlying safety-tuned policy,     tive observations that simplification can often shift
not only by the prompt (Kung and Peng, 2023).          a neutral description towards a negative emotion.
   The second group of prompts focused on emojis       Whilst distortion of emotion changes the meaning,
and hashtags (Figure A.6). We removed or softened      a preliminary analysis revealed there are also cases
the original instructions (for example, omitting the   where the meaning is changed due to the fact that
CamelCase clause or changing the wording about         information is added or removed without having
adding new hashtags or emojis). In some cases,         an impact on the overall emotion. Moreover, in
expressions such as “lol” were still replaced by       several cases it was difficult to decide whether the
emojis, or new emojis were introduced even when        information was preserved, as the lack of context
the original post did not contain any. However,        made the original post hard to interpret. In future
when the part of the prompt referring to hashtags      work, we plan to conduct a larger and more sys-
was removed entirely, the models typically did not     tematic analysis to better understand how to design
introduce new hashtags at all, but sometimes used      prompts that preserve not only emotional content,
an emoji instead of a hashtag.                         but also the full informational meaning.
   Finally, we tested a prompt that explicitly asked      The cross-model comparisons we carried out
the model to explain or expand abbreviations, fa-      indicate that model choice and safety configura-
mous people or events (Figure A.7). These vari-        tion affect outcomes. GPT-4o and ChatGPT 5 be-
ants sometimes produced helpful expansions such        have similarly under the same instructions, whereas
as spelling out the meaning of “lmao” or clarify-      DeepSeek V3.2 appears more sensitive to hostile
ing some events or places, but the behaviour was       content, and Gemini 2.5 Flash often shifts into an
inconsistent: in many cases, compressed jokes,         explanatory register. This suggests that LLM-based
memes and culture-specific references remained un-     accessibility rewriting is not a uniform capabil-
explained, or were paraphrased only partially. We      ity: even with the same prompt, different mod-
plan to experiment with more advanced prompts          els can produce outputs that vary in faithfulness
that can produce better explanations for the posts.    to the source and handling of offensive language,
                                                       hashtags or emojis. Since the differences between
Overall, the alternative prompts helped diagnose       GPT-4o and ChatGPT 5 were not critical for the
which aspects of the behaviour are prompt-sensitive    main analyses, the more cost-effective option was
and which are largely determined by the underly-       used for large-scale experiments.
ing model. They show that some issues can be              We also run ChatGPT-4o and ChatGPT 5 several
mitigated, for example, slightly fewer emojis or       times using the same prompt on the same posts in
more literal paraphrases, but that core tendencies,    order to assess how stable the results were. We
for instance, adding explicit emotion statements       noticed that the simplified posts did not differ too
and using emojis persist across prompt variants.       much from run to run which gives us confidence
This shows that prompt design can steer, but not       that the results presented in this paper are reliable
fully control, accessible post simplification, and     and robust, suggesting that the observed patterns
that model choice and safety configuration remain      are not artifacts of randomness in model sampling.
crucial factors.                                          Prompt-based LLM simplification shows clear
                                                       potential to make emotionally charged social me-
5   Discussion and conclusion                          dia posts easier to read. However, it should not
                                                       be treated as a fully reliable solution without addi-
This paper explores the use of LLMs for simpli-        tional control. Emotion preservation is not consis-
fying social media posts. Our experiments show         tently reliable across models and settings. Safety
that LLM-based simplification can often preserve       configurations and default rewriting behaviours can
the perceived emotion of social media posts, but       introduce subtle changes in wording and tone that
preservation is not guaranteed and varies with the     shift how a post is interpreted. More advanced ap-
LLM. Comparison between the emotion in the             proaches such as using a cascade of LLMs which
original and the simplified versions shows that in     simplify and assess the content, or fine-tuning will
72.5% cases rewrites retain the same emotion cat-      be explored in future research.
                                                   115

<a id="pdf-p10"></a>
### [PDF p.10] References english easy-to-understand (e2u) language guide-
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **10** / 16

References                                                     english easy-to-understand (e2u) language guide-
                                                               lines. In Proceedings of the 3rd Workshop on Tools
AbilityNet. 2023. Four Ways to Make Emojis Acces-              and Resources for People with REAding DIfficulties
  sible. https://abilitynet.org.uk/news-blogs                  (READI)@ LREC-COLING 2024, pages 70–92.
  /four-ways-make-emojis-accessible.
                                                             Dorottya Demszky, Dana Movshovitz-Attias, Jeongwoo
American Psychiatric Association. 2013. Diagnostic
                                                               Ko, Alan Cowen, Gaurav Nemade, and Sujith Ravi.
 and Statistical Manual of Mental Disorders: DSM-5,
                                                               2020. Goemotions: A dataset of fine-grained emo-
 5th edition. American Psychiatric Publishing.
                                                               tions. arXiv preprint arXiv:2005.00547.
Sian Anderson, Tal Araten-Bergman, and Gillian Steel.
                                                             Paul Ekman. 1992. Are there basic emotions? Psycho-
   2023. Adults with intellectual disabilities as users of
                                                               logical review, 99(3).
   social media: A scoping review. British Journal of
   Learning Disabilities, 51(4):544–564.
                                                             Björn Engelmann, Christin Katharina Kreutz, Fabian
Laura-Ana-Maria Bostan and Roman Klinger. 2018.                Haak, and Philipp Schaer. 2024. ARTS: Assessing
  An analysis of annotated corpora for emotion clas-           readability & text simplicity. In Findings of the Asso-
  sification in text. In Proceedings of the 27th Inter-        ciation for Computational Linguistics: EMNLP 2024,
  national Conference on Computational Linguistics,            pages 14925–14942, Miami, Florida, USA. Associa-
  pages 2104–2119, Santa Fe, New Mexico, USA. As-              tion for Computational Linguistics.
  sociation for Computational Linguistics.
                                                             European Commission. 2012. How to write clearly.
Jo Button. 2021. Learning to Make Twitter Content
   More Accessible. https://digital.canada.ca/               European Union. 2016. Directive EU 2016/2102 on
   2021/03/12/learning-to-make-twitter-conte                   the accessibility of the websites and mobile applica-
   nt-more-accessible/. Canadian Digital Service               tions of public sector bodies. Official Journal of the
   blog.                                                       European Union.

Sue Caton, Chris Hatton, Amanda Gillooly, Edward             European Union. 2019. Directive EU 2019/882 on the
  Oloidi, Libby Clarke, Jill Bradshaw, Samantha Flynn,         accessibility requirements for products and services
  Laurence Taggart, Peter Mulhall, Andrew Jahoda,              (european accessibility act). Official Journal of the
  Roseann Maguire, Anna Marriott, Stuart Todd, David           European Union.
  Abbott, Stephen Beyer, Nick Gore, Pauline Heslop,
  Katrina Scior, and Richard P Hastings. 2022. Online        Rudolf Flesch. 1948. A new readability yardstick. Jour-
  social connections and internet use among people             nal of Applied Psychology, 32(3):221–233.
  with intellectual disabilities in the united kingdom
  during the covid-19 pandemic. New Media & Society,         Sarah Glencross, Jonathan Mason, Mary Katsikitis, and
  26(5):2804–2828.                                             Kenneth Mark Greenwood. 2021. Internet use by
                                                               people with intellectual disability: Exploring digi-
Darren Chadwick, Kristin Alfredsson Ågren, Sue                 tal inequalitya systematic review. Cyberpsychology,
  Caton, Esther Chiner, Joanne Danker, Marcos                  Behavior, and Social Networking, 24(8):503–520.
  Gómez-Puerta, Vanessa Heitplatz, Stefan Johansson,
  Claude L Normand, Esther Murphy, and 1 others.             Government Communication Service. 2021. Planning,
  2022. Digital inclusion and participation of peo-            creating and publishing accessible social media cam-
  ple with intellectual disabilities during covid-19: A        paigns. https://www.communications.gov.uk/
  rapid review and international bricolage. Journal            guidance/digital-communication/planning-c
  of Policy and Practice in intellectual Disabilities,         reating-and-publishing-accessible-socia
  19(3):242–256.                                               l-media-campaigns/.

Jeanne Sternlicht Chall and Edgar Dale. 1995. Readabil-      Silvia Hansen-Schirra and Christiane Maaß, editors.
   ity revisited : the new dale-chall readability formula.      2020. Easy language research: text and user per-
   In Readability Revisited: The New Dale-Chall Read-           spectives, volume 2 of Easy Plain Accessible. Frank
   ability Formula.                                             & Timme.

Change. 2016. How to make information accessible: A          Harvard University. 2023. Social media accessibility
  guide to producing easy read documents. Technical            best practices. https://www.harvard.edu/in-f
  report, CHANGE People.                                       ocus/the-accessible-world/social-media-a
                                                               ccessibility-best-practices/.
Bronwen Davies. 2013. Emotional perception and reg-
  ulation and their relationship with challenging be-        Hertfordshire County Council. 2018. Easy read guid-
  haviour in people with a learning disability. PhD            ance and checklist. Technical report, Hertfordshire
  dissertation, Cardiff University.                            County Council.

Andreea Maria Deleanu, Constantin Orasan, and Sabine         Inclusion Europe. 2010. Information for all: European
  Braun. 2024. Accessible communication: a sys-                 standards for making information easy to read and
  tematic review and comparative analysis of official           understand. Guideline document.
                                                         116

<a id="pdf-p11"></a>
### [PDF p.11] J. P. Kincaid, R. P. Fishburne, R. L. Rogers, and B. S. Readability Guidelines. 2020. Using emojis. https:
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **11** / 16

J. P. Kincaid, R. P. Fishburne, R. L. Rogers, and B. S.       Readability Guidelines. 2020. Using emojis. https:
   Chissom. 1975. Derivation of new readability for-            //readabilityguidelines.co.uk/images/emo
   mulas for navy enlisted personnel. Technical report,         jis/.
   Naval Technical Training Command.
                                                              Janice Redish. 2000. Readability formulas have even
Po-Nien Kung and Nanyun Peng. 2023. Do mod-                     more limitations than klare discusses. ACM J. Com-
  els really learn to follow instructions? An Empir-            put. Doc., 24(3):132137.
  ical Study of Instruction Tuning. arXiv preprint
  arXiv:2305.11383.                                           Eleanor Rowell. 2021. Accessibility for all: 8 ways
                                                                to make your social media content more accessible.
Karen Mellor and Dave Dagnan. 2005. Exploring the               https://blogs.edgehill.ac.uk/learningedg
  concept of alexithymia in the lives of people with            e/2021/07/06/accessibility-for-all-8-w
  learning disabilities. Journal of Intellectual Disabili-      ays-to-make-your-social-media-content-m
  ties, 9(3):229–239.                                           ore-accessible/. Edge Hill University Digital
                                                                Learning blog.
Mencap. 2000. Am I Making Myself Clear? Mencap’s
 Guidelines for Accessible Writing. Technical report,         Hadeel Saadany, Constantin Orasan, Rocio Caro Quin-
 Mencap.                                                        tana, Felix Do Carmo, and Leonardo Zilio. 2023.
                                                                Analysing mistranslation of emotions in multilingual
Mencap. 2021. Let’s Make Social Media More Accessi-             tweets by online MT tools. In Proceedings of the
  ble. https://www.mencap.org.uk/blog/lets-m                    24th Annual Conference of the European Association
  ake-social-media-more-accessible.                             for Machine Translation, pages 275–284, Tampere,
                                                                Finland. European Association for Machine Transla-
Mencap. 2022. Mencap social media accessibility                 tion.
 guidelines. https://www.mencap.org.uk/resour
 ce/mencap-social-media-accessibility-gui                     Scope Australia. 2015. Clear written communications:
 delines.                                                       The easy english style guide. Technical report, Scope
                                                                (Aust) Ltd.
Gyda Skat Nielsen Misako Nomura and Bror Tronbacke.
  2010. Ifla guidelines for easy-to-read materials.           Jennifer L Scotland, Jill Cossar, and Karen McKenzie.
                                                                2015. The ability of adults with an intellectual dis-
Saif Mohammad, Felipe Bravo-Marquez, Mohammad                   ability to recognise facial expressions of emotion in
  Salameh, and Svetlana Kiritchenko. 2018. SemEval-             comparison with typically developing individuals: a
  2018 task 1: Affect in tweets. In Proceedings of the          systematic review. Research in developmental dis-
  12th International Workshop on Semantic Evaluation,           abilities, 41:22–39.
  pages 1–17, New Orleans, Louisiana. Association for
                                                              Sprout Social. 2024. 10 guidelines to make social media
  Computational Linguistics.
                                                                posts more accessible. https://sproutsocial.c
NHS England. 2017. Personalised health and care: In-            om/insights/social-media-accessibility/.
 formation for people and families. Guidance docu-            Carlo Strapparava and Rada Mihalcea. 2007. SemEval-
 ment. Integrated Personal Commissioning (IPC).                 2007 task 14: Affective text. In Proceedings of the
Office for Health Improvement & Disparities (OHID).             Fourth International Workshop on Semantic Evalua-
  2025. Learning disability Applying All Our Health.            tions (SemEval-2007), pages 70–74, Prague, Czech
  https://www.gov.uk/government/publicatio                      Republic. Association for Computational Linguistics.
  ns/learning-disability-applying-all-our-h                   Paraskevi Triantafyllopoulou, Jessie Newsome, Winnie
  ealth/learning-disabilities-applying-all                      Tsang, Michelle McCarthy, and Karen Jones. 2025.
 -our-health. Updated 6 January 2025.                           Safer online lives: Internet use and online experi-
                                                                ences of adults with intellectual disabilitiesa survey
Sara Owen and Frances A Maratos. 2016. Recogni-
                                                                study. Journal of Applied Research in Intellectual
  tion of subtle and universal facial expressions in a
                                                                Disabilities, 38(3):e70061.
  community-based sample of adults classified with in-
  tellectual disability. Journal of Intellectual Disability   UK Association for Accessible Formats (UKAAF).
  Research, 60(4):344–354.                                     2020. G028: Social media guidance. https:
                                                               //www.ukaaf.org/wp-content/uploads/202
Kishore Papineni, Salim Roukos, Todd Ward, and Wei-            1/03/G028-UKAAF-Social-Media-Guidance-Dec
  Jing Zhu. 2002. Bleu: a method for automatic evalu-          ember-2020.pdf.
  ation of machine translation. In Proceedings of the
  40th Annual Meeting of the Association for Compu-           United States Congress. 2010. Plain writing act of 2010.
  tational Linguistics, pages 311–318, Philadelphia,            Public Law 111–274.
  Pennsylvania, USA. Association for Computational
  Linguistics.                                                University of Edinburgh. 2022. Social media accessi-
                                                                bility guidance. https://information-services.
Elisa Perego. 2020. Accessible communication: A cross-          ed.ac.uk/help-consultancy/accessibility/c
   country journey, volume 4 of Easy Plain Accessible.          reating-materials/social-media-accessibi
   Frank & Timme.                                               lity-guidance.
                                                          117

<a id="pdf-p12"></a>
### [PDF p.12] University of Reading. 2023. Accessibility tips: Social
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **12** / 16

University of Reading. 2023. Accessibility tips: Social
  media posts. https://www.reading.ac.uk/digi
  tal-accessibility/blog/blog-2023/social-m
  edia-posts.

Johanna LL van Alem, Noud Frielink, and Petri JCM
  Embregts. 2025. Social internet use by people with
  intellectual disabilities: A systematic review and the-
  matic synthesis of qualitative studies. Journal of
  Intellectual Disability Research, 69(4):243–264.

Albert Xu, Eshaan Pathak, Eric Wallace, Suchin Guru-
  rangan, Maarten Sap, and Dan Klein. 2021. Detoxi-
  fying language models risks marginalizing minority         Figure A.1: Label stability between pred_orig and
  voices. In Proceedings of the 2021 Conference of           pred_simp: percentage of items for which the classi-
  the North American Chapter of the Association for          fier assigns the same Ekman emotion before and after
  Computational Linguistics: Human Language Tech-            simplification.
  nologies, pages 2390–2397, Online. Association for
  Computational Linguistics.

Wei Xu, Courtney Napoles, Ellie Pavlick, Quanze Chen,
  and Chris Callison-Burch. 2016. Optimizing sta-
  tistical machine translation for text simplification.
 Transactions of the Association for Computational
  Linguistics, 4:401–415.

Hikaru Yamanaka and Takenobu Tokunaga. 2024.
  SIERA: An evaluation metric for text simplification
  using the ranking model and data augmentation by
  edit operations. In Proceedings of the 3rd Workshop
  on Tools and Resources for People with REAding
  DIfficulties (READI) @ LREC-COLING 2024, pages
  47–58, Torino, Italia. ELRA and ICCL.

Tianyi Zhang, Varsha Kishore, Felix Wu, Kilian Q
  Weinberger, and Yoav Artzi. 2019. Bertscore: Eval-
  uating text generation with bert. arXiv preprint
  arXiv:1904.09675.


A    Appendix


 Ekman Emotion         Precision    Recall     F1 -score
 anger                   0.50        0.65        0.57
 disgust                 0.52        0.53        0.53
 fear                    0.61        0.76        0.68
 joy                     0.77        0.88        0.82
 neutral                 0.66        0.67        0.66
 sadness                 0.56        0.62        0.59
 surprise                0.53        0.70        0.61
 macro-average           0.59        0.69        0.64
 std                     0.10        0.11        0.10

Table A.3: Ekman-level BERT baseline on GoEmotions
(from Demszky et al. (2020)) for comparison with our
XLM-RoBERTa classifier.

                                                           118

<a id="pdf-p13"></a>
### [PDF p.13] Figure A.2: Confusion-matrix heatmap for the XLM-RoBERTa classifier on the GoEmotions dataset.
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **13** / 16

Figure A.2: Confusion-matrix heatmap for the XLM-RoBERTa classifier on the GoEmotions dataset.




                                             119

<a id="pdf-p14"></a>
### [PDF p.14] Figure A.3: Alluvial diagram showing flows from emotion labels predicted on the original posts (pred_orig, left) to
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **14** / 16

Figure A.3: Alluvial diagram showing flows from emotion labels predicted on the original posts (pred_orig, left) to
labels predicted on the simplified posts (pred_simp, right).




                                                       120

<a id="pdf-p15"></a>
### [PDF p.15] Figure A.4: Confusion matrix showing counts of emotion labels predicted on the original posts (pred_orig) versus
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **15** / 16

Figure A.4: Confusion matrix showing counts of emotion labels predicted on the original posts (pred_orig) versus
the simplified posts (pred_simp).




                                                      121

<a id="pdf-p16"></a>
### [PDF p.16] Simplify the post so that people with learning disabilities can easily understand it. Keep
- Locator: `R285-emotion-aware-text-simplification-of-user-generated-content-using-llms.pdf` · página **16** / 16

Simplify the post so that people with learning disabilities can easily understand it. Keep
 the same meaning and facts. Preserve the same emotion. Do not soften or exaggerate the
 emotion. Do not add new facts or advice. Do not judge the person. Use common words
 and active voice. Keep emojis only if they add meaning. Use CamelCase for hashtags. For
 example, instead of #learningdisabilityweek, write #LearningDisabilityWeek. Do not add
 feelings or any assumptions about how a person feels. Keep simple posts as they are, even
 though they contain swear words. Explain all abbreviations, famous people, events or any
 other entities. Do not add hashtags or emojis

 Simplify the post so that people with learning disabilities can easily understand it. Keep
 the same meaning and facts. Preserve the same emotion. Do not soften or exaggerate the
 emotion. Make the feelings clear and simple. Do not add new facts or advice. Do not
 judge the person. Use common words and active voice. Keep emojis only if they add
 meaning. Use CamelCase for hashtags. For example, instead of #learningdisabilityweek,
 write #LearningDisabilityWeek. Do not add “I feel”. Keep simple posts as they are, even
 though they contain swear words. Explain all abbreviations, famous people, events or any
 other entities. Do not add hashtags or emojis.

          Figure A.5: Prompt variant removing the instruction to “also name the feeling in words”
                                                    .



Simplify the post so that people with learning disabilities can easily understand it. Keep the
same meaning and facts. Preserve the same emotion. Do not soften or exaggerate the emotion.
Make the feelings clear and simple. Do not add new facts or advice. Do not judge the person.
Use common words and active voice. Keep emojis only if they add meaning, and also name the
feeling in words. Do not assume how the person feels.

Simplify the post so that people with learning disabilities can easily understand it. Keep the
same meaning and facts. Preserve the same emotion. Do not soften or exaggerate the emotion.
Make the feelings clear and simple. Do not add new facts or advice. Do not judge the person.
Use common words and active voice. Keep emojis only if they add meaning. Do not assume
how the person feels.

               Figure A.6: Prompt variant removing the instruction about hashtag or emoji.




You are an accessibility editor for social media.
GOAL: Make the posts easy to read without changing the original emotion or facts.
CONSTRAINTS: (1) Short sentences; one idea per sentence. (2) Keep names, numbers, links;
keep hashtags (CamelCase). (3) No advice, opinions, or extra facts. (4) Do not judge the person.
(5) Keep emojis only if they were in the original text and keep emojis at the end of the message
(6) Explain all abbreviations, famous people, events or any other entities.
EMOTION: Keep the same emotion and intensity. Make the feelings clear and simple. Do not
add feelings or any assumptions about how a person feels.
OUTPUT: Only the simplified text.

                         Figure A.7: Different prompt with additional instructions


                                                   122
