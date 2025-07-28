from helpers.helper import detect_intent, speak
from helpers.obsidian import setup_obsidian
from helpers.weather import setup_weather, get_weather
from helpers.calendar import create_event, get_calendar_service, get_upcoming_events
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable

model_name = "phi3:mini"
llm = OllamaLLM(model=model_name)
weather_engine = setup_weather()
obsidian_query_engine = setup_obsidian()
metaprompt = (
    "You are Luna, an AI assistant modeled after Jarvis from Iron Man. "
    "Respond concisely and precisely, using polite but direct language. "
    "Answer only what is asked—no extra details or filler. "
    "Maintain a calm, respectful tone without sounding chatty or verbose. "
    "Do not speculate or invent information; if uncertain, say you do not know. "
    "Always use the provided data in your response. "
    "Avoid any formatting like bold, italics, or highlights. "
    "Prioritize accuracy and brevity in every response."
)


template = PromptTemplate.from_template(
    "Answer conversationally:\n\n{question}\n\nMake sure you're aware of the metaprompt:\n\n{metaprompt}"
)
chain: Runnable = template | llm

# calendar = get_calendar_service()


# === QUERY LOOP ===
while True:
    query = input("\nAsk Luna a question (or 'exit'): ")
    if query.lower() in ['exit', 'quit']:
        break
    router = detect_intent(query, llm)
    if router == "calendar":
        print("calendar detected")
        events = get_upcoming_events(calendar, query)
        add = (
            f"The user asked: '{query}'. Here are the calendar events within the requested time frame:\n{events}\n"
            "Use ONLY these events to answer the question. "
            "Respond naturally and conversationally, like Jarvis would, without bullet points or lists."
        )
        response = chain.invoke({
            "question": add,
            "metaprompt": metaprompt
        })
    elif router == "notes":
        print("🔎 Using Obsidian notes...")
        information = obsidian_query_engine.invoke(query)
        add = (
            f"The user asked: '{query}'. Here is the information from the vector database. Please use this information to answer the question as best as possible.:\n{information}\n"
            "Use ONLY this information to answer the question. "
            "Respond naturally and conversationally, like Jarvis would, without bullet points or lists."
        )
        response = chain.invoke({
            "question": add,
            "metaprompt": metaprompt
        })
        # response = obsidian_query_engine.query(query)
    elif router == "weather":
        print("☀️ Gathering Weather Data")
        results = get_weather()['current']
        add = (
            f"The user asked: '{query}'. Here's the weather as a JSON:\n{results}\n"
            "Use ONLY these events to answer the question. "
            "Respond naturally and conversationally, like Jarvis would, without bullet points or lists."
        )
        print(add)
        response = chain.invoke({
            "question": add,
            "metaprompt": metaprompt
        })
    else:
        print("💬 Answering directly...")
        response = chain.invoke({
            "question": query,
            "metaprompt": metaprompt
        })

    print("\Luna says:\n", response)
    speak(str(response))