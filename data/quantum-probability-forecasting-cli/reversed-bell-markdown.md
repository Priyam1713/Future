# Quantum Probability Reference

Status: accepted

| Basis | Amplitude (real, imaginary) | Ideal probability |
|---|---|---|
| 00 | (0.7071067811865475, 0.0) | 0.4999999999999999 |
| 01 | (0.7071067811865475, 0.0) | 0.4999999999999999 |
| 10 | (0.0, 0.0) | 0.0 |
| 11 | (0.0, 0.0) | 0.0 |

CPU classical emulation only;no QPU,GPU,cloud,Aer execution or quantum advantage.
QAE,coherent oracle construction,variational and quantum-inspired algorithms are unimplemented.
Ideal model probabilities,finite simulated frequencies and unknown real-world event probabilities are distinct.
Known p is available directly without sampling;shared-stream identity is by construction,not superiority.
Population moments assume independent identically prepared Bernoulli trials;PRNG emulates this model. No confidence interval or financial forecasting skill certified.
Float64 libm results and exact JSON replay are scoped to the recorded runtime;cross-platform comparisons use1e-12 absolute tolerance.

```json
{
  "status": "accepted",
  "task": "simulate",
  "profile": {
    "id": "montanaro-ibm-small-circuit-cpu-probability-v1",
    "sha256": "abe755a144bf38b228ebbd0e6eb313b93405ff2d90fda75e1bcb2295196852dd",
    "catalog_sha256": "07de668e406ec059fd1e4472da5db6671d13897b67a2a02d8638cc05076772fa"
  },
  "request": {
    "schema_version": 1,
    "profile": {
      "id": "montanaro-ibm-small-circuit-cpu-probability-v1",
      "sha256": "abe755a144bf38b228ebbd0e6eb313b93405ff2d90fda75e1bcb2295196852dd",
      "catalog_sha256": "07de668e406ec059fd1e4472da5db6671d13897b67a2a02d8638cc05076772fa"
    },
    "task": "simulate",
    "backend": "standalone_cpu",
    "circuit": {
      "qubits": 2,
      "gates": [
        {
          "op": "h",
          "target": 0
        },
        {
          "op": "cx",
          "target": 0,
          "control": 1
        }
      ],
      "measurement": [
        0,
        1
      ]
    },
    "shots": null,
    "rng": null,
    "event": {
      "kind": "qubit_one",
      "value": 0
    },
    "reference": null,
    "provenance": {
      "source_ref": "quantum-prob-ibm-gates-v1",
      "rights": "self_authored",
      "attribution": "Original user-supplied circuit;IBM gate conventions."
    }
  },
  "request_sha256": "037cb347dcec867807e578c621adee9127a9fc794099d16ea201d879ef74c4ba",
  "sources": [
    {
      "id": "quantum-prob-montanaro-v1",
      "technique_id": 50,
      "rank": 1,
      "author": "Ashley Montanaro",
      "edition": "Quantum speedup of Monte Carlo methods;Proc.R.Soc.A471(2181),20150301;2015-09-08;DOI10.1098/rspa.2015.0301",
      "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4614442/",
      "locator": "Sections/source-payload hashes recorded in quantum_probability_forecasting_resource_audit.json",
      "ingestion": "facts_only",
      "rights_note": "CC BY4.0 per primary article;original concise mathematical facts only,no article body or figures redistributed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "quantum-prob-aer-docs-v1",
      "technique_id": 50,
      "rank": 2,
      "author": "IBM / Qiskit contributors",
      "edition": "Qiskit Aer0.18.2 documentation;inspected2026-11-07",
      "url": "https://qiskit.github.io/qiskit-aer/",
      "locator": "Sections/source-payload hashes recorded in quantum_probability_forecasting_resource_audit.json",
      "ingestion": "facts_only",
      "rights_note": "Facts-only API notes. Aer source Apache2.0 separately verified;documentation access does not certify installed operation.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "quantum-prob-risk-v1",
      "technique_id": 50,
      "rank": 3,
      "author": "Stefan Woerner and Daniel J. Egger",
      "edition": "Quantum risk analysis;npj Quantum Information5,Article15;2019-02-08;DOI10.1038/s41534-019-0130-6;peer-reviewed article,not book",
      "url": "https://www.nature.com/articles/s41534-019-0130-6",
      "locator": "Sections/source-payload hashes recorded in quantum_probability_forecasting_resource_audit.json",
      "ingestion": "facts_only",
      "rights_note": "CC BY4.0 verified in final article witness p8,subject to separately credited third-party material. Facts-only notes,no PDF/figures/data redistributed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "quantum-prob-risk-dnb-v1",
      "technique_id": 50,
      "rank": null,
      "author": "Stefan Woerner and Daniel J. Egger;German National Library witness",
      "edition": "Final8page npj article archived by DNB;distinct from arXiv1806.06893v1(2018),12pages",
      "url": "https://d-nb.info/1180117980/34",
      "locator": "Sections/source-payload hashes recorded in quantum_probability_forecasting_resource_audit.json",
      "ingestion": "facts_only",
      "rights_note": "CC BY4.0 article license inspected p8;metadata,math facts and locators only. No final/preprint byte-equivalence attested.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "quantum-prob-ibm-gates-v1",
      "technique_id": 50,
      "rank": null,
      "author": "IBM / Qiskit contributors",
      "edition": "IBM Quantum SDK latest gate documentation;RY andH matrix conventions",
      "url": "https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.RYGate",
      "locator": "Sections/source-payload hashes recorded in quantum_probability_forecasting_resource_audit.json",
      "ingestion": "facts_only",
      "rights_note": "Original gate-matrix factual notes;no third-party code copied. SDK package metadata separately declares Apache2.0.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "quantum-prob-ibm-bits-v1",
      "technique_id": 50,
      "rank": null,
      "author": "IBM / Qiskit contributors",
      "edition": "Bit-ordering guide;example requirementsqiskit[all]~=2.6.1",
      "url": "https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering",
      "locator": "Sections/source-payload hashes recorded in quantum_probability_forecasting_resource_audit.json",
      "ingestion": "facts_only",
      "rights_note": "Facts-only bit/register ordering notes.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "quantum-prob-aer-source-v1",
      "technique_id": 50,
      "rank": null,
      "author": "IBM / Qiskit contributors",
      "edition": "Qiskit Aer tag0.18.2;simulator,SamplerV2,backend gate sets andLICENSE source bytes inspected",
      "url": "https://github.com/Qiskit/qiskit-aer/tree/0.18.2",
      "locator": "Sections/source-payload hashes recorded in quantum_probability_forecasting_resource_audit.json",
      "ingestion": "facts_only",
      "rights_note": "Apache2.0 LICENSE.txt inspected. No source implementation or wheel redistributed;preserve license/notices on any later integration.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "quantum-prob-finance-tutorial-v1",
      "technique_id": 50,
      "rank": null,
      "author": "Qiskit Finance contributors",
      "edition": "Archived Qiskit Finance0.4.1 amplitude-estimation tutorial;legacy Sampler API,not current runtime proof",
      "url": "https://qiskit-community.github.io/qiskit-finance/tutorials/00_amplitude_estimation.html",
      "locator": "Sections/source-payload hashes recorded in quantum_probability_forecasting_resource_audit.json",
      "ingestion": "facts_only",
      "rights_note": "Facts-only archived example/algorithm notes;no notebook/code copied. Site warns code may not work with current Qiskit.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "quantum-prob-iqae-v1",
      "technique_id": 50,
      "rank": null,
      "author": "Qiskit Algorithms contributors",
      "edition": "Qiskit Algorithms0.4.0 IterativeAmplitudeEstimation reference",
      "url": "https://qiskit-community.github.io/qiskit-algorithms/stubs/qiskit_algorithms.IterativeAmplitudeEstimation.html",
      "locator": "Sections/source-payload hashes recorded in quantum_probability_forecasting_resource_audit.json",
      "ingestion": "facts_only",
      "rights_note": "Facts-only algorithm/API notes;package metadata Apache2.0. No installed operation or theorem proof reproduction claimed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "quantum-prob-mlae-v1",
      "technique_id": 50,
      "rank": null,
      "author": "Qiskit Algorithms contributors",
      "edition": "Qiskit Algorithms0.4.0 MaximumLikelihoodAmplitudeEstimation reference",
      "url": "https://qiskit-community.github.io/qiskit-algorithms/stubs/qiskit_algorithms.MaximumLikelihoodAmplitudeEstimation.html",
      "locator": "Sections/source-payload hashes recorded in quantum_probability_forecasting_resource_audit.json",
      "ingestion": "facts_only",
      "rights_note": "Facts-only schedule/likelihood/API notes;no implementation copied.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "quantum-prob-aer-pypi-v1",
      "technique_id": 50,
      "rank": null,
      "author": "Qiskit Aer maintainers / PyPI",
      "edition": "qiskit-aer0.18.2 release metadata and WindowsCPython3.12wheel listing",
      "url": "https://pypi.org/pypi/qiskit-aer/json",
      "locator": "Sections/source-payload hashes recorded in quantum_probability_forecasting_resource_audit.json",
      "ingestion": "facts_only",
      "rights_note": "Metadata only;Apache2.0 declared,source license inspected separately. Wheel not downloaded/installed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "quantum-prob-sdk-pypi-v1",
      "technique_id": 50,
      "rank": null,
      "author": "Qiskit maintainers / PyPI",
      "edition": "qiskit2.6.2 release metadata;Windowscp310abi3wheel listing",
      "url": "https://pypi.org/pypi/qiskit/json",
      "locator": "Sections/source-payload hashes recorded in quantum_probability_forecasting_resource_audit.json",
      "ingestion": "facts_only",
      "rights_note": "Metadata declares Apache2.0;no package acquired or runtime certified.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "quantum-prob-algorithms-pypi-v1",
      "technique_id": 50,
      "rank": null,
      "author": "Qiskit Algorithms maintainers / PyPI",
      "edition": "qiskit-algorithms0.4.0 release metadata;pure Python wheel listing",
      "url": "https://pypi.org/pypi/qiskit-algorithms/json",
      "locator": "Sections/source-payload hashes recorded in quantum_probability_forecasting_resource_audit.json",
      "ingestion": "facts_only",
      "rights_note": "Metadata declares Apache2.0;no package acquired or runtime certified.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    }
  ],
  "source_freeze_sha256": "dc7a03a73733b4adb1e6e2827df290a7fb8248ba14e75021bb7f25d53b822e5a",
  "bit_order": "q0 LSB;bitstrings q(n-1)..q0;ascending state index;identity qi->ci terminal mapping only",
  "result": {
    "statevector": [
      {
        "index": 0,
        "bitstring": "00",
        "real": 0.7071067811865475,
        "imag": 0.0,
        "probability": 0.4999999999999999
      },
      {
        "index": 1,
        "bitstring": "01",
        "real": 0.7071067811865475,
        "imag": 0.0,
        "probability": 0.4999999999999999
      },
      {
        "index": 2,
        "bitstring": "10",
        "real": 0.0,
        "imag": 0.0,
        "probability": 0.0
      },
      {
        "index": 3,
        "bitstring": "11",
        "real": 0.0,
        "imag": 0.0,
        "probability": 0.0
      }
    ],
    "normalization": {
      "norm": 0.9999999999999998,
      "error": 2.220446049250313e-16,
      "tolerance": 1e-12,
      "passed": true,
      "sampling_norm_divisor": 0.9999999999999998
    },
    "event": {
      "predicate": {
        "kind": "qubit_one",
        "value": 0
      },
      "indices": [
        1,
        3
      ],
      "ideal_model_probability": 0.5
    },
    "trace": [
      {
        "gate": {
          "op": "h",
          "target": 0
        },
        "depth": 1,
        "norm": 0.9999999999999998
      },
      {
        "gate": {
          "op": "cx",
          "target": 0,
          "control": 1
        },
        "depth": 2,
        "norm": 0.9999999999999998
      }
    ],
    "resources": {
      "qubits": 2,
      "dimension": 4,
      "primitive_gates": 2,
      "depth": 2,
      "gate_counts": {
        "id": 0,
        "x": 0,
        "h": 1,
        "ry": 0,
        "cx": 1
      },
      "measurement": [
        0,
        1
      ],
      "precision": "complex binary64",
      "statevector_payload_bytes": 64,
      "python_overhead_excluded": true,
      "ae_oracle_calls": null,
      "qae_implemented": false,
      "runtime_memory_measurement": "Separate resource measurements artifact;no variable timing in deterministic report."
    },
    "sampling": null,
    "classical": null,
    "reference": null
  },
  "code_sha256": "2fc23924ddfe00d6bf08b7d2d7dbd1c4fb0ca445339ee769faff52dc951866b5",
  "limits": [
    "CPU classical emulation only;no QPU,GPU,cloud,Aer execution or quantum advantage.",
    "QAE,coherent oracle construction,variational and quantum-inspired algorithms are unimplemented.",
    "Ideal model probabilities,finite simulated frequencies and unknown real-world event probabilities are distinct.",
    "Known p is available directly without sampling;shared-stream identity is by construction,not superiority.",
    "Population moments assume independent identically prepared Bernoulli trials;PRNG emulates this model. No confidence interval or financial forecasting skill certified.",
    "Float64 libm results and exact JSON replay are scoped to the recorded runtime;cross-platform comparisons use1e-12 absolute tolerance."
  ],
  "report_sha256": "12a26e628a5e7d6578e0d7db9fcdb520ae3159876bfc424a20bfd96e33925666"
}
```

