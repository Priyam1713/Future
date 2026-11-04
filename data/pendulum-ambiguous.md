# Pendulum — symbolic response

Profile: lonegren-web-symbolic-response-v1

Mode: manual. User-reported observations.

Question/context: What perspectives could help me reflect?

## Configuration

```json
{
  "mapping": {
    "clockwise": "yes",
    "counterclockwise": "no"
  },
  "complete": true,
  "missing_responses": [],
  "coverage": "user_declared_symbolic_mapping",
  "truth_validated": false
}
```

1. Reported searching (full); calibrated None; symbolic unresolved. Reasons: neutral_or_unclear_signal, unmapped_signal.

2. Reported still (full); calibrated None; symbolic unresolved. Reasons: neutral_or_unclear_signal, unmapped_signal.

Symbolic response: **unresolved**; resolved: False; conflicting: False. Reasons: neutral_or_unclear_signal, unmapped_signal.

Symbolic category only;not factual assurance

Modern editorial reflection: Keep the question open. Clarify the wording or the recorded signals;do not force a binary conclusion.

## Source-grounded procedural context

- The source starts with to-and-fro motion as a search state. Source: pendulum-lonegren-web-procedure-v1; The Search Position; pendulum.lonegren.search.

- Individual signals are permitted; suggested circular signals are a fallback,not universal. Source: pendulum-lonegren-web-procedure-v1; Yes and No; pendulum.lonegren.calibration.

- Incomplete responses call for clarification rather than a complete answer. Source: pendulum-lonegren-web-procedure-v1; Yes but and No but; pendulum.lonegren.partial.

- A separate misleading-question signal prompts reconsideration. Source: pendulum-lonegren-web-procedure-v1; Yes but and No but; pendulum.lonegren.rethink.

- Questions should admit a clear binary response;ambiguous wording matters. Source: pendulum-lonegren-web-procedure-v1; Asking questions through dowsing - The Eight Step Method,step5; pendulum.lonegren.question.

- The source suggests known-answer checking;this does not establish predictive validity. Source: pendulum-lonegren-web-procedure-v1; Dowsing blind;Checking and building confidence; pendulum.lonegren.checking.

[Author-associated procedure](https://www.geomancy.org/index.php/dowsing/the-pendulum)

## Limits

Search state depends on declared calibration/context;vertical alone is not a universal yes or search signal Calibration maps symbols;it does not validate factual answers Digital results are categories,not generated movement or physical ideomotor simulation No factual assurance,hidden events,health/financial advice,personality/emotional inference or confidence scores

No engine-observed motion or truth confidence.

## Exact replay metadata

```json
{
  "request": {
    "schema_version": 1,
    "profile": "lonegren-web-symbolic-response-v1",
    "task": "symbolic_response",
    "mode": "manual",
    "calibration": [
      {
        "signal": "clockwise",
        "response": "yes"
      },
      {
        "signal": "counterclockwise",
        "response": "no"
      }
    ],
    "observations": [
      {
        "signal": "searching"
      },
      {
        "signal": "still"
      }
    ],
    "question": "What perspectives could help me reflect?"
  },
  "profile": "lonegren-web-symbolic-response-v1",
  "profile_sha256": "54e6e4ea860a73511c6a377d6e25e9f19fc3aecb7c8bba7b43eb97a23674686b",
  "source_id": "pendulum-lonegren-web-procedure-v1",
  "protocol": null,
  "seed": null,
  "simulation": null,
  "calibration": {
    "mapping": {
      "clockwise": "yes",
      "counterclockwise": "no"
    },
    "complete": true,
    "missing_responses": [],
    "coverage": "user_declared_symbolic_mapping",
    "truth_validated": false
  },
  "aggregation": "Unanimous full resolved responses only;any partial,missing,neutral,unknown or disagreement makes session unresolved. No voting or confidence estimate.",
  "generated_response": null,
  "generated_signal": null,
  "physical_motion_generated": false,
  "question_in_rng": false
}
```

