from fastapi import APIRouter, Depends, HTTPException, Request

from app.application.services.{{cookiecutter.service_name}}_service import {{cookiecutter.service_class_name}}

router = APIRouter()


@router.post("/process")
async def {{cookiecutter.agent_name}}(request: Request, agent_service: {{cookiecutter.service_class_name}} = Depends({{cookiecutter.service_class_name}})):
    try:
        body = await request.json()

        # TODO: Process the news data

        # TODO: Criar a entidade que precisar

        # Exemplo:
        # news_data = News(
        #     news=body.get("news"),
        #     summary=body.get("summary"),
        #     source=body.get("source")
        #     )

        # TODO: Processar o input
        # Exemplo:
        # result = await agent_service.process_input(entity)
        # return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 