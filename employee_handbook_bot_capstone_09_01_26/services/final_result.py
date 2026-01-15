from utils.llm_setup import llm
from langchain_core.prompts import PromptTemplate
from langchain_classic import LLMChain

rag_prompt=PromptTemplate(
    input_variables=["question","context"],
    template="""
You are an AI assistant answering questions strictly from an employee handbook.

RULES:
-Answer ONLY using the provided context.
-Do NOT use external knowledge. 
-If the answer is not present in the context , say:
"According to the employee handbook, this information is not specified."

Context:
{context}

Question:
{question}

Answer:
"""
)

answer_chain=LLMChain(
    llm=llm,
    prompt=rag_prompt
)

def extract_context(query_result):
    context=[]
    for query in query_result['results']:
        context.append(query['payload']['text'])

    return context

def clean_output(text:str)->str:
    lines=text.splitlines()
    cleaned=[]
    for line in lines:
        if line.strip() and not line.lower().startswith(("of course","sure","here is")):
            cleaned.append(line.strip())
    
    return cleaned
