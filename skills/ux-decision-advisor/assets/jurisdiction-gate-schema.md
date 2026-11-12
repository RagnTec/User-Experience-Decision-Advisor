# Optional private Constraint Gate Record (v0.4D.1)

For decisions with a material external rule or proposed convention exception, the Agent **may** write a JSON record to an authorized private output path. This is a general illustrative audit structure; no user is required to fill it for an ordinary chat, and it must never be populated from a real internal project inside the public repo.

```json
{
  "scope": {
    "jurisdictions": ["Example Country"],
    "product_category": "generic consumer accessory",
    "stage": "concept_review",
    "effective_date_context": "2026-10-27"
  },
  "constraints": [
    {
      "id": "N1",
      "category": "INDUSTRY_CONVENTION",
      "applicability": "POSSIBLE",
      "verification": "UNVERIFIED",
      "source_ref": "",
      "version_or_date": "",
      "impact": "A common design pattern may be disrupted",
      "proposed_action": "PROPOSE_DEVIATION",
      "human_review": {"status": "PENDING", "role": "Product and compliance owner"}
    }
  ],
  "decision": {
    "stage": "EXPLORATION_ONLY",
    "implementation_authorized": false,
    "claim_of_compliance": false
  }
}
```

Valid `category`: `BINDING_LAW`, `MANDATORY_STANDARD`, `VOLUNTARY_STANDARD`, `CONTRACT_OR_PLATFORM`, `INDUSTRY_CONVENTION`, `ORGANIZATION_RULE`.

`applicability`: `APPLIES`, `POSSIBLE`, `NOT_APPLICABLE`, `UNRESOLVED`. `verification`: `OFFICIAL_VERIFIED`, `USER_DOCUMENT_ONLY`, `UNVERIFIED` (an *agent* must not equate `USER_DOCUMENT_ONLY` to current official verification). `proposed_action`: `FOLLOW`, `VERIFY`, `PROPOSE_DEVIATION`, `ESCALATE`, `REDESIGN`, `STOP`. `human_review.status`: `NOT_REQUESTED`, `PENDING`, `APPROVED`, `REJECTED`. `decision.stage`: `EXPLORATION_ONLY`, `CONDITIONAL_RECOMMENDATION`, `HOLD_FOR_SPECIALIST`, `READY_FOR_HUMAN_DECISION`, `STOP_CONFLICT`.

The optional checker rejects incorrect internal declarations (e.g., a purportedly legal exception or a convention deviation declared approved without a human reviewer). It **cannot** check whether a law exists, whether its scope is right, whether a human actually approved or whether a proposed deviation is safe. `implementation_authorized` and `claim_of_compliance` should remain `false` for agent-produced records. Keep the record outside all public source/install roots.
