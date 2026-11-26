# Human factors, physical interaction, and standards boundaries

Use for touchscreens, controls, posture, perception, workload, accessibility-related ergonomics, industrial interfaces, or machinery questions. Enter substantive review directly; do not block on a mode questionnaire.

## 1. Context before thresholds

Identify the actual user, task, environment, equipment, and consequence of error:

- gloves, footwear, hand dominance, mobility, reach, strength, and expertise;
- lighting, glare, vibration, noise, temperature, contamination, and motion;
- screen orientation, viewing distance, mounting, occlusion, and one-handed use;
- task frequency, urgency, fatigue, time pressure, and training;
- feedback, error recovery, and whether a control is safety-related.

A physical dimension is not an overall experience verdict. A larger target may reduce selection error while increasing reach or visual crowding; a smaller target may be acceptable only under specific observed conditions.

## 2. Reproducible physical calculations

Separate known inputs, assumptions, and unknowns. For a display:

- pixel pitch in mm/pixel = diagonal in inches × 25.4 ÷ diagonal in pixels;
- diagonal in pixels = √(horizontal pixels² + vertical pixels²);
- PPI = diagonal in pixels ÷ diagonal in inches.

A visual button of `w × h` pixels corresponds to `w × pixel pitch` by `h × pixel pitch` only under the stated scaling, resolution, orientation, and 1:1 physical-pixel assumptions. It is not the usable touch-response area.

Label controller hitboxes, scaling, OS/browser coordinate transforms, bezel/occlusion, palm rejection, and multi-touch behavior as unknown until inspected or measured.

Do not calculate from a diagonal size alone if the active area or aspect ratio is uncertain. Show the formula and rounded result; do not imply laboratory precision.

## 3. Touch and interaction evaluation

Assess at least:

- visual legibility and semantic recognition;
- effective hit area and spacing, including edge effects;
- accidental activation and neighboring-target errors;
- selection time, errors, and recovery in representative tasks;
- feedback and state visibility;
- glove/contact effects and environmental interference;
- accessibility and alternative input paths.

Do not attribute a universal millimeter threshold to ISO, IEC, or “industry practice” without an inspected applicable source. No fixed target size guarantees safety or usability across contexts.

When physical parameters or users are unavailable, propose a targeted test rather than inventing a numeric pass/fail criterion. Record task, device, participant characteristics, errors, near-misses, assistance, and recovery.

## 4. Cognitive and organizational factors

Use theory to generate testable explanations, not to decorate conclusions:

- mental models and signifier–feedback mismatch;
- attention, working memory, and cognitive load;
- slips versus mistakes and error recovery;
- trust, perceived control, and automation dependence;
- body mechanics, reach, posture, and fatigue;
- procedures, training, staffing, and production pressure.

Do not claim that a mechanism occurred in the real user group without observation. Expert walkthroughs identify risks and hypotheses, not user prevalence.

## 5. Standards and legal authority

Distinguish:

1. binding law or regulation in the applicable jurisdiction;
2. contractual or organizational requirements;
3. voluntary standards and guidelines;
4. research findings and validated instruments;
5. heuristics, expert judgment, and design hypotheses.

Before citing a standard, verify the current edition, amendments, scope, definitions, and exact clauses in an authoritative source. Record retrieval date and applicability. A standard's legal force depends on jurisdiction and adoption.

Official starting points verified for this local pilot on 2026-11-25:

- [ISO 9241-11:2018 — usability framework](https://www.iso.org/standard/63500.html). It provides a conceptual framework; it does not prescribe a universal task-success/time formula or fixed interface dimensions.
- [ISO 9241-920:2024 — tactile and haptic interactions](https://www.iso.org/standard/80751.html). Inspect scope and current edition before applying it; do not assume it contains a universal touch-target threshold.
- [ISO 13850:2015 — emergency stop function](https://www.iso.org/standard/59970.html). This concerns machinery emergency-stop design, not ordinary touchscreen usability.
- [IEC 60204-1:2016 + AMD1:2021](https://webstore.iec.ch/en/publication/66124). Check the applicable consolidated edition and machine context.
- [IEC 60947-5-5:2026](https://webstore.iec.ch/en/publication/69111). Check current edition, scope, and local adoption; do not mix it with ordinary UI touch-target guidance.

These links establish official publication records, not a completed compliance assessment. Do not reproduce copyrighted standard text or invent clauses.

## 6. Safety-related controls

Do not equate an ordinary touchscreen button with a compliant emergency stop or safety-rated control. Safety functions require machine risk assessment, applicable functional-safety processes, hardware/control-system validation, and authorized expert review.

When a question involves hazardous motion, emergency response, medical use, or injury risk, state the boundary and escalate to the responsible safety/compliance owner. Do not provide a design sign-off.

## 7. Output structure

Lead with the context-specific judgment. Then provide:

- known parameters and reproducible calculations;
- plausible interaction or human-factor mechanisms;
- credible counterexamples;
- what requires measurement;
- standards/legal status and verification gaps;
- smallest feasible verification plan;
- decision consequence and owner.

Keep “design suggestion,” “research evidence,” “standard requirement,” and “legal approval” visibly distinct.
