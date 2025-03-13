from portkey_ai import Portkey
import os
from dotenv import load_dotenv
import pathlib
import base64
load_dotenv(override=True)

portkey = Portkey(
    base_url="https://ai-gateway.apps.cloud.rt.nyu.edu/v1/",
    api_key=os.getenv("PORTKEY_API_KEY"),  
    virtual_key=os.getenv("VERTEX_VIRTUAL_KEY")
)

base_path = r"/Volumes/One Touch/OCR/PDFs"
pdf_count = 0

# Count actual PDF files
for pdf_dir in os.listdir(base_path):
    if pdf_dir.endswith('.pdf'):  # Directory names end with .pdf
        filename = pdf_dir[:-4]  # Remove .pdf extension
        pdf_path = os.path.join(base_path, pdf_dir, f"{filename}.pdf")
        
        if os.path.exists(pdf_path) and os.path.isfile(pdf_path):
            filepath = pathlib.Path(pdf_path)
            
            # Read the PDF file and encode it
            encoded_pdf = base64.b64encode(filepath.read_bytes()).decode('utf-8')
            
            # Format the system prompt
            system_prompt = "You are an intelligent assistant tasked with performing OCR on PDFs containing executive orders. The PDF may contain multiple executive orders in various layouts, including multi-column formats. Your task is to:" + \
                        "\n\n1. Identify and extract the specific executive order indicated in the file name." + \
                        "\n   - Example: If the file name is `2004-03-7606.pdf`, focus only on Public Land Order 7606." + \
                        "\n   - Ignore all other content in the document." + \
                        "\n\n2. Handle multi-column layouts accurately:" + \
                        "\n   - Read text column by column, ensuring content from different columns is not mixed." + \
                        "\n   - Maintain proper order and structure of the text." + \
                        "\n\n3. Extract only the relevant content for the specified executive order:" + \
                        "\n   - Include title, sections, dates, and associated details." + \
                        "\n   - Exclude unrelated content or other executive orders." + \
                        "\n\n4. If the file name contains \"03\" or \"33\", assume it is a Public Land Order and confirm that multiple orders may exist in the document. Still, extract only the one matching the number in the file name (e.g., \"7606\")." + \
                        "\n\n5. If no matching executive order is found in the document, perform OCR on the entire document and return all the text content. Preserve the document structure as much as possible, including headings, paragraphs, and any multi-column format." + \
                        "\n\n6. IMPORTANT: Process ALL pages of the document, even if they appear to have lower quality or are difficult to read. Make your best effort to extract text from every page and do not skip pages that seem to have lower quality." + \
                        "\n\n7. IMPORTANT: You must return your results in valid JSON format with the following structure:" + \
                        "\n```json" + \
                        "\n{" + \
                        "\n  \"filename\": \"string\", // The original filename" + \
                        "\n  \"matched_order\": true/false, // Whether a specific order matching the filename was found" + \
                        "\n  \"order_number\": \"string\", // The order number if found (e.g., \"7606\")" + \
                        "\n  \"order_title\": \"string\", // The title of the order if found" + \
                        "\n  \"document_text\": \"string\" // Either the text of the matching order (if matched_order=true) or the full document text (if matched_order=false)" + \
                        "\n}" + \
                        "\n```" + \
                        "\n\nDo not include any text outside of the JSON structure. The JSON must be valid and parseable." + \
                        "\n\nAs a senior professional in this field, you will receive a bonus if your assistance significantly improves the OCR process and extraction accuracy."
            
            # Create the user prompt with the PDF data
            user_prompt = f"Here is the PDF file named {filename}.pdf. Please analyze it according to the instructions above."
            
            completion = portkey.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:application/pdf;base64,{encoded_pdf}"
                            }
                        }
                    ]}
                ],
                model="gemini-2.0-flash"
            )

            print(completion)