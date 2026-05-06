from fastapi import APIRouter
from app.models.agent import AgentRequest, AgentResponse
from app.agent.graph import workflow
from langchain.messages import HumanMessage

router = APIRouter()


@router.post("/agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest) -> AgentResponse:
    # Run the agent workflow with the user's query
    result = await workflow.ainvoke({"messages": [HumanMessage(content=request.query)]})

    # Extract the final response from the last message
    final_message = result["messages"][-1]
    response_content = final_message.content

    return AgentResponse(response=response_content)

