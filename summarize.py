from langchain.document_loaders import AmazonTextractPDFLoader
from langchain.llms import Bedrock
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# loader = AmazonTextractPDFLoader("./samples/discharge-summary.png")
# document = loader.load()

def generate_summary(input):
    template = """

    Given a full document, give me a concise summary. Skip any preamble text and just give the summary.

    <document>{doc_text}</document>
    <summary>"""

    prompt = PromptTemplate(template=template, input_variables=["doc_text"])
    bedrock_llm = Bedrock(client=Bedrock, model_id="anthropic.claude-v2")

    num_tokens = bedrock_llm.get_num_tokens(input)
    print (f"Our prompt has {num_tokens} tokens \n\n=========================\n")

    llm_chain = LLMChain(prompt=prompt, llm=bedrock_llm)
    summary = llm_chain.run(input)

    print(summary.replace("</summary>","").strip())
    return summary.replace("</summary>","").strip()

generate_summary()