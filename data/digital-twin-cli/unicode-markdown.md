# Digital Twin — offline scalar replay

````json
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
      "A": "1",
      "B": "0",
      "H": "1",
      "Q": "0",
      "R": "1",
      "m0": "0",
      "P0": "1"
    },
    "timeline": {
      "initial_at": "2020-01-01T00:00:00Z",
      "step_seconds": 1,
      "evaluation_at": "2020-01-01T00:00:07Z"
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
        "value": "2",
        "control": "0"
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
      }
    ],
    "horizon": 0,
    "scenarios": [],
    "reference_scenario": null,
    "provenance": {
      "source_ref": "digital-twin-welch-bishop-2002-v1",
      "rights": "self_authored",
      "attribution": "Original Δ example ``` fenced safely",
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
  "input_sha256": "0faf6d79634ba6dbf4bb473e617d9617bd55ec7267eae8f215be42e208e014c9",
  "parameters_sha256": "f3516c1790d29cf725605c194a8cbbf9393480f023f820599a8ab6af64e70100",
  "asset_sha256": "896b659ab59f466124e90cc770cfe10be83cb1b1a534924f4aa6516436a0523c",
  "model_sha256": "908f46ddbf770519954393aa05c81ee0637fa2ca771750727c6d71bc805a0245",
  "source_manifest_sha256": "9e25d912734ccee8c74fe1315fb668fd09196156ff38b4de6ffa066f3f31a85d",
  "source_freeze_sha256": "dcf761387ae33b7dc816380ef0f7af60cfcedda8c4783faa5614cf32b8c2f239",
  "snapshot_sha256": "eb2927f4cde89cdf2196bfc9c863a8491c4e65f18cf000c28fa3d7d6ea94ad4a",
  "code_sha256": "baafad5ee98e365b18b168ad1500c44dc9e20718d10e137f3f6bd78dd99ab45f",
  "budget": {
    "combined_steps": 2,
    "scalar_cells": 224,
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
      "value": "2",
      "prior_mean": "0",
      "prior_variance": "1",
      "predicted_measurement": "0",
      "innovation_variance": "2",
      "innovation": "2",
      "gain": "1/2",
      "posterior_mean": "1",
      "posterior_variance": "1/2",
      "correction": "applied",
      "open_loop_mean": "0",
      "open_loop_variance": "1",
      "open_loop_measurement": "0",
      "persistence_measurement": null,
      "persistence_source_id": null,
      "filter_squared_error": "4",
      "open_loop_squared_error": "4",
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
      "prior_mean": "1",
      "prior_variance": "1/2",
      "predicted_measurement": "1",
      "innovation_variance": "3/2",
      "innovation": "1",
      "gain": "1/3",
      "posterior_mean": "4/3",
      "posterior_variance": "1/3",
      "correction": "applied",
      "open_loop_mean": "0",
      "open_loop_variance": "1",
      "open_loop_measurement": "0",
      "persistence_measurement": "2",
      "persistence_source_id": "r1",
      "filter_squared_error": "1",
      "open_loop_squared_error": "4",
      "persistence_squared_error": "0"
    }
  ],
  "final_posterior": {
    "mean": "4/3",
    "variance": "1/3",
    "timestamp": "2020-01-01T00:00:02Z"
  },
  "evaluation": {
    "eligible_target_ids": [
      "r1",
      "r2"
    ],
    "filter_all": {
      "status": "finite",
      "count": 2,
      "sum_squared_error": "5",
      "mean_squared_error": "5/2"
    },
    "open_loop_all": {
      "status": "finite",
      "count": 2,
      "sum_squared_error": "8",
      "mean_squared_error": "4"
    },
    "matched_target_ids": [
      "r2"
    ],
    "three_way_matched": {
      "filter": {
        "status": "finite",
        "count": 1,
        "sum_squared_error": "1",
        "mean_squared_error": "1"
      },
      "open_loop": {
        "status": "finite",
        "count": 1,
        "sum_squared_error": "4",
        "mean_squared_error": "4"
      },
      "persistence": {
        "status": "finite",
        "count": 1,
        "sum_squared_error": "0",
        "mean_squared_error": "0"
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
    "timestamp": "2020-01-01T00:00:02Z",
    "mean": "4/3",
    "variance": "1/3",
    "accepted_history_sha256": "e6cec9154943c4e548a0e83783a8b63544e45e6f193f1eb7179a7eb35ec3ae38"
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
  "report_sha256": "d21ed6599fa0abbbd4eb75263dcd86c9e43f713a4d827095c090e7b3920e83e0"
}
````

