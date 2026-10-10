---
lab2_edge_cases:
  E1: {rule: R-08, count: 3}
  E2: {rule: R-06, count: 2}
  E3: {rule: R-09, count: 4}
  E4: {rule: R-10, count: 4}
  E5: {rule: R-12, count: 1}
  E6: {rule: R-13, count: 11}
---
<!-- ai-generated: 90% - AI drafted the explanations from the specification and practice log; student should review. -->

# Edge cases in the practice event log

## E1 - clock skew produces a negative lead time

- What the log contains: Three commit and successful deployment pairs have the commit timestamp later than the delivery timestamp.
- What a default definition would have done: Dropping negative samples would hide three clock-skewed deliveries and make the median look selectively cleaner.
- Why the rule is defensible: Keeping each pair at zero preserves the shipped work while avoiding an impossible negative elapsed duration.

## E2 - a revert of a revert

- What the log contains: Two commits are revert commits, including a revert that points through another revert to the original change.
- What a default definition would have done: Counting every revert as new work would inflate distinct changes and distort delivery volume.
- Why the rule is defensible: Revert chains describe undoing and restoring the same change, so their identity belongs to the original work.

## E3 - a hotfix that never touched `main`

- What the log contains: Four distinct off-main commit shas are carried by production deployments inside the observation window.
- What a default definition would have done: Filtering to the main branch would omit these shipped hotfixes and understate measured lead-time pairs.
- Why the rule is defensible: Production delivery is the relevant boundary; branch naming does not determine whether users received the change.

## E4 - a deployment with zero linked commits

- What the log contains: Four in-window production deployments have empty commit lists but still have deployment records and outcomes.
- What a default definition would have done: Ignoring them would undercount release frequency and shrink the denominators for instability rates.
- Why the rule is defensible: A deployment happened even when its change links are missing, so operational activity and its outcome remain measurable.

## E5 - a deployment that failed and never recovered

- What the log contains: One in-window failed deployment has no covering incident with a recorded resolution.
- What a default definition would have done: Inventing a recovery at the end of the window would claim a resolution that the event log never records.
- Why the rule is defensible: The failure remains visible in the failure rate, while a recovery duration is reported only when a recovery instant exists.

## E6 - overlapping incidents

- What the log contains: Eleven unordered incident pairs have intersecting intervals, including incidents that cover the same failed deployment.
- What a default definition would have done: Merging intervals or summing their duration would confuse incident overlap with the time to recover each deployment.
- Why the rule is defensible: Recovery belongs to each failed deployment; independent incident records should remain separate and auditable.

## Gaming demonstration

I improved `deployment_frequency_per_day` under R-11 by moving two successful multi-change deployments past the window and adding thirteen empty production deployment records. The dashboard then counts 53 deployments in the same 21 days, crossing the 25% improvement threshold, while filtering to the original work shows that only 58 of the original 65 changes were delivered in-window. In a real team, an incentive tied to frequent releases could encourage splitting or recording deployments while allowing valuable work to wait. The team lead or delivery manager whose score is tied to the frequency target would be rewarded, while users waiting for the delayed changes would bear the cost.
