# Cognitive Biases in AI
The goal of the project is to see whether AI models are susceptible to various cognitive biases.
## Methodology
The project is using AI inference to check whether it shows the signs of cognitive biases.<br>
The models are supported via an OpenAI-compatible endpoint, in the case of current review - OpenAI.

Only the models from Google Gemini series are being tested here due to the free-tier of Google Vertex.

At the current moment, the models are being checked for **anchoring bias**.

> Anchoring Bias: run an unmodified (`control`) prompt, and compare the results to a modified (`test`) prompt<br>
> with an anchor attached. The setting for the anchoring bias is AI as a Judge, where the anchor is the court interruption.

More biases will be added in the future.
