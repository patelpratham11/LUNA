from helpers.helper import detect_intent, speak
from helpers.obsidian import setup_obsidian
from helpers.weather import setup_weather, get_weather
from helpers.calendar import create_event, get_calendar_service, get_upcoming_events
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable

# === SETUP ===

# LLM and tools
model_name = "phi3:mini"
llm = OllamaLLM(model=model_name)
obsidian_query_engine = setup_obsidian()
weather_engine = setup_weather()
calendar = get_calendar_service()

# Metaprompt
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

# PromptTemplate
template = PromptTemplate.from_template(
    "Question:\n{question}\n\nRespond as Luna, using the following guidance:\n{metaprompt}"
)

# Chain
chain: Runnable = template | llm


# === HANDLERS ===

def answer_with_context(context: str, query: str) -> str:
    full_prompt = (
        f"The user asked: '{query}'\n"
        f"{context}\n"
        "Use ONLY this information to answer the question. "
        "Respond naturally and conversationally, like Jarvis would, without bullet points or lists."
    )
    return chain.invoke({
        "question": full_prompt,
        "metaprompt": metaprompt
    })


# === MAIN LOOP ===

if __name__ == "__main__":
    while True:
        query = input("\nAsk Luna a question (or 'exit'): ")
        if query.lower() in ['exit', 'quit']:
            break

        router = detect_intent(query, llm)

        if router == "calendar":
            print("📅 Calendar intent detected...")
            events = get_upcoming_events(calendar, query)
            context = f"Here are the calendar events within the requested time frame:\n{events}"
            response = answer_with_context(context, query)

        elif router == "notes":
            print("🗒️ Searching Obsidian notes...")
            notes = obsidian_query_engine.invoke(query)
            context = f"Here is the information retrieved from your personal notes:\n{notes}"
            response = answer_with_context(context, query)

        elif router == "weather":
            print("☀️ Gathering weather data...")
            weather = get_weather()
            context = f"Here's the current weather as a JSON:\n{weather}"
            response = answer_with_context(context, query)

        else:
            print("💬 General query detected...")
            response = chain.invoke({
                "question": query,
                "metaprompt": metaprompt
            })

        print("\nLuna says:\n", response)
        # speak(str(response))  # Uncomment if needed