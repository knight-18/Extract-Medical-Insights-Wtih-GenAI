import os
from langchain.llms.bedrock import Bedrock


def get_text_response(input_content): #text-to-text 클라이언트 함수

    llm = Bedrock( #Bedrock llm 클라이언트 생성
        credentials_profile_name=os.environ.get("BWB_PROFILE_NAME"), #AWS 자격 증명에 사용할 프로필 이름을 설정합니다(기본값이 아닌 경우)
        region_name=os.environ.get("BWB_REGION_NAME"), #리전 이름을 설정합니다(기본값이 아닌 경우)
        endpoint_url=os.environ.get("BWB_ENDPOINT_URL"), #endpoint URL을 설정합니다 (필요한 경우)
        model_id="anthropic.claude-v2:1", 
        model_kwargs={
            "max_tokens_to_sample": 512,
            "temperature": 0,
            "top_p": 0.01,
            "top_k": 0,
        }
    )
    
    return llm.predict(input_content) #프롬프트에 응답을 반환

