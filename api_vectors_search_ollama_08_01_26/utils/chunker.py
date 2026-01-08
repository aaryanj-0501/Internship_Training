import re

def chunk_text(text:str, chunk_size:int=300,overlap:int=1):
    chunks=[]

    sentences=re.split(r'(?<=[.!?]) +', text)
    current_chunk=[]
    current_length=0

    for sentence in sentences:
        sentence_length=len(sentence)

        if current_length + sentence_length>chunk_size:
            chunks.append(" ".join(current_chunk))

            #keep overlap chunk for context
            current_chunk=current_chunk[-overlap:]
            current_length=sum(len(s) for s in current_chunk)

        current_chunk.append(sentence)
        current_length+=sentence_length

    #Add remaining chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

