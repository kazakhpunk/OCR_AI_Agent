## Main Components

The `ocr.py` script is the current main implementation for OCR processing of executive orders. It uses Vertex AI's Gemini model through Portkey for high-quality OCR and text extraction.


Key features:

- Uses Portkey for high-quality OCR and text extraction.
- Incorporates Vertex AI's Gemini model for high-quality OCR and text extraction.
- Includes a custom prompt to extract the relevant content for the specified executive order.
- Identifies specific executive orders based on filename patterns
- Returns results in structured JSON format


Usage:

```
python ocr.py
```

Configuration:

- `PORTKEY_API_KEY`: Your Portkey API key.
- `VERTEX_AI_API_KEY`: Your Vertex AI API key.
- The name of the Gemini model to use.


Sample output JSON format:

```
{
  "filename": "7606.pdf",
  "matched_order": true,
  "order_number": "7606",
  "order_title": "Executive Order 7606",
  "document_text": "..."
}
```


### truncated.ipynb (v1)

This Jupyter notebook represents an earlier approach using CrewAI with multiple specialized AI agents working together. While innovative, this approach proved computationally wasteful and complex.

Key issues with the v1 approach:

- Uses multiple LLM calls for what can be accomplished in a single pass

- CrewAI overhead creates unnecessary complexity

- Higher API costs due to multiple agent conversations

- Slower processing time with multiple communication steps

Components in v1:

- Quality Analyzer agent

- OCR Processor agent (using PyPDF2, pdfminer, EasyOCR)

- Executive Order Identifier agent

- Complex agent-to-agent communication patterns


## Getting Started

1. Clone this repository

2. Install the required dependencies

```
pip install portkey-ai python-dotenv
```

or

```
pip install -r requirements.txt
```

3. Set your API keys in the `ocr.py` script

4. Run the `ocr.py` script

```
python ocr.py
```

