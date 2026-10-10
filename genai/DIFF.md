---
lab3_genai_diff:
  instrumentation: "OpenTelemetry OTLP JSON 1.0 manual fixture"
  spec_ref: "semantic-conventions-genai@e57c543b4889619eb2a05702471937db5119165d"
  attributes:
    - {name: gen_ai.operation.name, emitted: true, in_spec: true, stability: development}
    - {name: gen_ai.provider.name, emitted: true, in_spec: true, stability: development}
    - {name: gen_ai.request.model, emitted: true, in_spec: true, stability: development}
    - {name: gen_ai.response.model, emitted: true, in_spec: true, stability: development}
    - {name: gen_ai.response.finish_reasons, emitted: true, in_spec: true, stability: development}
---
<!-- ai-generated: 85% - AI assembled a disclosed OTLP fixture and checked its attribute names against the pinned registry. -->

# What the library emits, against the spec

This is a small manual OTLP JSON fixture for a chat completion, not an export captured from an automatically instrumented provider SDK. It records the operation, provider, requested model, response model and stop reason. The comparison uses the pinned GenAI semantic-conventions repository, where all five attributes are defined with development stability. The exercise demonstrates the shape of the diff and is transparent about the fixture's provenance; a production dashboard should be based on spans exported by the actual client instrumentation and should avoid high-cardinality or sensitive prompt content.
