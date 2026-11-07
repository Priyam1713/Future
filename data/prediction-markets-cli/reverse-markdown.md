# Prediction markets — offline binary LMSR play credits

```json
{
  "status": "accepted",
  "technique_id": 58,
  "schema_version": 1,
  "profile": {
    "id": "prediction-markets-binary-lmsr-play-money-v1",
    "version": 1,
    "sha256": "d36cca55bf080adabc57d6190820812802ec4386ffe5199676a6ef0b17aad000",
    "catalog_sha256": "e36ed82d53463ad118427a7825c22e293d6a1cec15fd587bb5f55b8de72f36b1"
  },
  "request": {
    "schema_version": 1,
    "profile": {
      "id": "prediction-markets-binary-lmsr-play-money-v1",
      "version": 1,
      "sha256": "d36cca55bf080adabc57d6190820812802ec4386ffe5199676a6ef0b17aad000",
      "catalog_sha256": "e36ed82d53463ad118427a7825c22e293d6a1cec15fd587bb5f55b8de72f36b1"
    },
    "market": {
      "id": "market1",
      "version": 1,
      "question_id": "question1",
      "question_version": 1,
      "event_id": "event1",
      "definition": "Does synthetic event1 occur?",
      "positive_rule": "YES pays1playcredit per recordedshare",
      "negative_rule": "NO pays1playcredit per recordedshare",
      "outcomes": [
        "YES",
        "NO"
      ],
      "exhaustive": true,
      "created_at": "2025-01-01T00:00:00Z",
      "close_at": "2025-01-10T00:00:00Z",
      "resolver": "admin",
      "liquidity": "1",
      "money_unit": "play_credit"
    },
    "accounts": [
      {
        "id": "alice",
        "initial_credit": "10"
      },
      {
        "id": "bob",
        "initial_credit": "10"
      }
    ],
    "events": [
      {
        "id": "e1",
        "type": "quote",
        "at": "2025-01-02T00:00:00Z",
        "actor": "alice",
        "quote_id": "quote1",
        "outcome": "YES",
        "delta": "1"
      },
      {
        "id": "e2",
        "type": "execute",
        "at": "2025-01-02T00:01:00Z",
        "actor": "alice",
        "quote_id": "quote1"
      },
      {
        "id": "e3",
        "type": "quote",
        "at": "2025-01-03T00:00:00Z",
        "actor": "alice",
        "quote_id": "quote3",
        "outcome": "YES",
        "delta": "-1"
      },
      {
        "id": "e4",
        "type": "execute",
        "at": "2025-01-03T00:01:00Z",
        "actor": "alice",
        "quote_id": "quote3"
      }
    ],
    "provenance": {
      "synthetic": true,
      "source_ref": "prediction-markets-cost-function-v1",
      "rights": "self_authored",
      "attribution": "Future original synthetic play-credit example",
      "snapshot": "Original fictional LMSR play-credit ledger; no actual money or traders.",
      "snapshot_sha256": "e61decf19b247c86d53c92ac181ef7f671ab25716bb00e472abac61806d4b35d"
    }
  },
  "input_sha256": "8b74e1f078812387253818df520f2242561991e940b8d808db083d9d55e6da8b",
  "market_sha256": "2d448c5398ac9710c09a53ca1617fa287d12112852b6a62c33381356fdb5fdbb",
  "initial_accounts_sha256": "2cbdf914f4e819ae9e8c95bd3bcca5a4a9568b132cf5671f99b79b16cbafc2d6",
  "schema_sha256": "6e43a8abb1eca937618430509d341e5ee42d167741fdd5ca8ae37a6264493800",
  "source_manifest_sha256": "e36ed82d53463ad118427a7825c22e293d6a1cec15fd587bb5f55b8de72f36b1",
  "source_freeze_sha256": "ad9ed7d6709b65be7f17c66dc3ba59fdf625ee46e995975de671e725e61e06f9",
  "code_sha256": "7bde9e5304e3c0f3d2b87ddae17b792d758e75c448f968f5629f3245a0daf1b5",
  "initial": {
    "q": {
      "YES": "0",
      "NO": "0"
    },
    "accounts": {
      "alice": {
        "cash": "10",
        "positions": {
          "YES": "0",
          "NO": "0"
        }
      },
      "bob": {
        "cash": "10",
        "positions": {
          "YES": "0",
          "NO": "0"
        }
      }
    },
    "maker_cash": "0.693147180559945309417235",
    "maker_reserve": "0.693147180559945309417235",
    "net_charges": "0",
    "total_payout": "0"
  },
  "final": {
    "q": {
      "YES": "0",
      "NO": "0"
    },
    "accounts": {
      "alice": {
        "cash": "10",
        "positions": {
          "YES": "0",
          "NO": "0"
        }
      },
      "bob": {
        "cash": "10",
        "positions": {
          "YES": "0",
          "NO": "0"
        }
      }
    },
    "maker_cash": "0.693147180559945309417235",
    "maker_reserve": "0.693147180559945309417235",
    "net_charges": "0",
    "total_payout": "0",
    "market_status": "open",
    "winning_outcome": null,
    "settled": false,
    "economic_revision": 2,
    "executed_trades": 2,
    "settlements": 0,
    "charges": [
      "0.620114506958277524631763",
      "-0.620114506958277524631763"
    ],
    "realized_maker_profit": null,
    "remaining_payout_liability": "0",
    "ideal_loss_bound_approx": "0.69314718055994530941723212145817656807550013436025525412068000949339362196969472",
    "funded_loss_bound": "0.693147180559945309417235",
    "worst_modeled_loss_before_settlement": "0",
    "raw_cost_approx": "0.69314718055994530941723212145817656807550013436025525412068000949339362196969472",
    "rounded_cost_potential": "0.693147180559945309417232",
    "modeled_prices": {
      "YES": "0.5",
      "NO": "0.5"
    },
    "price_scope": "Historical model diagnostics; not executable after market close/resolution"
  },
  "trace": [
    {
      "index": 0,
      "event": {
        "id": "e1",
        "type": "quote",
        "at": "2025-01-02T00:00:00Z",
        "actor": "alice",
        "quote_id": "quote1",
        "outcome": "YES",
        "delta": "1"
      },
      "intent_sha256": "dcfda2c30a24a756026c495b45383bf5cf5aa510972e221e0a178248df308095",
      "decision": "quoted",
      "reason": null,
      "data": {
        "receipt": {
          "id": "quote1",
          "actor": "alice",
          "outcome": "YES",
          "delta": "1",
          "created_at": "2025-01-02T00:00:00Z",
          "economic_revision": 0,
          "q_before": {
            "YES": "0",
            "NO": "0"
          },
          "q_after": {
            "YES": "1",
            "NO": "0"
          },
          "potential_before": "0.693147180559945309417232",
          "potential_after": "1.313261687518222834048995",
          "charge": "0.620114506958277524631763",
          "modeled_prices_before": {
            "YES": "0.5",
            "NO": "0.5"
          },
          "modeled_prices_after": {
            "YES": "0.73105857863000487925115924182183627436514464016505651927636590791904045307020464",
            "NO": "0.26894142136999512074884075817816372563485535983494348072363409208095954692979536"
          },
          "executable_now": true,
          "feasibility_reasons": []
        },
        "receipt_sha256": "66ee710abd1e5150bf77eaed1d62354bb3886ff1ceaa6b5527ebee1f644a7688"
      },
      "clock_closed": false,
      "market_status_after": "open",
      "economic_revision_after": 0,
      "financial_before_sha256": "cb1a9149440ed799433cf4e3b020b8622b73065615a820eadceaa52e4b74e21d",
      "financial_after_sha256": "cb1a9149440ed799433cf4e3b020b8622b73065615a820eadceaa52e4b74e21d",
      "financial_after": {
        "q": {
          "YES": "0",
          "NO": "0"
        },
        "accounts": {
          "alice": {
            "cash": "10",
            "positions": {
              "YES": "0",
              "NO": "0"
            }
          },
          "bob": {
            "cash": "10",
            "positions": {
              "YES": "0",
              "NO": "0"
            }
          }
        },
        "maker_cash": "0.693147180559945309417235",
        "maker_reserve": "0.693147180559945309417235",
        "net_charges": "0",
        "total_payout": "0"
      }
    },
    {
      "index": 1,
      "event": {
        "id": "e2",
        "type": "execute",
        "at": "2025-01-02T00:01:00Z",
        "actor": "alice",
        "quote_id": "quote1"
      },
      "intent_sha256": "f9215dba9c6c3ed8429bfe65700932e3781512e05983a7f1536ef492e4884745",
      "decision": "executed",
      "reason": null,
      "data": {
        "ledger_entry_sha256": "64c64736f798a85270d543722ff8cffe7176e495a0b6cdbd133786a42fa5ce9f",
        "charge": "0.620114506958277524631763"
      },
      "clock_closed": false,
      "market_status_after": "open",
      "economic_revision_after": 1,
      "financial_before_sha256": "cb1a9149440ed799433cf4e3b020b8622b73065615a820eadceaa52e4b74e21d",
      "financial_after_sha256": "4c8e49b436e9f1c7edd66ca7bca7b7da4bc39d3f178d11ad01cb390542ec4ae9",
      "financial_after": {
        "q": {
          "YES": "1",
          "NO": "0"
        },
        "accounts": {
          "alice": {
            "cash": "9.379885493041722475368237",
            "positions": {
              "YES": "1",
              "NO": "0"
            }
          },
          "bob": {
            "cash": "10",
            "positions": {
              "YES": "0",
              "NO": "0"
            }
          }
        },
        "maker_cash": "1.313261687518222834048998",
        "maker_reserve": "0.693147180559945309417235",
        "net_charges": "0.620114506958277524631763",
        "total_payout": "0"
      }
    },
    {
      "index": 2,
      "event": {
        "id": "e3",
        "type": "quote",
        "at": "2025-01-03T00:00:00Z",
        "actor": "alice",
        "quote_id": "quote3",
        "outcome": "YES",
        "delta": "-1"
      },
      "intent_sha256": "152eba5d1c1c0ec44c36387ddd3154b194edb92e0c0de67a370ecef2065ae42c",
      "decision": "quoted",
      "reason": null,
      "data": {
        "receipt": {
          "id": "quote3",
          "actor": "alice",
          "outcome": "YES",
          "delta": "-1",
          "created_at": "2025-01-03T00:00:00Z",
          "economic_revision": 1,
          "q_before": {
            "YES": "1",
            "NO": "0"
          },
          "q_after": {
            "YES": "0",
            "NO": "0"
          },
          "potential_before": "1.313261687518222834048995",
          "potential_after": "0.693147180559945309417232",
          "charge": "-0.620114506958277524631763",
          "modeled_prices_before": {
            "YES": "0.73105857863000487925115924182183627436514464016505651927636590791904045307020464",
            "NO": "0.26894142136999512074884075817816372563485535983494348072363409208095954692979536"
          },
          "modeled_prices_after": {
            "YES": "0.5",
            "NO": "0.5"
          },
          "executable_now": true,
          "feasibility_reasons": []
        },
        "receipt_sha256": "21c8ac12a7c5c4196341f99c55ab9df6ef03a233fa9c447619dcf80fb815aa64"
      },
      "clock_closed": false,
      "market_status_after": "open",
      "economic_revision_after": 1,
      "financial_before_sha256": "4c8e49b436e9f1c7edd66ca7bca7b7da4bc39d3f178d11ad01cb390542ec4ae9",
      "financial_after_sha256": "4c8e49b436e9f1c7edd66ca7bca7b7da4bc39d3f178d11ad01cb390542ec4ae9",
      "financial_after": {
        "q": {
          "YES": "1",
          "NO": "0"
        },
        "accounts": {
          "alice": {
            "cash": "9.379885493041722475368237",
            "positions": {
              "YES": "1",
              "NO": "0"
            }
          },
          "bob": {
            "cash": "10",
            "positions": {
              "YES": "0",
              "NO": "0"
            }
          }
        },
        "maker_cash": "1.313261687518222834048998",
        "maker_reserve": "0.693147180559945309417235",
        "net_charges": "0.620114506958277524631763",
        "total_payout": "0"
      }
    },
    {
      "index": 3,
      "event": {
        "id": "e4",
        "type": "execute",
        "at": "2025-01-03T00:01:00Z",
        "actor": "alice",
        "quote_id": "quote3"
      },
      "intent_sha256": "4db093a32c7b22e5ee18961c5cb52853b6bf8d49e28dc79dd76a20b6252fd4de",
      "decision": "executed",
      "reason": null,
      "data": {
        "ledger_entry_sha256": "b1d18aef489776711cfbda181a95f36fd2da6068961928925a8dc6b14ed60f18",
        "charge": "-0.620114506958277524631763"
      },
      "clock_closed": false,
      "market_status_after": "open",
      "economic_revision_after": 2,
      "financial_before_sha256": "4c8e49b436e9f1c7edd66ca7bca7b7da4bc39d3f178d11ad01cb390542ec4ae9",
      "financial_after_sha256": "cb1a9149440ed799433cf4e3b020b8622b73065615a820eadceaa52e4b74e21d",
      "financial_after": {
        "q": {
          "YES": "0",
          "NO": "0"
        },
        "accounts": {
          "alice": {
            "cash": "10",
            "positions": {
              "YES": "0",
              "NO": "0"
            }
          },
          "bob": {
            "cash": "10",
            "positions": {
              "YES": "0",
              "NO": "0"
            }
          }
        },
        "maker_cash": "0.693147180559945309417235",
        "maker_reserve": "0.693147180559945309417235",
        "net_charges": "0",
        "total_payout": "0"
      }
    }
  ],
  "ledger": [
    {
      "kind": "trade",
      "event_id": "e2",
      "at": "2025-01-02T00:01:00Z",
      "actor": "alice",
      "quote_id": "quote1",
      "quote_sha256": "66ee710abd1e5150bf77eaed1d62354bb3886ff1ceaa6b5527ebee1f644a7688",
      "outcome": "YES",
      "delta": "1",
      "charge": "0.620114506958277524631763",
      "potential_before": "0.693147180559945309417232",
      "potential_after": "1.313261687518222834048995",
      "q_before": {
        "YES": "0",
        "NO": "0"
      },
      "q_after": {
        "YES": "1",
        "NO": "0"
      },
      "actor_cash_before": "10",
      "actor_cash_after": "9.379885493041722475368237",
      "maker_cash_before": "0.693147180559945309417235",
      "maker_cash_after": "1.313261687518222834048998",
      "index": 1,
      "previous_sha256": null,
      "economic_revision": 1,
      "sha256": "64c64736f798a85270d543722ff8cffe7176e495a0b6cdbd133786a42fa5ce9f"
    },
    {
      "kind": "trade",
      "event_id": "e4",
      "at": "2025-01-03T00:01:00Z",
      "actor": "alice",
      "quote_id": "quote3",
      "quote_sha256": "21c8ac12a7c5c4196341f99c55ab9df6ef03a233fa9c447619dcf80fb815aa64",
      "outcome": "YES",
      "delta": "-1",
      "charge": "-0.620114506958277524631763",
      "potential_before": "1.313261687518222834048995",
      "potential_after": "0.693147180559945309417232",
      "q_before": {
        "YES": "1",
        "NO": "0"
      },
      "q_after": {
        "YES": "0",
        "NO": "0"
      },
      "actor_cash_before": "9.379885493041722475368237",
      "actor_cash_after": "10",
      "maker_cash_before": "1.313261687518222834048998",
      "maker_cash_after": "0.693147180559945309417235",
      "index": 2,
      "previous_sha256": "64c64736f798a85270d543722ff8cffe7176e495a0b6cdbd133786a42fa5ce9f",
      "economic_revision": 2,
      "sha256": "b1d18aef489776711cfbda181a95f36fd2da6068961928925a8dc6b14ed60f18"
    }
  ],
  "ledger_sha256": "063ef619d3451b3189daaf8a240937913f6be14333050b57a05dc4689650a62b",
  "quotes": [
    {
      "receipt": {
        "id": "quote1",
        "actor": "alice",
        "outcome": "YES",
        "delta": "1",
        "created_at": "2025-01-02T00:00:00Z",
        "economic_revision": 0,
        "q_before": {
          "YES": "0",
          "NO": "0"
        },
        "q_after": {
          "YES": "1",
          "NO": "0"
        },
        "potential_before": "0.693147180559945309417232",
        "potential_after": "1.313261687518222834048995",
        "charge": "0.620114506958277524631763",
        "modeled_prices_before": {
          "YES": "0.5",
          "NO": "0.5"
        },
        "modeled_prices_after": {
          "YES": "0.73105857863000487925115924182183627436514464016505651927636590791904045307020464",
          "NO": "0.26894142136999512074884075817816372563485535983494348072363409208095954692979536"
        },
        "executable_now": true,
        "feasibility_reasons": []
      },
      "receipt_sha256": "66ee710abd1e5150bf77eaed1d62354bb3886ff1ceaa6b5527ebee1f644a7688",
      "used": true
    },
    {
      "receipt": {
        "id": "quote3",
        "actor": "alice",
        "outcome": "YES",
        "delta": "-1",
        "created_at": "2025-01-03T00:00:00Z",
        "economic_revision": 1,
        "q_before": {
          "YES": "1",
          "NO": "0"
        },
        "q_after": {
          "YES": "0",
          "NO": "0"
        },
        "potential_before": "1.313261687518222834048995",
        "potential_after": "0.693147180559945309417232",
        "charge": "-0.620114506958277524631763",
        "modeled_prices_before": {
          "YES": "0.73105857863000487925115924182183627436514464016505651927636590791904045307020464",
          "NO": "0.26894142136999512074884075817816372563485535983494348072363409208095954692979536"
        },
        "modeled_prices_after": {
          "YES": "0.5",
          "NO": "0.5"
        },
        "executable_now": true,
        "feasibility_reasons": []
      },
      "receipt_sha256": "21c8ac12a7c5c4196341f99c55ab9df6ef03a233fa9c447619dcf80fb815aa64",
      "used": true
    }
  ],
  "budget": {
    "work": 384,
    "returned_cells": 384
  },
  "numerics": {
    "precision": 80,
    "rounding": "ROUND_HALF_EVEN",
    "Emin": -999999,
    "Emax": 999999,
    "cash_quantum": "1e-24",
    "price_absolute_tolerance": "1e-60",
    "cost_absolute_tolerance": "1e-60",
    "reserve_pad_quanta": 2,
    "oracle_precision": 120
  },
  "invariants": {
    "cash_conservation": true,
    "nonnegative_balances_positions": true,
    "positions_equal_quantities": true,
    "quantized_potential_telescoping": true,
    "funded_maker_bound": true,
    "one_time_settlement": true,
    "scope": "Exact finite decimal cash-grid accounting; ln/exp prices/costs are finite-precision approximations"
  },
  "counters": {
    "actions": 4,
    "quotes": 2,
    "executed_trades": 2,
    "settlements": 0,
    "rejected_actions": 0,
    "idempotent_replays": 0
  },
  "sources": [
    {
      "id": "prediction-markets-wolfers-zitzewitz-v1",
      "technique_id": 58,
      "rank": 1,
      "author": "Justin Wolfers and Eric Zitzewitz",
      "edition": "Prediction Markets;Journal of Economic Perspectives18(2),107–126;Spring2004;DOI10.1257/0895330041371321",
      "url": "https://www.aeaweb.org/articles?id=10.1257%2F0895330041371321",
      "locator": "Original publisher metadata/abstract; market design and probability interpretation depend on conditions,not guaranteed by mechanism code.",
      "ingestion": "facts_only",
      "rights_note": "AEA copyright; complimentary reading is not blanket redistribution; facts only.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "prediction-markets-hanson-v1",
      "technique_id": 58,
      "rank": 2,
      "author": "Robin Hanson",
      "edition": "Logarithmic Market Scoring Rules for Modular Combinatorial Information Aggregation;Journal of Prediction Markets1(1),3–15;2007;DOI10.5750/jpm.v1i1.417",
      "url": "https://www.ubplj.org/index.php/jpm/article/view/417",
      "locator": "Original ranked journal page. Site Published field13December2012 differs from2007issue/PDF copyright; treat separately,not as a2012algorithm edition.",
      "ingestion": "facts_only",
      "rights_note": "University of Buckingham Press2007 all rights reserved; no article body/figures copied.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "prediction-markets-hanson-journal-pdf-v1",
      "technique_id": 58,
      "rank": null,
      "author": "Robin Hanson / University of Buckingham Press",
      "edition": "Official2007journal PDF;13pages;JPM1,3–15",
      "url": "https://www.ubplj.org/index.php/jpm/article/download/417/448",
      "locator": "Primary scoring-rule and market-scoring sections inspected; logarithmic scoring foundations and combination distinctions.",
      "ingestion": "facts_only",
      "rights_note": "Copyright2007UBP/all rights reserved; facts/math only,no body or figures redistributed.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "prediction-markets-hanson-draft-v1",
      "technique_id": 58,
      "rank": null,
      "author": "Robin Hanson / George Mason University",
      "edition": "Author working draft;January2002;12pages",
      "url": "https://hanson.gmu.edu/mktscore.pdf",
      "locator": "Title/date/intro inspected; repeated deeper retrieval timed out. Draft is not the2007journal edition or the separate2003Combinatorial Information Market Design article.",
      "ingestion": "facts_only",
      "rights_note": "Reading witness only; no draft text copied.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "prediction-markets-wolfers-author-v1",
      "technique_id": 58,
      "rank": null,
      "author": "Justin Wolfers and Eric Zitzewitz / NBER author site",
      "edition": "Published2004JEP author witness;20pages",
      "url": "https://users.nber.org/~jwolfers/papers/Predictionmarkets.pdf",
      "locator": "Intro/design context inspected; repeat deeper retrieval timed out. Real market evidence does not establish accuracy for this synthetic ledger.",
      "ingestion": "facts_only",
      "rights_note": "Published article copyright retained; no body/figures/data copied.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "prediction-markets-cost-function-v1",
      "technique_id": 58,
      "rank": null,
      "author": "Yiling Chen and Jennifer Wortman Vaughan",
      "edition": "Connections Between Markets and Learning;ACM SIGecom Exchanges9(1),June2010;5pages",
      "url": "https://econcs.seas.harvard.edu/sites/g/files/omnuum6346/files/econcs/files/chensigecom10.pdf",
      "locator": "Section2 explicitly defines trade cost C(q+r)-C(q),gradient prices,LMSR log-sum-exp cost and b log N worst-case maker loss.",
      "ingestion": "facts_only",
      "rights_note": "Primary mathematical facts only; no article text/code redistributed.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "prediction-markets-decimal-v1",
      "technique_id": 58,
      "rank": null,
      "author": "Python Software Foundation",
      "edition": "Python3.12 Decimal documentation;3.12.16docs observed,runtime3.12.10 tested separately",
      "url": "https://docs.python.org/3.12/library/decimal.html",
      "locator": "Fixed contexts,Decimal ln/exp correctly rounded HALF_EVEN,quantize and traps; Decimal transcendental results approximate,not rational exact.",
      "ingestion": "facts_only",
      "rights_note": "Documentation facts only; original implementation,no copied source code.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    }
  ],
  "empirical_forecast_accuracy_validated": false,
  "limitations": [
    "Real money,deposits,wagering,external trading orsettlement",
    "Live trader/user services orauthenticated authority",
    "Continuous double auction",
    "Conditional/combinatorial/multioutcome markets",
    "Short selling,leverage,fees,fundingchanges",
    "Empirical market efficiency orforecast accuracy",
    "Synthetic play credits only; no deposits,trading or external settlement occur.",
    "Actor/authority/clock/rights declarations are not external authentication or consent certification.",
    "Quantized total potentials telescope exactly on the cash grid; transcendental functions are not exact rational calculations.",
    "Local owner can rewrite all history; retain external anchors for independent immutability assurance.",
    "Trades use strict-before-close timing,not51/57inclusive forecast cutoff semantics."
  ],
  "report_sha256": "2d8c824d9879a415ec067ce9fe21aa7f5aef4cea0edb8a866915d29fd87b113b"
}
```

