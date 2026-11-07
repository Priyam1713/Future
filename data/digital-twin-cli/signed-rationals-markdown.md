# Digital Twin — offline scalar replay

```json
{
  "status": "accepted",
  "technique_id": 53,
  "schema_version": 1,
  "profile": {
    "id": "digital-twin-offline-scalar-state-replay-v1",
    "sha256": "3a16aa2f9855eae8351726f565a616dcefc3a7d1a14db0c9642dadd7df091db4",
    "catalog_sha256": "9e25d912734ccee8c74fe1315fb668fd09196156ff38b4de6ffa066f3f31a85d"
  },
  "schema_sha256": "d730fcd418678eeec627ec2e1018641c3c7780c9c9d79ae55da1be8659297642",
  "request": {
    "schema_version": 1,
    "profile": {
      "id": "digital-twin-offline-scalar-state-replay-v1",
      "sha256": "3a16aa2f9855eae8351726f565a616dcefc3a7d1a14db0c9642dadd7df091db4",
      "catalog_sha256": "9e25d912734ccee8c74fe1315fb668fd09196156ff38b4de6ffa066f3f31a85d"
    },
    "mode": "synthetic",
    "asset": {
      "id": "asset-1",
      "state_unit": "V",
      "measurement_unit": "V",
      "parameter_version": "v1"
    },
    "parameters": {
      "version": "v1",
      "A": "-1/2",
      "B": "-2",
      "H": "-3/2",
      "Q": "1/4",
      "R": "7/5",
      "m0": "-1",
      "P0": "3/2"
    },
    "timeline": {
      "initial_at": "2020-01-01T00:00:00Z",
      "step_seconds": 1,
      "evaluation_at": "2020-01-01T00:00:08Z"
    },
    "records": [
      {
        "id": "r1",
        "asset_id": "asset-1",
        "state_unit": "V",
        "measurement_unit": "V",
        "tick": 1,
        "timestamp": "2020-01-01T00:00:01Z",
        "available_at": "2020-01-01T00:00:01Z",
        "value": "1",
        "control": "-2"
      },
      {
        "id": "r2",
        "asset_id": "asset-1",
        "state_unit": "V",
        "measurement_unit": "V",
        "tick": 2,
        "timestamp": "2020-01-01T00:00:02Z",
        "available_at": "2020-01-01T00:00:02Z",
        "value": "2",
        "control": "0"
      },
      {
        "id": "r3",
        "asset_id": "asset-1",
        "state_unit": "V",
        "measurement_unit": "V",
        "tick": 3,
        "timestamp": "2020-01-01T00:00:03Z",
        "available_at": "2020-01-01T00:00:03Z",
        "value": "3",
        "control": "0"
      }
    ],
    "horizon": 0,
    "scenarios": [],
    "reference_scenario": null,
    "provenance": {
      "source_ref": "digital-twin-welch-bishop-2002-v1",
      "rights": "self_authored",
      "attribution": "Future original scalar fixture",
      "snapshot": "Original synthetic scalar observations; no real people or devices.",
      "snapshot_sha256": "eb2927f4cde89cdf2196bfc9c863a8491c4e65f18cf000c28fa3d7d6ea94ad4a",
      "archive_checks": {
        "source": false,
        "units": false,
        "timestamps": false,
        "rights": false
      }
    }
  },
  "input_sha256": "321d2bf5a93cfcdb5d8df3504316a14d78a850275e28f587b5b025ab9cce9256",
  "parameters_sha256": "18d5216355a03c9719c8ea5a0746f1db5ba9cb77626a92edcb0174ae90b8368a",
  "asset_sha256": "896b659ab59f466124e90cc770cfe10be83cb1b1a534924f4aa6516436a0523c",
  "model_sha256": "5f41448714aa7c15d37deeffaaecc93168c0c0178564227d6f5b75316f5e7102",
  "source_manifest_sha256": "9e25d912734ccee8c74fe1315fb668fd09196156ff38b4de6ffa066f3f31a85d",
  "source_freeze_sha256": "dcf761387ae33b7dc816380ef0f7af60cfcedda8c4783faa5614cf32b8c2f239",
  "snapshot_sha256": "eb2927f4cde89cdf2196bfc9c863a8491c4e65f18cf000c28fa3d7d6ea94ad4a",
  "code_sha256": "baafad5ee98e365b18b168ad1500c44dc9e20718d10e137f3f6bd78dd99ab45f",
  "budget": {
    "combined_steps": 3,
    "scalar_cells": 272,
    "integer_bits": 8192
  },
  "rows": [
    {
      "id": "r1",
      "tick": 1,
      "forecast_origin": "2020-01-01T00:00:00Z",
      "timestamp": "2020-01-01T00:00:01Z",
      "available_at": "2020-01-01T00:00:01Z",
      "available_at_update": true,
      "available_at_evaluation": true,
      "value": "1",
      "prior_mean": "9/2",
      "prior_variance": "5/8",
      "predicted_measurement": "-27/4",
      "innovation_variance": "449/160",
      "innovation": "31/4",
      "gain": "-150/449",
      "posterior_mean": "858/449",
      "posterior_variance": "140/449",
      "correction": "applied",
      "open_loop_mean": "9/2",
      "open_loop_variance": "5/8",
      "open_loop_measurement": "-27/4",
      "persistence_measurement": null,
      "persistence_source_id": null,
      "filter_squared_error": "961/16",
      "open_loop_squared_error": "961/16",
      "persistence_squared_error": null
    },
    {
      "id": "r2",
      "tick": 2,
      "forecast_origin": "2020-01-01T00:00:01Z",
      "timestamp": "2020-01-01T00:00:02Z",
      "available_at": "2020-01-01T00:00:02Z",
      "available_at_update": true,
      "available_at_evaluation": true,
      "value": "2",
      "prior_mean": "-429/449",
      "prior_variance": "589/1796",
      "predicted_measurement": "1287/898",
      "innovation_variance": "76793/35920",
      "innovation": "509/898",
      "gain": "-17670/76793",
      "posterior_mean": "-83388/76793",
      "posterior_variance": "16492/76793",
      "correction": "applied",
      "open_loop_mean": "-9/4",
      "open_loop_variance": "13/32",
      "open_loop_measurement": "27/8",
      "persistence_measurement": "1",
      "persistence_source_id": "r1",
      "filter_squared_error": "259081/806404",
      "open_loop_squared_error": "121/64",
      "persistence_squared_error": "1"
    },
    {
      "id": "r3",
      "tick": 3,
      "forecast_origin": "2020-01-01T00:00:02Z",
      "timestamp": "2020-01-01T00:00:03Z",
      "available_at": "2020-01-01T00:00:03Z",
      "available_at_update": true,
      "available_at_evaluation": true,
      "value": "3",
      "prior_mean": "41694/76793",
      "prior_variance": "93285/307172",
      "predicted_measurement": "-62541/76793",
      "innovation_variance": "12798641/6143440",
      "innovation": "292920/76793",
      "gain": "-2798550/12798641",
      "posterior_mean": "-3725922/12798641",
      "posterior_variance": "2611980/12798641",
      "correction": "applied",
      "open_loop_mean": "9/8",
      "open_loop_variance": "45/128",
      "open_loop_measurement": "-27/16",
      "persistence_measurement": "2",
      "persistence_source_id": "r2",
      "filter_squared_error": "85802126400/5897164849",
      "open_loop_squared_error": "5625/256",
      "persistence_squared_error": "1"
    }
  ],
  "final_posterior": {
    "mean": "-3725922/12798641",
    "variance": "2611980/12798641",
    "timestamp": "2020-01-01T00:00:03Z"
  },
  "evaluation": {
    "eligible_target_ids": [
      "r1",
      "r2",
      "r3"
    ],
    "filter_all": {
      "status": "finite",
      "count": 3,
      "sum_squared_error": "1425384317039879765/19021989291571984",
      "mean_squared_error": "1425384317039879765/57065967874715952"
    },
    "open_loop_all": {
      "status": "finite",
      "count": 3,
      "sum_squared_error": "21485/256",
      "mean_squared_error": "21485/768"
    },
    "matched_target_ids": [
      "r2",
      "r3"
    ],
    "three_way_matched": {
      "filter": {
        "status": "finite",
        "count": 2,
        "sum_squared_error": "70719021303709369/4755497322892996",
        "mean_squared_error": "70719021303709369/9510994645785992"
      },
      "open_loop": {
        "status": "finite",
        "count": 2,
        "sum_squared_error": "6109/256",
        "mean_squared_error": "6109/512"
      },
      "persistence": {
        "status": "finite",
        "count": 2,
        "sum_squared_error": "2",
        "mean_squared_error": "1"
      }
    },
    "exclusions": [
      {
        "id": "r1",
        "reason": "no_previous_available_observation",
        "scope": "three_way_matched"
      }
    ],
    "meaning": "Pre-update measurement-scale squared errors; no latent-state ground truth, posterior-fit score, empirical skill or uncertainty-coverage certification"
  },
  "scenario_fork": {
    "timestamp": "2020-01-01T00:00:03Z",
    "mean": "-3725922/12798641",
    "variance": "2611980/12798641",
    "accepted_history_sha256": "9034f92441c0184d8fcde0e5fa15f85dfac024af4e77b1794e234fe1265ae9a1"
  },
  "scenarios": [],
  "comparisons": [],
  "sources": [
    {
      "id": "digital-twin-nasem-v1",
      "technique_id": 53,
      "rank": 1,
      "author": "National Academies of Sciences, Engineering, and Medicine",
      "edition": "Foundational Research Gaps and Future Directions for Digital Twins;2024;DOI10.17226/26894",
      "url": "https://www.nationalacademies.org/read/26894",
      "locator": "Publisher report,2024 edition andDOI",
      "ingestion": "facts_only",
      "rights_note": "Copyright2024 National Academy of Sciences,all rights reserved. Online/free access does not grant redistribution;facts andoriginal short notes only,no body/figures/PDF bundled.",
      "checked_on": "2026-11-07",
      "access": "read",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "digital-twin-grieves-v1",
      "technique_id": 53,
      "rank": 2,
      "author": "Michael W. Grieves",
      "edition": "Digital Twin: Manufacturing Excellence through Virtual Factory Replication;2014 whitepaper;8PDF pages includingcover,7numbered body pages",
      "url": "https://edisciplinas.usp.br/pluginfile.php/8935104/mod_resource/content/1/MichaelGrieves-white-paper-2014.pdf",
      "locator": "Cover,numbered pp1–2 concept model;pp4–5 conceptualization/comparison/collaboration",
      "ingestion": "facts_only",
      "rights_note": "Copyright Michael W. Grieves,LLC2014. Primary author paper viaUSP educational witness;no redistribution license inferred. Inventory Book label isbibliographic lead,notverified monograph/ISBN.",
      "checked_on": "2026-11-07",
      "access": "read",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "digital-twin-nasem-landscape-v1",
      "technique_id": 53,
      "rank": null,
      "author": "National Academies of Sciences, Engineering, and Medicine",
      "edition": "Foundational Research Gaps and Future Directions for Digital Twins;2024;DOI10.17226/26894",
      "url": "https://www.nationalacademies.org/read/26894/chapter/4",
      "locator": "Chapter2,pp21–22 definition;pp30–32 VVUQ",
      "ingestion": "facts_only",
      "rights_note": "Copyright2024 National Academy of Sciences,all rights reserved. Online/free access does not grant redistribution;facts andoriginal short notes only,no body/figures/PDF bundled.",
      "checked_on": "2026-11-07",
      "access": "read",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "digital-twin-nasem-physical-v1",
      "technique_id": 53,
      "rank": null,
      "author": "National Academies of Sciences, Engineering, and Medicine",
      "edition": "Foundational Research Gaps and Future Directions for Digital Twins;2024;DOI10.17226/26894",
      "url": "https://www.nationalacademies.org/read/26894/chapter/6",
      "locator": "Chapter4,pp69–71 data quality,sampling,privacy",
      "ingestion": "facts_only",
      "rights_note": "Copyright2024 National Academy of Sciences,all rights reserved. Online/free access does not grant redistribution;facts andoriginal short notes only,no body/figures/PDF bundled.",
      "checked_on": "2026-11-07",
      "access": "read",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "digital-twin-nasem-feedback-v1",
      "technique_id": 53,
      "rank": null,
      "author": "National Academies of Sciences, Engineering, and Medicine",
      "edition": "Foundational Research Gaps and Future Directions for Digital Twins;2024;DOI10.17226/26894",
      "url": "https://www.nationalacademies.org/read/26894/chapter/7",
      "locator": "Chapter5,pp78–83;data assimilation andcontinual model updating;Conclusion5-2",
      "ingestion": "facts_only",
      "rights_note": "Copyright2024 National Academy of Sciences,all rights reserved. Online/free access does not grant redistribution;facts andoriginal short notes only,no body/figures/PDF bundled.",
      "checked_on": "2026-11-07",
      "access": "read",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "digital-twin-nasem-rights-v1",
      "technique_id": 53,
      "rank": null,
      "author": "National Academies Press",
      "edition": "Current rights andpermissions webpage",
      "url": "https://www.nationalacademies.org/request-rights-and-permissions",
      "locator": "Distributing PDFs andpermission process",
      "ingestion": "facts_only",
      "rights_note": "Policy facts only;no permission obtained orneeded forsource-body redistribution because none isbundled.",
      "checked_on": "2026-11-07",
      "access": "read",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "digital-twin-welch-bishop-2002-v1",
      "technique_id": 53,
      "rank": null,
      "author": "Greg Welch andGary Bishop",
      "edition": "An Introduction to the Kalman Filter;UNC TR95-041;updated2002-03-11;16pages",
      "url": "https://www.mit.edu/course/16/16.070/www/project/PF_kalman_intro.pdf",
      "locator": "Primary author technical report throughMIT course witness;Section1 p2 assumptions;Table1-1/1-2,p5,Eqs1.9–1.13",
      "ingestion": "facts_only",
      "rights_note": "Publicly accessible educational witness;no blanket redistribution license observed. Numerical facts andoriginal derivations only;no text/code/figures/PDF bundled.",
      "checked_on": "2026-11-07",
      "access": "read",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "digital-twin-welch-bishop-2006-lead-v1",
      "technique_id": 53,
      "rank": null,
      "author": "Greg Welch andGary Bishop",
      "edition": "TR95-041;indexed2006-07-24 update,notfetched orsubstituted for2002 witness",
      "url": "https://www.cs.unc.edu/~welch/media/pdf/kalman_intro.pdf",
      "locator": "Direct author-hosted URL returned404 byweb andurllib;metadata lead only",
      "ingestion": "facts_only",
      "rights_note": "No source body acquired fromthis URL;do notattribute inspected2002 equations toanunread2006version.",
      "checked_on": "2026-11-07",
      "access": "404;metadata_only",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "digital-twin-nasem-summary-v1",
      "technique_id": 53,
      "rank": null,
      "author": "National Academies of Sciences, Engineering, and Medicine",
      "edition": "Foundational Research Gaps and Future Directions for Digital Twins;2024;DOI10.17226/26894",
      "url": "https://www.nationalacademies.org/read/26894/chapter/2",
      "locator": "Summarypp1–4;definition andfit-for-purpose context",
      "ingestion": "facts_only",
      "rights_note": "Copyright2024 National Academy of Sciences,all rights reserved. Online/free access does not grant redistribution;facts andoriginal short notes only,no body/figures/PDF bundled.",
      "checked_on": "2026-11-07",
      "access": "read",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    }
  ],
  "scope": {
    "mode": "synthetic",
    "synthetic_correctness": "Supported bounded numerical replay",
    "archival": "Requires independent source, units, timestamp and rights review; declarations are not certification",
    "empirical_accuracy": "Not certified without real data and held-out validation",
    "live_synchronization": false,
    "decision_feedback": false,
    "actuator_control": false,
    "complete_real_time_twin_certified": false,
    "covariance": "Conditional model variance under declared linear/noise assumptions; not calibrated empirical uncertainty"
  },
  "limits": [
    "Complete real-time digital twin certification",
    "Live synchronization or decision feedback",
    "Actuator control",
    "Empirical accuracy or uncertainty coverage without held-out validation",
    "Parameter learning",
    "Smoothing or delayed asynchronous correction",
    "Automatic imputation/outlier deletion",
    "Multivariate/nonlinear models",
    "Urban/personal/behavioral twin certification"
  ],
  "report_sha256": "8d096d0a0f015b8eb570c262c3d7bbab7d93f2f5756e797b59f182ba7bde9775"
}
```

