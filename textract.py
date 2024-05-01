# from langchain.document_loaders import AmazonTextractPDFLoader
from langchain.prompts import PromptTemplate
import os
import json
import boto3
from langchain_community.document_loaders import AmazonTextractPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


# loader = AmazonTextractPDFLoader("./samples/discharge-summary.png")
# document = loader.load()

# def generate_summary(input):
#     template = """

#     Given a full document, give me a concise summary. Skip any preamble text and just give the summary.

#     <document>{doc_text}</document>
#     <summary>"""

#     prompt = PromptTemplate(template=template, input_variables=["doc_text"])
#     bedrock_llm = Bedrock(client=bedrock, model_id="anthropic.claude-v2")

#     num_tokens = bedrock_llm.get_num_tokens(input)
#     print (f"Our prompt has {num_tokens} tokens \n\n=========================\n")

#     llm_chain = LLMChain(prompt=prompt, llm=bedrock_llm)
#     summary = llm_chain.run(input)

#     print(summary.replace("</summary>","").strip())
#     return summary.replace("</summary>","").strip()


#
def get_summary(text):
    session = boto3.Session(
        profile_name=os.environ.get("default")
    ) #sets the profile name to use for AWS credentials

    bedrock = session.client(
        service_name='bedrock-runtime', #creates a Bedrock client
        region_name=os.environ.get("us-east-1"),
        # endpoint_url=os.environ.get("BWB_ENDPOINT_URL")
    ) 

    #
    bedrock_model_id = "ai21.j2-ultra-v1" #set the foundation model

    prompt = "What is the largest city in New Hampshire?" #the prompt to send to the model

    body = json.dumps({
        "prompt": prompt, #AI21
        "maxTokens": 1024, 
        "temperature": 0, 
        "topP": 0.5, 
        "stopSequences": [], 
        "countPenalty": {"scale": 0 }, 
        "presencePenalty": {"scale": 0 }, 
        "frequencyPenalty": {"scale": 0 }
    }) #build the request payload

    #
    response = bedrock.invoke_model(body=body, modelId=bedrock_model_id, accept='application/json', contentType='application/json') #send the payload to Bedrock

    #
    response_body = json.loads(response.get('body').read()) # read the response

    response_text = response_body.get("completions")[0].get("data").get("text") #extract the text from the JSON response

    print(response_text)


def extract_text_from_pdf(pdf_path):
    loader = AmazonTextractPDFLoader(pdf_path)
    documents = loader.load()
    # print("Number of documents: ",  len(documents))

    # for document in documents:
    #     print(document.page_content)
    return documents[0].page_content

# extract_text_from_pdf("./discharge-summary.png")

def fun():
    text = extract_text_from_pdf("./2022-Shareholder-Letter.pdf")
    print(text)
    # get_summary(text)
    return

fun()