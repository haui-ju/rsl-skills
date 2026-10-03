# A Low-Resource Speech-Driven NLP Pipeline for Sinhala Dyslexia

> Fuente PDF: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · técnica **locator index** (página + ancla) + chunks Graphify

## Metadata
- Stem: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance`
- PDF: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf`
- DOI: `10.26615/978-954-452-098-4-106`
- Pages: `9`
- Structured_at: `2026-10-03T23:23:18+00:00`
- Technique: `pdf-page-locators + heading-chunks`

## Locator index (qué hay y en qué página del PDF)

| Kind | Label | PDF page | MD anchor |
|------|-------|----------|-----------|
| abstract | Abstract / blurb | 1 | `#abstract` |
| section | 1.1 Problem | 1 | `#p1-1-1-problem` |
| section | 1 Introduction | 1 | `#p1-1-introduction` |
| section | 1.3 Objective                                         Several dyslexia-specific applications have | 2 | `#p2-1-3-objective-several-dyslexia-specific-applications-have` |
| section | 2.1 Assistive tech in NLP                            low-resource, non-Latin-script contexts like Sin | 2 | `#p2-2-1-assistive-tech-in-nlp-low-resource-non-latin-script-contexts-like-sin` |
| section | 2.3 Error correction in low-resource NLP | 3 | `#p3-2-3-error-correction-in-low-resource-nlp` |
| section | 3.1 Component Breakdown                             Specifically, we define four primary error cate | 4 | `#p4-3-1-component-breakdown-specifically-we-define-four-primary-error-cate` |
| section | 3.1.4 Text-to-Speech: gTTS Sinhala Playback               its quick turnaround time and native web/mobile | 5 | `#p5-3-1-4-text-to-speech-gtts-sinhala-playback-its-quick-turnaround-time-and-nati` |
| section | 4 Evaluation Setup | 6 | `#p6-4-evaluation-setup` |
| section | 5.3 Evaluation Results | 7 | `#p7-5-3-evaluation-results` |
| section | 5.1 Performance Scores | 7 | `#p7-5-1-performance-scores` |
| section | 5.1.2 Correction Module | 7 | `#p7-5-1-2-correction-module` |
| section | 5.5 Latency and Real-Time Performance | 7 | `#p7-5-5-latency-and-real-time-performance` |
| section | 5.2 Table of Evaluation Metrics                          Each component was benchmarked for average in | 7 | `#p7-5-2-table-of-evaluation-metrics-each-component-was-benchmarked-for-average-in` |
| section | 7 Conclusion and Future Work | 8 | `#p8-7-conclusion-and-future-work` |
| section | 6 Discussion                                        and Sinhala language computing, with the poten | 8 | `#p8-6-discussion-and-sinhala-language-computing-with-the-poten` |
| concept | R473 | ? | `#concept-r473` |
| concept | resource | ? | `#concept-resource` |
| concept | speech | ? | `#concept-speech` |
| concept | driven | ? | `#concept-driven` |
| concept | pipeline | ? | `#concept-pipeline` |
| concept | sinhala | ? | `#concept-sinhala` |
| concept | dyslexia | ? | `#concept-dyslexia` |
| concept | assistance | ? | `#concept-assistance` |
| finding | port dyslexic users in English and other widely spo- ken languages, speakers of low-resour… | 1 | `#finding-port-dyslexic-users-in-english-and-other` |
| finding | De- researched and under-served area, particularly spite this, very few digital interventi… | 1 | `#finding-de-researched-and-under-served-area-pa` |
| finding | significant impact on personal and profes- sional lives. | 1 | `#finding-significant-impact-on-personal-and-profe` |
| finding | This work addresses that gap by 1.1 Problem focusing on Sinhala, a low-resource language w… | 1 | `#finding-this-work-addresses-that-gap-by-1-1-prob` |
| finding | How- Mistral-based model to generate corrected text. | 1 | `#finding-how-mistral-based-model-to-generate-cor` |
| finding | These results demonstrate tion tools (De Silva, 2024). | 1 | `#finding-these-results-demonstrate-tion-tools-de` |
| page | p.1: A Low-Resource Speech-Driven NLP Pipeline for Sinhala Dyslexia | 1 | `#pdf-p1` |
| page | p.2: adults. Furthermore, existing spell checkers or nisms (Heilman et al., 2006) (Rello and Ba | 2 | `#pdf-p2` |
| page | p.3: 2.2 Speech-to-Text and Text-to-Speech for ods (Herath et al., 2020). Yet, these systems ty | 3 | `#pdf-p3` |
| page | p.4: based architectures can be orchestrated to support allowing accurate phoneme-to-grapheme m | 4 | `#pdf-p4` |
| page | p.5: (e.g., omission, substitution, insertion, reversal), | 5 | `#pdf-p5` |
| page | p.6: 3.2 Design goals https://github.com/PeshalaPerera/sinhala- | 6 | `#pdf-p6` |
| page | p.7: Model Description mT5-small + Mistral API | 7 | `#pdf-p7` |
| page | p.8: likely with domain-specific fine-tuning. Addition- | 8 | `#pdf-p8` |
| page | p.9: References D. D. Perera et al. 2022. Sinbert: A transformer-based | 9 | `#pdf-p9` |

## Abstract
<a id="abstract"></a>

port dyslexic users in English and other widely spo- ken languages, speakers of low-resource and non- Dyslexia in adults remains an under- Latin script languages remain underserved. De- researched and under-served area, particularly spite this, very few digital interventions exist for in non-English-speaking contexts, despite its Sinhala-speaking adults with dyslexia. significant impact on personal and profes- sional lives. This work addresses that gap by 1.1 Problem focusing on Sinhala, a low-resource language with limited tools for linguistic accessibility. Existing assistive technologies for dyslexia are We present an assistive system explicitly predominantly designed for children and primar- designed for Sinhala-speaking adults with ily focus on English and Latin script languages. dyslexia. The system integrates Whisper Tools such as Grammarly, NaturalReader, and for speech-to-text conversion, SinBERT, Read and Write have demonstrated success in en- an open-sourced fine-tuned BERT model trained for Sinhala to identify common hancing language accessibility for dyslexic users dyslexic errors, and a combined mT5 and in these languages (Patnoorkar et al., 2023). How- Mistral-based model to generate corrected text. ever, these solutions are not linguistically or cultur- Finally, the output is converted back to speech ally adapted to accommodate Sinhala orthography, using gTTS, creating a complete multimodal speech phonemes, or adult-specific learning needs. feedback loop. Despite the challenges posed Sinhala is a low-resource language in the NLP by limited Sinhala-language datasets, the landscape due to the scarcity of annotated corpora, system achieves 0.66 transcription accuracy and 0.7 correction accuracy with 0.65 overall pretrained language models, and text normaliza- system accuracy. These results demonstrate tion tools (De Silva, 2024). This lack of infras- both the feasibility and effectiveness of the tructure limits the development of inclusive appli- approach. Ultimately, this work highlights cations. Adults with dyslexia, particularly in non- the importance of inclusive Natural Language English contexts, face even greater marginaliza- Processing (NLP) technologies in underrepre- tion due to inadequate educational support and a sented languages and showcases a practical lack of appropriate digital tools (Goodman et al., step toward improving accessibility for adult 2022). dyslexic users. 1.2 Gap 1 Introduction The majority of existing dyslexia-foc

## Keywords

- _(none auto-detected)_

## Concept index (graph hooks + página)

<a id="concept-r473"></a>
### [PDF p.?] Concept: R473
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **?**

<a id="concept-resource"></a>
### [PDF p.?] Concept: resource
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **?**

<a id="concept-speech"></a>
### [PDF p.?] Concept: speech
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **?**

<a id="concept-driven"></a>
### [PDF p.?] Concept: driven
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **?**

<a id="concept-pipeline"></a>
### [PDF p.?] Concept: pipeline
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **?**

<a id="concept-sinhala"></a>
### [PDF p.?] Concept: sinhala
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **?**

<a id="concept-dyslexia"></a>
### [PDF p.?] Concept: dyslexia
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **?**

<a id="concept-assistance"></a>
### [PDF p.?] Concept: assistance
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **?**


## Findings index (graph hooks + página)

<a id="finding-port-dyslexic-users-in-english-and-other"></a>
### [PDF p.1] Finding: port dyslexic users in English and other widely spo- ken languages, speakers of low-resource and non- Dyslexia in adults remains an under- Latin script languages remain underserved.
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **1**

<a id="finding-de-researched-and-under-served-area-pa"></a>
### [PDF p.1] Finding: De- researched and under-served area, particularly spite this, very few digital interventions exist for in non-English-speaking contexts, despite its Sinhala-speaking adults with dyslexia.
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **1**

<a id="finding-significant-impact-on-personal-and-profe"></a>
### [PDF p.1] Finding: significant impact on personal and profes- sional lives.
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **1**

<a id="finding-this-work-addresses-that-gap-by-1-1-prob"></a>
### [PDF p.1] Finding: This work addresses that gap by 1.1 Problem focusing on Sinhala, a low-resource language with limited tools for linguistic accessibility.
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **1**

<a id="finding-how-mistral-based-model-to-generate-cor"></a>
### [PDF p.1] Finding: How- Mistral-based model to generate corrected text.
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **1**

<a id="finding-these-results-demonstrate-tion-tools-de"></a>
### [PDF p.1] Finding: These results demonstrate tion tools (De Silva, 2024).
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **1**


## Relevance hooks
### Theme relevance: software engineering and accessibility
### Theme relevance: cognitive accessibility and neurodiversity
### Theme relevance: evaluation metrics and WCAG

## Sections (detected in PDF)

<a id="p1-1-1-problem"></a>
### [PDF p.1] Section: 1.1 Problem
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **1** · ancla `#p1-1-1-problem`

<a id="p1-1-introduction"></a>
### [PDF p.1] Section: 1 Introduction
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **1** · ancla `#p1-1-introduction`

<a id="p2-1-3-objective-several-dyslexia-specific-applications-have"></a>
### [PDF p.2] Section: 1.3 Objective                                         Several dyslexia-specific applications have
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **2** · ancla `#p2-1-3-objective-several-dyslexia-specific-applications-have`

<a id="p2-2-1-assistive-tech-in-nlp-low-resource-non-latin-script-contexts-like-sin"></a>
### [PDF p.2] Section: 2.1 Assistive tech in NLP                            low-resource, non-Latin-script contexts like Sin
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **2** · ancla `#p2-2-1-assistive-tech-in-nlp-low-resource-non-latin-script-contexts-like-sin`

<a id="p3-2-3-error-correction-in-low-resource-nlp"></a>
### [PDF p.3] Section: 2.3 Error correction in low-resource NLP
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **3** · ancla `#p3-2-3-error-correction-in-low-resource-nlp`

<a id="p4-3-1-component-breakdown-specifically-we-define-four-primary-error-cate"></a>
### [PDF p.4] Section: 3.1 Component Breakdown                             Specifically, we define four primary error cate
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **4** · ancla `#p4-3-1-component-breakdown-specifically-we-define-four-primary-error-cate`

<a id="p5-3-1-4-text-to-speech-gtts-sinhala-playback-its-quick-turnaround-time-and-nati"></a>
### [PDF p.5] Section: 3.1.4 Text-to-Speech: gTTS Sinhala Playback               its quick turnaround time and native web/mobile
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **5** · ancla `#p5-3-1-4-text-to-speech-gtts-sinhala-playback-its-quick-turnaround-time-and-nati`

<a id="p6-4-evaluation-setup"></a>
### [PDF p.6] Section: 4 Evaluation Setup
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **6** · ancla `#p6-4-evaluation-setup`

<a id="p7-5-3-evaluation-results"></a>
### [PDF p.7] Section: 5.3 Evaluation Results
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **7** · ancla `#p7-5-3-evaluation-results`

<a id="p7-5-1-performance-scores"></a>
### [PDF p.7] Section: 5.1 Performance Scores
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **7** · ancla `#p7-5-1-performance-scores`

<a id="p7-5-1-2-correction-module"></a>
### [PDF p.7] Section: 5.1.2 Correction Module
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **7** · ancla `#p7-5-1-2-correction-module`

<a id="p7-5-5-latency-and-real-time-performance"></a>
### [PDF p.7] Section: 5.5 Latency and Real-Time Performance
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **7** · ancla `#p7-5-5-latency-and-real-time-performance`

<a id="p7-5-2-table-of-evaluation-metrics-each-component-was-benchmarked-for-average-in"></a>
### [PDF p.7] Section: 5.2 Table of Evaluation Metrics                          Each component was benchmarked for average in
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **7** · ancla `#p7-5-2-table-of-evaluation-metrics-each-component-was-benchmarked-for-average-in`

<a id="p8-7-conclusion-and-future-work"></a>
### [PDF p.8] Section: 7 Conclusion and Future Work
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **8** · ancla `#p8-7-conclusion-and-future-work`

<a id="p8-6-discussion-and-sinhala-language-computing-with-the-poten"></a>
### [PDF p.8] Section: 6 Discussion                                        and Sinhala language computing, with the poten
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **8** · ancla `#p8-6-discussion-and-sinhala-language-computing-with-the-poten`


## Page chunks (texto por página del PDF)

_Cada heading es un nodo Graphify. El label incluye la página para volver al PDF sin releer todo._

<a id="pdf-p1"></a>
### [PDF p.1] A Low-Resource Speech-Driven NLP Pipeline for Sinhala Dyslexia
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **1** / 9

A Low-Resource Speech-Driven NLP Pipeline for Sinhala Dyslexia
                             Assistance

                    Peshala Perera                                 Deshan Sumanathilaka
          Informatics Institute of Technology                        School of Computing
          57, Ramakrishna Road, Colombo 06                       Swansea University, Swansea
                        Sri Lanka                                      United Kingdom
              peshala.s.perera@gmail.com                          deshankoshala@gmail.com


                      Abstract                               port dyslexic users in English and other widely spo-
                                                             ken languages, speakers of low-resource and non-
    Dyslexia in adults remains an under-                     Latin script languages remain underserved. De-
    researched and under-served area, particularly           spite this, very few digital interventions exist for
    in non-English-speaking contexts, despite its
                                                             Sinhala-speaking adults with dyslexia.
    significant impact on personal and profes-
    sional lives. This work addresses that gap by
                                                             1.1 Problem
    focusing on Sinhala, a low-resource language
    with limited tools for linguistic accessibility.       Existing assistive technologies for dyslexia are
    We present an assistive system explicitly              predominantly designed for children and primar-
    designed for Sinhala-speaking adults with              ily focus on English and Latin script languages.
    dyslexia. The system integrates Whisper                Tools such as Grammarly, NaturalReader, and
    for speech-to-text conversion, SinBERT,
                                                           Read and Write have demonstrated success in en-
    an open-sourced fine-tuned BERT model
    trained for Sinhala to identify common                 hancing language accessibility for dyslexic users
    dyslexic errors, and a combined mT5 and                in these languages (Patnoorkar et al., 2023). How-
    Mistral-based model to generate corrected text.        ever, these solutions are not linguistically or cultur-
    Finally, the output is converted back to speech        ally adapted to accommodate Sinhala orthography,
    using gTTS, creating a complete multimodal             speech phonemes, or adult-specific learning needs.
    feedback loop. Despite the challenges posed               Sinhala is a low-resource language in the NLP
    by limited Sinhala-language datasets, the              landscape due to the scarcity of annotated corpora,
    system achieves 0.66 transcription accuracy
    and 0.7 correction accuracy with 0.65 overall
                                                           pretrained language models, and text normaliza-
    system accuracy. These results demonstrate             tion tools (De Silva, 2024). This lack of infras-
    both the feasibility and effectiveness of the          tructure limits the development of inclusive appli-
    approach. Ultimately, this work highlights             cations. Adults with dyslexia, particularly in non-
    the importance of inclusive Natural Language           English contexts, face even greater marginaliza-
    Processing (NLP) technologies in underrepre-           tion due to inadequate educational support and a
    sented languages and showcases a practical             lack of appropriate digital tools (Goodman et al.,
    step toward improving accessibility for adult
                                                           2022).
    dyslexic users.
                                                             1.2 Gap
1   Introduction
                                                           The majority of existing dyslexia-focused applica-
Dyslexia is a lifelong language-based learning dis-        tions are targeted at early intervention for children.
order that affects reading fluency, spelling, and          In contrast, adult users remain significantly under-
written expression despite normal intelligence and         represented in both research and application devel-
education. It is estimated to affect 5–10% of the          opment (Sadusky et al., 2021). This gap is par-
global population (Santhiya et al., 2023). Individ-        ticularly evident in non-English-speaking regions
uals with dyslexia struggle with phonological pro-         where technological adoption lags, and awareness
cessing, decoding, and linguistic fluency, which           around adult dyslexia is limited.
leads to significant obstacles in education and daily         In Sinhala, no comprehensive NLP-driven tools
life (Roitsch and Watson, 2019). While digital             currently exist that combine speech recognition, er-
tools and NLP technologies have advanced to sup-           ror correction, and speech synthesis tailored for

                                                       925
                    Proceedings of Recent Advances in Natural Language Processing,pages 925–933
                                                  Varna, Sep 8–10, 2025
                                   https://doi.org/10.26615/978-954-452-098-4-106

<a id="pdf-p2"></a>
### [PDF p.2] adults. Furthermore, existing spell checkers or nisms (Heilman et al., 2006) (Rello and Baeza-
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **2** / 9

adults. Furthermore, existing spell checkers or       nisms (Heilman et al., 2006) (Rello and Baeza-
grammar tools fail to address cognitive and phono-    Yates, 2013). Recent research has also explored
logical errors common in dyslexic speech and writ-    adaptive interfaces and inclusive design principles
ing (Rupasinghe et al., 2020). The absence of         to further improve accessibility in writing tools
domain-specific NLP tools reinforces a cycle of ex-   (Wood et al., 2018) (Al-Azawei et al., 2016).
clusion for this population.

1.3    Objective                                         Several dyslexia-specific applications have
                                                      emerged in the form of mobile apps or browser
This study aims to develop a localized NLP-based
                                                      extensions, targeting early learners and children
assistive system for Sinhala-speaking adults with
                                                      (Al-Wabil et al., 2007). However, the vast
dyslexia. The system is designed as a real-time
                                                      majority are language-specific (mainly English
speech-driven tool to support reading, writing, and
                                                      or Western European languages) and are not
comprehension. The objective is to combine mul-
                                                      adaptable to the linguistic diversity or script
tiple NLP modules, speech-to-text (STT), error
                                                      complexity of non-Latin languages. This issue
classification, grammatical error correction (GEC),
                                                      is particularly critical in the context of Sinhala, a
and text-to-speech (TTS) into a single end-to-end
                                                      language with unique phonological and morpho-
application that is both accessible and linguisti-
                                                      logical characteristics that complicate the direct
cally appropriate for Sinhala. The system inte-
                                                      application of mainstream assistive technologies.
grates modern transformer-based architectures and
                                                      A recent review highlights that most assistive
builds upon publicly available pre-trained models,
                                                      applications for Sinhala-speaking adults remain
adapted for Sinhala. This approach allows the
                                                      underdeveloped, with research efforts historically
application to function in a low-resource setting
                                                      focused on children or English-language tools
while maintaining modularity, accuracy, and real-
                                                      (Perera and Sumanathilaka, 2025). The review
time feedback.
                                                      stresses the urgent need for adult-focused, cultur-
   The main contributions of this studies can be
                                                      ally adapted NLP tools and emphasizes the role
summarized as follows.
                                                      of low-resource NLP pipelines in closing this
    • Introduces the first real-time NLP-based        accessibility gap.
      dyslexia assistant tailored for Sinhala.
    • Integrates Whisper, SinBERT, mT5, Mistral,           Recent advances in error correction and assis-
      and gTTS in a modular speech-to-text and          tive NLP demonstrate the potential of language
      text-to-speech pipeline.                          models for supporting users with dyslexia and re-
    • Demonstrates competitive accuracy (66%            lated linguistic impairments. For instance, (In-
      STT, 70% correction) using synthetically gen-     gólfsdóttir et al., 2023) explored byte-level gram-
      erated dyslexic Sinhala data.                     matical error correction using synthetic and cu-
                                                        rated corpora, including writing by dyslexic in-
   Moving forward, this study will present the re-
                                                        dividuals, in morphologically rich languages like
lated work, proposed methodology, results, and
                                                        Icelandic. Their study shows that byte-level en-
discussion.
                                                        coding outperforms subword-based models in han-
2     Related Work                                      dling complex semantic and syntactic errors—
                                                        highlighting promising directions for correction in
2.1    Assistive tech in NLP                            low-resource, non-Latin-script contexts like Sin-
NLP has become central to the development of as-        hala. Similarly, (Zhang et al., 2020) introduced
sistive tools that support individuals with reading     a Soft-Masked BERT architecture for Chinese
and writing difficulties, including dyslexia. Main-     spelling correction. Their model enhances BERT’s
stream applications such as Grammarly, Speechify,       ability to both detect and correct errors by decou-
and Read and Write use grammar correction, text-        pling these tasks and employing a soft-masking
to-speech, and predictive typing to provide en-         mechanism between the detection and correction
hanced language accessibility. These tools are          phases. This two-stage method outperforms base-
largely effective for users in English-speaking en-     line BERT models and provides inspiration for
vironments and rely heavily on pretrained lan-          modular designs in error correction pipelines tar-
guage models and rule-based feedback mecha-             geting cognitive writing impairments.

                                                  926

<a id="pdf-p3"></a>
### [PDF p.3] 2.2 Speech-to-Text and Text-to-Speech for ods (Herath et al., 2020). Yet, these systems typ-
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **3** / 9

2.2   Speech-to-Text and Text-to-Speech for                ods (Herath et al., 2020). Yet, these systems typ-
      accessibility                                        ically offer shallow coverage and do not handle
                                                           complex dyslexic error patterns such as letter re-
Speech technologies have played an increasing
                                                           versals, insertions, and omissions. No large-scale
role in assistive contexts, particularly through
                                                           Sinhala GEC dataset currently exists to train super-
automatic speech recognition (ASR) and text-to-
                                                           vised models, making prompt-based and few-shot
speech (TTS) systems. Whisper, developed by
                                                           learning strategies more suitable for real-world ap-
OpenAI, introduced a robust multilingual ASR
                                                           plications.
system capable of transcribing speech in over
90 languages, including Sinhala (Radford et al.,           2.4 Classification models for dyslexia-like
2022). Whisper’s ability to generalize across                  errors
languages without retraining has made it a use-
                                                         Identifying the type of error is often a prerequisite
ful zero-shot model in low-resource environments.
                                                         to delivering more targeted correction. Pretrained
Transformer-based ASR architectures like the
                                                         classification models such as BERT and its mul-
Transformer Transducer have further improved
                                                         tilingual or domain-specific variants are widely
real-time transcription performance.
                                                         used for this purpose. In Sinhala NLP, SinBERT,
   In parallel, open-source TTS tools such as gTTS
                                                         a BERT-based language model fine-tuned on Sin-
(Google Text-to-Speech) have simplified the pro-
                                                         hala corpora, has emerged as a competitive en-
cess of converting text to spoken feedback. While
                                                         coder for downstream tasks such as sentence clas-
TTS systems are widely used in accessibility tools
                                                         sification and intent detection (Perera et al., 2022).
for visually impaired and dyslexic users, many sys-
                                                         As SinBERT is based on RoBERTa, it inherits ro-
tems lack emotion, emphasis control, or fine-tuned
                                                         bust pretraining optimization techniques (Liu et al.,
output in regional languages, especially Sinhala
                                                         2019) and benefits from subword-level represen-
(Vats et al., 2020). Advances like FastSpeech 2
                                                         tation crucial for agglutinative languages like Sin-
have shown that expressive and low-latency TTS
                                                         hala (Wu and Dredze, 2020).
is feasible even in multilingual contexts (Ren et al.,
                                                             However, to date, no known classification
2020).
                                                         model has been applied specifically to catego-
   Despite the availability of Whisper and gTTS,         rize dyslexia-inspired error patterns in Sinhala text.
few projects combine ASR and TTS modules into            The application of SinBERT for such a classifica-
complete assistive systems, particularly for adult       tion task represents a novel approach, enabling the
dyslexic users.                                          system to tailor correction strategies dynamically
                                                         depending on whether an error is due to substitu-
2.3   Error correction in low-resource NLP
                                                         tion, omission, insertion, or reversal.
Grammatical Error Correction (GEC) is a core task            Existing systems generally focus on monolin-
in NLP assistive applications, helping users with        gual, text-only interfaces, are language-restricted
dyslexia or language learning difficulties to im-        to English, and lack the modularity or real-time
prove fluency and syntactic accuracy. State-of-          capacity for integration into accessible platforms.
the-art GEC systems use text-to-text models such         The system proposed in this paper is distinct in the
as T5, mT5, and GECToR to identify and correct           following ways:
various grammatical errors (Bryant et al., 2022)
                                                              • It is Sinhala-specific, addressing a critical ac-
(Xue et al., 2021). GECToR, in particular, adopts
                                                                cessibility gap in a low-resource language
a tagging-based method that has proven effective
                                                                context.
with limited data (Omelianchuk et al., 2020). For
                                                              • It fuses multiple transformer-based models
truly low-resource settings, pretraining with copy-
                                                                (Whisper, SinBERT, mT5, and Mistral) in a
augmented architectures has also shown promise
                                                                cohesive pipeline.
(Chau et al., 2021).
                                                              • It is optimized for real-time interaction, pro-
   However, the performance of these models is
                                                                viding instantaneous correction and playback,
tightly coupled with the availability of high-quality
                                                                which is crucial for user engagement and
annotated dataset resources that are severely lack-
                                                                learning feedback.
ing for Sinhala. Some efforts have been made to
develop Sinhala spell checkers or grammar correc-           This work bridges a significant gap in assistive
tion tools using lexicon-based or statistical meth-        NLP by demonstrating how modular transformer-

                                                     927

<a id="pdf-p4"></a>
### [PDF p.4] based architectures can be orchestrated to support allowing accurate phoneme-to-grapheme mapping
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **4** / 9

based architectures can be orchestrated to support        allowing accurate phoneme-to-grapheme mapping
users in non-Latin, low-resource environments             even in low-resource contexts. Audio input is re-
with a specific emphasis on adult dyslexic speak-         sampled to 16 kHz and passed through a log-Mel
ers of Sinhala.                                           spectrogram encoder. The model then decodes it
                                                          into text using beam search and multilingual align-
3     System Architecture and Pipeline                    ment layers.
                                                             In this system, Whisper runs locally with quan-
The system combines speech and transformer-
                                                          tized weights to reduce inference latency. Prepro-
based models into a modular architecture opti-
                                                          cessing includes noise reduction and silence trim-
mized for low-resource Sinhala NLP. Each model
                                                          ming. Despite the lack of a Sinhala-specific ASR
was chosen for its effectiveness in real-time, low-
                                                          corpus, Whisper shows strong performance on Sin-
data environments.
                                                          hala speech due to its cross-lingual generalization
   This section describes the end-to-end architec-
                                                          and large model capacity, making it ideal for real-
ture of the proposed Sinhala dyslexia assistant sys-
                                                          time dyslexia assistance. Whisper was chosen
tem. It integrates multiple NLP components into
                                                          for its strong baseline performance, fast inference,
a real-time pipeline optimised for speech-based in-
                                                          and cross-lingual adaptability in low-resource con-
teraction, error classification, text correction, and
                                                          texts.
audio playback. The high level overview of the al-
gorithm is presented in the Figure 1.                     3.1.2 SinBERT Error Classification
                                                        To identify the dominant dyslexia-related error
                                                        type in a transcribed sentence, the system uses
                                                        SinBERT, a Sinhala-specific language model built
                                                        upon the RoBERTa architecture (Perera et al.,
                                                        2022). SinBERT has been extensively pre-trained
                                                        on sin-cc-15M, a large and diverse monolingual
                                                        corpus of Sinhala web text. This pretraining en-
                                                        ables it to learn the morphological, syntactic, and
                                                        semantic nuances of Sinhala, crucial for effective
                                                        performance in low-resource language contexts.
                                                           Its application to dyslexic pattern detection is
Figure 1: Methodology process flow showing the end-     novel, enabling improved precision in downstream
to-end pipeline: from speech input to playback using    modules. In this system, SinBERT is fine-tuned
Whisper, SinBERT, mT5, Mistral, and gTTS.               to classify common dyslexia-inspired error pat-
                                                        terns (e.g., substitution, omission), serving as a
                                                        lightweight and efficient sentence-level classifier.
3.1     Component Breakdown                             Specifically, we define four primary error cate-
The overall interaction between core modules is il-     gories commonly observed in dyslexic Sinhala
lustrated below.                                        writing: substitution (e.g., ගස → කස), inser-
                                                        tion (e.g., ගස → ගසා), omission (e.g., ගසක‍්
3.1.1    Whisper-Based Speech-to-Text (STT)             → ගක‍්), and reversal (e.g., ගම → මග). These
Whisper is a multilingual encoder-decoder auto-         labels were used to annotate a synthetic training
matic speech recognition (ASR) model developed          dataset for fine-tuning. SinBERT’s output pre-
by OpenAI, trained on 680,000 hours of supervised       dicts the error class for each sentence and guides
data across a wide range of languages and tasks         adaptive correction strategies, such as dynamic
(Radford et al., 2022). It supports zero-shot tran-     prompt formulation for mT5 or error-specific post-
scription, meaning it can recognize speech in un-       processing. SinBERT’s architectural strength and
derrepresented languages like Sinhala without ex-       language-aware training make it well-suited for
plicit fine-tuning. This is achieved through Whis-      classification tasks in Sinhala and other underrep-
per’s large-scale training on diverse, noisy audio      resented scripts.
data with multilingual transcriptions. For Sinhala         SinBERT’s predicted error category is used
transcription, Whisper internally uses a language       to adaptively guide the next stage of correction.
ID token to condition the decoder during inference,     Specifically, based on the identified error type

                                                    928

<a id="pdf-p5"></a>
### [PDF p.5] (e.g., omission, substitution, insertion, reversal),
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **5** / 9

(e.g., omission, substitution, insertion, reversal),
the system dynamically generates a task-specific
prompt to steer the mT5 model toward a more ap-
propriate correction strategy. For example, if an
omission is detected, the prompt may explicitly in-
struct the model to insert missing particles or char-
acters. This error-aware prompting approach im-
proves correction relevance and overall accuracy
across varied dyslexic patterns.
3.1.3    Grammatical Correction: mT5 +
         Mistral
The correction phase combines two powerful mod-
els for error correction.

  1. Stage 1 - mT5: Structural and Grammati-
     cal Correction (Xue et al., 2021) is used for
     grammatical correction using prompt-based
     text-to-text transformation.
     mT5, a multilingual text-to-text transformer,
     is used to perform core grammatical correc-
     tions such as fixing tense, agreement, syn-
     tactic errors, and structural phrasing. It op-
     erates on the transcribed text (or SinBERT-          Figure 2: Example of the correction process from
     annotated text), outputting a grammatically          dyslexic input to refined output using mT5 and Mistral.
     improved sentence that maintains the in-
     tended meaning.

  2. Stage 2 — Mistral: Fluency, Style, and
     Idiomatic Enhancement (Mistral AI, 2023),          lightweight and accessible Python library that in-
     a decoder-only transformer, refines the mT5        terfaces with Google’s multilingual TTS engine.
     output by enhancing fluency and preserving         gTTS supports Sinhala phoneme synthesis, allow-
     natural phrasing.                                  ing the system to vocalize corrected sentences
     The output from mT5 is then passed to Mis-         clearly an essential feature for adults with dyslexia
     tral, a decoder-only transformer designed for      who struggle with reading comprehension.
     text generation with stylistic fluency. Mistral
     refines the mT5 output by enhancing natural             Despite its limited expressiveness (e.g., lack of
     phrasing, idiomatic expressions, and improv-         pitch control, emotion, or emphasis), gTTS was
     ing readability while preserving semantic in-        selected due to its ease of integration, low re-
     tegrity.                                             source usage, and native support for Sinhala. It
   This dual-model pipeline ensures both syntac-          allows for fast audio generation without requiring
tic correctness and stylistic naturalness. Figure 2       local model deployment, making it ideal for real-
illustrates the end-to-end correction process us-         time applications on both web and mobile plat-
ing a real example. This dual-model pipeline en-          forms. The generated audio is directly streamed
sures both syntactic correctness and stylistic qual-      to the frontend, closing the feedback loop and en-
ity. mT5 was selected for its ability to generalize       abling auditory reinforcement, which is known to
across languages, while Mistral enhances fluency          improve engagement and learning among dyslexic
using token-level instruction-following prompts.          users (Vats et al., 2020). While its lack of emo-
                                                          tional modulation and pitch control is a limitation,
3.1.4 Text-to-Speech: gTTS Sinhala Playback               its quick turnaround time and native web/mobile
The final corrected sentence is converted into            support make it suitable for real-time feedback in
audio using Google Text-to-Speech (gTTS), a               this context.

                                                    929

<a id="pdf-p6"></a>
### [PDF p.6] 3.2 Design goals https://github.com/PeshalaPerera/sinhala-
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **6** / 9

3.2    Design goals                                             https://github.com/PeshalaPerera/sinhala-
The system was designed to be inclusive, efficient,             dyslexia-assistant
and adaptable for real-time Sinhala language assis-
tance, particularly supporting adults with dyslexia.          • Dataset Access: The Sinhala dyslexic
It aims to provide accurate feedback quickly, using             error dataset (3,000 samples) used for train-
lightweight models suitable for low-resource envi-              ing and evaluation is hosted on Hugging Face:
ronments.                                                       https://huggingface.co/datasets/peshalaperera/
                                                                sinhala-dyslexia-assistant-articulation-errors
4     Evaluation Setup
                                                              These resources are released under open li-
4.1    Dataset                                              censes to facilitate future research and develop-
To address the lack of dyslexic Sinhala corpora,            ment in inclusive language technologies for under-
a 3000-sample parallel dataset was created using            represented languages.
the OpenSLR SLR63 Sinhala Read Speech cor-
pus as the base. Clean sentences were modified              4.4 Metrics used
using rule-based transformations (substitution, in-         4.4.1 BLEU and GLEU for Correction
sertion, omission, reversal) to simulate dyslexic er-             Quality
rors. Each dyslexic variant was paired with its orig-
                                                        To assess the grammatical and semantic accuracy
inal sentence, and corresponding audio paths were
                                                        of corrected sentences, BLEU (Papineni et al.,
preserved for STT evaluation.
                                                        2002) and GLEU (Wu et al., 2016) metrics were
    Source       OpenSLR-SLR63      Sinhala   Read      employed. BLEU captures n-gram precision,
    Corpus       Speech                                 whereas GLEU incorporates both precision and re-
    Final        3000                                   call, making it more suitable for grammatical error
    Samples                                             correction tasks with short sentence lengths.
    Error        Substitution, Insertion, Omission,         4.4.2 Word Error Rate (WER) for STT
    Types        Reversal                                         Accuracy
    Split        80% Train / 20% Test (stratified)
    Audio        FLAC, resampled to 16 kHz              WER was used to evaluate the Whisper model’s
    Format                                              transcription accuracy. It is defined as follows,

          Table 1: Custom Dataset Overview                                          S+D+I
                                                                          WER =
                                                                                      N

4.2    Data Split                                              where S is the number of substitutions, D dele-
                                                            tions, I insertions, and N is the number of words
The dataset was split into training (80%) and test-
                                                            in the reference sentence. Whisper achieved an av-
ing (20%) subsets using stratified sampling by er-
                                                            erage WER of 34%, resulting in an effective ac-
ror type. This ensured balanced evaluation across
                                                            curacy of 66%, which aligns with expected perfor-
all four error categories. Audio samples were re-
                                                            mance in zero-shot Sinhala transcription (Radford
sampled to 16 kHz for Whisper-based transcription
                                                            et al., 2022).
benchmarking.

4.3    Public Access                                        4.5 Comparison with Baselines

To support transparency, reproducibility, and fur-      To validate the effectiveness of the full pipeline, re-
ther research in low-resource assistive NLP, both       sults were compared against three baseline models.
the codebase and dataset used in this study have           These results demonstrate that the combination
been made publicly available:                           of error classification and hybrid correction signifi-
                                                        cantly outperformed both isolated correction meth-
     • Code Repository:       The complete im-          ods and rule-based strategies. Additionally, the
       plementation of the proposed system,             use of Mistral for stylistic fluency improved the
       including preprocessing, model integration,      readability of outputs as confirmed by human eval-
       and prototype interface, is accessible at:       uators.

                                                      930

<a id="pdf-p7"></a>
### [PDF p.7] Model Description mT5-small + Mistral API
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **7** / 9

Model       Description                                             mT5-small + Mistral API
    Variant                                                             Metric          Score
    Rule-       Uses basic word substitutions via                       BLEU            0.359
    Based       dictionary logics.                                      GLEU            0.575
    mT5     +   Full NLP pipeline combining mT5-                        Accuracy         0.70
    Mistral     based correction and Mistral refine-                    WER             0.322
                ment.                                                   Edit Distance    1.66

Table 2: Baseline Model Variants for Correction Com-                         Whisper-Sinhala
parison
                                                                           Metric        Score
                                                                           BLEU          0.279
5     Results                                                              GLEU          0.444
                                                                           Accuracy      0.659
This section presents the quantitative and qual-                           WER           0.333
itative results obtained from evaluating the sys-                          Edit Distance 0.545
tem across its three core modules: speech-to-text
(STT), error classification, and grammatical error       Table 3: Evaluation metrics for text correction and
correction. The evaluation demonstrates the effec-       speech transcription modules in the Sinhala Dyslexia
tiveness of the proposed model pipeline and high-        Assistant pipeline.
lights key strengths of the integrated approach.
                                                             5.3 Evaluation Results
5.1     Performance Scores
                                                             Figure 3 illustrates the average performance of the
5.1.1    Speech-to-Text (STT)
                                                             text correction module across key NLP evaluation
The Whisper model, used in zero-shot mode for                metrics.
Sinhala ASR, achieved a 66% accuracy, measured
by a Word Error Rate (WER) of 34% across the
600 testing audio samples. While Whisper was not
fine-tuned specifically on Sinhala, its multilingual
training enabled high baseline performance, even
in phonetically complex utterances.

5.1.2    Correction Module
The final correction output, combining mT5 and
Mistral, reached a accuracy of 70% and a GLEU                Figure 3: Text correction performance using BLEU,
score of 57% on the test set. Human evalua-                  GLEU, Accuracy, WER, and Edit Distance averaged
tion also confirmed high readability and semantic            over 600 test samples.
preservation of the corrected outputs.

5.1.3    Overall System                                      5.4 Prototype Interface
The combined evaluation of all components                To demonstrate real-world usability, a working
speech-to-text transcription, error correction,          prototype was developed using a web-based inter-
yielded an overall system accuracy of 65%. This          face. This interface supports accessibility and re-
metric reflects the end-to-end performance of the        inforces learning through multimodal feedback, as
full pipeline, from voice input to corrected speech      shown in Figure 4.
output.
                                                             5.5 Latency and Real-Time Performance
5.2     Table of Evaluation Metrics                          Each component was benchmarked for average in-
Table 3 shows that the mT5-small + Mistral model             ference time on a consumer-grade laptop (Intel i5,
gave good correction results with 70% accuracy.              8GB RAM).
Whisper-Sinhala also gave good speech-to-text re-            • Whisper STT: 1.2 seconds (per 5s audio)
sults with 65.9% accuracy, showing that both parts           • SinBERT Classification: 60 ms
work well together in the system.                            • mT5 + Mistral Correction: 900 ms

                                                       931

<a id="pdf-p8"></a>
### [PDF p.8] likely with domain-specific fine-tuning. Addition-
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **8** / 9

likely with domain-specific fine-tuning. Addition-
                                                          ally, although gTTS provides basic Sinhala TTS
                                                          functionality, it lacks emotion and pitch control—
                                                          features critical for adult comprehension, and cur-
                                                          rently, there are no expressive open-source Sinhala
                                                          voice models available to fill this gap.

                                                          7 Conclusion and Future Work

Figure 4: Prototype interface showing corrected Sin-    This study introduces the first real-time NLP-
hala sentence with playback and recording controls.     based assistive system designed specifically for
                                                        Sinhala-speaking adults with dyslexia, an under-
                                                        served population in both language technology and
• gTTS Audio Generation: 300 ms                         accessibility research. The system features a mod-
   The entire pipeline runs in 2.5 seconds per input,   ular pipeline incorporating Whisper for speech-to-
making it viable for real-time use in interactive ap-   text, SinBERT for dyslexia-related error detection,
plications, especially on mobile devices.               mT5 and Mistral for correction, and gTTS for text-
5.6    Error Analysis                                   to-speech output. Despite the challenges of work-
                                                        ing with simulated data and limited linguistic re-
Although the system demonstrates high correc-           sources, the system achieved 66% speech-to-text
tion accuracy, it occasionally overcorrects rare id-    accuracy and 61% correction accuracy, demon-
iomatic expressions or misclassifies ambiguous          strating strong performance in a low-resource set-
omissions. Future work will address these via user      ting. This work addresses a notable gap at the
feedback loops and targeted fine-tuning.                intersection of assistive NLP, speech technology,
6     Discussion                                        and Sinhala language computing, with the poten-
                                                        tial to benefit both academic research and real-
The development and evaluation of the Sinhala           world accessibility. Looking ahead, future efforts
Dyslexia Assistant system reveal several promis-        will focus on implementing personalized correc-
ing outcomes, along with known constraints and          tion mechanisms based on user-specific error his-
avenues for further advancement. The system             tory and establishing collaborations with educa-
demonstrates real-world utility by delivering cor-      tional and healthcare institutions in Sri Lanka to
rected audio feedback in under 2.5 seconds, en-         support broader deployment and local adaptation.
abling real-time use and supporting immediate
learning for dyslexic users. Its modular archi-           Limitation
tecture, comprising discrete components for STT,
classification, correction, and TTS offers multiple     While the proposed system demonstrates promis-
advantages, including independent upgrades, eas-        ing results in a low-resource language setting, sev-
ier debugging and testing, and customisation po-        eral limitations that impact its overall effective-
tential for future multilingual deployments. The        ness and user experience remain. Firstly, the use
REST API-based modular design further enhances          of synthetic data for model training, although nec-
its ability to integrate with external learning plat-   essary due to data scarcity, may not fully cap-
forms and accessibility services.                       ture the nuances of real-world dyslexic writing pat-
   Despite these strengths, the system faces no-        terns. This limits the model’s ability to gener-
table challenges. Sinhala lacks large-scale anno-       alize to authentic user input. Secondly, the cur-
tated datasets for grammatical correction or error      rent text-to-speech component, implemented using
classification, limiting the effectiveness of mod-      gTTS, lacks prosody and emotional tone, resulting
els trained solely on real-world data. To address       in a less engaging auditory experience for users.
this, the system relies on synthetic dyslexic er-       Lastly, the system does not yet support personal-
rors generated from the SLR63 dataset, although         ization or maintain user history, which restricts its
these may not fully capture the diversity of real       ability to adapt to individual error patterns over
user patterns. While Whisper performs well in its       time.
current implementation, further improvements are

                                                    932

<a id="pdf-p9"></a>
### [PDF p.9] References D. D. Perera et al. 2022. Sinbert: A transformer-based
- Locator: `R473-a-low-resource-speech-driven-nlp-pipeline-for-sinhala-dyslexia-assistance.pdf` · página **9** / 9

References                                                      D. D. Perera et al. 2022. Sinbert: A transformer-based
                                                                  language model for sinhala. In Proceedings of the
Ahmed Al-Azawei, Filippo Serenelli, and Karsten                   Asian NLP Workshop.
  Lundqvist. 2016. Universal design for learning (udl):
  A content analysis of peer-reviewed journal papers            Peshala Perera and Deshan Sumanathilaka. 2025. Re-
  from 2012 to 2015. Journal of the Scholarship of                cent trends and challenges in assistive applications
  Teaching and Learning, 16(3):39–56.                             for sinhala-speaking adults with dyslexia: A decade
                                                                  in review. In Proceedings of the 5th International
A. Al-Wabil, P. Zaphiris, and S. Wilson. 2007. Web                Conference on Advanced Research in Computing
  navigation for individuals with dyslexia: An ex-                (ICARC). IEEE.
  ploratory study. Universal Access in the Information
  Society.                                                      Alec Radford et al. 2022. Robust speech recognition
                                                                  via whisper. OpenAI Technical Report.
Christopher Bryant, Mariano Felice, and Ted Briscoe.
  2022. Grammatical error correction: A survey.                 Luz Rello and Ricardo Baeza-Yates. 2013. Good fonts
  Computational Linguistics.                                      for dyslexia. In Proceedings of the 15th Interna-
                                                                  tional ACM SIGACCESS Conference on Computers
Chi Hong Chau, Dian Yu, and Zhaopeng Tu. 2021.                    and Accessibility (ASSETS).
  Improving grammatical error correction via pre-
  training a copy-augmented architecture with unla-             Yi Ren, Chenxu Hu, Xu Tan, Tao Qin, Sheng Zhao,
  beled data. In EMNLP.                                           and Tie-Yan Liu. 2020. Fastspeech 2: Fast and high-
                                                                  quality end-to-end text to speech. In NeurIPS.
D. De Silva. 2024. Challenges in sinhala nlp and speech
   systems. In Proceedings of NLP4Low.                          Julie Roitsch and Linda Watson. 2019. Dyslexia and
                                                                   language processing: Implications for adult learning
C. Goodman, S. Kahta, and R. Schiff. 2022. Digital                 and assessment. Journal of Learning Disabilities,
   inclusion for adults with dyslexia. Assistive Technol-          52(4):345–356.
   ogy Journal.
                                                                G. Rupasinghe, K. Karunanayaka, and R. Pushpananda.
Michael Heilman, Kevyn Collins-Thompson, Jamie                     2020. Arunalu: Learning ecosystem to overcome
  Callan, and Maxine Eskenazi. 2006. Classroom as-                 sinhala reading weakness due to dyslexia. In Pro-
  sistive technology: Providing feedback for writing.              ceedings of the International Conference on Ad-
  In Proceedings of the Human Language Technology                 vances in ICT for Emerging Regions (ICTer).
  Conference of the NAACL.
                                                                M. Sadusky, R. O’Reilly, and H. Tanaka. 2021. Adult
Dinesh Herath, Hansi Hettiarachchi, and Surangika                 dyslexia: An overlooked population. Applied Lin-
  Ranathunga. 2020. Sinhala spell checker using neu-              guistics and Special Education.
  ral networks. In Proceedings of NLP4LRC.
                                                                K. Santhiya, R. Perera, and D. De Silva. 2023. Early de-
Svanhvít Lilja Ingólfsdóttir, Pétur Orri Ragnarsson,               tection of dyslexia in south asian contexts. Journal
  Haukur Páll Jónsson, Haukur Barri Símonarson, Vil-               of Learning Disabilities.
  hjálmur Þorsteinsson, and Vésteinn Snæbjarnarson.
  2023. Byte-level grammatical error correction using           Parth Vats, Anish Narayanan, and Mohit Bansal.
  synthetic and curated corpora.                                  2020. Evaluating text-to-speech for low-resource
                                                                  languages. In Proceedings of Interspeech.
Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Man-
  dar Joshi, Danqi Chen, Omer Levy, Mike Lewis,                 Sarah G. Wood, J. H. Moxley, E. L. Tighe, and R. K.
  Luke Zettlemoyer, and Veselin Stoyanov. 2019.                   Wagner. 2018. Does use of text-to-speech and re-
  Roberta: A robustly optimized bert pretraining ap-              lated read-aloud tools improve reading comprehen-
  proach. arXiv preprint arXiv:1907.11692.                        sion for students with reading disabilities? Review
                                                                  of Educational Research, 88(3):358–388.
Mistral AI. 2023. Mistral-7b technical report. https:
                                                                Shijie Wu and Mark Dredze. 2020. Are all languages
  //mistral.ai/news/announcing-mistral-7b/.
                                                                  created equal in multilingual bert? In ACL.
Kostiantyn Omelianchuk, Viacheslav Atrasevich, and
                                                                Yonghui Wu, Mike Schuster, Zhifeng Chen, et al. 2016.
  Artur Belov. 2020. Gector – grammatical error cor-
                                                                  Google’s neural machine translation system: Bridg-
  rection: Tag, not rewrite. In BEA Workshop at ACL.
                                                                  ing the gap between human and machine translation.
Kishore Papineni, Salim Roukos, Todd Ward, and Wei-               arXiv preprint, arXiv:1609.08144.
  Jing Zhu. 2002. Bleu: A method for automatic eval-            Linting Xue, Noah Constant, Adam Roberts, et al. 2021.
  uation of machine translation. In Proceedings of the            mt5: A massively multilingual pre-trained text-to-
  40th Annual Meeting of the Association for Compu-               text transformer. In Proceedings of NAACL.
  tational Linguistics (ACL), pages 311–318.
                                                                Shaohua Zhang, Haoran Huang, Jicong Liu, and Hang
R. Patnoorkar et al. 2023. Assistive technology adop-             Li. 2020. Spelling error correction with soft-masked
   tion for dyslexia: A global review. Education Tech-            bert.
   nology Journal.

                                                          933
