import gc
import logging
from uuid import UUID, uuid4
from app import crud
from app.schemas.common_schema import IChatResponse, IUserMessage
from app.utils.uuid6 import uuid7
from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from app.core import security
from app.api.deps import get_redis_client
from app.models.sugesstions_model import Intention, Intentions
from fastapi_pagination import add_pagination
from pydantic import ValidationError, BaseModel
from starlette.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router as api_router_v1
from app.core.config import ModeEnum, settings
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware, db
from contextlib import asynccontextmanager
from app.utils.fastapi_globals import GlobalsMiddleware
from app.utils.document import split_docs
from fastapi_limiter import FastAPILimiter
from jose import jwt
from fastapi_limiter.depends import WebSocketRateLimiter
from langchain_openai import OpenAI
from langchain.schema import HumanMessage
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import PGVector
from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser

from sqlalchemy.pool import NullPool, QueuePool

async def user_id_identifier(request: Request):
    if request.scope["type"] == "http":
        # Retrieve the Authorization header from the request
        auth_header = request.headers.get("Authorization")

        if auth_header is not None:
            # Check that the header is in the correct format
            header_parts = auth_header.split()
            if len(header_parts) == 2 and header_parts[0].lower() == "bearer":
                token = header_parts[1]
                try:
                    payload = jwt.decode(
                        token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
                    )
                except (jwt.JWTError, ValidationError):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Could not validate credentials",
                    )
                user_id = payload["sub"]
                print("here2", user_id)
                return user_id

    if request.scope["type"] == "websocket":
        return request.scope["path"]

    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]

    client = request.client
    ip = getattr(client, "host", "0.0.0.0")
    return ip + ":" + request.scope["path"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    redis_client = await get_redis_client()
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    await FastAPILimiter.init(redis_client, identifier=user_id_identifier)

    # text = "\n12 Ways to Live More Sustainably\nEvery day we make choices in our lives that affect the  environment, the climate and other species. From what we eat to how many  children we decide to have, there's a lot we can do to “choose wild” and reduce  our environmental footprint to leave more room for wild animals and plants. Our  individual actions matter — but we can't do it alone. Share this page to  inspire others and check  out our action alerts for ways you can advocate for policy change. \n\n  \n  Think twice before shopping.\n  Ditch plastic and switch to reuse.\n  Take extinction off your plate.\n  Simplify the holidays.\n  Choose organic.\n  Ditch fast fashion and animal-based textiles.\n  Be water wise.\n  Drive less, drive green.\n  Green your home.\n  Boycott products that endanger wildlife.\n  Fight for the right to choose when and if to start a family.\n  Take action. Use your voice.\n\nProtect Threatened Corals in Puerto RicoTAKE ACTI\n1. Think twice before shopping.\n\nconsider buying secondhand\nLearn more about the benefits of secondhand shopping.  \n2. Ditch plastic and switch to reuse.\nPlastic never goes away. At  least 14 million tons of it ends up in the ocean annually, making up 80% of all  marine debris. Every year thousands of seabirds, sea turtles, seals and other  marine mammals are killed after ingesting plastic or getting tangled up in it.  You can start cutting down on your plastic waste in a few simple steps: Use reusable  bags when you shop, ditch single-use water bottles, bags and straws, and avoid  products made from or packaged in plastic whenever possible (e.g., select  unwrapped produce at the grocery store). Switch from single-use to reusable  products every chance you get — every piece of plastic avoided is a win for the  planet. \n  \nLearn more aboutplastics pollutionin our oceans andthe problem with plastic bags.\n\n3. Take extinction off your plate.\nMeat production is one of the  most environmentally destructive industries on the planet, responsible for  massive amounts of water use, pollution, greenhouse gas emissions and habitat  destruction. So when you choose to eat more plant-based foods and reduce your  meat consumption you reduce your environmental footprint. Also, food is the  single largest category of material thrown into municipal landfills. In the  United States nearly 40% of edible food goes to waste — and all of the land,  water and other natural resources that went into producing it go to waste along  with it. Prevent food waste with smart, planned shopping and make sure to consume  what you purchase. \n  \nLearn more abouthow to adopt an  Earth-friendly dietandbeat food waste.\n\n4. Simplify the holidays.\nHolidays, birthdays, weddings and other celebrations are  often excessively wasteful. In December, for example, Americans create 23% more  waste than in other months of the year. But it's not just the extra trash  that's a problem. All the fossil fuels, trees and other natural resources that  go into producing gifts, decorations, single-use dinnerware and wrapping paper  make our celebrations dreary for wildlife and the habitat they need to survive.  But you can redefine your celebrations in ways that respect land, waters and  wildlife. Instead of celebrating your next holiday with plastic décor,  excessive gifts and single-use food and drink containers, you can decorate with  foraged plants, give homemade or secondhand gifts, and serve plant-based meals  with reusable dinnerware. \n  \nLearn more about how to simplify the holidays and  have more fun with less stuff. \n\n5. Choose organic.\nFrom coffee to fruit to  clothing, choosing organic products helps reduce your impact on wildlife and  the planet. More than 2 billion pounds of pesticides  are sold annually in the United States. Pesticides are pervasive in fish and wildlife  habitat and threaten the survival and recovery of hundreds of federally listed  species. Pesticides also pollute the air, water and soil and contaminate the  food we eat. If you garden, avoid pesticides at home by growing organically.  Building wildlife habitat in your yard by growing native, pollinator-friendly  plants and removing invasive species will attract beneficial insects and help  keep unwanted pests away. When you choose organic, you're keeping harmful  pesticides out of our land and water, protecting farm workers, vulnerable  communities, wildlife and your family. \n  \nLearn about how we're fighting to stop the most toxic pesticides.  \n\n6. Ditch fast fashion and animal-based textiles.\nFast fashion is an enormous, rapidly  growing industry. The number of new garments made per year has nearly doubled  over the past 20 years, and our global consumption of fashion has increased by  400%. The fast fashion industry is a significant contributor to the climate  crisis, responsible for as much as 10% of global carbon emissions. Animal-based  textiles like wool are responsible for water pollution, widespread habitat loss  from deforestation, and other harms to wildlife. Slow down your fashion by  caring for your clothes, repairing when possible and, when you need new  clothes, shop secondhand or join clothing swaps. If you must buy new, look past  the greenwashing and purchase clothing made of truly sustainable materials like  organic cotton or Tencel from brands that are made to last. \n  \nRead about greenwashing of the wool industry and the harms of fast fashion. \n\n7. Be water wise.\nWater conservation is  critical as our growing population puts increased demand on the nation's water  sources and we face unprecedented droughts. You can conserve water by taking  shorter showers, fixing leaky toilets, and choosing low-flow and low-water  appliance options. Consider xeriscaping your yard, a landscaping technique that  uses native, drought-adapted plants that require less water and maintenance  over time and provide habitat and food for birds and bees. Also, one of the  biggest water hogs is animal agriculture, so shifting your diet away from meat  and dairy products saves water too. \n  \nLearn about safeguarding water for people and wildlife.\n\n8. Drive less, drive green.\nFossil-fueled transportation  emissions create greenhouse gases, smog, soot and other harmful air pollution.  But changing your driving habits can dramatically reduce your carbon footprint.  Walk, bike, carpool, use public transportation or join ride or bike shares  whenever possible. Combine errands to make fewer trips. Participate in, or  start, car-free days in your community. Ask your local officials to invest in  electric vehicle fleets and charging stations, and if you're in the market for  a new car, consider buying electric. It's also important to keep your car in  shape with regular tune-ups and tire inflations. Tune-ups can increase your  fuel efficiency — a tire that is 20% underinflated can  increase a vehicle's fuel consumption by 10%. \n  \nLearn more abouttransportation and global warming.\n\n9. Green your home.\nJust as keeping your car in  shape improves your fuel efficiency, keeping your home in shape improves your  energy efficiency. Make sure your home has adequate insulation and  energy-saving windows and use a programmable thermostat for more efficient  heating and cooling — and, of course, energy-saving lightbulbs for more  efficient lighting. If your state allows you to pick your electricity supplier,  use a company that generates at least half of its power from wind, solar and  other clean sources. Installing rooftop solar panels or solar water heating  also helps the planet and can save you money. Many states now offer incentives  to help you green your home or rental at low or no cost. Call your energy  provider to see if it offers free energy audits or knows of a company that  does. \n  \nLearn how tokeep cool without the climate costandweatherize for wildlife. \n\n10. Boycott products that endanger wildlife.\nProducts made from animals on  the endangered species list are illegal to buy, sell, import or trade in the  United States, but if a plant or animal hasn't been listed yet, they can still  be harmed for someone's profit. Also, some products harm endangered species by  threatening their habitat, from cutting down old-growth forests to using up the  water that riparian species need to survive. To avoid contributing to the  endangerment of wildlife, shop conscientiously and look for products made from  sustainable materials like bamboo and dine at restaurants that refuse to serve  imperiled species like bluefin tuna. \n  \nJoin theBluefin Boycottand learn more about how the world comes together to tackle wildlife trade.\n\n11. Fight for the right to choose when and if to start a family.\nWith more than 8 billion  people in the world our demands for food, water, land and fossil fuels are  pushing other species to extinction. Human population growth and consumption  are at the root of our most pressing environmental crises, but they're often  left out of the conversation. By advancing reproductive health, rights and  justice and gender equity, we can improve the health of people and the planet  because better education and access to family-planning services decreases  family size and our overall carbon footprint. Get the conversation started by  talking about family planning with your partner. In your community, stand up  for reproductive freedom by supporting comprehensive sex ed in schools, free  and easily accessible contraception and abortion access. \n  \nLearn more about human population growth and overconsumption and sign up to distribute our endangered species condoms. \n12. Take action. Use your voice.\nOne of the best things you  can do for wildlife and the planet, today and for the future, is to get  politically involved in your community and at the national level. Vote for  candidates with strong environmental platforms. Urge your representatives to  pass stronger policies to limit greenhouse gases, fight climate change, protect  wildlife and public lands and support access to reproductive health services. Vote  with your wallet by donating to organizations fighting to end  the extinction crisis. Sign and share action alerts, attend events, and talk to  your friends about endangered species protection and the need to address human  population growth and overconsumption. \n  \nCheck out our current action alerts."
    # docs = split_docs(text, chunk_size=1000, chunk_overlap=20)
    # print('docs', docs)

    # embeddings = OpenAIEmbeddings()

    # CONNECTION_STRING = settings.VECTOR_DATABASE_URI
    # print('CONNECTION_STRING', CONNECTION_STRING)
    # COLLECTION_NAME = "12_ways_to_live_more_sustainably"

    # app.vector_db = PGVector.from_documents(
    # embedding=embeddings,
    # documents=docs,
    # collection_name=COLLECTION_NAME,
    # connection_string=CONNECTION_STRING,
    # )
    # print('vector_db', app.vector_db)
    yield
    # shutdown
    await FastAPICache.clear()
    await FastAPILimiter.close()
    gc.collect()


# Core Application Instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=settings.ASYNC_DATABASE_URI,
    engine_args={
        "echo": False,
        # "pool_pre_ping": True,
        # "pool_size": settings.POOL_SIZE,
        # "max_overflow": 64,
        "poolclass": NullPool
        if settings.MODE == ModeEnum.testing
        else QueuePool,  # Asincio pytest works with NullPool
    },
)
app.add_middleware(GlobalsMiddleware)

# Set all CORS origins enabled
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


class CustomException(Exception):
    http_code: int
    code: str
    message: str

    def __init__(
        self,
        http_code: int = 500,
        code: str | None = None,
        message: str = "This is an error message",
    ):
        self.http_code = http_code
        self.code = code if code else str(self.http_code)
        self.message = message


@app.get("/")
async def root():
    """
    An example "Hello world" FastAPI route.
    """
    # if oso.is_allowed(user, "read", message):
    return {"message": "Hello World"}

@app.websocket("/mirror")
async def websocket_mirror(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Receive and send back the client message
            data = await websocket.receive_json()
            await websocket.send_json(data)
        except WebSocketDisconnect:
            logging.info("websocket disconnect")
            break
        except Exception as e:
            logging.error(e)
            await websocket.close()

class Item(BaseModel):
    product_title: str
    user_info: str
@app.post("/intentions")
async def endpoint(item: Item):
    user_info = item.user_info
    product_title = item.product_title
    # get user_id
    # get user_message
    # message = user_message.message
    # session_id = str(uuid4())
    # key: str = f"user_id:{user_id}:session:{session_id}"
    # await websocket.accept()
    # redis_client = await get_redis_client()
    # ws_ratelimit = WebSocketRateLimiter(times=200, hours=24)
    # chat = ChatOpenAI(temperature=0, openai_api_key=settings.OPENAI_API_KEY)
    chat_history = []
    # docs_with_scores = app.vector_db.similarity_search_with_score(user_message.message)
    # print(docs_with_scores)
    # retriever = app.vector_db.as_retriever(search_kwargs={'k': 3})  # default 4
    model = OpenAI()
    
    parser = PydanticOutputParser(pydantic_object=Intentions)
    prompt_str = """Our intentions and motivations can often be complex and subconscious, leading us to make purchases that might not align with our best interests or long-term goals. Sometimes, we make purchases based on emotions, societal pressures, or habits without fully considering the consequences. Recognizing and understanding these unrecognized intentions can help us make more informed and mindful purchasing decisions

{user_info}. I found this amazon product named "{product_title}" Could you warn me of the potential unrecognized intentions that might be motivating me to buy this item? I wanna ensure that I'm not going to regret buying this item in a few weeks from now.
"""
    prompt_template = prompt_str + "Please tailor your answer to who I am\n{format_response}" if user_info else prompt_str + "{format_response}"
    
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["user_info", "product_title"], partial_variables={"format_response": parser.get_format_instructions()}
    )

    chain = prompt | model | parser
    print(chain)
    result = chain.invoke({"user_info": user_info, "product_title": product_title})
    print('result', result)
    return result
    # prompt = PromptTemplate.from_template(prompt_template)
    # chain_type_kwargs = {"prompt": PROMPT}
    # print(chain_type_kwargs)
    # qa = RetrievalQA.from_chain_type(
    #     llm=llm,
    #     chain_type="stuff",
    #     retriever=retriever,
    #     chain_type_kwargs=chain_type_kwargs,
    # )
    # print(qa._chain_type)
    # result = qa.run(user_info, product_title)
    # llm_chain = LLMChain(prompt=PROMPT, llm=llm)
    # result = llm_chain.run()
    # print('result', result)
    # return result
    # And a query intended to prompt a language model to populate the data structure.
                # await websocket.send_json(resp.dict())

                # # # Construct a response
                # start_resp = IChatResponse(
                #     sender="bot", message="", type="start", message_id="", id=""
                # )
                # await websocket.send_json(start_resp.dict())

                # result = chat([HumanMessage(content=resp.message)])
    # chat_history.append((user_message.message, result))
    # end_resp = IChatResponse(
    #     sender="bot",
    #     message=result,
    #     type="end",
    #     message_id=str(uuid7()),
    #     id=str(uuid7()),
    # )
    # # await websocket.send_json(end_resp.dict())
    # return end_resp.dict()



@app.websocket("/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: UUID):
    session_id = str(uuid4())
    key: str = f"user_id:{user_id}:session:{session_id}"
    await websocket.accept()
    redis_client = await get_redis_client()
    ws_ratelimit = WebSocketRateLimiter(times=200, hours=24)
    chat = ChatOpenAI(temperature=0, openai_api_key=settings.OPENAI_API_KEY)
    chat_history = []

    async with db():
        user = await crud.user.get_by_id_active(id=user_id)
        if user is not None:
            await redis_client.set(key, str(websocket))

    active_connection = await redis_client.get(key)
    if active_connection is None:
        await websocket.send_text(f"Error: User ID '{user_id}' not found or inactive.")
        await websocket.close()
    else:
        while True:
            try:
                # Receive and send back the client message
                data = await websocket.receive_json()
                await ws_ratelimit(websocket)
                user_message = IUserMessage.parse_obj(data)
                user_message.user_id = user_id

                resp = IChatResponse(
                    sender="you",
                    message=user_message.message,
                    type="stream",
                    message_id=str(uuid7()),
                    id=str(uuid7()),
                )
                # docs_with_scores = app.vector_db.similarity_search_with_score(user_message.message)
                # print(docs_with_scores)
                retriever = app.vector_db.as_retriever(search_kwargs={'k': 3})  # default 4

                prompt_template = """You are an intelligent assistant designed to interact with users looking to live a more sustainable lifestyle. Your purpose is to help users explore and apply knowledge related to sustainability. If a user mentions a specific topic, provide relevant details and suggest sustainable alternatives or practices. Additionally, always prioritize positive reinforcement and motivation to inspire users to adopt a more sustainable lifestyle. 

you will be given a user's journal output

JOURNAL: "{question}"

You will need to comment on the user's journal output with sustainability knowledge. You will also need to suggest sustainable alternatives or practices to the user.
If there is no mention of anything related to sustainability, ignore the user's response and reply with: "None". Otherwise you will need to comment on the user's journal output on how he can live a more sustainable lifestyle.
COMMENT:
"""
# You will be given 2 main things:
#  - JOURNAL: a user's journal output
# KNOWLEDGE: {context}
#  - KNOWLEDGE: sustainability knowledge related to the user's journal output.


                PROMPT = PromptTemplate(
                    template=prompt_template, input_variables=["question"]
                )
                chain_type_kwargs = {"prompt": PROMPT}
                print(chain_type_kwargs)
                qa = RetrievalQA.from_chain_type(
                    llm=OpenAI(),
                    chain_type="stuff",
                    retriever=retriever,
                    chain_type_kwargs=chain_type_kwargs,
                )
                print(qa._chain_type)
                result = qa.run(user_message.message)
                print('result', result)
                # await websocket.send_json(resp.dict())

                # # # Construct a response
                # start_resp = IChatResponse(
                #     sender="bot", message="", type="start", message_id="", id=""
                # )
                # await websocket.send_json(start_resp.dict())

                # result = chat([HumanMessage(content=resp.message)])
                chat_history.append((user_message.message, result))

                end_resp = IChatResponse(
                    sender="bot",
                    message=result,
                    type="end",
                    message_id=str(uuid7()),
                    id=str(uuid7()),
                )
                await websocket.send_json(end_resp.dict())
            except WebSocketDisconnect:
                logging.info("websocket disconnect")
                break
            except Exception as e:
                logging.error(e)
                resp = IChatResponse(
                    message_id="",
                    id="",
                    sender="bot",
                    message="Sorry, something went wrong. Your user limit of api usages has been reached.",
                    type="error",
                )
                await websocket.send_json(resp.dict())

        # Remove the live connection from Redis
        await redis_client.delete(key)


# Add Routers
app.include_router(api_router_v1, prefix=settings.API_V1_STR)
add_pagination(app)
